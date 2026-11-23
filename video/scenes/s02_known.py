"""
Section 02: what was known. A search for prior art sets four sources down the left; each finding opens beside its
source (Anthropic's guide: the model's call against every time, "belongs in a hook"; ImpossibleBench's two results,
each on its own benchmark; Morris's 116 refused deletes, 25 removed another way), and the four become the rows of a
ledger whose last row, this experiment, is empty.

Another study's shares are drawn in grey and white, never in the run colours: green and red mean a kept or a changed
test in this video, so Morris's 25 are lit white, not red as the storyboard has it.

Every wait inside a beat is a fraction of its window (`ctx.at`), so a re-timed voice needs no edit.
"""
from __future__ import annotations

from manim import *

import style
from pipeline import charts
from pipeline.beats import Beat, BeatScene

SOURCES = ("vendor's docs", "papers", "deployments", "the issue tracker")
RAIL_X, RAIL_W = -4.95, 3.0
FIG_X = 1.75   # the centre of the stage right of the rail

# Anthropic's best-practices page (sources.yaml S6; research/prior-art.md), quoted exactly.
DOC_TITLE = "Best practices for Claude Code"
DOC_QUOTE = ("“Claude Code applies this every time”",
             "“[...] a rule that can't have exceptions,", "in which case it belongs in a hook”")
DOC_LIT = "belongs in a hook"

# ImpossibleBench (S2): GPT-5's cheating on Conflicting-LiveCodeBench, 92% to 1% with the right prompt; hidden tests
# took cheating on Impossible-SWEbench near zero, at a cost in performance (no figure given in the script).
LCB = (92, 1)

# Morris (S3): 4,209 refusals; after a refused rm -rf, 25 of 116 episodes removed the same target another way.
MORRIS = (25, 116)

# The ledger: what each source measured. Ticks only where research/prior-art.md says so.
COLUMNS = (("prose",), ("hook",), ("both",), ("Claude", "Code"), ("current", "models"), ("every", "call"))
# The ledger's layout: a column's width, a row's height, the name cards' width, the first column's x.
COL_W, ROW_H, HEAD_W, X_FIRST = 1.22, 0.56, 2.9, -1.5
LEDGER = (
    ("Claude Code docs", {3}),         # Claude Code's own guide; advice, no counts
    ("ImpossibleBench", {0}),          # prompts varied; 2025 models, its own scaffold
    ("Morris", {1, 4}),                # platform deny rules; 30 models, production, Oct 2026
    ("issue 29709", {1, 3}),           # one Edit hook in Claude Code; one report
)


def quote_line(text: str, lit: str = "") -> Text:
    """A quoted line in grey with a phrase ready to light: one Text, so its words keep their spacing. Ligatures off,
    so glyph i is character i and `light` can find the phrase by its index."""
    t = Text(text, color=style.MUTED, font_size=style.TYPE["label"], disable_ligatures=True)
    t.lit_span = (text.index(lit), text.index(lit) + len(lit)) if lit and lit in text else None
    return style._stamp(t, text)


def light(line: Text) -> Animation:
    """The line's phrase turns white: a Transform of the whole line, so no slice of it is left on stage alone."""
    lit = line.copy()
    a, b = line.lit_span
    lit[a:b].set_color(style.WHITE)
    return Transform(line, lit)


def ledger() -> tuple[VGroup, VGroup]:
    """The ledger's column heads and one row per source: its name on a card, then a tick or a dash per column.
    (heads, rows), each row VGroup(card, name, marks)."""
    heads = VGroup()
    for i, words in enumerate(COLUMNS):
        head = style.text_rows(*[style.label_text(w, color=style.MUTED) for w in words], align=ORIGIN)
        head.move_to(RIGHT * (X_FIRST + COL_W * i) + UP * 1.55, aligned_edge=DOWN)
        heads.add(head)
    rows = VGroup()
    for r, (name, ticks) in enumerate(LEDGER):
        y = 0.95 - ROW_H * r
        box = style.card(HEAD_W, ROW_H - 0.1).move_to(RIGHT * (X_FIRST - 0.55 - COL_W / 2 - HEAD_W / 2) + UP * y)
        word = style.label_text(name, color=style.WHITE).move_to(box)
        marks = VGroup(*[(style.tick() if i in ticks else Line(LEFT * 0.14, RIGHT * 0.14, color=style.DIM,
                                                           stroke_width=3))
                         .move_to(RIGHT * (X_FIRST + COL_W * i) + UP * y) for i in range(len(COLUMNS))])
        rows.add(VGroup(box, word, marks))
    return heads, rows


