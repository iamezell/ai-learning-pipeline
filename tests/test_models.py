import pytest
from pydantic import ValidationError

from learning_pipeline.models import (
    MAX_TOTAL_CARDS,
    AudioQuizItem,
    ClozeCard,
    Concept,
    DiscriminationCard,
    Flashcard,
    LearningPackage,
    MultipleChoiceQuestion,
    TeachBackPrompt,
)


def test_flash_card():
    card = Flashcard(
        question="What is OCR?",
        answer="Optical Character Recognition",
        importance=3,
    )

    assert card.question == "What is OCR?"
    assert card.answer == "Optical Character Recognition"
    assert card.importance == 3


def _flash(question: str, importance: int) -> Flashcard:
    return Flashcard(
        question=question,
        answer=f"answer for {question}",
        importance=importance,
    )


def _mcq(question: str, importance: int) -> MultipleChoiceQuestion:
    return MultipleChoiceQuestion(
        question=question,
        choices=["A", "B", "C", "D"],
        correct_answer="A",
        explanation="because",
        importance=importance,
    )


def _discrimination(question: str, importance: int) -> DiscriminationCard:
    return DiscriminationCard(
        question=question,
        answer="answer",
        concept_a="a",
        concept_b="b",
        discriminating_feature="feature",
        importance=importance,
    )


def _cloze(importance: int, label: str) -> ClozeCard:
    text = f"OCR uses {label} during preprocessing."
    return ClozeCard(text=text, hidden=label, importance=importance)


def _package(**overrides) -> LearningPackage:
    data = {
        "title": "OCR",
        "learning_objectives": ["Understand OCR"],
        "concepts": [Concept(term="OCR", explanation="Optical Character Recognition")],
        "pre_questions": ["What is OCR?"],
        "recall_cards": [],
        "concept_cards": [],
        "discrimination_cards": [],
        "cloze_cards": [],
        "scenario_cards": [],
        "multiple_choice": [],
        "teach_back": [
            TeachBackPrompt(prompt="Explain OCR", keypoints=["definition"])
        ],
        "apply_tasks": ["Skim an OCR pipeline diagram"],
        "audio_lesson": "Lesson text.",
        "audio_quiz": [
            AudioQuizItem(question="Q?", answer="A", pause_seconds=5)
        ],
    }
    data.update(overrides)
    return LearningPackage(**data)


def test_trim_to_budget_respects_caps_and_max_total():
    package = _package(
        recall_cards=[_flash(f"r{i}", 5 - (i % 5)) for i in range(6)],
        concept_cards=[_flash(f"c{i}", 5 - (i % 5)) for i in range(8)],
        discrimination_cards=[
            _discrimination(f"d{i}", 5 - (i % 5)) for i in range(8)
        ],
        cloze_cards=[_cloze(5 - (i % 5), f"term{i}") for i in range(8)],
        scenario_cards=[_flash(f"s{i}", 5 - (i % 5)) for i in range(7)],
        multiple_choice=[_mcq(f"m{i}", 5 - (i % 5)) for i in range(7)],
    )

    trimmed = package.trim_to_budget()

    assert len(trimmed.recall_cards) <= 3
    assert len(trimmed.concept_cards) <= 5
    assert len(trimmed.discrimination_cards) <= 5
    assert len(trimmed.cloze_cards) <= 5
    assert len(trimmed.scenario_cards) <= 4
    assert len(trimmed.multiple_choice) <= 4
    assert trimmed.total_cards <= MAX_TOTAL_CARDS


def test_overshoot_concept_cards_parse_then_trim():
    package = _package(
        concept_cards=[_flash(f"c{i}", max(1, 5 - i)) for i in range(6)],
    )

    assert len(package.concept_cards) == 6
    trimmed = package.trim_to_budget()
    assert len(trimmed.concept_cards) == 5
    assert [card.question for card in trimmed.concept_cards] == [
        "c0",
        "c1",
        "c2",
        "c3",
        "c4",
    ]

def test_trim_to_budget_keeps_highest_importance():
    package = _package(
        recall_cards=[
            _flash("keep-high", 5),
            _flash("drop-low", 1),
            _flash("keep-mid", 4),
            _flash("drop-lower", 2),
        ],
        # Stay under MAX_TOTAL_CARDS after per-type caps so only the
        # per-type sort/truncate decides which recall cards survive.
        concept_cards=[_flash(f"c{i}", 5) for i in range(5)],
        discrimination_cards=[_discrimination(f"d{i}", 5) for i in range(3)],
        cloze_cards=[_cloze(5, f"term{i}") for i in range(3)],
        scenario_cards=[_flash(f"s{i}", 5) for i in range(2)],
        multiple_choice=[_mcq(f"m{i}", 5) for i in range(2)],
    )

    trimmed = package.trim_to_budget()
    recall_questions = {card.question for card in trimmed.recall_cards}

    assert "keep-high" in recall_questions
    assert "keep-mid" in recall_questions
    assert "drop-low" not in recall_questions
    assert trimmed.total_cards <= MAX_TOTAL_CARDS


def test_multiple_choice_requires_correct_answer_in_choices():
    with pytest.raises(ValidationError, match="correct_answer not among choices"):
        MultipleChoiceQuestion(
            question="What is OCR?",
            choices=["A", "B", "C"],
            correct_answer="D",
            explanation="missing",
            importance=3,
        )


def test_cloze_requires_hidden_in_text():
    with pytest.raises(ValidationError, match="does not appear in text"):
        ClozeCard(
            text="OCR converts images into text.",
            hidden="deskewing",
            importance=3,
        )
