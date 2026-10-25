"""Microsoft-ecosystem vision provider.

IMPORTANT HONESTY NOTE: this provider is NOT Microsoft Magma. It calls a
real Azure AI Foundry vision deployment (e.g. a GPT-4o-class model such as
the `4Omni` deployment) as the practical "stay inside the Microsoft/Azure
boundary" option -- which matters because Aino itself already runs on
Azure AI Search, so keeping this capability in the same ecosystem avoids
adding a second cloud AI vendor relationship. The `magma` name is legacy
demo routing only.

Update 2026-09-29: real Magma-8B is listed in the Foundry model catalog;
Foundry Managed Compute (preview) may host it if it is available in the
project (it needs a GPU quota request). It also expects a
different output format (x-first, 0-1 scale, mark-based). See
docs/magma-readiness.md before adding it. Give real Magma its own provider
and rename this one, so results from the two are never confused.

Requires FOUNDRY_API_KEY, FOUNDRY_ENDPOINT, and FOUNDRY_DEPLOYMENT in the
environment (see .env.example).
"""

import base64
import json
import os

from openai import AzureOpenAI

from prototype.base import VisionProvider
from prototype.providers.gemini_robotics import _CODE_FENCE_RE

DEFAULT_PROMPT = (
    "Describe the objects visible in this image and, where possible, "
    "their approximate positions relative to each other (e.g. top-left, "
    "center, near the X). Be specific about labels/tags/text visible on "
    "objects."
)


def _extract_points(raw_text: str) -> list[dict]:
    """Return point observations when the deployment followed the JSON prompt."""
    fence_match = _CODE_FENCE_RE.match(raw_text.strip())
    json_text = fence_match.group(1) if fence_match else raw_text
    try:
        parsed = json.loads(json_text)
    except (json.JSONDecodeError, TypeError):
        return []

    if not isinstance(parsed, list):
        return []
    return [item for item in parsed if isinstance(item, dict) and "point" in item]


class MagmaProvider(VisionProvider):
    """Azure AI Foundry vision provider (stand-in for Magma -- see module docstring)."""

    def __init__(self) -> None:
        api_key = os.getenv("FOUNDRY_API_KEY")
        endpoint = os.getenv("FOUNDRY_ENDPOINT")
        self._deployment = os.getenv("FOUNDRY_DEPLOYMENT", "gpt-4o")
        if not api_key or not endpoint:
            raise EnvironmentError(
                "FOUNDRY_API_KEY and FOUNDRY_ENDPOINT must both be set. "
                "Copy .env.example to .env and fill in real values from "
                "your Azure AI Foundry resource."
            )
        self._client = AzureOpenAI(
            api_key=api_key,
            azure_endpoint=endpoint,
            api_version="2024-12-01-preview",
        )

    def describe_image(self, image_path: str, prompt: str = DEFAULT_PROMPT) -> dict:
        """Send *image_path* to an Azure AI Foundry vision deployment.

        Returns:
            {
                "provider": "azure_ai_foundry_vision",
                "deployment": <deployment name>,
                "description": <the model's text response>,
                "points": [{"point": [y, x], "label": str}, ...],
                "raw_text": <the model's raw response text>,
            }

        The Foundry deployment may return either prose or the point JSON
        requested by the demo prompt. JSON wrapped in a Markdown fence is
        parsed into points so the existing overlay pipeline can render it.
        """
        with open(image_path, "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode("utf-8")

        response = self._client.chat.completions.create(
            model=self._deployment,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_b64}"
                            },
                        },
                    ],
                }
            ],
        )

        raw_text = response.choices[0].message.content or ""
        return {
            "provider": "azure_ai_foundry_vision",
            "deployment": self._deployment,
            "description": raw_text,
            "points": _extract_points(raw_text),
            "raw_text": raw_text,
        }
