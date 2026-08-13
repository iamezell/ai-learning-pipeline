from pathlib import Path

import typer

from learning_pipeline.audio.elevenlabs import create_audio_lesson
from learning_pipeline.audio.quiz import create_audio_quiz
from learning_pipeline.exporters.remnote import export_remnote
from learning_pipeline.learning.claude import create_learning_package
from learning_pipeline.sources.web import WebSource


app = typer.Typer()


@app.command()
def learn(url: str) -> None:
    typer.echo(f"Learning from {url}")

    web_source = WebSource()
    source = web_source.load(url)

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    slug = url.rstrip("/").split("/")[-1] or "page"
    output_file = output_dir / f"{slug}.md"
    output_file.write_text(source.content, encoding="utf-8")

    typer.echo(f"Saved to {output_file}")

    learning_package = create_learning_package(source)

    typer.echo(f"Created learning package: {learning_package}")

    learning_file = output_dir / f"{slug}-learning.json"
    learning_file.write_text(
        learning_package.model_dump_json(indent=2),
        encoding="utf-8",
    )

    typer.echo(f"Saved to {learning_file}")

    audio_file = output_dir / f"{slug}-lesson.mp3"
    typer.echo(f"Creating audio lesson from {learning_file} to {audio_file}")
    create_audio_lesson(
        text=learning_package.audio_lessons,
        output_path=audio_file,
        voice_id="21m00Tcm4TlvDq8ikWAM",
    )
    typer.echo(f"Saved to {audio_file}")

    quiz_file = output_dir / f"{slug}-quiz.mp3"

    typer.echo(f"Creating audio quiz from {learning_file} to {quiz_file}")

    create_audio_quiz(
        items=learning_package.audio_quizzes or [],
        output_path=quiz_file,
        voice_id="21m00Tcm4TlvDq8ikWAM",
    )

    typer.echo(f"Saved to {quiz_file}")

    remnote_file = output_dir / f"{slug}-remnote.md"

    typer.echo(f"Exporting to {remnote_file}")

    export_remnote(
        learning_package=learning_package,
        output_path=remnote_file,
    )

    typer.echo(f"Saved to {remnote_file}")


if __name__ == "__main__":
    app()
