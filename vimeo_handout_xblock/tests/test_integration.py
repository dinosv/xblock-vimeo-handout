"""Integration tests for the full XBlock lifecycle."""

import json
from unittest.mock import MagicMock, patch
from xblock.test.toy_runtime import ToyRuntime
from xblock.fields import ScopeIds
from vimeo_handout_xblock.vimeo_handout import VimeoHandoutXBlock


def _make_block(**kwargs):
    runtime = ToyRuntime()
    block = VimeoHandoutXBlock(runtime, scope_ids=ScopeIds("user", "vimeo_handout", "def_id", "usage_id"))
    for key, value in kwargs.items():
        setattr(block, key, value)
    return block


class TestFullRoundTrip:
    """Test saving settings then rendering student view."""

    def test_save_then_render(self):
        block = _make_block()
        embed = '<iframe src="https://player.vimeo.com/video/42" width="640" height="360"></iframe>'

        # Save via handler
        request = MagicMock()
        request.params = {}
        request.body = json.dumps({"vimeo_embed_code": embed}).encode()
        response = block.save_settings(request)
        data = json.loads(response.body)
        assert data["result"] == "success"

        # Render student view
        frag = block.student_view({})
        assert "player.vimeo.com/video/42" in frag.content

    @patch("vimeo_handout_xblock.vimeo_handout.default_storage")
    def test_upload_then_render(self, mock_storage):
        mock_storage.save.return_value = "xblock/vimeo/handout/notes.pdf"
        mock_storage.url.return_value = "/media/xblock/vimeo/handout/notes.pdf"

        block = _make_block(vimeo_embed_code="")

        # Upload handout
        upload = MagicMock()
        upload.file = MagicMock()
        upload.file.name = "notes.pdf"
        request = MagicMock()
        request.params = {"file": upload, "file_type": "handout"}
        response = block.upload_file(request)
        data = json.loads(response.body)
        assert data["result"] == "success"

        # Render student view
        frag = block.student_view({})
        assert "notes.pdf" in frag.content
