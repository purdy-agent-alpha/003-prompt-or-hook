"""The experiment's runs as the scenes count them: experiment/runs/2026-11-22/results.json, read once.

Plain Python (no Manim), so test_data.py checks the counts the video shows against the report's figures."""
import json
from pathlib import Path

RESULTS = json.loads((Path(__file__).resolve().parents[1] / "experiment" / "runs" / "2026-11-22" /
                      "results.json").read_text())
MODELS = ("haiku", "sonnet", "opus")
CHANGED = "edited the test"


def runs(arms: str | tuple[str, ...], models: str | tuple[str, ...] = MODELS, refused: bool = False) -> list[dict]:
    """Runs of these arms and models, by model, then arm, then run 1 to 10; with `refused`, only those in which a
    hook refused at least one call."""
    arms, models = ((arms,) if isinstance(arms, str) else arms), ((models,) if isinstance(models, str) else models)
    out = [r for r in RESULTS["runs"] if r["arm"] in arms and r["model"] in models and (r["blocks"] or not refused)]
    return sorted(out, key=lambda r: (models.index(r["model"]), arms.index(r["arm"]), int(r["id"].rsplit("-", 1)[1])))


def changed(arms: str | tuple[str, ...], models: str | tuple[str, ...] = MODELS) -> int:
    """Runs of these arms and models whose test was changed, by any means."""
    return sum(r["outcome"] == CHANGED for r in runs(arms, models))
