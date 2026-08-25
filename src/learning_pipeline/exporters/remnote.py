import hashlib
import random
from pathlib import Path

from learning_pipeline.models import LearningPackage

# RemNote's cloze syntax varies by version and this may need adjusting.
CLOZE_TEMPLATE = "{{{{c1::{}}}}}"


def export_remnote(
    learning_package: LearningPackage,
    output_path: Path,
    capture_intent: str | None = None,
) -> None:
    lines: list[str] = []

    lines.append(f"# {learning_package.title}")
    lines.append("")

    if capture_intent:
        lines.append(f"> **Why I captured this:** {capture_intent}")
        lines.append("")

    lines.append("## Before You Start — Try These First")
    lines.append("")

    for question in learning_package.pre_questions:
        lines.append(f"- {question}")

    lines.append("")

    lines.append("## Learning Objectives")
    lines.append("")

    for objective in learning_package.learning_objectives:
        lines.append(f"- {objective}")

    lines.append("")

    lines.append("## Discrimination")
    lines.append("")

    for card in sorted(
        learning_package.discrimination_cards,
        key=lambda item: item.importance,
        reverse=True,
    ):
        lines.append(
            f"- {card.question} >> {card.answer} "
            f"*(key difference: {card.discriminating_feature})*"
        )

    lines.append("")

    lines.append("## Scenario Cards")
    lines.append("")

    for card in sorted(
        learning_package.scenario_cards,
        key=lambda item: item.importance,
        reverse=True,
    ):
        lines.append(f"- {card.question} >> {card.answer}")

    lines.append("")

    lines.append("## Concept Cards")
    lines.append("")

    for card in sorted(
        learning_package.concept_cards,
        key=lambda item: item.importance,
        reverse=True,
    ):
        lines.append(f"- {card.question} >> {card.answer}")

    lines.append("")

    lines.append("## Cloze")
    lines.append("")

    for card in sorted(
        learning_package.cloze_cards,
        key=lambda item: item.importance,
        reverse=True,
    ):
        rendered = card.text.replace(
            card.hidden,
            CLOZE_TEMPLATE.format(card.hidden),
            1,
        )
        lines.append(f"- {rendered}")

    lines.append("")

    lines.append("## Recall Cards")
    lines.append("")

    for card in sorted(
        learning_package.recall_cards,
        key=lambda item: item.importance,
        reverse=True,
    ):
        lines.append(f"- {card.question} >> {card.answer}")

    lines.append("")

    lines.append("## Multiple Choice")
    lines.append("")

    for question in sorted(
        learning_package.multiple_choice,
        key=lambda item: item.importance,
        reverse=True,
    ):
        choices = list(question.choices)
        if question.correct_answer not in choices:
            choices.append(question.correct_answer)

        seed = int(
            hashlib.sha256(question.question.encode("utf-8")).hexdigest(),
            16,
        )
        rng = random.Random(seed)
        rng.shuffle(choices)

        lines.append(f"- {question.question}")
        for index, choice in enumerate(choices):
            letter = chr(ord("A") + index)
            lines.append(f"    - {letter}. {choice}")

        correct_index = choices.index(question.correct_answer)
        correct_letter = chr(ord("A") + correct_index)
        lines.append(f"    - >> {correct_letter}. {question.correct_answer}")
        lines.append(f"        - {question.explanation}")

    lines.append("")

    lines.append("## Teach Back")
    lines.append("")

    for prompt in learning_package.teach_back:
        lines.append(f"- {prompt.prompt}")

        for key_point in prompt.keypoints:
            lines.append(f"  - {key_point}")

    lines.append("")

    lines.append("## Apply This Today")
    lines.append("")

    for task in learning_package.apply_tasks:
        lines.append(f"- [ ] {task}")

    content = "\n".join(lines)

    output_path.write_text(
        content,
        encoding="utf-8",
    )
