import argparse

__all__ = ["parse"]


def parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Wallpaper downloader")
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Available commands"
    )

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

    apply_parser = subparsers.add_parser("apply", help="Apply a wallpaper")
    apply_parser.add_argument("image", nargs=1, type=str, help="The image to apply.")
    apply_parser.add_argument(
        "--binary",
        nargs=1,
        help="The binary to select to apply the wallpaper.",
        choices=["xwallpaper", "feh"],
    )

    parser.add_argument
    args = parser.parse_args()
    return args
