"""Sanitise Vimeo embed HTML to prevent XSS."""

from html.parser import HTMLParser

ALLOWED_ATTRS = {"src", "width", "height", "frameborder", "allow", "allowfullscreen"}
VIMEO_PREFIX = "https://player.vimeo.com/video/"


class _IframeExtractor(HTMLParser):
    """Extract iframe tags from HTML."""

    def __init__(self):
        super().__init__()
        self.iframes = []

    def handle_starttag(self, tag, attrs):
        if tag == "iframe":
            self.iframes.append(dict(attrs))


def sanitise_vimeo_embed(html):
    """Sanitise pasted Vimeo embed code.

    Returns a clean iframe string or raises ValueError.
    """
    if not html or not isinstance(html, str):
        raise ValueError("Embed code must be a non-empty string.")

    html = html.strip()
    if not html:
        raise ValueError("Embed code must be a non-empty string.")

    parser = _IframeExtractor()
    parser.feed(html)

    if not parser.iframes:
        raise ValueError("No iframe tag found in embed code.")

    if len(parser.iframes) > 1:
        raise ValueError("Embed code must contain a single iframe.")

    attrs = parser.iframes[0]
    src = attrs.get("src", "")

    if not src.startswith(VIMEO_PREFIX):
        raise ValueError(
            f"iframe src must start with {VIMEO_PREFIX} (got: {src!r}). "
            "Paste the embed code from Vimeo's share dialog."
        )

    safe_attrs = []
    for key in ALLOWED_ATTRS:
        if key in attrs:
            if key == "allowfullscreen":
                safe_attrs.append("allowfullscreen")
            else:
                value = attrs[key].replace('"', "&quot;")
                safe_attrs.append(f'{key}="{value}"')

    attr_str = " ".join(safe_attrs)
    return f"<iframe {attr_str}></iframe>"
