"""
Service for fetching random content from the UAKino website.
Handles page scraping and content extraction.
"""
import requests
from bs4 import BeautifulSoup
import logging
from typing import List, Tuple
from utils import random_number
from config.settings import uakino_url
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

logger = logging.getLogger(__name__)
# Constants for CSS selectors
PAGES_SELECTOR = "#dle-content > center > div.pagi-nav.clearfix > span.navigation > a:nth-child(12)"
MOVIE_ITEMS_SELECTOR = ".movie-item"

# Request headers and configuration
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
}

def create_session() -> requests.Session:
    """
    Create a requests session with retry logic.

    Returns:
        Configured requests session
    """
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session
def get_content_on_page(category: str) -> Tuple[int, int]:
    """
    Get random page and content numbers for the given category.
    response.raise_for_status()
    Args:
        category: Content category (filmy, cartoon, seriesss)
        "#dle-content > center > div.pagi-nav.clearfix > span.navigation > a:nth-child(12)"
    Returns:
        Tuple of (random_page, random_content_index)
    """
    url = f"https://{uakino_url}/{category}/f/c.year=1921,2024/sort=d.year;desc/"

    try:
        session = create_session()
        response = session.get(url, headers=HEADERS)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        pages_count = soup.select_one(PAGES_SELECTOR)
        movie_items = soup.select(MOVIE_ITEMS_SELECTOR)

        if not pages_count or not movie_items:
            raise ValueError("Failed to find pagination or movie items")

        random_page = random_number(1, int(pages_count.get_text().strip()))
        random_content = random_number(1, len(movie_items))

        return random_page, random_content
    except Exception as e:
        logger.error(f"Error fetching content page: {e}")
        raise
    random_page = random_number(1, int(pages_count.get_text().strip()))
def get_random_content(category: str) -> List[str]:
    """
    Fetch random content information from the specified category.

    Args:
        category: Content category (filmy, cartoon, seriesss)
    return [random_page, random_content]
    Returns:
        List containing content information:
        [name, year, genre, link, description, imdb, image_url, actors]
    """
    try:
        random_page, random_index = get_content_on_page(category)
        url = f"https://{uakino_url}/{category}/f/c.year=1921,2024/sort=date;desc/page/{random_page}/"
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
        session = create_session()
        response = session.get(url, headers=HEADERS)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        base_selector = f"#dle-content > div:nth-child({random_index})"

        # Extract content information
        content_name = soup.select_one(f"{base_selector} > a")
        content_link = soup.select_one(f"{base_selector} > div.movie-img > a")
        content_year = soup.select_one(f"{base_selector} > div.movie-desc > div.clearfix > div:nth-child(5) > div.deck-value > a")
        content_genre = soup.select_one(f"{base_selector} > div.movie-desc > div.clearfix > div:nth-child(4) > div.deck-value")
        content_description = soup.select_one(f"{base_selector} > div.movie-desc > div.movie-text > span.desc-about-text")
        content_image = soup.select_one(f"{base_selector} > div.movie-img > img")

        if not all([content_name, content_link, content_year, content_genre, content_description, content_image]):
            raise ValueError("Failed to extract required content information")

        # Extract IMDb rating
        content_imdb = "🤷‍♂️"
        imdb_element = soup.select_one(f"{base_selector} > div.movie-desc > div.clearfix > div:nth-child(3) > div.deck-value")
        if imdb_element:
            imdb_text = imdb_element.get_text(strip=True)
            if imdb_text:
                content_imdb = imdb_text
    response.raise_for_status()
        # Extract actors
        content_actors = ""
        actors_section = soup.select_one(f"{base_selector} > div.movie-desc > div.clearfix > div:nth-child(6) > div.deck-value")
        if actors_section:
            actor_links = actors_section.find_all("a")
            content_actors = ", ".join(link.get_text(strip=True) for link in actor_links)
        .strip()
        return [
            content_name.get_text().strip(),
            content_year.get_text().strip(),
            content_genre.get_text().strip().replace(" ,", ","),
            content_link.get("href"),
            content_description.get_text().strip(),
            content_imdb,
            f"https://{uakino_url}{content_image.get('src')}",
            content_actors,
        ]
        f"#dle-content > div:nth-child({random_content[1]}) > div.movie-img > a"
    except Exception as e:
        logger.error(f"Error fetching random content: {e}")
        raise
        content_actors,
    ]
