"""Utilities for automated merge conflict resolution."""

from __future__ import annotations

from typing import List


def auto_merge_conflict_blocks(content: str) -> str:
    """Resolve simple git conflict markers using heuristics.

    Parameters
    ----------
    content:
        File content potentially containing conflict markers.

    Returns
    -------
    str
        Content with conflicts resolved.
    """

    lines = content.splitlines()
    resolved: List[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("<<<<<<<"):
            head: List[str] = []
            i += 1
            while i < len(lines) and not lines[i].startswith("======="):
                head.append(lines[i])
                i += 1
            i += 1  # skip =======
            incoming: List[str] = []
            while i < len(lines) and not lines[i].startswith(">>>>>>>"):
                incoming.append(lines[i])
                i += 1
            i += 1  # skip >>>>>>>
            block = incoming if len(incoming) >= len(head) else head
            resolved.extend(block)
            continue
        resolved.append(line)
        i += 1
    return "\n".join(resolved)
