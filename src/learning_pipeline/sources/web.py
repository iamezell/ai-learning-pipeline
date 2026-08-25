import httpx
from bs4 import BeautifulSoup
from markdownify import markdownify as md

from learning_pipeline.models import SourceDocument

_CONTENT_SELECTORS = (
    "main",
    "article",
    "[role=main]",
    "#content",
    ".content",
    "#main-content",
)

_STRIP_TAGS = ("script", "style", "nav", "footer", "aside", "form", "noscript")


class WebSource:
    def load(self, url: str, *, capture_intent: str | None = None) -> SourceDocument:
        response = httpx.get(
            url,
            follow_redirects=True,
            timeout=30.0,
            headers={"User-Agent": "ai-learning-pipeline/0.1"},
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        article = None
        for selector in _CONTENT_SELECTORS:
            article = soup.select_one(selector)
            if article is not None:
                break

        if article is None:
            article = soup.body

        if article is None:
            raise ValueError("Could not find the main article content")

        for tag in article.find_all(_STRIP_TAGS):
            tag.decompose()

        markdown = md(
            str(article),
            heading_style="ATX",
        )

        title = (
            soup.title.string.strip()
            if soup.title and soup.title.string
            else "Untitled"
        )

        return SourceDocument(
            title=title,
            content=markdown,
            source_url=url,
            capture_intent=capture_intent,
        )
