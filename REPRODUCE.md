# Reproduce

Tools: https://github.com/lpurdy01/video_pipeline_workspace/tree/cdbab44 (Levi Purdy's video pipeline, public), changed for the channel in a copy that is not public

## The experiment (everything the findings rest on)

Python 3.10 or later. From `experiment/`:

```
python3 score.py 2026-11-22  # rewrites runs/2026-11-22/results.json and results.md from the saved runs
python3 -m pytest test_score.py   # the scorer's known-answer tests (made-up transcripts)
```

Every run's transcript is `experiment/runs/2026-11-22/ID.jsonl` and its facts `ID.json`, so every count can be
rechecked without calling a model. Running the agents again (`python3 run.py BATCH`, `experiment/README.md`) needs
Claude Code signed in to a Claude subscription and a sandbox in which only the run's folder is writable. A new batch
will not give the same runs: the models are sampled, and what runs behind a model name changes over time.

## The report

`report/report.md` is typeset as `report/report.pdf` by `report.py` in the channel's tools (Markdown and WeasyPrint).

## The video

Rendered with a copy of Levi Purdy's verification-compiler video pipeline (branch `video2-section1-hook` at
`cdbab44` in his repository), with the channel's changes: new chart kinds, the voice step, and fixes to the gate and
the assembly. That copy is not published yet; releasing it as the channel's shared tools repository is planned, not
done. What is here: the video's own code, `video/style.py` and one scene per section in `video/scenes/`.

- What cannot be reproduced exactly: the agents' runs, the checks made by models, and the voice render.
