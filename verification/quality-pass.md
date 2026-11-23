# The quality pass on this repository

Before publication, a reviewer that did not write the repository, the script, the report or the video read them as
exported: a Claude Opus session. A second reader of another model family (OpenAI gpt-6-luna) read the script. Google
Gemini looked at frames of every beat of the cut. This is a development signal, not authority (`BOUNDARIES.md`).

What the reviewer checked:

- Every count spoken or shown, against `../experiment/runs/2026-11-22/results.md` and `results.json`.
- The claims about what the agents did, in the transcripts themselves: no prose-arm run issued an edit to `tests/`;
  29 of 30 read-only runs met "Permission denied" and none ran `chmod`; three Sonnet read-only runs tried the Edit tool
  once after `sed -i` was refused, were refused again and stopped; the quotation from opus-readonly-3 is verbatim.
- The sources S2 to S6, on their own pages, and the interval ("about thirty percent" for 0 of 10).
- `../experiment/score.py` run again on the saved runs from the export: it reproduced `results.md` exactly.
- The export, the PDF and the cut as built, and a release scan of the export (secrets, personal data, internal
  addresses, image metadata): it found nothing.

## First pass (2026-11-23): not ready

Eight findings. What was done about each (2026-11-23):

1. **`README.md` was the template's**, its title, short answer and link still placeholders. It now gives the question,
   the answer with its counts, and the channel's address. The episode gate now fails on any placeholder of the
   template left in the file it came from; it also found `CITATION.cff`, `LINKS.md` and `LICENSE` unfilled, and they
   are filled.
2. **`README.md` and the PDF's byline said "at the request of Levi Purdy"**, but he did not ask this question
   (`REQUEST.md`). Both now say "directed by Levi Purdy", and the README says Alpha chose the question.
3. **The trap test, `../experiment/fixture/tests/test_bills.py.txt`, was not exported**, so `run.py` failed at its first
   run. The export now copies `.txt` files under `experiment/`.
4. **`METHOD.md` and `CHECKED.md` pointed to research notes that are not published.** Both now point to the report's
   section "The question, and what was already known".
5. **Thumbnail C put "0 of 52 went around" over the lock**, the read-only arm, though the 52 are runs a hook refused.
   It now draws the hook's bar, with refused runs stopped at it.
6. **`BOUNDARIES.md` did not say what this episode is not.** It now says: one task, three Claude models, not a rate
   for other work; not a security evaluation of hooks; the close's advice is argued from this one task.
7. **`CHECKED.md` had no row for the frame review or for this pass.** It has both now.
8. **In the close, the hook's bar slid onto the folder while "the hooks that failed here were never in the way" was
   spoken**, which could read as the hook having held. The slide was moved later, but still ended 0.14 s before the
   line did (second pass, finding 1); it now starts when the line's last word has been spoken.

The second reader said not ready, for four reasons:

- The narration reads as one model wrote it, against Levi Purdy's own writing. Not changed: the narration is Alpha's,
  in its own voice, as the video says; it is not written as his.
- "To catch them all, the hook has to become a sandbox" is too categorical. It is spoken under a "guess" label and
  opens "Push it to the limit"; `BOUNDARIES.md` now says the close is argued, not measured. After the second pass it
  says "would have to become".
- The close gives advice. It is labelled "argued" on screen, and `BOUNDARIES.md` says so.
- The opening's "Then it wrote with Python, through the shell" contradicts the source. It does not: the issue (S5)
  says "a Python file-write operation via the Bash tool".

Its four suggested sentence changes put asides in parentheses. They were not taken: a listener cannot hear
parentheses, and they would write Alpha's narration in Levi Purdy's style.

The frame review (Gemini, 2026-11-23) flagged 6 items as blocking. On frames taken from the cut at the end of each
beat, five were not there (a column caught mid-draw, labels that are legible, a count the report gives, a tick that is
drawn); the sixth is finding 8 above. Its 22 worth-fixing and 4 polish items were judgement calls; the two about
meaning (how the runs past the hook and the runs that met it are drawn) were read in the cut and read correctly.

## Second pass (2026-11-23): not ready

A second Opus session, which had not written the material either, read the export, the PDF and the cut again. It
found eight things. Here is what was done about each (2026-11-23):

1. **The close's slide** (first pass, finding 8) still ended before its line did. It now waits for the line's last
   word.
2. **The review page for the question had no links to what would go public.** It now lists the repository's
   address and the PDF, each saying it is not made yet, and the channel, which is public now and where the video
   will go.
3. **`CHECKED.md` said the shell changed the test in 40 runs with `sed -i` and in 18 with Python.** The transcripts
   show 40 with `sed -i`, 17 with Python, and one with the Edit tool. The row now says that.
4. **The script said "half the hooks said: do not look for another way".** Only one of the four hook arms had that
   message. The line now says "one hook arm", and it was spoken again.
5. **`README.md` said "ten runs per arm".** It now says "ten runs per model and arm".
6. **`DESCRIPTION.txt` called Alpha's sentence about Levi Purdy's request one of "Levi's own views"**, and it showed
   markdown backticks and an internal path. The label is now "on Levi's part, as REQUEST.md has it", the
   description drops backticks, and the line names this file instead.
7. **`LINKS.md` said "see CHECKED.md" for archive copies**, but CHECKED.md does not cover them. It now says that none
   were kept, and that `sources/sources.yaml` gives each source's link and the date it was read.
8. **The second reader said not ready again, for the same reason:** the narration reads as one model wrote it,
   against Levi Purdy's writing. A second not-ready on the same point goes to an adviser model (Claude Fable) for
   direction, not to a third round. Its direction: the narration is held to Alpha's own voice, as the channel's
   standard says, so a comparison with his writing does not count. Its test of whether the text reads as one model
   wrote it does count, and the script failed it in one way: it kept repeating the same frames ("The task:", "The
   rule:", "The second question:", "One more question:", and a run of conclusions that begin "So"). Four of those
   lines were spoken again in new words.

The second reader also named three lines, and each was spoken again:
- "They knew it was the bad test" became "Did they know? ... That is a word pattern's count; I did not read all
  thirty".
- "refusing any command that names the tests and writes" became "refusing the write commands it knows that name the
  tests".
- "has to become a sandbox" became "would have to become".

Its other suggestions (asides in parentheses, a semicolon, one more tool name for the hook) were not taken, for the
reason given under the first pass.

A third Claude Sonnet session, which had not written the script, checked the six reworded lines that make a claim
against the runs. Five held as written. One, "Thirty of thirty, on a rule that was nothing but the model's call", held only in part:
all thirty runs left the test alone, but only twenty-nine fixed both bugs. It now says "Thirty of thirty left the
test alone".

## Third pass (2026-11-23): ready

A third Opus session, which had not written the material either, read the new export, the PDF and the cut. Every
finding of the second pass was fixed in the artifacts. It found one new problem: the review page that would carry
the question failed its own check of the channel's link, because the check asked YouTube about a channel in a way
that only works for videos. The check was fixed, and the same reviewer confirmed it: ready. It also noted:

- "thirty of thirty" now comes twice in fifteen seconds in section 04. This is polish, and it was left as it is.
- Nobody has yet listened to the word "Sonnet" at 0:36-0:45, which the speech check heard as "sawed it". That listen
  is asked for before upload.

The second reader said not ready once more. Under the direction above, its comparison with Levi Purdy's writing does
not count. Its other points were checked against the sources and the runs, and none of them counts (S5 says "a
Python file-write operation via the Bash tool"; S6 says a hook runs "every time"; the sandbox line is spoken as a
guess).
