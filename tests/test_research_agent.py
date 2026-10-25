"""Tests for the sales research agent's pure-logic pieces (no network/API calls)."""

from __future__ import annotations

from pathlib import Path

from sales.research_agent import (
    CompanyTarget,
    PageContent,
    _raw_fallback_brief,
    discover_domain_dirs,
    normalize_website,
    parse_all_domains,
    parse_leads_dir,
    parse_leads_file,
    slugify,
    write_account_file,
)


class TestSlugify:
    def test_basic_name(self):
        assert slugify("Abbott Laboratories") == "abbott-laboratories"

    def test_strips_punctuation(self):
        assert slugify("SAS Laboratoires CLARINS") == "sas-laboratoires-clarins"

    def test_handles_ampersand_and_periods(self):
        assert slugify("QT Corp. & Co.") == "qt-corp-co"

    def test_empty_falls_back(self):
        assert slugify("***") == "company"


class TestNormalizeWebsite:
    def test_adds_https_when_missing_scheme(self):
        assert normalize_website("abbott.com") == "https://abbott.com"

    def test_leaves_existing_scheme_alone(self):
        assert normalize_website("http://example.com") == "http://example.com"

    def test_strips_surrounding_whitespace(self):
        assert normalize_website("  abbott.com  ") == "https://abbott.com"


class TestParseLeadsFile:
    def test_parses_all_five_companies(self, tmp_path: Path):
        leads_path = tmp_path / "leads.md"
        leads_path.write_text(
            "# Header\n\n"
            "### 1. Abbott Laboratories\n"
            "**ARR:** USD 250,200\n"
            "**Website:** abbott.com\n"
            "**Industry:** Healthcare manufacturer\n\n"
            "### 2. Dall Energy\n"
            "**ARR:** EUR 81,900\n"
            "**Website:** dallenergy.com\n"
            "**Industry:** Biomass energy\n",
            encoding="utf-8",
        )
        targets = parse_leads_file(leads_path)
        assert [t.name for t in targets] == ["Abbott Laboratories", "Dall Energy"]
        assert targets[0].website == "abbott.com"
        assert "USD 250,200" in targets[0].context
        assert "Healthcare manufacturer" in targets[0].context

    def test_skips_block_without_website(self, tmp_path: Path):
        leads_path = tmp_path / "leads.md"
        leads_path.write_text(
            "### 1. No Website Co\n**ARR:** EUR 1\n",
            encoding="utf-8",
        )
        assert parse_leads_file(leads_path) == []

    def test_real_leads_file_parses(self):
        """Legacy single-file parser still works if pointed at an old-style file."""
        repo_root = Path(__file__).resolve().parent.parent
        real_leads = repo_root / "sales" / "manufacturing-leads.md"
        if not real_leads.exists():
            return  # file has been migrated to sales/manufacturing/; nothing to check
        targets = parse_leads_file(real_leads)
        names = [t.name for t in targets]
        assert names == [
            "Abbott Laboratories",
            "Dall Energy",
            "QT Corporation",
            "Patria Oyj",
            "SAS Laboratoires CLARINS",
        ]
        websites = {t.name: t.website for t in targets}
        assert websites["Abbott Laboratories"] == "abbott.com"
        assert websites["SAS Laboratoires CLARINS"] == "groupeclarins.com"


