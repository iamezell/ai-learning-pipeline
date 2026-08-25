from pathlib import Path
from typing import Optional

import typer

from learning_pipeline.audio.elevenlabs import create_audio_lesson
from learning_pipeline.audio.quiz import create_audio_quiz
from learning_pipeline.exporters.remnote import export_remnote
from learning_pipeline.learning.claude import create_learning_package
from learning_pipeline.models import LearningPackage
from learning_pipeline.sources.web import WebSource


app = typer.Typer()


@app.command()
def learn(
    url: Optional[str] = typer.Argument(None),
    no_audio: bool = typer.Option(
        False,
        "--no-audio",
        help="Skip ElevenLabs generation.",
    ),
    from_json: Optional[Path] = typer.Option(
        None,
        "--from-json",
        help="Load a saved learning package instead of calling Claude.",
    ),
    intent: Optional[str] = typer.Option(
        None,
        "--intent",
        "-i",
        help="Why you're capturing this. One line. Drives the whole package.",
    ),
    no_intent: bool = typer.Option(
        False,
        "--no-intent",
        help="Skip the intent prompt and generate a general-purpose package.",
    ),
) -> None:
    if from_json is None and not url:
        raise typer.BadParameter("Provide a URL or --from-json PATH")

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    capture_intent: str | None = None

    if from_json is not None:
        learning_package = LearningPackage.model_validate_json(
            from_json.read_text(encoding="utf-8"),
        )
        slug = from_json.stem.removesuffix("-learning") or from_json.stem
        typer.echo(f"Loaded learning package from {from_json}")
    else:
        if intent is None and not no_intent:
            typer.echo("Why are you capturing this? (one line, Enter to skip)")
            intent = typer.prompt("  intent", default="", show_default=False) or None

        capture_intent = intent

        typer.echo(f"Learning from {url}")

        web_source = WebSource()
        source = web_source.load(url, capture_intent=intent)

        slug = url.rstrip("/").split("/")[-1] or "page"
        output_file = output_dir / f"{slug}.md"
        output_file.write_text(source.content, encoding="utf-8")

        typer.echo(f"Saved to {output_file}")

        learning_package = create_learning_package(source)

        typer.echo(
            f"Created package: {learning_package.total_cards} cards, "
            f"{len(learning_package.pre_questions)} pre-questions, "
            f"{len(learning_package.audio_quiz)} quiz items"
        )

    learning_file = output_dir / f"{slug}-learning.json"
    learning_file.write_text(
        learning_package.model_dump_json(indent=2),
        encoding="utf-8",
    )

    typer.echo(f"Saved to {learning_file}")

    if no_audio:
        typer.echo("Audio generation skipped (--no-audio)")
    else:
        audio_file = output_dir / f"{slug}-lesson.mp3"
        typer.echo(f"Creating audio lesson from {learning_file} to {audio_file}")
        create_audio_lesson(
            text=learning_package.audio_lesson,
            output_path=audio_file,
            voice_id="21m00Tcm4TlvDq8ikWAM",
        )
        typer.echo(f"Saved to {audio_file}")

        quiz_file = output_dir / f"{slug}-quiz.mp3"

        typer.echo(f"Creating audio quiz from {learning_file} to {quiz_file}")

        create_audio_quiz(
            items=learning_package.audio_quiz,
            output_path=quiz_file,
            voice_id="21m00Tcm4TlvDq8ikWAM",
        )

        typer.echo(f"Saved to {quiz_file}")

    remnote_file = output_dir / f"{slug}-remnote.md"

    typer.echo(f"Exporting to {remnote_file}")

    export_remnote(
        learning_package=learning_package,
        output_path=remnote_file,
        capture_intent=capture_intent,
    )

    typer.echo(f"Saved to {remnote_file}")


if __name__ == "__main__":
    app()
