import logging
import os

from wallctl.parser import parse

from .base import download_image, download_rand

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():
    args = parse()

    if args.random:
        download_rand()
    elif args.url:
        url = args.url[0]
        download_image(url, os.path.basename(url))
