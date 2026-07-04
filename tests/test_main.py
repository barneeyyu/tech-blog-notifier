import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from unittest.mock import MagicMock, patch

def test_new_articles_are_processed(mocker):
    mocker.patch("main.load_state", return_value={"netflix": []})
    mocker.patch("main.save_state")
    mocker.patch("main.fetch_articles", return_value=[
        {"id": "id1", "title": "New Article", "body": "Body", "url": "https://x.com"}
    ])
    mocker.patch("main.summarize_article", return_value={
        "zh_title": "新文章", "zh_summary": "摘要"
    })
    mock_broadcast = mocker.patch("main.broadcast_article")

    mocker.patch.dict(os.environ, {
        "GEMINI_API_KEY": "g-key",
        "LINE_CHANNEL_ACCESS_TOKEN": "l-token",
    })

    from main import run
    run(state_path="state.json", feeds=[{
        "key": "netflix", "name": "Netflix Tech Blog",
        "emoji": "🎬", "rss": "https://netflixtechblog.com/feed"
    }])

    assert mock_broadcast.called

def test_seen_articles_are_skipped(mocker):
    mocker.patch("main.load_state", return_value={"netflix": ["id1"]})
    mocker.patch("main.save_state")
    mocker.patch("main.fetch_articles", return_value=[
        {"id": "id1", "title": "Old Article", "body": "Body", "url": "https://x.com"}
    ])
    mock_broadcast = mocker.patch("main.broadcast_article")
    mock_summarize = mocker.patch("main.summarize_article")

    mocker.patch.dict(os.environ, {
        "GEMINI_API_KEY": "g-key",
        "LINE_CHANNEL_ACCESS_TOKEN": "l-token",
    })

    from main import run
    run(state_path="state.json", feeds=[{
        "key": "netflix", "name": "Netflix Tech Blog",
        "emoji": "🎬", "rss": "https://netflixtechblog.com/feed"
    }])

    assert not mock_broadcast.called
    assert not mock_summarize.called
