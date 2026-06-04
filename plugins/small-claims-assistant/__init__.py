from __future__ import annotations

from pathlib import Path


HERE = Path(__file__).resolve().parent


def register(ctx) -> None:
    ctx.register_skill(
        name="notice-of-claim-intake",
        path=HERE / "skills" / "notice-of-claim-intake",
    )
    ctx.register_skill(
        name="notice-of-claim-pdf-generation",
        path=HERE / "skills" / "notice-of-claim-pdf-generation",
    )
    ctx.register_skill(
        name="notice-of-claim-filing-adapter",
        path=HERE / "skills" / "notice-of-claim-filing-adapter",
    )