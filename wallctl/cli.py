import logging

from wallctl.parser import parse

from .base import download_rand

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():
    args = parse()

    if args.random:
        download_rand()
