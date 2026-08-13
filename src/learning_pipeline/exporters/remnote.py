from pathlib import Path

from learning_pipeline.models import LearningPackage


def export_remnote(
    learning_package: LearningPackage,
    output_path: Path,
) -> None:
    lines: list[str] = []

    lines.append(f"# {learning_package.title}")
    lines.append("")

    lines.append("## Learning Objectives")
    lines.append("")

    for objective in learning_package.learning_objectives:
        lines.append(f"- {objective}")

    lines.append("")

    lines.append("## Recall Cards")
    lines.append("")

    for card in learning_package.recall_cards:
        lines.append(f"- {card.question} >> {card.answer}")

    lines.append("")

    lines.append("## Concept Cards")
    lines.append("")

    for card in learning_package.concept_cards:
        lines.append(f"- {card.question} >> {card.answer}")

    lines.append("")

    lines.append("## Scenario Cards")
    lines.append("")

    for card in learning_package.scenario_cards:
        lines.append(f"- {card.question} >> {card.answer}")

    lines.append("")

    lines.append("## Multiple Choice")
    lines.append("")

    for question in learning_package.multiple_choice:
        lines.append(f"- {question.question} >>A)")

        correct_choice = question.correct_answer

        lines.append(f"  - {correct_choice}")

        for choice in question.choices:
            if choice != correct_choice:
                lines.append(f"  - {choice}")

        lines.append(f"    - Explanation: {question.explanation}")

    lines.append("")

    lines.append("## Teach Back")
    lines.append("")

    for prompt in learning_package.teach_back:
        lines.append(f"- {prompt.prompt}")

        for key_point in prompt.keypoints:
            lines.append(f"  - {key_point}")

    content = "\n".join(lines)

    output_path.write_text(
        content,
        encoding="utf-8",
    )
