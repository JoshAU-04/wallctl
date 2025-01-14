import logging
import os

from wallctl.parser import Parser
from typing import Union, Literal

from .base import (
    DEFAULT_PATH,
    apply_wallpaper,
    download_category,
    download_image,
    download_rand,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_path(args) -> Union[Literal[""], str]:
    path: str = ""
    if args.path:
        path = os.path.expanduser(args.path)
        os.makedirs(path, exist_ok=True)
        os.chdir(path)
    else:
        os.makedirs(os.path.expanduser(DEFAULT_PATH), exist_ok=True)
        os.chdir(os.path.expanduser(DEFAULT_PATH))
    return path


def main():
    parser = Parser()
    args = parser.parse()
    path = get_path(args)

    if args.command == "random":
        download_rand(path)
    elif args.command == "category":
        if args.download_category:
            path = os.path.join(args.download_category)
            download_category(args.download_category, path)
    elif args.command == "apply":
        apply_wallpaper(args.image, args.binary)
    elif args.url:
        url = args.url[0]
        download_image(url, os.path.basename(url))