class TestParseLeadsDir:
    def test_parses_profile_pages_skips_readme(self, tmp_path: Path):
        leads_dir = tmp_path / "manufacturing"
        leads_dir.mkdir()
        (leads_dir / "README.md").write_text("# Index\n\nNot a company.\n", encoding="utf-8")
        (leads_dir / "abbott-laboratories.md").write_text(
            "# Abbott Laboratories\n\n"
            "**Last seen in top 5:** Week of 2026-09-07\n"
            "**ARR:** USD 250,200\n"
            "**Website:** abbott.com\n"
            "**Industry:** Healthcare manufacturer\n",
            encoding="utf-8",
        )
        (leads_dir / "dall-energy.md").write_text(
            "# Dall Energy\n\n**ARR:** EUR 81,900\n**Website:** dallenergy.com\n",
            encoding="utf-8",
        )
        targets = parse_leads_dir(leads_dir)
        names = sorted(t.name for t in targets)
        assert names == ["Abbott Laboratories", "Dall Energy"]
        websites = {t.name: t.website for t in targets}
        assert websites["Abbott Laboratories"] == "abbott.com"

    def test_missing_dir_returns_empty(self, tmp_path: Path):
        assert parse_leads_dir(tmp_path / "does-not-exist") == []

    def test_targets_are_stamped_with_dir_name_as_domain(self, tmp_path: Path):
        leads_dir = tmp_path / "healthcare"
        leads_dir.mkdir()
        (leads_dir / "acme-health.md").write_text(
            "# Acme Health\n\n**Website:** acmehealth.com\n",
            encoding="utf-8",
        )
        targets = parse_leads_dir(leads_dir)
        assert targets[0].domain == "healthcare"

    def test_explicit_domain_overrides_dir_name(self, tmp_path: Path):
        leads_dir = tmp_path / "some-folder"
        leads_dir.mkdir()
        (leads_dir / "acme.md").write_text(
            "# Acme\n\n**Website:** acme.com\n",
            encoding="utf-8",
        )
        targets = parse_leads_dir(leads_dir, domain="custom-domain")
        assert targets[0].domain == "custom-domain"

    def test_real_manufacturing_dir_parses(self):
        repo_root = Path(__file__).resolve().parent.parent
        real_dir = repo_root / "sales" / "manufacturing"
        if not real_dir.is_dir():
            return
        targets = parse_leads_dir(real_dir)
        names = {t.name for t in targets}
        assert "Abbott Laboratories" in names
        websites = {t.name: t.website for t in targets}
        assert websites["Abbott Laboratories"] == "abbott.com"


class TestRawFallbackBrief:
    def test_no_pages_produces_explanatory_message(self):
        company = CompanyTarget(name="Acme", website="acme.com")
        brief = _raw_fallback_brief(company, [])
        assert "No pages could be fetched" in brief
        assert "acme.com" in brief

    def test_pages_are_rendered_as_snippets(self):
        company = CompanyTarget(name="Acme", website="acme.com")
        pages = [PageContent(url="https://acme.com", title="Acme Home", text="Welcome to Acme.")]
        brief = _raw_fallback_brief(company, pages)
        assert "Acme Home" in brief
        assert "https://acme.com" in brief
        assert "Welcome to Acme." in brief


class TestDiscoverDomainDirs:
    def test_discovers_vertical_subdirs_excluding_reserved_names(self, tmp_path: Path):
        (tmp_path / "manufacturing").mkdir()
        (tmp_path / "healthcare").mkdir()
        (tmp_path / "accounts").mkdir()
        (tmp_path / "__pycache__").mkdir()
        (tmp_path / ".hidden").mkdir()
        (tmp_path / "notes.md").write_text("not a dir", encoding="utf-8")
        domains = discover_domain_dirs(tmp_path)
        assert sorted(d.name for d in domains) == ["healthcare", "manufacturing"]

    def test_missing_sales_root_returns_empty(self, tmp_path: Path):
        assert discover_domain_dirs(tmp_path / "does-not-exist") == []


class TestParseAllDomains:
    def test_aggregates_targets_across_domains_with_domain_stamped(self, tmp_path: Path):
        manufacturing = tmp_path / "manufacturing"
        manufacturing.mkdir()
        (manufacturing / "abbott-laboratories.md").write_text(
            "# Abbott Laboratories\n\n**Website:** abbott.com\n",
            encoding="utf-8",
        )
        healthcare = tmp_path / "healthcare"
        healthcare.mkdir()
        (healthcare / "acme-health.md").write_text(
            "# Acme Health\n\n**Website:** acmehealth.com\n",
            encoding="utf-8",
        )
        (tmp_path / "accounts").mkdir()

        targets = parse_all_domains(tmp_path)
        by_name = {t.name: t for t in targets}
        assert set(by_name) == {"Abbott Laboratories", "Acme Health"}
        assert by_name["Abbott Laboratories"].domain == "manufacturing"
        assert by_name["Acme Health"].domain == "healthcare"

    def test_missing_sales_root_returns_empty(self, tmp_path: Path):
        assert parse_all_domains(tmp_path / "does-not-exist") == []


class TestWriteAccountFile:
    def test_nests_output_under_domain_subfolder(self, tmp_path: Path):
        company = CompanyTarget(name="Abbott Laboratories", website="abbott.com", domain="manufacturing")
        path = write_account_file(company, "Some brief content.", out_dir=tmp_path)
        assert path == tmp_path / "manufacturing" / "abbott-laboratories.md"
        assert path.exists()

    def test_writes_flat_when_domain_is_blank(self, tmp_path: Path):
        company = CompanyTarget(name="Acme", website="acme.com")
        path = write_account_file(company, "Some brief content.", out_dir=tmp_path)
        assert path == tmp_path / "acme.md"
        assert path.exists()
