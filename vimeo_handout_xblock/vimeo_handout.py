"""Vimeo Handout XBlock."""

from importlib import resources as _resources

from django.template import Context, Template
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
        from django.core.files.storage import default_storage

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
