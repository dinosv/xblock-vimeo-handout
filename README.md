# xblock-vimeo-handout

Minimal XBlock for Open edX that embeds a Vimeo video (via native iframe embed
code) and provides handout/presentation file downloads.

## Installation

    pip install git+https://github.com/<org>/xblock-vimeo-handout.git

For Tutor: add to `OPENEDX_EXTRA_PIP_REQUIREMENTS` in your Tutor config.

Then add `"vimeo_handout"` to the Advanced Module List in Studio course settings.
