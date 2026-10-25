"""Reusable company research agent for sales/account "goldmine" files.

Given a company name and website, this module fetches a handful of public
pages from the company's own site (homepage plus any discoverable
about/news/investor pages), extracts readable text with BeautifulSoup, and
writes a structured markdown write-up to ``sales/accounts/<slug>.md``.

Design notes:
  * Data gathering relies on direct HTTP fetch + HTML parsing (``requests``
    + ``bs4``), not on Gemini's search-grounding tool -- that tool has been
    observed to hit ``429 RESOURCE_EXHAUSTED`` on this API key, so it can't
    be a hard dependency.
  * If ``GEMINI_API_KEY`` is set, the scraped text is summarized into the
    write-up with ``gemini-3.6-flash`` (NOT ``gemini-2.5-flash``, which
    404s as "no longer available to new users" on this key). Without a key,
    the tool still produces a useful file from raw scraped snippets alone.
  * Can auto-discover targets across every domain folder under
    ``sales/`` (e.g. ``sales/manufacturing/``, ``sales/construction/``,
    ``sales/healthcare/``) -- each domain is scanned automatically, with
    no code changes needed when a new vertical shows up -- or take an
    explicit ``--domain``/``--leads-dir``/``--company``+``--website``.

Usage:
    python -m sales.research_agent --all
    python -m sales.research_agent --company "Acme Corp" --website acme.com
"""

from __future__ import annotations

import argparse
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

REPO_ROOT = Path(__file__).resolve().parent.parent
SALES_ROOT = REPO_ROOT / "sales"
# Per-vertical directories of company profile pages, e.g. sales/manufacturing/,
# sales/construction/, sales/healthcare/, etc. Each such directory contains
# one "# Company Name" markdown file per company (plus a README.md index,
# which is skipped) with **Website:**/**ARR:**/**Industry:** fields -- see
# sales/manufacturing/README.md for the convention.
LEADS_DIR = SALES_ROOT / "manufacturing"  # default single-domain dir
ACCOUNTS_DIR = SALES_ROOT / "accounts"
# Sibling directories of sales/ that are not themselves a vertical/domain,
# so should be skipped when auto-discovering domains to scan.
NON_DOMAIN_DIRS = {"accounts", "__pycache__"}

USER_AGENT = "physical-agents-research-agent/1.0 (+internal sales research tool)"
REQUEST_TIMEOUT = 10
MAX_PAGES_PER_SITE = 5
MAX_CHARS_PER_PAGE = 4000

# Candidate paths, beyond the homepage, worth trying on most corporate
# sites. Not all will exist; 404s are skipped silently.
CANDIDATE_PATHS = [
    "/about", "/about-us", "/company", "/who-we-are",
    "/news", "/newsroom", "/press", "/press-releases", "/media",
    "/investors", "/investor-relations",
]

GEMINI_MODEL = "gemini-3.6-flash"


@dataclass
class PageContent:
    url: str
    title: str
    text: str


@dataclass
class CompanyTarget:
    name: str
    website: str
    context: str = ""  # optional extra context (e.g. ARR/industry blurb)
    domain: str = ""  # vertical this target came from, e.g. "manufacturing"


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or "company"


def normalize_website(website: str) -> str:
    website = website.strip()
    if not website.startswith(("http://", "https://")):
        website = f"https://{website}"
    return website


def _fetch(url: str) -> requests.Response | None:
    try:
        response = requests.get(
            url, headers={"User-Agent": USER_AGENT}, timeout=REQUEST_TIMEOUT
        )
        if response.status_code >= 400:
            return None
        return response
    except requests.RequestException:
        return None


