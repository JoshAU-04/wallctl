import argparse

__all__ = ["parse"]


def parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Wallpaper downloader")
    parser.add_argument(
        "--random",
        action="store_true",
        required=False,
        help="download a random wallpaper",
    )
    parser.add_argument(
        "--url",
        nargs=1,
        type=str,
        help="download a wallpaper from a given url",
    )

    parser.add_argument
    args = parser.parse_args()
    return args
