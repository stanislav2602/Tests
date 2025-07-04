import pytest
from scraping import scrape_articles
from unittest.mock import patch, Mock

MOCK_HTML = """
<html>
    <body>
        <article class="tm-articles-list__item">
            <h2 class="tm-title">
                <a class="tm-title__link" href="/ru/articles/1/">Тестовая статья 1</a>
            </h2>
            <time datetime="2023-10-01">2023-10-01</time>
            <div class="article-formatted-body">Статья про дизайн и фото</div>
            <a class="tm-article-snippet__hubs-item-link">web</a>
        </article>
        <article class="tm-articles-list__item">
            <h2 class="tm-title">
                <a class="tm-title__link" href="/ru/articles/2/">Тестовая статья 2</a>
            </h2>
            <time datetime="2023-10-02">2023-10-02</time>
            <div class="article-formatted-body">Статья про что-то другое</div>
            <a class="tm-article-snippet__hubs-item-link">технологии</a>
        </article>
    </body>
</html>
"""

@pytest.mark.parametrize("mock_html, expected_results", [
    (
        MOCK_HTML,
        [
            {
                'date': '2025-06-04',
                'title': 'Тестовая статья',
                'link': 'https://habr.com/ru/articles/'
            }
        ]
    ),
    (
        "<html><body></body></html>",
        []
    ),
])
def test_scrape_articles(mock_html, expected_results):
    with patch('scraping.requests.get') as mock_get, \
         patch('scraping.BeautifulSoup') as mock_soup:
        mock_response = Mock()
        mock_response.text = mock_html
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        mock_soup.return_value = BeautifulSoup(mock_html, 'html.parser')
        results = scrape_articles()
        assert results == expected_results

def test_scrape_articles_request_error():
    with patch('scraping.requests.get') as mock_get:
        mock_get.side_effect = Exception("Ошибка соединения")
        results = scrape_articles()
        assert 'error' in results
        assert "Ошибка соединения" in results['error']