"""Google Gemini Robotics-ER 2 provider.

Confirmed real API shape as of 2026-08-22 (see RESEARCH_LOG.md and
ai.google.dev/gemini-api/docs/robotics-overview): the model takes an
uploaded image plus a text prompt and returns normalized [y, x] point
coordinates (0-1000 scale) with labels, as JSON text.

Requires GEMINI_API_KEY in the environment (see .env.example).
"""

import json
import os
import re

from google import genai

from prototype.base import VisionProvider

# Despite the prompt asking for plain JSON, the model commonly wraps its
# answer in a markdown code fence (```json ... ``` or ``` ... ```) --
# confirmed live 2026-09-03. Strip that fence before parsing.
_CODE_FENCE_RE = re.compile(r"^```(?:json)?\s*(.*?)\s*```$", re.DOTALL)

DEFAULT_PROMPT = (
    'Point to no more than 20 items in the image. The label returned '
    'should be an identifying name for the object detected. The answer '
    'should follow the json format: [{"point": <point>, "label": '
    '<label>}, ...]. The points are in [y, x] format normalized to 0-1000.'
)

MODEL_ID = "gemini-robotics-er-2-preview"


class GeminiRoboticsProvider(VisionProvider):
    """Gemini Robotics-ER 2 vision-spatial provider."""

    def __init__(self) -> None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "GEMINI_API_KEY is not set. Copy .env.example to .env and "
                "fill in a real key from Google AI Studio."
            )
        self._client = genai.Client(api_key=api_key)

    def describe_image(self, image_path: str, prompt: str = DEFAULT_PROMPT) -> dict:
        """Upload *image_path* and ask Gemini Robotics-ER 2 to locate objects.

        Returns:
            {
                "provider": "gemini_robotics_er_2",
                "model": MODEL_ID,
                "points": [{"point": [y, x], "label": str}, ...],
                "raw_text": <the model's raw response text>,
            }

        If the model's response isn't valid JSON (it's a preview model,
        this can happen), "points" is an empty list and "raw_text" still
        carries the full response for manual inspection.
        """
        uploaded_file = self._client.files.upload(file=image_path)

        response = self._client.models.generate_content(
            model=MODEL_ID,
            contents=[uploaded_file, prompt],
        )

        raw_text = response.text or ""
        fence_match = _CODE_FENCE_RE.match(raw_text.strip())
        json_text = fence_match.group(1) if fence_match else raw_text
        try:
            points = json.loads(json_text)
        except (json.JSONDecodeError, TypeError):
            points = []

        return {
            "provider": "gemini_robotics_er_2",
            "model": MODEL_ID,
            "points": points,
            "raw_text": raw_text,
        }