class S02Known(BeatScene):
    section_id = "02_what_was_known"
    title = "What Was Known"

    def storyboard(self) -> list[Beat]:
        return [
            Beat("First, what was already known", self.b_search, kind="search"),
            Beat("Anthropic's own guide for Claude", self.b_docs, kind="document"),
            Beat("ImpossibleBench gave models tasks", self.b_impossible, kind="dumbbell"),
            Beat("A study of four thousand", self.b_morris, kind="unit"),
            Beat("What I could not find", self.b_ledger, kind="ledger"),
        ]

    def _source(self, i: int, ctx, frac: float):
        """Light source i on the rail and dim the others: the finding on the right came from it."""
        anims = []
        for j, (box, word) in enumerate(self._owned["rail"][1]):
            on = j == i
            anims += [box.animate.set_stroke(style.WHITE if on else style.DIM, width=2.6 if on else 2.0),
                      word.animate.set_color(style.WHITE if on else style.MUTED)]
        self.play(*anims, run_time=ctx.at(frac, 0.4))

    # ---------------------------------------------------------------- beats --
    def b_search(self, ctx):
        field = style.card(RAIL_W, 0.6)
        lens = VGroup(Circle(radius=0.12, color=style.WHITE, stroke_width=3),
                      Line(ORIGIN, DR * 0.13, color=style.WHITE, stroke_width=3.4))
        lens[1].shift(lens[0].point_at_angle(-PI / 4) - lens[1].get_start())
        what = style.label_text("prior art", color=style.WHITE)
        VGroup(lens, what).arrange(RIGHT, buff=0.25).move_to(field)
        search = VGroup(field, lens, what).move_to(RIGHT * RAIL_X + UP * 1.85)
        tiles = VGroup()
        for i, words in enumerate(SOURCES):
            box = style.card(RAIL_W, 0.62).move_to(RIGHT * RAIL_X + UP * (0.85 - 0.86 * i))
            tiles.add(VGroup(box, style.label_text(words, color=style.WHITE).move_to(box)))
        ctx.lopsided("the search sets its sources down the left; the first finding opens beside them next line")
        a, b = ctx.budget(0.35, 1.2)
        self.play(FadeIn(search, shift=DOWN * 0.1), run_time=a)
        self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.15) for t in tiles], lag_ratio=0.3), run_time=b)
        self._owned["rail"] = VGroup(search, tiles)

    def b_docs(self, ctx):
        who = VGroup(style.label_text("Anthropic", color=style.MUTED),
                     style.label_text(DOC_TITLE, color=style.WHITE)).arrange(RIGHT, buff=0.4)
        quote = VGroup(*[quote_line(l, DOC_LIT) for l in DOC_QUOTE])
        body = style.text_rows(who, style.text_rows(*quote), buff=0.32)
        page = style.card(body.width + 0.7, body.height + 0.6)
        VGroup(page, body).move_to(RIGHT * FIG_X + UP * 1.2)
        body.move_to(page)

        y = -1.05
        card = style.page_card(width=1.5, height=1.5, rules=4).move_to(RIGHT * (FIG_X - 2.6) + UP * y)
        call = style.label_text("the model's call", color=style.arm_color("prose")).next_to(card, RIGHT, buff=0.35)
        bar = style.hook_bar(height=1.2, label=False).move_to(RIGHT * (FIG_X + 1.55) + UP * y)
        tests = style.folder(width=1.2, height=0.95).next_to(bar, RIGHT, buff=0.25)
        tests[2].scale(0.85)
        every = style.label_text("every time", color=style.arm_color("hook")).next_to(tests, RIGHT, buff=0.35)

        self._source(0, ctx, 0.0)
        # "Anthropic's own guide for Claude Code says"
        ctx.show(page, who, tag="page", run_time=ctx.at(0.03, 0.5), nudge=False)
        # "a line in CLAUDE.md is the model's call"
        self.play(FadeIn(card, shift=UP * 0.15), run_time=ctx.at(0.2, 0.45))
        self.play(FadeIn(call, shift=RIGHT * 0.1), run_time=ctx.at(0.26, 0.4))
        self._owned["call"] = VGroup(card, call)
        # "while a hook runs every time": the bar, and the page's own words for it.
        self.play(FadeIn(tests), GrowFromEdge(bar[0], UP), run_time=ctx.at(0.38, 0.5))
        self.play(FadeIn(every, shift=RIGHT * 0.1), FadeIn(quote[0], shift=RIGHT * 0.1), run_time=ctx.at(0.44, 0.5))
        self._owned["every"] = VGroup(bar[0], tests, every)
        # "A rule that can't have exceptions, it says, belongs in a hook."
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.1) for l in quote[1:]], lag_ratio=0.4),
                  run_time=ctx.at(0.6, 0.8))
        self._owned["quote"] = quote
        self.play(light(quote[2]), run_time=ctx.at(0.82, 0.5))

    def b_impossible(self, ctx):
        ctx.clear_stage("rail", run_time=0.35)
        self._source(1, ctx, 0.03)
        x0, width = FIG_X - 3.9, 7.8
        plot = charts.Plot(RIGHT * x0 + DOWN * 1.75, width, 0.01, (0, 100), (0, 1),
                           x_ticks=[(0, "0%"), (50, "50%"), (100, "100%")])
        who = style.label_text("Zhong et al., 2025 · ImpossibleBench", color=style.MUTED)
        who.move_to(RIGHT * FIG_X + UP * 2.0)
        y1, y2 = UP * (0.75 + 1.75), UP * (-0.7 + 1.75)
        name1 = style.label_text("Conflicting-LiveCodeBench · GPT-5", color=style.WHITE)
        name2 = style.label_text("Impossible-SWEbench · tests hidden", color=style.WHITE)
        name1.next_to(plot.at(0, 0) + y1, UP, buff=0.4).align_to(plot.at(0, 0), LEFT)
        name2.next_to(plot.at(0, 0) + y2, UP, buff=0.4).align_to(plot.at(0, 0), LEFT)
        hi, lo = plot.at(LCB[0], 0) + y1, plot.at(LCB[1], 0) + y1
        span = Line(hi, hi, color=style.WHITE, stroke_width=8, stroke_opacity=0.5)
        before = Dot(hi, radius=0.13, color=style.MUTED)
        after = Dot(lo, radius=0.13, color=style.WHITE)
        v_before = style.label_text(f"{LCB[0]}%", color=style.MUTED).next_to(before, UP, buff=0.22)
        v_after = style.label_text(f"{LCB[1]}%", color=style.WHITE).next_to(after, LEFT, buff=0.22)
        prompt = style.label_text("the right prompt", color=style.WHITE).next_to(Line(lo, hi), DOWN, buff=0.22)
        near = Dot(plot.at(1, 0) + y2, radius=0.13, color=style.WHITE)
        near_word = style.label_text("near zero", color=style.WHITE).next_to(near, RIGHT, buff=0.3)
        cost_word = style.label_text("at a cost in performance", color=style.WHITE)
        cost = style.boxed(cost_word)
        cost.next_to(near_word, RIGHT, buff=0.6)

        ctx.show(who, plot, tag="plot", run_time=ctx.at(0.05, 0.5), nudge=False)
        # "gave models tasks whose tests contradict the specification, so any pass is a cheat"
        self.play(FadeIn(name1, shift=RIGHT * 0.1), run_time=ctx.at(0.2, 0.4))
        self.play(FadeIn(before, scale=0.6), FadeIn(v_before), run_time=ctx.at(0.3, 0.5))
        # "The right prompt cut GPT-5's cheating on one benchmark from ninety-two percent to one"
        self.add(span)
        self.play(span.animate.put_start_and_end_on(hi, lo), run_time=ctx.at(0.4, 1.4))
        self.play(FadeIn(after, scale=0.6), FadeIn(v_after), FadeIn(prompt),
                  run_time=ctx.at(0.5, 0.5))
        self._owned["lcb"] = VGroup(name1, span, before, after, v_before, v_after, prompt)
        # "hiding the tests took cheating on another near zero, at a cost in performance"
        self.play(FadeIn(name2, shift=RIGHT * 0.1), run_time=ctx.at(0.62, 0.4))
        self.play(FadeIn(near, scale=0.6), FadeIn(near_word), run_time=ctx.at(0.72, 0.5))
        self.play(FadeIn(cost, shift=LEFT * 0.15), run_time=ctx.at(0.84, 0.5))
        self._owned["swe"] = VGroup(name2, near, near_word, cost)

    def b_morris(self, ctx):
        ctx.clear_stage("rail", run_time=0.35)
        self._source(2, ctx, 0.02)
        kept, total = MORRIS
        cells = charts.waffle(0, style.WHITE, total=total, cols=12, cell=0.24, gap=0.07)
        cells.move_to(RIGHT * (FIG_X - 1.2) + DOWN * 0.15)
        lit = charts.waffle(kept, style.WHITE, total=kept, cols=12, cell=0.24, gap=0.07)
        for sq, home in zip(lit, cells):
            sq.move_to(home)
        who = style.label_text("Morris, Oct 2026 · 4,209 refusals", color=style.MUTED)
        who.next_to(cells, UP, buff=0.35).align_to(cells, LEFT)
        refused = VGroup(style.label_text(f"{total} refused", color=style.WHITE),
                         style.mono_text("rm -rf", color=style.WHITE, size="label")).arrange(RIGHT, buff=0.2)
        another = style.text_rows(style.label_text(f"{kept} removed the target", color=style.WHITE),
                                  style.label_text("another way, same turn", color=style.WHITE), buff=0.16)
        side = style.text_rows(refused, another, buff=0.7).next_to(cells, RIGHT, buff=0.6)

        # "A study of four thousand two hundred and nine refusals on a production agent platform"
        ctx.show(who, tag="who", run_time=ctx.at(0.04, 0.4), nudge=False)
        # "found that after a refused recursive delete": one square a refused rm -rf.
        self.play(LaggedStart(*[FadeIn(c, scale=0.5) for c in cells], lag_ratio=0.01), run_time=ctx.at(0.07, 1.6))
        self.play(FadeIn(refused, shift=LEFT * 0.1), run_time=ctx.at(0.18, 0.4))
        self._owned["cells"] = VGroup(cells, refused)
        # "twenty-five of a hundred and sixteen episodes removed the same target another way, in the same turn"
        self.play(LaggedStart(*[FadeIn(c, scale=1.4) for c in lit], lag_ratio=0.08), run_time=ctx.at(0.52, 1.6))
        self.play(FadeIn(another, shift=LEFT * 0.1), run_time=ctx.at(0.66, 0.5))
        self._owned["lit"] = VGroup(lit, another)
        self.play(LaggedStart(*[Indicate(c, color=style.WHITE, scale_factor=1.25) for c in lit], lag_ratio=0.05),
                  run_time=ctx.at(0.84, 1.2))

    def b_ledger(self, ctx):
        ctx.clear_stage("rail", run_time=0.35)
        search, tiles = self._owned.pop("rail")
        heads, rows = ledger()
        y = 0.95 - ROW_H * len(LEDGER) - 0.12
        mine = style.card(rows[0][0].get_right()[0] - rows[0][0].get_left()[0] + COL_W * len(COLUMNS) + 0.3, ROW_H,
                      style.WHITE, dashed=True)
        mine.move_to(RIGHT * (rows[0][0].get_left()[0] + mine.width / 2) + UP * y)
        mine_word = style.label_text("this experiment", color=style.WHITE).move_to(RIGHT * rows[0][0].get_x() + UP * y)
        slots = VGroup(*[Circle(radius=0.13, color=style.WHITE, stroke_width=2.2)
                         .move_to(RIGHT * (X_FIRST + COL_W * i) + UP * y) for i in range(len(COLUMNS))])
        missed = style.label_text("not found", color=style.MUTED)
        missed.next_to(mine, DOWN, buff=0.35).align_to(mine, LEFT)

        # The four sources become the ledger's rows.
        a, b = ctx.budget(0.3, 0.8)
        self.play(FadeOut(search), run_time=a)
        self.play(*[ReplacementTransform(t, VGroup(r[0], r[1])) for t, r in zip(tiles, rows)],
                  LaggedStart(*[FadeIn(h, shift=DOWN * 0.1) for h in heads], lag_ratio=0.15), run_time=b)
        self._owned["heads"] = heads
        self._owned["rows"] = VGroup(*[VGroup(r[0], r[1]) for r in rows])
        # "the same rule given as prose, as a hook, and as both, in Claude Code, on current models, with every call
        # recorded": each source's ticks and gaps, column by column as the line names them.
        for i, frac in enumerate((0.1, 0.17, 0.24, 0.33, 0.44, 0.53)):
            self.play(*[FadeIn(r[2][i], scale=1.3) for r in rows], *style.highlight(heads[i], style.WHITE),
                      run_time=ctx.at(frac, 0.4))
        self._owned["marks"] = VGroup(*[r[2] for r in rows])
        # Nobody's row has all six: the empty row, lit.
        self.play(Create(mine), FadeIn(mine_word), run_time=ctx.at(0.62, 0.6))
        self.play(LaggedStart(*[FadeIn(s, scale=0.6) for s in slots], lag_ratio=0.15), run_time=ctx.at(0.68, 0.8))
        self._owned["mine"] = VGroup(mine, mine_word, slots)
        # "If it exists, my search missed it."
        ctx.show(missed, tag="missed", run_time=ctx.at(0.8, 0.5), nudge=False)
