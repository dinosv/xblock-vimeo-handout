"""Vimeo Handout XBlock for Open edX."""

__version__ = "0.1.0"

try:
    from .vimeo_handout import VimeoHandoutXBlock
except ImportError:
    # XBlock SDK not installed (e.g. running unit tests for pure-Python modules).
    VimeoHandoutXBlock = None
