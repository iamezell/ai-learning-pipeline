# AI Learning Pipeline

Python package for an AI learning pipeline.

## Layout

```
ai-learning-pipeline/
├── src/
│   └── learning_pipeline/
│       └── __init__.py
├── tests/
├── .env
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
cp .env.example .env
```

## Tests

```bash
pytest
```
