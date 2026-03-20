"""Tests for Vimeo iframe sanitisation."""

import pytest
from vimeo_handout_xblock.sanitise import sanitise_vimeo_embed


class TestSanitiseVimeoEmbed:
    """Test iframe sanitisation."""

    def test_valid_embed(self):
        html = (
            '<iframe src="https://player.vimeo.com/video/123456789"'
            ' width="640" height="360" frameborder="0"'
            ' allow="autoplay; fullscreen" allowfullscreen></iframe>'
        )
        result = sanitise_vimeo_embed(html)
        assert 'src="https://player.vimeo.com/video/123456789"' in result
        assert "<iframe" in result
        assert "</iframe>" in result

    def test_valid_embed_with_query_params(self):
        html = (
            '<iframe src="https://player.vimeo.com/video/123456789'
            '?badge=0&amp;autopause=0" width="640" height="360"'
            ' frameborder="0" allowfullscreen></iframe>'
        )
        result = sanitise_vimeo_embed(html)
        assert "player.vimeo.com/video/123456789" in result

    def test_rejects_non_vimeo_src(self):
        html = '<iframe src="https://evil.com/video"></iframe>'
        with pytest.raises(ValueError, match="Vimeo"):
            sanitise_vimeo_embed(html)

    def test_rejects_no_iframe(self):
        html = '<div>not an iframe</div>'
        with pytest.raises(ValueError, match="iframe"):
            sanitise_vimeo_embed(html)

    def test_rejects_multiple_iframes(self):
        html = (
            '<iframe src="https://player.vimeo.com/video/1"></iframe>'
            '<iframe src="https://player.vimeo.com/video/2"></iframe>'
        )
        with pytest.raises(ValueError, match="single"):
            sanitise_vimeo_embed(html)

    def test_rejects_script_injection(self):
        html = (
            '<iframe src="https://player.vimeo.com/video/123"'
            ' onload="alert(1)"></iframe>'
        )
        result = sanitise_vimeo_embed(html)
        assert "onload" not in result

    def test_strips_surrounding_markup(self):
        html = (
            '<div><script>alert(1)</script>'
            '<iframe src="https://player.vimeo.com/video/123"'
            ' width="640" height="360"></iframe></div>'
        )
        result = sanitise_vimeo_embed(html)
        assert "<script>" not in result
        assert "<div>" not in result

    def test_rejects_empty_input(self):
        with pytest.raises(ValueError):
            sanitise_vimeo_embed("")

    def test_rejects_none_input(self):
        with pytest.raises(ValueError):
            sanitise_vimeo_embed(None)
