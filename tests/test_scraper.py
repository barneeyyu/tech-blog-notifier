import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from unittest.mock import MagicMock
from scraper import fetch_articles

def _make_feed(entries):
    feed = MagicMock()
    feed.entries = entries
    feed.bozo = False
    return feed

def _make_entry(id_, title, summary, link, published_parsed=None):
    import time
    e = MagicMock()
    e.id = id_
    e.title = title
    e.summary = summary
    e.link = link
    e.published_parsed = published_parsed or time.gmtime()
    return e

def test_fetch_articles_returns_list(mocker):
    entry = _make_entry("id1", "Hello World", "Summary text", "https://example.com/1")
    mocker.patch("feedparser.parse", return_value=_make_feed([entry]))
    articles = fetch_articles("https://example.com/rss")
    assert isinstance(articles, list)
    assert len(articles) == 1

def test_fetch_articles_maps_fields(mocker):
    entry = _make_entry("id1", "Hello World", "Summary text", "https://example.com/1")
    mocker.patch("feedparser.parse", return_value=_make_feed([entry]))
    articles = fetch_articles("https://example.com/rss")
    a = articles[0]
    assert a["id"] == "id1"
    assert a["title"] == "Hello World"
    assert a["body"] == "Summary text"
    assert a["url"] == "https://example.com/1"

def test_fetch_articles_returns_empty_on_error(mocker):
    mocker.patch("feedparser.parse", side_effect=Exception("network error"))
    articles = fetch_articles("https://example.com/rss")
    assert articles == []
