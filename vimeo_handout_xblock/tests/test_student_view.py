"""Tests for VimeoHandoutXBlock student view."""

import pytest
from unittest.mock import MagicMock, patch
from xblock.fields import ScopeIds
from xblock.test.toy_runtime import ToyRuntime
from vimeo_handout_xblock.vimeo_handout import VimeoHandoutXBlock


def _make_block(**kwargs):
    """Create a VimeoHandoutXBlock instance for testing."""
    runtime = ToyRuntime()
    scope_ids = ScopeIds("student_1", "vimeo_handout", "def_id_1", "usage_id_1")
    block = VimeoHandoutXBlock(runtime, scope_ids=scope_ids)
    for key, value in kwargs.items():
        setattr(block, key, value)
    return block


class TestStudentView:
    """Test student_view rendering."""

    def test_renders_embed_code(self):
        embed = '<iframe src="https://player.vimeo.com/video/123" width="640" height="360"></iframe>'
        block = _make_block(vimeo_embed_code=embed)
        frag = block.student_view({})
        assert "player.vimeo.com/video/123" in frag.content

    def test_no_embed_shows_placeholder(self):
        block = _make_block(vimeo_embed_code="")
        frag = block.student_view({})
        assert "No video" in frag.content or "no video" in frag.content.lower()

    def test_handout_link_shown_when_set(self):
        block = _make_block(
            vimeo_embed_code="",
            handout_filename="lecture1.pdf",
        )
        frag = block.student_view({})
        assert "lecture1.pdf" in frag.content

    def test_presentation_link_shown_when_set(self):
        block = _make_block(
            vimeo_embed_code="",
            presentation_filename="slides.pdf",
        )
        frag = block.student_view({})
        assert "slides.pdf" in frag.content

    def test_no_download_links_when_no_files(self):
        block = _make_block(vimeo_embed_code="", handout_filename="", presentation_filename="")
        frag = block.student_view({})
        assert "download" not in frag.content.lower() or "No" in frag.content
