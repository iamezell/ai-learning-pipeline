import httpx
from bs4 import BeautifulSoup
from markdownify import markdownify as md

from learning_pipeline.models import SourceDocument


class WebSource:
    def load(self, url: str) -> SourceDocument:
        response = httpx.get(
            url,
            follow_redirects=True,
            timeout=30.0,
            headers={"User-Agent": "ai-learning-pipeline/0.1"},
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        article = soup.find("main")

        if not article:
            raise ValueError("Could not find the main article content")

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
        )
