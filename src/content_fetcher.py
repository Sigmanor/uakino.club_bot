import requests
from bs4 import BeautifulSoup
from src.utils import random_number
from src.config import uakino_url
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging

logger = logging.getLogger(__name__)


def create_session():
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retries))
    return session


def get_content_on_page(category):
    session = create_session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    }

    try:
        url = f"https://{uakino_url}/{category}/f/c.year=1921,2022/sort=d.year;desc/"
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        pages_count = soup.select_one(
            "#dle-content > center > div.pagi-nav.clearfix > span.navigation > a:nth-child(12)"
        )

        movie_items = soup.select(".movie-item")
        random_page = random_number(1, int(pages_count.get_text().strip()))
        random_content = random_number(1, len(movie_items))

        return [random_page, random_content]
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching content: {e}")
        raise


def get_random_content(category):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    }

    random_content = get_content_on_page(category)

    url = f"https://{uakino_url}/{category}/f/c.year=1921,2024/sort=date;desc/page/{random_content[0]}/"

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    content_name = (
        soup.select_one(f"#dle-content > div:nth-child({random_content[1]}) > a")
        .get_text()
        .strip()
    )

    content_link = soup.select_one(
        f"#dle-content > div:nth-child({random_content[1]}) > div.movie-img > a"
    ).get("href")

    content_year = (
        soup.select_one(
            f"#dle-content > div:nth-child({random_content[1]}) > div.movie-desc > div.clearfix > div:nth-child(5) > div.deck-value > a"
        )
        .get_text()
        .strip()
    )

    content_genre = (
        soup.select_one(
            f"#dle-content > div:nth-child({random_content[1]}) > div.movie-desc > div.clearfix > div:nth-child(4) > div.deck-value"
        )
        .get_text()
        .strip()
        .replace(" ,", ",")
    )

    content_description = (
        soup.select_one(
            f"#dle-content > div:nth-child({random_content[1]}) > div.movie-desc > div.movie-text > span.desc-about-text"
        )
        .get_text()
        .strip()
    )

    content_image = soup.select_one(
        f"#dle-content > div:nth-child({random_content[1]}) > div.movie-img > img"
    ).get("src")

    content_imdb = "🤷‍♂️"
    element = soup.select_one(
        f"#dle-content > div:nth-child({random_content[1]}) > div.movie-desc > div.clearfix > div:nth-child(3) > div.deck-value"
    )
    if element:
        text = element.get_text(strip=True)
        if text:
            content_imdb = text

    content_actors_section = soup.select_one(
        f"#dle-content > div:nth-child(3) > div.movie-desc > div.clearfix > div:nth-child(6) > div.deck-value"
    )

    content_actors = ""

    if content_actors_section:
        links = content_actors_section.find_all("a")
        content_actors = ", ".join(link.get_text(strip=True) for link in links)

    return [
        content_name,
        content_year,
        content_genre,
        content_link,
        content_description,
        content_imdb,
        f"https://{uakino_url}{content_image}",
        content_actors,
    ]
