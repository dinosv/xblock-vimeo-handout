"""Tests for VimeoHandoutXBlock studio view and handlers."""

import json
import pytest
from unittest.mock import MagicMock, patch, mock_open
from xblock.test.toy_runtime import ToyRuntime
from xblock.fields import ScopeIds
from vimeo_handout_xblock.vimeo_handout import VimeoHandoutXBlock


def _make_block(**kwargs):
    runtime = ToyRuntime()
    block = VimeoHandoutXBlock(runtime, scope_ids=ScopeIds("user", "vimeo_handout", "def_id", "usage_id"))
    for key, value in kwargs.items():
        setattr(block, key, value)
    return block


class TestStudioView:
    """Test studio_view rendering."""

    def test_renders_studio_form(self):
        block = _make_block()
        frag = block.studio_view({})
        assert "<textarea" in frag.content

    def test_shows_current_embed_code(self):
        embed = '<iframe src="https://player.vimeo.com/video/999"></iframe>'
        block = _make_block(vimeo_embed_code=embed)
        frag = block.studio_view({})
        assert "999" in frag.content


class TestSaveHandler:
    """Test the save_settings handler."""

    def test_save_valid_embed_code(self):
        block = _make_block()
        embed = '<iframe src="https://player.vimeo.com/video/123" width="640" height="360"></iframe>'
        request = MagicMock()
        request.params = {}
        request.body = json.dumps({"vimeo_embed_code": embed}).encode()
        response = block.save_settings(request)
        data = json.loads(response.body)
        assert data["result"] == "success"
        assert "player.vimeo.com/video/123" in block.vimeo_embed_code

    def test_save_invalid_embed_code(self):
        block = _make_block()
        request = MagicMock()
        request.params = {}
        request.body = json.dumps({"vimeo_embed_code": "<script>alert(1)</script>"}).encode()
        response = block.save_settings(request)
        data = json.loads(response.body)
        assert data["result"] == "error"


class TestFileUploadHandler:
    """Test the file upload handler."""

    @patch("vimeo_handout_xblock.vimeo_handout.default_storage")
    def test_upload_handout(self, mock_storage):
        mock_storage.save.return_value = "xblock/vimeo/handout/test.pdf"
        block = _make_block()
        upload = MagicMock()
        upload.file = MagicMock()
        upload.file.name = "test.pdf"
        request = MagicMock()
        request.params = {"file": upload, "file_type": "handout"}
        response = block.upload_file(request)
        data = json.loads(response.body)
        assert data["result"] == "success"
        assert block.handout_filename == "test.pdf"

    @patch("vimeo_handout_xblock.vimeo_handout.default_storage")
    def test_upload_presentation(self, mock_storage):
        mock_storage.save.return_value = "xblock/vimeo/presentation/slides.pptx"
        block = _make_block()
        upload = MagicMock()
        upload.file = MagicMock()
        upload.file.name = "slides.pptx"
        request = MagicMock()
        request.params = {"file": upload, "file_type": "presentation"}
        response = block.upload_file(request)
        data = json.loads(response.body)
        assert data["result"] == "success"
        assert block.presentation_filename == "slides.pptx"
