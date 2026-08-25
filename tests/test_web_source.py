from unittest.mock import MagicMock, patch

from learning_pipeline.models import SourceDocument
from learning_pipeline.sources.web import WebSource


HTML_WITH_MAIN = """
<html>
  <head><title>What is OCR?</title></head>
  <body>
    <main>
      <h1>OCR</h1>
      <p>Optical character recognition.</p>
    </main>
  </body>
</html>
"""

HTML_WITHOUT_MAIN = """
<html>
  <head><title>Missing Main</title></head>
  <body><p>No article here.</p></body>
</html>
"""

HTML_WITH_SCRIPT = """
<html>
  <head><title>Script Page</title></head>
  <body>
    <main>
      <p>Visible lesson text.</p>
      <script>window.TRACK='secret-payload';</script>
    </main>
  </body>
</html>
"""


def test_web_source_load_returns_source_document():
    mock_response = MagicMock()
    mock_response.text = HTML_WITH_MAIN
    mock_response.raise_for_status = MagicMock()

    with patch(
        "learning_pipeline.sources.web.httpx.get",
        return_value=mock_response,
    ) as mock_get:
        source = WebSource().load("https://example.com/what-is/ocr/")

    mock_get.assert_called_once_with(
        "https://example.com/what-is/ocr/",
        follow_redirects=True,
        timeout=30.0,
        headers={"User-Agent": "ai-learning-pipeline/0.1"},
    )
    mock_response.raise_for_status.assert_called_once_with()

    assert isinstance(source, SourceDocument)
    assert source.title == "What is OCR?"
    assert source.source_url == "https://example.com/what-is/ocr/"
    assert "Optical character recognition" in source.content


def test_web_source_load_requires_main_content():
    mock_response = MagicMock()
    mock_response.text = HTML_WITHOUT_MAIN
    mock_response.raise_for_status = MagicMock()

    with patch(
        "learning_pipeline.sources.web.httpx.get",
        return_value=mock_response,
    ):
        source = WebSource().load("https://example.com/page/")

    assert isinstance(source, SourceDocument)
    assert source.title == "Missing Main"
    assert "No article here." in source.content


def test_web_source_strips_script_from_content():
    mock_response = MagicMock()
    mock_response.text = HTML_WITH_SCRIPT
    mock_response.raise_for_status = MagicMock()

    with patch(
        "learning_pipeline.sources.web.httpx.get",
        return_value=mock_response,
    ):
        source = WebSource().load("https://example.com/script/")

    assert "Visible lesson text." in source.content
    assert "secret-payload" not in source.content
    assert "<script" not in source.content.lower()
