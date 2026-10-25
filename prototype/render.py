"""Turn an uploaded document into a PNG the vision providers can accept.

The sample material in `OCR/` is single-page engineering drawings stored as
PDFs, but both providers in `prototype/providers/` expect a raster image.
This module is the bridge: it rasterises page 1 of a PDF, and passes real
images through untouched.
"""

from __future__ import annotations

import os

import pymupdf

PDF_EXTENSION = ".pdf"
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tif", ".tiff"}

# Engineering drawings carry small callouts and dimension text. Rendering at
# roughly 2x the PDF's native resolution keeps that text legible to the model
# without producing an upload large enough to slow the demo down.
RENDER_ZOOM = 2.0


class UnsupportedDocumentError(ValueError):
    """Raised when a file is neither a PDF nor a supported raster image."""


def render_to_png(source_path: str, output_path: str, page_number: int = 0) -> str:
    """Write *source_path* to *output_path* as a PNG and return that path.

    PDFs are rasterised at `RENDER_ZOOM`; images are re-encoded as PNG so
    everything downstream can assume a single, known format.
    """
    extension = os.path.splitext(source_path)[1].lower()

    if extension == PDF_EXTENSION:
        with pymupdf.open(source_path) as document:
            if page_number >= document.page_count:
                raise UnsupportedDocumentError(
                    f"Page {page_number + 1} requested but the document has "
                    f"only {document.page_count} page(s)."
                )
            matrix = pymupdf.Matrix(RENDER_ZOOM, RENDER_ZOOM)
            document[page_number].get_pixmap(matrix=matrix).save(output_path)
        return output_path

    if extension in IMAGE_EXTENSIONS:
        # Imported lazily so a PDF-only run doesn't require Pillow.
        from PIL import Image

        with Image.open(source_path) as image:
            rgba = image.convert("RGBA")
            canvas = Image.new("RGBA", rgba.size, "white")
            canvas.alpha_composite(rgba)
            canvas.convert("RGB").save(output_path, format="PNG")
        return output_path

    raise UnsupportedDocumentError(
        f"Unsupported file type '{extension}'. Supply a PDF or one of: "
        f"{', '.join(sorted(IMAGE_EXTENSIONS))}."
    )


def page_count(source_path: str) -> int:
    """Return the number of pages, treating any raster image as a single page."""
    if os.path.splitext(source_path)[1].lower() == PDF_EXTENSION:
        with pymupdf.open(source_path) as document:
            return document.page_count
    return 1
