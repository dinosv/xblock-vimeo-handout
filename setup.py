import os
from setuptools import setup


def package_data(pkg, roots):
    data = []
    for root in roots:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))
    return {pkg: data}


setup(
    name="xblock-vimeo-handout",
    version="0.1.0",
    description="Minimal Vimeo embed + handout/presentation XBlock for Open edX",
    author="DSV",
    packages=["vimeo_handout_xblock"],
    python_requires=">=3.11",
    install_requires=["xblock", "web-fragments"],
    entry_points={"xblock.v1": ["vimeo_handout = vimeo_handout_xblock:VimeoHandoutXBlock"]},
    package_data=package_data("vimeo_handout_xblock", ["static"]),
    license="AGPLv3",
)
