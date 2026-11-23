# Method

- How the question became sub-questions: (1) given the same never-rule, how often does a coding agent break it with no
  rule, with the rule in CLAUDE.md, with a hook, with both? (2) When a hook refuses, does the agent stop, or reach the
  same effect another way? (3) Does the refusal's wording change that? (4) Does a hook that also screens the shell, or a
  read-only folder, close the other ways? (5) What did published work already measure, and on which agents?
- Searched, where and when (2026-11-22): web search for coding agents bypassing denied tool calls, runtime enforcement
  against prompt instructions, measured route-around rates; arXiv; the Claude Code issue tracker; Anthropic's Claude Code
  documentation. What was found is in report/report.md, "The question, and what was already known"; sources in
  sources/sources.yaml. The working notes (research/) are not published.
- Models and tools, by version: Claude Code 2.1.318 in print mode (`claude -p`, stream-json, bypassPermissions, 40 turns
  at most) with claude-haiku-5-5, claude-sonnet-5-5 and claude-opus-5-5, signed in with a Claude subscription; Python
  3.12.3 and unittest for the library; bubblewrap under podman unshare as the sandbox. Ten runs per model and arm,
  four at a time, on 2026-11-22. experiment/README.md has the arms and the measures; run.py and score.py are the code.
- How the experiment was designed: the idea of a task whose tests contradict its specification is ImpossibleBench's
  (S2); the honest way out (the rule says to leave the test and report it) follows the audit that found "cheating"
  vanishes when stopping is allowed (S7); the refusal wording arm answers the next step S3 names. The hooks live outside
  the repository after a pilot run in which Haiku read a hook kept inside the repository and so learned the rule as
  prose. The shell-screening and read-only arms were added after the first runs showed Sonnet editing files through
  the shell, where an Edit and Write hook never runs.
- Dead ends and dropped claims, each with why: a search summary said that in Permission Denied (S4) workarounds made up
  about 97% of policy-induced failures; the figure is not in the abstract and not in the text read, so it is dropped
  (S10). The first scoring counted Python's cache folder under tests/ as a changed test; the fixture now ignores it.
