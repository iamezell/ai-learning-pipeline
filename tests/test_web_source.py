from unittest.mock import MagicMock, patch

import pytest

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
        with pytest.raises(ValueError, match="main article content"):
            WebSource().load("https://example.com/page/")
