"""Helpers for resolving git merge conflicts."""

from __future__ import annotations

import re


def auto_merge_conflict_blocks(content: str) -> str:
    """Auto-resolve simple conflict blocks by taking the incoming changes."""

    pattern = re.compile(
        r"<<<<<<<[^\n]*\n(?P<head>.*?)\n=======\n(?P<incoming>.*?)\n>>>>>>>[^\n]*\n",
        re.DOTALL,
    )

    def _choose(match: re.Match[str]) -> str:
        return match.group("incoming")

    return re.sub(pattern, _choose, content)
