"""Draw Gemini Robotics-ER 2 points back onto the source drawing.

The model returns points as [y, x] normalised to a 0-1000 grid (see
`providers/gemini_robotics.py`). Raw coordinates aren't demoable on their
own, so this renders them as labelled markers on top of the image -- the
"show it read the drawing" half of the demo.
"""

from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont

COORDINATE_SCALE = 1000.0

MARKER_RADIUS = 9
MARKER_OUTLINE_WIDTH = 3
MARKER_FILL = (255, 62, 0)
MARKER_OUTLINE = (255, 255, 255)
LABEL_TEXT = (255, 255, 255)
LABEL_BACKGROUND = (17, 24, 39)
LABEL_PADDING = 5


def _load_font(image_width: int) -> ImageFont.ImageFont:
    """Pick a label size that stays readable on large drawings."""
    size = max(14, min(34, image_width // 70))
    for candidate in ("arial.ttf", "DejaVuSans.ttf", "LiberationSans-Regular.ttf"):
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _to_pixels(point: list, width: int, height: int) -> tuple[int, int] | None:
    """Convert one normalised [y, x] pair into pixel coordinates."""
    if not isinstance(point, (list, tuple)) or len(point) != 2:
        return None
    try:
        y_normalised, x_normalised = float(point[0]), float(point[1])
    except (TypeError, ValueError):
        return None

    x = int(x_normalised / COORDINATE_SCALE * width)
    y = int(y_normalised / COORDINATE_SCALE * height)
    # Keep markers inside the canvas even if the model over/undershoots.
    return max(0, min(width - 1, x)), max(0, min(height - 1, y))


def draw_points(image_path: str, points: list, output_path: str) -> int:
    """Overlay *points* on *image_path*, save to *output_path*, return the count drawn.

    Malformed entries are skipped rather than raising, because the provider is
    a preview model and an imperfect response should still produce a demo.
    """
    with Image.open(image_path) as source:
        image = source.convert("RGB")

    draw = ImageDraw.Draw(image)
    font = _load_font(image.width)
    drawn = 0

    for entry in points:
        if not isinstance(entry, dict):
            continue
        pixel = _to_pixels(entry.get("point"), image.width, image.height)
        if pixel is None:
            continue

        x, y = pixel
        draw.ellipse(
            [
                (x - MARKER_RADIUS, y - MARKER_RADIUS),
                (x + MARKER_RADIUS, y + MARKER_RADIUS),
            ],
            fill=MARKER_FILL,
            outline=MARKER_OUTLINE,
            width=MARKER_OUTLINE_WIDTH,
        )

        label = str(entry.get("label", "")).strip()
        if label:
            _draw_label(draw, label, x, y, font, image.width, image.height)
        drawn += 1

    image.save(output_path, format="PNG")
    return drawn


def _draw_label(
    draw: ImageDraw.ImageDraw,
    label: str,
    x: int,
    y: int,
    font: ImageFont.ImageFont,
    image_width: int,
    image_height: int,
) -> None:
    """Draw a label chip beside a marker, nudged to stay on-canvas."""
    left, top, right, bottom = draw.textbbox((0, 0), label, font=font)
    text_width, text_height = right - left, bottom - top

    box_x = x + MARKER_RADIUS + LABEL_PADDING
    box_y = y - text_height // 2 - LABEL_PADDING

    # Flip the chip to the other side of the marker if it would overflow.
    if box_x + text_width + LABEL_PADDING * 2 > image_width:
        box_x = x - MARKER_RADIUS - text_width - LABEL_PADDING * 3
    box_x = max(0, box_x)
    box_y = max(0, min(image_height - text_height - LABEL_PADDING * 2, box_y))

    draw.rectangle(
        [
            (box_x, box_y),
            (box_x + text_width + LABEL_PADDING * 2, box_y + text_height + LABEL_PADDING * 2),
        ],
        fill=LABEL_BACKGROUND,
    )
    draw.text(
        (box_x + LABEL_PADDING - left, box_y + LABEL_PADDING - top),
        label,
        font=font,
        fill=LABEL_TEXT,
    )
