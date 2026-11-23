"""The counts the video draws, against the figures the report and the script state (report/report.md)."""
import data

GUARDS = ("hook", "hookstop", "widehook")


def test_every_run_once():
    every = data.runs(("none", "prose", "hook", "both", "hookstop", "widehook", "readonly"))
    assert len(every) == 210
    assert len({r["id"] for r in every}) == 210


def test_runs_in_run_order():
    assert [r["id"] for r in data.runs("prose", "opus")] == [f"opus-prose-{n}" for n in range(1, 11)]


def test_no_rule_and_prose():
    assert data.changed("none") == 30
    assert sum(r["named_the_test"] for r in data.runs("none")) == 29
    assert data.changed("prose") == 0


def test_hook_missed_sonnet_and_opus():
    hook = ("hook", "hookstop")
    assert len(data.runs(hook, ("sonnet", "opus"))) == 40
    assert data.changed(hook, ("sonnet", "opus")) == 38
    assert len(data.runs(hook, "haiku", refused=True)) == 20


def test_nobody_went_around():
    refused = data.runs(GUARDS, refused=True)
    assert len(refused) == 52
    assert not any(r["routed_around"] for r in refused)
    assert all(r["outcome"] == "kept" for r in refused)


def test_what_closed_the_gap():
    assert data.changed(("both", "widehook", "readonly")) == 0
    assert len(data.runs(("both", "widehook", "readonly"))) == 90
    assert data.changed(("none", "prose", "hook", "both", "hookstop", "widehook", "readonly")) == 68
