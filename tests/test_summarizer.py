import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from unittest.mock import MagicMock
from summarizer import summarize_article

def test_summarize_returns_dict(mocker):
    mock_model = MagicMock()
    mock_model.generate_content.return_value.text = "中文標題\n這是摘要內容。"
    mocker.patch("google.generativeai.GenerativeModel", return_value=mock_model)
    mocker.patch("google.generativeai.configure")

    result = summarize_article(
        title="Hello World",
        body="This is the article body.",
        api_key="test-key"
    )
    assert "zh_title" in result
    assert "zh_summary" in result

def test_summarize_parses_response(mocker):
    mock_model = MagicMock()
    mock_model.generate_content.return_value.text = "你好世界\n這篇文章介紹了重要技術。"
    mocker.patch("google.generativeai.GenerativeModel", return_value=mock_model)
    mocker.patch("google.generativeai.configure")

    result = summarize_article("Hello World", "Body text.", "test-key")
    assert result["zh_title"] == "你好世界"
    assert "這篇文章" in result["zh_summary"]

def test_summarize_returns_fallback_on_error(mocker):
    mocker.patch("google.generativeai.GenerativeModel", side_effect=Exception("API error"))
    mocker.patch("google.generativeai.configure")

    result = summarize_article("Hello World", "Body.", "test-key")
    assert result["zh_title"] == "Hello World"
    assert result["zh_summary"] == ""
