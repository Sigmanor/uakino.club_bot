import pytest
from unittest.mock import Mock, patch, MagicMock
from bs4 import BeautifulSoup
import requests
from src.content_fetcher import create_session, get_content_on_page, get_random_content

MOCK_HTML_CONTENT = """
<div id="dle-content">
    <div class="movie-item"></div>
    <div>
        <a>Test Movie</a>
        <div class="movie-img">
            <a href="/movie/123">Link</a>
            <img src="/image.jpg">
        </div>
        <div class="movie-desc">
            <div class="clearfix">
                <div></div>
                <div></div>
                <div>
                    <div class="deck-value">8.5</div>
                </div>
                <div>
                    <div class="deck-value">Action, Drama</div>
                </div>
                <div>
                    <div class="deck-value">
                        <a>2022</a>
                    </div>
                </div>
            </div>
            <div class="movie-text">
                <span class="desc-about-text">Movie description</span>
            </div>
        </div>
    </div>
    <div>
        <div class="movie-desc">
            <div class="clearfix">
                <div></div>
                <div></div>
                <div></div>
                <div></div>
                <div></div>
                <div>
                    <div class="deck-value">
                        <a>Actor 1</a>
                        <a>Actor 2</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <center>
        <div class="pagi-nav clearfix">
            <span class="navigation">
                <a>1</a>
                <a>2</a>
                <a>3</a>
                <a>4</a>
                <a>5</a>
                <a>6</a>
                <a>7</a>
                <a>8</a>
                <a>9</a>
                <a>10</a>
                <a>11</a>
                <a>12</a>
            </span>
        </div>
    </center>
</div>
"""


@pytest.fixture
def mock_session():
    session = Mock()
    adapter = Mock()
    adapter.max_retries = Mock()
    adapter.max_retries.total = 3
    adapter.max_retries.backoff_factor = 0.5
    adapter.max_retries.status_forcelist = [500, 502, 503, 504]
    session.adapters = {"https://": adapter}
    return session


@pytest.fixture
def mock_response():
    response = Mock()
    response.text = MOCK_HTML_CONTENT
    response.raise_for_status = Mock()
    return response


@pytest.fixture
def mock_random():
    with patch("src.content_fetcher.random_number") as mock:
        mock.return_value = 2
        yield mock


@patch("src.content_fetcher.uakino_url", "test.com")
def test_create_session():
    session = create_session()
    assert isinstance(session, requests.Session)
    adapter = session.adapters["https://"]
    assert adapter.max_retries.total == 3
    assert adapter.max_retries.backoff_factor == 0.5
    assert set(adapter.max_retries.status_forcelist) == {500, 502, 503, 504}


@patch("src.content_fetcher.uakino_url", "test.com")
@patch("src.content_fetcher.create_session")
def test_get_content_on_page_success(
    mock_create_session, mock_session, mock_response, mock_random
):
    mock_create_session.return_value = mock_session
    mock_session.get.return_value = mock_response

    result = get_content_on_page("movies")

    assert result == [2, 2]
    mock_session.get.assert_called_once_with(
        "https://test.com/movies/f/c.year=1921,2022/sort=d.year;desc/",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
        },
        timeout=10,
    )


@patch("src.content_fetcher.uakino_url", "test.com")
@patch("src.content_fetcher.create_session")
def test_get_content_on_page_error(mock_create_session, mock_session):
    mock_create_session.return_value = mock_session
    mock_session.get.side_effect = requests.exceptions.RequestException("Test error")

    with pytest.raises(requests.exceptions.RequestException):
        get_content_on_page("movies")


@patch("src.content_fetcher.uakino_url", "test.com")
@patch("requests.get")
@patch("src.content_fetcher.get_content_on_page")
def test_get_random_content_success(mock_get_content_on_page, mock_get, mock_random):
    mock_get_content_on_page.return_value = [2, 2]
    mock_response = Mock()
    mock_response.text = MOCK_HTML_CONTENT
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    result = get_random_content("movies")

    mock_get.assert_called_once_with(
        "https://test.com/movies/f/c.year=1921,2024/sort=date;desc/page/2/",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
        },
    )

    assert isinstance(result, list)
    assert len(result) == 8
    assert result[0] == "Test Movie"
    assert result[1] == "2022"
    assert result[2] == "Action, Drama"
    assert result[3] == "/movie/123"
    assert result[4] == "Movie description"
    assert result[5] == "8.5"
    assert result[6] == "https://test.com/image.jpg"
    assert result[7] == "Actor 1, Actor 2"


@patch("src.content_fetcher.uakino_url", "test.com")
@patch("requests.get")
@patch("src.content_fetcher.get_content_on_page")
def test_get_random_content_error(mock_get_content_on_page, mock_get):
    mock_get_content_on_page.return_value = [2, 2]
    mock_get.side_effect = requests.exceptions.RequestException("Test error")

    with pytest.raises(requests.exceptions.RequestException):
        get_random_content("movies")
