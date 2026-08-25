from anthropic import Anthropic

from learning_pipeline.config import get_anthropic_api_key
from learning_pipeline.models import LearningPackage, SourceDocument


SYSTEM_PROMPT = """You build learning material for one specific learner from
one source document.

You are not summarising. You are constructing retrieval practice: material that
forces the learner to produce answers from memory rather than recognise them on
a page.

Two rules govern everything you generate.

RULE 1 — CARDS ARE SCARCE.
You have a hard budget and it is deliberately tight. Fewer, better cards beat
comprehensive coverage every time: a learner with 800 cards reviews none of
them. Every card must earn its place against the learner's stated intent. When
in doubt, cut.

RULE 2 — FAVOUR DISTINCTION OVER DEFINITION.
Most difficulty in a technical domain comes from adjacent concepts blurring
together, not from missing definitions. A card that forces the learner to
separate two confusable things is worth five that define them individually.
Prioritise discrimination cards.

Recall cards are capped hardest on purpose — acronym expansion is not
knowledge. Only include one if the learner will need to produce that fact aloud
in conversation.

Use only information supported by the source. If the source is thin on
something the learner clearly needs, say so in a learning objective rather than
filling the gap from your own knowledge.

Ignore navigation, advertisements, calls to action, related links, footers, and
other page furniture.

The audio lesson is a different writing task from everything else. Write it for
LISTENING: spoken register, contractions, short sentences. Open with something
concrete — a specific situation, not a definition. No bullet points, no
headings, no "firstly/secondly" scaffolding. Signpost transitions in speech
("here's where it gets interesting"). 400–700 words: dense and re-listenable
beats long and thorough, because this gets replayed rather than studied once.

Audio quiz questions must work without a screen. Set `pause_seconds`
individually per question based on how long that answer actually takes to say
aloud — a one-word answer needs about 5 seconds, a three-part explanation needs
about 20. Never use the same value throughout. Order questions so related ones
are not adjacent; interleaving beats blocking.
"""


def create_learning_package(
    source: SourceDocument,
) -> LearningPackage:
    client = Anthropic(api_key=get_anthropic_api_key())

    intent_block = (
        f"""LEARNER INTENT — THIS DRIVES EVERY DECISION BELOW

The learner captured this source for a specific reason:

    "{source.capture_intent}"

Weight everything against that: which concepts matter, which distinctions are
worth drilling, what the scenarios are built around, what the apply-tasks are,
what the audio lesson emphasises.

Material that is interesting but irrelevant to this intent should be CUT, not
included at low importance. If the source does not actually serve the stated
intent well, say so plainly in the first learning objective rather than
generating around the gap.
"""
        if source.capture_intent
        else (
            "LEARNER INTENT\n\nNone given. Generate for general understanding, "
            "weighting towards the concepts most load-bearing in the source.\n"
        )
    )

    response = client.messages.parse(
        model="claude-sonnet-4-5",
        max_tokens=12000,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"""{intent_block}
Title: {source.title}
Source URL: {source.source_url}

SOURCE MATERIAL:

{source.content}
""",
            }
        ],
        output_format=LearningPackage,
    )

    return response.parsed_output.trim_to_budget()
