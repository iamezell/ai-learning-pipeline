from learning_pipeline.models import Flashcard


def test_flash_card():
    card = Flashcard(
        question="What is OCR?",
        answer="Optical Character Recognition",
    )

    assert card.question == "What is OCR?"
    assert card.answer == "Optical Character Recognition"