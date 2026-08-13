from pathlib import Path

from elevenlabs.client import ElevenLabs

from learning_pipeline.config import get_elevenlabs_api_key


def text_to_speech(
    text: str,
    voice_id: str = "21m00Tcm4TlvDq8ikWAM",
) -> bytes:
    client = ElevenLabs(api_key=get_elevenlabs_api_key())
    audio = client.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    return b"".join(chunk for chunk in audio)


def create_audio_lesson(
    text: str,
    output_path: Path,
    voice_id: str = "21m00Tcm4TlvDq8ikWAM",
) -> None:
    output_path.write_bytes(text_to_speech(text=text, voice_id=voice_id))
