"""Async workflow scheduling utilities."""

from __future__ import annotations

import asyncio
from typing import Any, Dict, Iterable, List, Callable


class WorkflowScheduler:
    """Run tasks with asynchronous parallelism."""

    def __init__(self, max_parallel: int = 3) -> None:
        self.max_parallel = max_parallel

    async def run_parallel(
        self,
        modules: Iterable[str],
        run_fn: Callable[[str, Dict[str, Any] | None], Dict[str, Any]],
        context: Dict[str, Any] | None = None,
    ) -> List[Dict[str, Any]]:
        """Execute modules concurrently using an asyncio semaphore."""

        semaphore = asyncio.Semaphore(self.max_parallel)

        async def _run(module: str) -> Dict[str, Any]:
            async with semaphore:
                return await asyncio.to_thread(run_fn, module, context)

        tasks = [asyncio.create_task(_run(m)) for m in modules]
        return await asyncio.gather(*tasks)
