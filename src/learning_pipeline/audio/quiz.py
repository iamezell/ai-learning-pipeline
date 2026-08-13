from io import BytesIO
from pathlib import Path

from pydub import AudioSegment

from learning_pipeline.audio.elevenlabs import text_to_speech
from learning_pipeline.models import AudioQuizItem


def create_audio_quiz(
    items: list[AudioQuizItem],
    output_path: Path,
    voice_id: str,
) -> None:
    quiz = AudioSegment.empty()

    intro = text_to_speech(
        text=(
            "Audio review. Answer the questions out loud. "
            "After the pause, you will hear the answer."
        ),
        voice_id=voice_id,
    )
    quiz += AudioSegment.from_file(BytesIO(intro), format="mp3")
    quiz += AudioSegment.silent(duration=2000)

    for index, item in enumerate(items, start=1):
        question = text_to_speech(
            text=f"Question {index}: {item.question}",
            voice_id=voice_id,
        )
        answer = text_to_speech(
            text=f"Answer: {item.answer}",
            voice_id=voice_id,
        )

        quiz += AudioSegment.from_file(BytesIO(question), format="mp3")
        quiz += AudioSegment.silent(duration=item.pause_seconds * 1000)
        quiz += AudioSegment.from_file(BytesIO(answer), format="mp3")
        quiz += AudioSegment.silent(duration=3000)

    quiz.export(output_path, format="mp3", bitrate="128k")