def _extract_text(html: str) -> tuple[str, str]:
    """Return (title, cleaned visible text) from raw HTML."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()
    title = soup.title.get_text(strip=True) if soup.title else ""
    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines()]
    cleaned = "\n".join(line for line in lines if line)
    return title, cleaned[:MAX_CHARS_PER_PAGE]


def fetch_company_pages(website: str) -> list[PageContent]:
    """Fetch the homepage plus a few candidate sub-pages for *website*."""
    base_url = normalize_website(website)
    pages: list[PageContent] = []
    seen = set()

    home = _fetch(base_url)
    if home is not None:
        title, text = _extract_text(home.text)
        if text:
            pages.append(PageContent(url=home.url, title=title, text=text))
            seen.add(urlparse(home.url).path.rstrip("/") or "/")

    parsed = urlparse(base_url)
    origin = f"{parsed.scheme}://{parsed.netloc}"
    for path in CANDIDATE_PATHS:
        if len(pages) >= MAX_PAGES_PER_SITE:
            break
        if path in seen:
            continue
        candidate_url = urljoin(origin, path)
        response = _fetch(candidate_url)
        if response is None:
            continue
        title, text = _extract_text(response.text)
        if text:
            pages.append(PageContent(url=response.url, title=title, text=text))
            seen.add(path)

    return pages


def _gemini_summarize(company: CompanyTarget, pages: list[PageContent]) -> str | None:
    """Ask Gemini to synthesize scraped pages into a sales-research brief.

    Returns None (rather than raising) on any failure -- missing key,
    quota exhaustion, network error, etc. -- so callers can fall back to a
    raw-snippet write-up.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None

    try:
        from google import genai
    except ImportError:
        return None

    corpus_parts = []
    for page in pages:
        corpus_parts.append(f"### Source: {page.url}\nTitle: {page.title}\n\n{page.text}")
    corpus = "\n\n---\n\n".join(corpus_parts)
    if not corpus.strip():
        return None

    prompt = (
        "You are a B2B sales research analyst. Using ONLY the scraped "
        f"website content below for the company \"{company.name}\" "
        f"({company.website}), write a concise markdown research brief "
        "with these sections: '## Company Overview', '## Recent News', "
        "'## Manufacturing / Operations Footprint', "
        "'## Leadership & Key Contacts', and "
        "'## Notes for M-Files / VMAN Vision Pitch' (document-management "
        "and vision-spatial AI angles suggested by what you read). If a "
        "section has no supporting evidence in the source text, write "
        "'No information found in scraped sources.' under that heading "
        "instead of guessing. Do not fabricate facts not present in the "
        "sources.\n\n"
        f"{company.context}\n\n"
        f"SCRAPED CONTENT:\n{corpus}"
    )

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[prompt],
        )
        return (response.text or "").strip() or None
    except Exception:
        return None


def _raw_fallback_brief(company: CompanyTarget, pages: list[PageContent]) -> str:
    """Build a plain markdown brief from raw scraped snippets, no LLM."""
    if not pages:
        return (
            "## Company Overview\n\nNo pages could be fetched from "
            f"{company.website} (site may block automated requests, or be "
            "unreachable from this environment).\n"
        )

    parts = ["## Scraped Source Snippets\n"]
    for page in pages:
        snippet = page.text[:800]
        parts.append(f"### {page.title or page.url}\n**Source:** {page.url}\n\n{snippet}\n")
    return "\n".join(parts)


def research_company(company: CompanyTarget) -> str:
    """Run the full pipeline for one company and return markdown content."""
    pages = fetch_company_pages(company.website)
    summary = _gemini_summarize(company, pages)

    lines = [f"# {company.name}", ""]
    if company.context:
        lines.append(company.context)
        lines.append("")
    lines.append(f"**Website:** {company.website}")
    lines.append("")

    if summary:
        lines.append(summary)
        lines.append("")
        lines.append("<!-- Synthesized by gemini-3.6-flash from scraped sources below. -->")
    else:
        lines.append(_raw_fallback_brief(company, pages))

    lines.append("")
    lines.append("## Sources Fetched")
    if pages:
        for page in pages:
            lines.append(f"- {page.url}")
    else:
        lines.append("- (none reachable)")

    return "\n".join(lines) + "\n"


def _parse_company_block(text: str, name: str) -> CompanyTarget | None:
    """Extract website/ARR/industry fields from a single company profile page."""
    website_match = re.search(r"\*\*Website:\*\*\s*(\S+)", text)
    arr_match = re.search(r"\*\*ARR:\*\*\s*(.+)", text)
    industry_match = re.search(r"\*\*Industry:\*\*\s*(.+)", text)
    if not website_match:
        return None

    context_bits = []
    if arr_match:
        context_bits.append(f"**ARR:** {arr_match.group(1).strip()}")
    if industry_match:
        context_bits.append(f"**Industry:** {industry_match.group(1).strip()}")

    return CompanyTarget(
        name=name,
        website=website_match.group(1).strip(),
        context="\n".join(context_bits),
    )


def parse_leads_file(leads_path: Path) -> list[CompanyTarget]:
    """Parse a single markdown file containing one or more "### N. Name" blocks.

    Kept for compatibility with the older single-file leads format
    (each company is a "### N. Name" heading followed by **Field:** lines
    until the next "### " heading or end of file).
    """
    text = leads_path.read_text(encoding="utf-8")
    targets: list[CompanyTarget] = []

    heading_re = re.compile(r"^### \d+\.\s+(.+)$", re.MULTILINE)
    matches = list(heading_re.finditer(text))
    for idx, match in enumerate(matches):
        name = match.group(1).strip()
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        target = _parse_company_block(text[start:end], name)
        if target is not None:
            targets.append(target)

    return targets


