from pathlib import Path

import httpx
import typer
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from learning_pipeline.learning.claude import create_learning_package
from learning_pipeline.models import SourceDocument

app = typer.Typer()

@app.command()
def learn(url: str) -> None:
    typer.echo(f"Learning from {url}")
    

    response = httpx.get(url, follow_redirects=True, timeout=30.0, headers={"User-Agent": "ai-learning-pipeline/0.1"})

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    article = soup.find("main")

    if not article:
        raise typer.BadParameter("Could not find the main article content")

    markdown = md(
        str(article),
        heading_style="ATX",
    )

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    slug = url.rstrip("/").split("/")[-1] or "page"
    output_file = output_dir / f"{slug}.md"
    output_file.write_text(markdown, encoding="utf-8")

    typer.echo(f"Saved to {output_file}")

    source = SourceDocument(
        title=soup.title.string.strip() if soup.title.string else "Untitled",
        content=markdown,
        source_url=url,
    )

    learning_package = create_learning_package(source)

    typer.echo(f"Created learning package: {learning_package}")

    learning_file = output_dir / f"{slug}-learning.json"
    learning_file.write_text(learning_package.model_dump_json(indent=2), encoding="utf-8")

    typer.echo(f"Saved to {learning_file}")


if __name__ == "__main__":
    app()
