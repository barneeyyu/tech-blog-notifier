import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from unittest.mock import MagicMock
from notifier import format_message, broadcast_article

def test_format_message_contains_fields():
    msg = format_message(
        name="Netflix Tech Blog",
        emoji="🎬",
        zh_title="你好世界",
        original_title="Hello World",
        zh_summary="這是摘要。",
        url="https://example.com/article"
    )
    assert "Netflix Tech Blog" in msg
    assert "你好世界" in msg
    assert "Hello World" in msg
    assert "這是摘要。" in msg
    assert "https://example.com/article" in msg

def test_broadcast_article_calls_api(mocker):
    mock_api = MagicMock()
    mocker.patch("notifier.MessagingApi", return_value=mock_api)
    mocker.patch("notifier.ApiClient")

    broadcast_article(
        token="test-token",
        name="Netflix Tech Blog",
        emoji="🎬",
        zh_title="你好世界",
        original_title="Hello World",
        zh_summary="摘要",
        url="https://example.com"
    )
    assert mock_api.broadcast.called
