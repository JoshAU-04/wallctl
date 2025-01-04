"""Python setup.py for wallctl package"""

import io
import os

from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file 'safely'.
    >>> read("wallctl", "VERSION")
    '0.2.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path: str):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="wallctl",
    version="0.2.0",
    description="Wallpaper downloader",
    url="https://github.com/JoshAU-04/wallctl/",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="JoshAU-04",
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=read_requirements("requirements.txt"),
    entry_points={"console_scripts": ["wallctl = wallctl.__main__:main"]},
    extras_require={"dev": read_requirements("requirements-dev.txt")},
)
