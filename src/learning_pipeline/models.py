from pydantic import BaseModel


class SourceDocument(BaseModel):
    title: str
    content: str
    source_url: str | None = None



class Concept(BaseModel):
    term: str
    explanation: str


class Flashcard(BaseModel):
    question: str
    answer: str



class MultipleChoiceQuestion(BaseModel):
    question: str
    choices: list[str]
    correct_answer: str
    explanation: str


class TeachBackPrm(BaseModel):
    concept: Concept
    source_document: SourceDocument
    flashcards: list[Flashcard]
    multiple_choice_questions: list[MultipleChoiceQuestion]


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

    recall_cards: list[Flashcard]
    concept_cards: list[Flashcard]
    scenario_cards: list[Flashcard]

    multiple_choice: list[MultipleChoiceQuestion]
    teach_back: list[TeachBackPrompt]

    audio_lessons: str | None = None
    audio_quizzes: list[AudioQuizItem] | None = None
    