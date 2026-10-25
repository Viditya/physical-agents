"""Tests for Gemini Robotics-ER 2 response parsing.

These exercise only the response-parsing logic, not the network call, so
they run without a GEMINI_API_KEY.
"""

from __future__ import annotations

import json

from prototype.providers.gemini_robotics import _CODE_FENCE_RE


def _strip_fence(raw_text: str) -> str:
    """Mirror the fence-stripping done in describe_image."""
    match = _CODE_FENCE_RE.match(raw_text.strip())
    return match.group(1) if match else raw_text


class TestCodeFenceStripping:
    def test_strips_json_labelled_fence(self):
        raw = '```json\n[{"point": [1, 2], "label": "x"}]\n```'
        assert json.loads(_strip_fence(raw)) == [{"point": [1, 2], "label": "x"}]

    def test_strips_bare_fence(self):
        raw = '```\n[{"point": [1, 2], "label": "x"}]\n```'
        assert json.loads(_strip_fence(raw)) == [{"point": [1, 2], "label": "x"}]

    def test_passes_through_plain_json_unchanged(self):
        raw = '[{"point": [1, 2], "label": "x"}]'
        assert json.loads(_strip_fence(raw)) == [{"point": [1, 2], "label": "x"}]

    def test_real_world_multiline_response(self):
        # Captured live from gemini-robotics-er-2-preview on 2026-09-03.
        raw = (
            "```json\n"
            "[\n"
            '  {"point": [224, 278], "label": "dimension callout"},\n'
            '  {"point": [524, 307], "label": "component"}\n'
            "]\n"
            "```"
        )
        points = json.loads(_strip_fence(raw))
        assert len(points) == 2
        assert points[0]["label"] == "dimension callout"
