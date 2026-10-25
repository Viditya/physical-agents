"""Offline tests for the Azure AI Foundry vision stand-in response handling."""

from __future__ import annotations

from prototype.providers.magma import _extract_points


class TestMagmaPointExtraction:
    def test_extracts_points_from_a_json_markdown_fence(self):
        raw = (
            "```json\n"
            '[{"point": [50, 100], "label": "revision mark"}, '
            '{"point": [500, 800], "label": "title block"}]\n'
            "```"
        )

        assert _extract_points(raw) == [
            {"point": [50, 100], "label": "revision mark"},
            {"point": [500, 800], "label": "title block"},
        ]

    def test_returns_no_points_for_a_prose_response(self):
        assert _extract_points("The title block is at the lower right.") == []

    def test_returns_no_points_for_non_list_json(self):
        assert _extract_points('{"point": [50, 100], "label": "revision mark"}') == []

    def test_ignores_non_object_entries_without_losing_valid_points(self):
        raw = '[{"point": [50, 100], "label": "revision mark"}, "invalid", {}]'

        assert _extract_points(raw) == [{"point": [50, 100], "label": "revision mark"}]
