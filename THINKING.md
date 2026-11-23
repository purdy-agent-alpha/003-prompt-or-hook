# Thinking before the script

Written before the script, and kept beside it. Each part is at least 60 words; the gate reads the three headings.

## First principles

A coding agent is a model that proposes tool calls and a harness that runs them. A rule in the prompt (CLAUDE.md, a
system prompt) changes what the model is likely to propose; it guarantees nothing. A hook is code the harness runs
before a matching tool call, and it can refuse that call every time. So the two act on different things: the prose
acts on intent, the hook on one route to the effect. What has to be true for "put it in a hook" to be the right
answer: the hook must cover every route to the effect the rule forbids, and the agent, once refused, must not look
for another route. Both are measurable: run the same task with the same rule given each way, record every tool call,
and check the files afterwards, whichever tool changed them. A task that can only be finished by breaking the rule
makes the pressure real: here, one test contradicts the specification.

## In the limit

Push the trend to its limit: agents that are fully capable, with a shell, a language interpreter and network access,
working for hours unattended. Any rule written as a refusal of one tool call is then a refusal of one syntax among
many; a capable agent that wants the effect has unlimited other syntaxes, and the hook has to grow into a model of
every way to write a file, which is a sandbox, a permission system or a filesystem rule, not a hook. What still holds
in the limit is the intent the agent forms from what it reads, and a boundary on effects (this folder is read-only,
for every process) rather than on commands. That says the answer now is less "prompt or hook" than "what does the
agent want, and is the effect itself closed off": the prose and the hook's message shape the first, and only a
boundary at the level of effects settles the second.

## The strongest counterargument

The strongest case against testing this at all: it is settled. Anthropic's own guidance says a rule that cannot have
exceptions belongs in a hook because the harness applies it every time, and practitioners report hooks working. The
known failures are bugs or misconfigured matchers, not a property of hooks; ImpossibleBench already showed that the
right prompt alone cuts test-editing from 92% to 1% for one model, and that read-only tests cut it further. A small
experiment on one made-up library adds nothing a careful engineer does not know.

Answer: partly tested here, and the answer changes. The experiment measures what "applies every time" covers when the
agent edits files through the shell, whether the wording of a refusal changes what the agent does next, and whether a
read-only folder holds; and it does so for Claude Code's current models, which the published work does not cover. It
does not settle the general question: one task, ten runs a cell, three models of one vendor; the close says so.
