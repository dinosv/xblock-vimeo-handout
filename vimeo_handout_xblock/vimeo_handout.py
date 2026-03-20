"""Vimeo Handout XBlock."""

from xblock.core import XBlock
from xblock.fragment import Fragment


class VimeoHandoutXBlock(XBlock):
    """Embeds a Vimeo video and provides handout/presentation downloads."""

    display_name = "Vimeo + Handout"
