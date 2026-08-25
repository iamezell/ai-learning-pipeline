from pydantic import BaseModel, Field, model_validator


CARD_BUDGET = {
    "recall": 3,
    "concept": 5,
    "discrimination": 5,
    "cloze": 5,
    "scenario": 4,
    "multiple_choice": 4,
}
MAX_TOTAL_CARDS = 20

_CARD_LIST_ATTRS = {
    "recall": "recall_cards",
    "concept": "concept_cards",
    "discrimination": "discrimination_cards",
    "cloze": "cloze_cards",
    "scenario": "scenario_cards",
    "multiple_choice": "multiple_choice",
}


class SourceDocument(BaseModel):
    title: str
    content: str
    source_url: str | None = None
    capture_intent: str | None = None



class Concept(BaseModel):
    term: str
    explanation: str


class Flashcard(BaseModel):
    question: str
    answer: str
    importance: int = Field(
        ge=1,
        le=5,
        description=(
            "How essential this card is to the learner's stated intent. "
            "5 = essential. 1 = peripheral. Be discriminating: if everything "
            "is a 5 the ranking is useless."
        ),
    )



class MultipleChoiceQuestion(BaseModel):
    question: str
    choices: list[str]
    correct_answer: str
    explanation: str
    importance: int = Field(
        ge=1,
        le=5,
        description=(
            "How essential this card is to the learner's stated intent. "
            "5 = essential. 1 = peripheral. Be discriminating: if everything "
            "is a 5 the ranking is useless."
        ),
    )

    @model_validator(mode="after")
    def _correct_answer_in_choices(self):
        if self.correct_answer not in self.choices:
            raise ValueError(
                f"correct_answer not among choices: {self.question!r}"
            )
        return self


class DiscriminationCard(BaseModel):
    question: str = Field(
        description=(
            "A question that cannot be answered without holding both "
            "concepts in mind at once. It must force a distinction, not a "
            "definition. Good: 'You need to pull handwritten values off a "
            "scanned form — why is OCR alone insufficient and what does ICR "
            "add?' Bad: 'What is ICR?'"
        )
    )
    answer: str
    concept_a: str
    concept_b: str
    discriminating_feature: str = Field(
        description="The single feature that separates the two concepts."
    )
    importance: int = Field(ge=1, le=5)


class ClozeCard(BaseModel):
    text: str = Field(
        description="A complete, load-bearing sentence from the material."
    )
    hidden: str = Field(
        description=(
            "The exact span within `text` to hide. Must appear verbatim in "
            "`text`. Hide the span that carries the meaning, never an "
            "incidental noun."
        )
    )
    importance: int = Field(ge=1, le=5)

    @model_validator(mode="after")
    def _hidden_in_text(self):
        if self.hidden not in self.text:
            raise ValueError(
                f"hidden {self.hidden!r} does not appear in text {self.text!r}"
            )
        return self


class TeachBackPrompt(BaseModel):
    prompt: str
    keypoints: list[str]


class AudioQuizItem(BaseModel):
    question: str
    answer: str
    pause_seconds: int


class LearningPackage(BaseModel):
    title: str
    learning_objectives: list[str]

    concepts: list[Concept]

    pre_questions: list[str] = Field(
        max_length=6,
        description=(
            "Questions the learner probably CANNOT answer yet, to attempt "
            "BEFORE studying. Attempting and failing improves retention of what "
            "follows. Hard but answerable from the source."
        ),
    )

    recall_cards: list[Flashcard] = Field(max_length=6)
    concept_cards: list[Flashcard] = Field(max_length=10)
    discrimination_cards: list[DiscriminationCard] = Field(max_length=10)
    cloze_cards: list[ClozeCard] = Field(max_length=10)
    scenario_cards: list[Flashcard] = Field(max_length=8)
    multiple_choice: list[MultipleChoiceQuestion] = Field(max_length=8)

    teach_back: list[TeachBackPrompt]

    apply_tasks: list[str] = Field(
        max_length=4,
        description=(
            "One or two concrete things the learner could do TODAY with this "
            "material, roughly 20 minutes each, tied directly to their stated "
            "intent."
        ),
    )

    audio_lesson: str
    audio_quiz: list[AudioQuizItem]

    @property
    def total_cards(self) -> int:
        return sum(
            len(getattr(self, attr)) for attr in _CARD_LIST_ATTRS.values()
        )

    def trim_to_budget(self) -> "LearningPackage":
        """Enforce CARD_BUDGET and MAX_TOTAL_CARDS after generation.

        Field max_length values are only a sanity guard against pathological
        overshoot so parsing can succeed; this method is the actual budget.
        """
        for key, attr in _CARD_LIST_ATTRS.items():
            cards = sorted(
                getattr(self, attr),
                key=lambda card: card.importance,
                reverse=True,
            )
            setattr(self, attr, cards[: CARD_BUDGET[key]])

        while self.total_cards > MAX_TOTAL_CARDS:
            candidates: list[tuple[int, str, int]] = []
            for attr in _CARD_LIST_ATTRS.values():
                cards = getattr(self, attr)
                if len(cards) <= 1:
                    continue
                for index, card in enumerate(cards):
                    candidates.append((card.importance, attr, index))

            if not candidates:
                break

            _importance, attr, index = min(
                candidates,
                key=lambda item: (item[0], item[1], item[2]),
            )
            del getattr(self, attr)[index]

        return self
