import argparse

__all__ = ["parse"]


def parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Wallpaper downloader")
    parser.add_argument(
        "random",
        help="download a random wallpaper",
    )
    args = parser.parse_args()
    return args
