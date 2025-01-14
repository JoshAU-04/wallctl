import logging
import os
import subprocess
from typing import Generator, Optional

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

BLOCK_SIZE = 1024 * 1024

URL_BASE = "https://4kwallpapers.com"
URL_RAND = "/random-wallpapers"

DEFAULT_PATH = "~/Pictures/Wallpapers"

__all__ = ["download_rand", "apply_wallpaper"]


def fetch_html(url: str) -> BeautifulSoup:
    """Fetch the HTML content of a given URL.

    :param url: The URL to fetch the html from.
    :return: A beautiful soup. Literally.
    """

    try:
        response = requests.get(url, allow_redirects=True)
        response.raise_for_status()
        return BeautifulSoup(response.text, "lxml")
    except requests.RequestException as err:
        logging.error(f"Failed to fetch HTML: {err}")
        raise


def find_pages(base_url: str) -> Generator[str, None, None]:
    """Yield all page URLs from the given base URL.

    :param base_url: The base url. Such as https://4kwallpapers.com/
    :returns: A generator containing one or more hyperlink references.
    """

    soup = fetch_html(base_url)
    for link in soup.find_all("a", itemprop="url"):
        yield link["href"]


def extract_image_metadata(soup: BeautifulSoup) -> tuple[str, str]:
    """Extract image metadata from parsed HTML.

    :param soup: The soup to parse.
    :returns: A tuple that returns the postfix and href (respectively).
    """
    image_tag = soup.find("a", id="resolution")
    if not image_tag:
        raise ValueError("Image resolution link not found")
    postfix = soup.find("meta", itemprop="keywords")["content"]  # pyright: ignore
    href = image_tag["href"]  # pyright: ignore
    return postfix.replace(" ", "-").replace(",", "")[:20], href  # pyright: ignore


def download_image(url: str, filepath: str) -> None:
    """Download an image and save it to a file with a progress bar.

    :param url: The url to download.
    :param filepath: New filepath. Any already-existing paths will be
        overwritten.
    """

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get("content-length", 0))

        with (
            open(filepath, "wb") as file,
            tqdm(
                total=total_size, unit="B", unit_scale=True, desc="Downloading"
            ) as progress_bar,
        ):
            for chunk in response.iter_content(BLOCK_SIZE):
                file.write(chunk)
                progress_bar.update(len(chunk))
    except requests.RequestException as err:
        logging.exception(f"Failed to download {url}: {err}")


def process_page(url: str, index: Optional[int], path: Optional[str]) -> None:
    """Process a single page and download the corresponding image.

    :param url: The URL of the page to process. Important: Must be a *page*
        URL.
    :param index: This is an optional value used purely for sorting purposes.
    :param path: The path to download the wallpapers to. (default: ~/Pictures/Wallpapers)
    """
    soup = fetch_html(url)
    postfix, href = extract_image_metadata(soup)
    image_url = URL_BASE + href
    image_name = f"{index if index is not None else 'NA'}-{postfix}.jpg"
    if path is None:
        filepath = os.path.join(os.path.expanduser(DEFAULT_PATH), image_name)
    else:
        filepath = os.path.join(
            os.getcwd(), f"{index if index is not None else 'NA'}-{postfix}.jpg"
        )
    download_image(image_url, filepath)


def download_rand(path: str) -> None:
    """Download a random wallpaper from 4kwallpapers.com

    :param path: The path to download the wallpapers to.
    :returns: None
    """

    for index, page_url in enumerate(find_pages(URL_BASE + URL_RAND)):
        try:
            logging.info(f"Processing page {page_url}")
            process_page(page_url, index, path)
            logging.info("Done")
            logging.shutdown()
        except Exception as e:
            logging.error(f"Error processing page {page_url}: {e}")


def download_category(category: str, path: str) -> None:
    """Download a wallpaper from a specific category.

    :param category: The category to download from.
    :param path: Path to download the wallpapers to.
    """

    if category not in [
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
    ]:
        logging.exception("Invalid category: {}", category)

    url = f"{URL_BASE}/{category}"

    os.makedirs(os.path.expanduser(os.path.join(path, category)), exist_ok=True)

    for index, page_url in enumerate(find_pages(url)):
        try:
            logging.info(f"Processing page {page_url}")
            process_page(page_url, index, path)
            logging.info("Done")
            logging.shutdown()
        except Exception as e:
            logging.error(f"Error processing page {page_url}: {e}")


def apply_wallpaper(wallpaper: str, binary: Optional[str]) -> None:
    """Apply a wallpaper.

    Note that this applies to all monitors.

    This assumes that a wallpaper utility is set, such as:

     - xwallpaper
     - feh
     - wal?

    :param wallpaper: The wallpaper path to apply. (absolute path.)
    :param binary: The utility to set the wallpaper with.
    :raises FileNotFoundError: If the path doesn't exist.
    """

    if os.path.isfile(wallpaper) is not True:
        logging.exception("Cannot find {}", wallpaper)

    valid_binaries = ["feh", "xwallpaper"]
    logging.debug(binary)

    # when specified this makes my job a lot easier
    if binary not in valid_binaries:
        logging.exception("Invalid binary: {}", binary)

    match binary:
        case "feh":
            subprocess.run([binary, "--bg-scale", "--no-fehbg", wallpaper])
        case "xwallpaper":
            subprocess.run([binary, "--zoom", wallpaper])
        case _:
            logging.exception(
                f"{binary} not supported. (Please file a bug report) (ty)"
            )
