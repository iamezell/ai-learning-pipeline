from anthropic import Anthropic

from learning_pipeline.models import LearningPackage, SourceDocument


SYSTEM_PROMPT = """
You are an expert instructional designer.

Your job is to transform authoritative source material into a high-quality
learning package designed for active recall and deep understanding.

Use only information supported by the provided source material.

Ignore webpage navigation, advertisements, calls to action, related links,
footers, and other content that is not part of the educational material.

Create learning material that tests multiple levels of understanding:

1. Recall — important facts and terminology.
2. Conceptual understanding — why and how things work.
3. Application — scenarios requiring the learner to apply the material.
4. Teach-back — prompts requiring the learner to explain concepts aloud.

The audio lesson should be written specifically for listening rather than
simply reading the source verbatim. Explain concepts conversationally while
remaining faithful to the source.

Audio quiz questions should work without looking at a screen. Give the
learner enough pause time to answer aloud before hearing the answer.
"""


def create_learning_package(
    source: SourceDocument,
) -> LearningPackage:
    client = Anthropic()

    response = client.messages.parse(
        model="claude-sonnet-4-5",
        max_tokens=10000,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"""
Title: {source.title}
Source URL: {source.source_url}

SOURCE MATERIAL:

{source.content}
""",
            }
        ],
        output_format=LearningPackage,
    )

    return response.parsed_output