def parse_leads_dir(leads_dir: Path = LEADS_DIR, domain: str | None = None) -> list[CompanyTarget]:
    """Parse company profile pages out of a directory like sales/manufacturing/.

    Each file is expected to be "# Company Name" followed by **Field:**
    lines. README.md (the dated index) is skipped. *domain* defaults to
    the directory's own name (e.g. "manufacturing") and is stamped onto
    each parsed CompanyTarget so multi-domain runs can tell targets apart.
    """
    targets: list[CompanyTarget] = []
    if not leads_dir.is_dir():
        return targets
    if domain is None:
        domain = leads_dir.name

    for path in sorted(leads_dir.glob("*.md")):
        if path.name.lower() == "readme.md":
            continue
        text = path.read_text(encoding="utf-8")
        heading_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        if not heading_match:
            continue
        name = heading_match.group(1).strip()
        target = _parse_company_block(text, name)
        if target is not None:
            target.domain = domain
            targets.append(target)

    return targets


def discover_domain_dirs(sales_root: Path = SALES_ROOT) -> list[Path]:
    """Find every vertical/domain directory under sales/ (e.g. manufacturing/,
    construction/, healthcare/), skipping sales/accounts/ and other
    non-domain siblings.
    """
    if not sales_root.is_dir():
        return []
    return sorted(
        p for p in sales_root.iterdir()
        if p.is_dir() and p.name not in NON_DOMAIN_DIRS and not p.name.startswith(".")
    )


def parse_all_domains(sales_root: Path = SALES_ROOT) -> list[CompanyTarget]:
    """Parse company profile pages across every domain directory under sales/.

    This is the "hunt across all verticals, not just manufacturing" entry
    point -- new folders like sales/construction/ or sales/healthcare/ are
    picked up automatically with no code changes needed.
    """
    targets: list[CompanyTarget] = []
    for domain_dir in discover_domain_dirs(sales_root):
        targets.extend(parse_leads_dir(domain_dir, domain=domain_dir.name))
    return targets


def write_account_file(company: CompanyTarget, markdown: str, out_dir: Path = ACCOUNTS_DIR) -> Path:
    """Write to out_dir/<domain>/<slug>.md when a domain is known, else
    out_dir/<slug>.md (keeps flat single-domain runs backward compatible).
    """
    target_dir = out_dir / company.domain if company.domain else out_dir
    target_dir.mkdir(parents=True, exist_ok=True)
    out_path = target_dir / f"{slugify(company.name)}.md"
    out_path.write_text(markdown, encoding="utf-8")
    return out_path


def run(targets: list[CompanyTarget], out_dir: Path = ACCOUNTS_DIR) -> list[Path]:
    written = []
    for target in targets:
        markdown = research_company(target)
        written.append(write_account_file(target, markdown, out_dir))
    return written


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--all", action="store_true",
        help=(
            "Research every company across every domain directory under "
            "sales/ (e.g. sales/manufacturing/, sales/construction/, ...). "
            "Use --domain to restrict to a single one."
        ),
    )
    parser.add_argument("--company", help="Single company name to research")
    parser.add_argument("--website", help="Website for --company")
    parser.add_argument(
        "--domain",
        help=(
            "Restrict --all to a single domain folder name under sales/ "
            "(e.g. 'manufacturing'). Omit to scan every domain."
        ),
    )
    parser.add_argument(
        "--leads-dir",
        help="Explicit directory of company profile pages (used with --all; overrides --domain)",
    )
    parser.add_argument(
        "--leads-file",
        help="Path to a single legacy leads markdown file (overrides --leads-dir/--domain with --all)",
    )
    parser.add_argument(
        "--sales-root", default=str(SALES_ROOT),
        help="Root sales/ directory to discover domain folders under (used with --all)",
    )
    parser.add_argument(
        "--out-dir", default=str(ACCOUNTS_DIR),
        help="Directory to write sales/accounts/<domain>/<slug>.md files into",
    )
    args = parser.parse_args(argv)

    out_dir = Path(args.out_dir)

    if args.all:
        if args.leads_file:
            targets = parse_leads_file(Path(args.leads_file))
        elif args.leads_dir:
            targets = parse_leads_dir(Path(args.leads_dir))
        elif args.domain:
            targets = parse_leads_dir(Path(args.sales_root) / args.domain, domain=args.domain)
        else:
            targets = parse_all_domains(Path(args.sales_root))
    elif args.company and args.website:
        targets = [CompanyTarget(name=args.company, website=args.website)]
    else:
        parser.error("Provide --all, or both --company and --website")
        return

    for path in run(targets, out_dir):
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
