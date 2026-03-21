"""Vimeo Handout XBlock."""

import json
import os
from importlib import resources as _resources

from django.core.files.storage import default_storage
from django.template import Context, Template
from webob import Response
from xblock.core import XBlock
from xblock.fields import Scope, String
from web_fragments.fragment import Fragment


class VimeoHandoutXBlock(XBlock):
    """Embeds a Vimeo video and provides handout/presentation downloads."""

    display_name = String(
        display_name="Display Name",
        default="Vimeo Video",
        scope=Scope.settings,
    )
    vimeo_embed_code = String(
        display_name="Vimeo Embed Code",
        default="",
        scope=Scope.content,
        help="Paste the embed HTML from Vimeo's share dialog.",
    )
    handout_path = String(
        display_name="Handout file path",
        default="",
        scope=Scope.content,
    )
    handout_filename = String(
        display_name="Handout filename",
        default="",
        scope=Scope.content,
    )
    presentation_path = String(
        display_name="Presentation file path",
        default="",
        scope=Scope.content,
    )
    presentation_filename = String(
        display_name="Presentation filename",
        default="",
        scope=Scope.content,
    )

    @staticmethod
    def _resource_string(path):
        """Read a resource file from the package."""
        return (
            _resources.files("vimeo_handout_xblock")
            .joinpath(path)
            .read_text(encoding="utf-8")
        )

    def _get_download_url(self, path):
        """Generate a download URL for a stored file."""
        if not path:
            return ""
        return default_storage.url(path)

    def student_view(self, context=None):
        """Render the student-facing view."""
        template_str = self._resource_string("static/html/student_view.html")
        template = Template(template_str)
        ctx = Context(
            {
                "vimeo_embed_code": self.vimeo_embed_code,
                "handout_filename": self.handout_filename,
                "handout_url": self._get_download_url(self.handout_path),
                "presentation_filename": self.presentation_filename,
                "presentation_url": self._get_download_url(self.presentation_path),
            }
        )
        html = template.render(ctx)
        frag = Fragment(html)
        frag.add_css(self._resource_string("static/css/vimeo_handout.css"))
        return frag

    def studio_view(self, context=None):
        """Render the Studio editing view."""
        template_str = self._resource_string("static/html/studio_view.html")
        template = Template(template_str)
        ctx = Context({
            "vimeo_embed_code": self.vimeo_embed_code,
            "handout_filename": self.handout_filename,
            "presentation_filename": self.presentation_filename,
        })
        html = template.render(ctx)
        frag = Fragment(html)
        frag.initialize_js("VimeoHandoutStudioInit")
        return frag

    @XBlock.handler
    def save_settings(self, request, suffix=""):
        """Save the embed code."""
        from .sanitise import sanitise_vimeo_embed

        try:
            data = json.loads(request.body)
            embed_code = data.get("vimeo_embed_code", "").strip()
            if embed_code:
                embed_code = sanitise_vimeo_embed(embed_code)
            self.vimeo_embed_code = embed_code
            return Response(
                json_body={"result": "success"},
            )
        except (ValueError, json.JSONDecodeError) as exc:
            return Response(
                json_body={"result": "error", "message": str(exc)},
            )

    @XBlock.handler
    def upload_file(self, request, suffix=""):
        """Handle file upload for handout or presentation."""
        try:
            upload = request.params["file"]
            file_type = request.params.get("file_type", "")
            if file_type not in ("handout", "presentation"):
                raise ValueError("file_type must be 'handout' or 'presentation'")

            filename = os.path.basename(upload.file.name)
            storage_path = f"xblock/vimeo/{file_type}/{filename}"
            saved_path = default_storage.save(storage_path, upload.file)

            if file_type == "handout":
                self.handout_path = saved_path
                self.handout_filename = filename
            else:
                self.presentation_path = saved_path
                self.presentation_filename = filename

            return Response(
                json_body={"result": "success", "filename": filename},
            )
        except Exception as exc:
            return Response(
                json_body={"result": "error", "message": str(exc)},
            )
