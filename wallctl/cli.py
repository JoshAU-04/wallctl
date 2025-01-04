import logging
import os

from wallctl.parser import Parser

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


def main():
    parser = Parser()
    args = parser.parse()

    if args.path:
        path = os.path.join(
            os.path.expanduser(args.path),
            args.download_category if args.download_category else "",
        )
        os.makedirs(path, exist_ok=True)
        os.chdir(path)
    else:
        os.makedirs(os.path.expanduser(DEFAULT_PATH), exist_ok=True)
        os.chdir(os.path.expanduser(DEFAULT_PATH))
    if args.command == "random":
        download_rand(args.path)
    elif args.command == "category":
        download_category(args.download_category, args.path)
    elif args.command == "apply":
        apply_wallpaper(args.image, args.binary)
    elif args.url:
        url = args.url[0]
        download_image(url, os.path.basename(url))
