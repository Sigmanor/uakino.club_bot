import requests
from bs4 import BeautifulSoup
from utils import random_number
from contextlib import suppress
from config import uakino_url
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time


def create_session():
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def get_content_with_retry(url, headers, max_retries=3):
    for attempt in range(max_retries):
        try:
            session = create_session()
            response = session.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2**attempt)  # Exponential backoff


def get_content_on_page(category):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "uk,en-US;q=0.7,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

    url = f"https://{uakino_url}/{category}/f/c.year=1921,2024/sort=d.year;desc/"

    try:
        response = get_content_with_retry(url, headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Find last page number more reliably
        pagination = soup.select(".pagi-nav a")
        if pagination:
            pages = [int(p.text) for p in pagination if p.text.isdigit()]
            max_page = max(pages) if pages else 1
        else:
            max_page = 1

        movie_items = soup.select(".movie-item")
        if not movie_items:
            raise ValueError("No movie items found on page")

        random_page = random_number(1, max_page)
        random_content = random_number(1, len(movie_items))

        return [random_page, random_content]

    except requests.RequestException as e:
        logging.error(f"Request failed: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Error parsing content: {str(e)}")
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
