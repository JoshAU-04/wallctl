import argparse


from .base import DEFAULT_PATH


class Parser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Download and apply wallpapers from 4kwallpapers.com"
        )

        self.subparsers = self.parser.add_subparsers(
            title="Commands",
            dest="command",
            required=True,
        )

        self.parser.add_argument(
            "--url",
            type=str,
            help="download a wallpaper from a given url",
        )

        category_parser = self.subparsers.add_parser(
            "category",
            help="Download a wallpaper from a specific category",
        )

        category_parser.add_argument(
            "download_category",
            type=str,
            help="The category to download the wallpaper from",
            choices=[
                "abstract",
                "animals",
                "anime",
                "architecture",
                "bikes",
                "black-dark",
                "cars",
                "celebrities",
                "cute",
                "fantasy",
                "flowers",
                "food",
                "games",
                "gradients",
                "CGI",
                "lifestyle",
                "love",
                "military",
                "minimal",
                "movies",
                "music",
                "nature",
                "people",
                "photography",
                "quotes",
                "sci-fi",
                "space",
                "sports",
                "technology",
                "world",
            ],
        )

        category_parser.add_argument(
            "--resolution",
            type=str,
            help="The resolution of the wallpaper to download",
        )

        random_parser = self.subparsers.add_parser(
            "random", help="Download a random wallpaper"
        )
        random_parser.add_argument(
            "--resolution",
            type=str,
            help="The resolution of the wallpaper to download",
        )

        apply_parser = self.subparsers.add_parser("apply", help="Apply a wallpaper")
        apply_parser.add_argument("image", type=str, help="The image to apply.")

        apply_parser.add_argument(
            "--binary",
            help="The binary to select to apply the wallpaper.",
            choices=["xwallpaper", "feh"],
        )

        self.parser.add_argument(
            "--path",
            type=str,
            help="The path to download the wallpapers to.",
            default=DEFAULT_PATH,
        )

    def parse(self) -> argparse.Namespace:
        return self.parser.parse_args()
