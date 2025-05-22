from pathlib import Path

PARTIAL_DIR = Path("prompt-partials")


def load_prompt(path: str) -> str:
    text = Path(path).read_text()
    for partial in PARTIAL_DIR.glob("*.partial.md"):
        tag = f"<<{partial.stem.upper()}>>"
        if tag in text:
            text = text.replace(tag, partial.read_text())
    return text
