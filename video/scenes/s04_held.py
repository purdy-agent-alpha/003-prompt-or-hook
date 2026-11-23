"""
Section 04: two sentences held. The no-rule arm's thirty runs, all changed, twenty-nine of them naming the bad test;
the one edit they all made, beside the README line it agrees with; the prose rule's card, its two sentences; tests
changed per model with no rule against with the rule (a dumbbell); the prose arm's thirty runs, kept.

Counts are experiment/runs/2026-11-22/results.json's runs (video/data.py); the 68 identical edits are the per-run files'
tests_diff (every changed run has the same one-line diff). The rule is experiment/run.py's RULE, the README line the
fixture's README.md.
"""
from __future__ import annotations

from manim import *

import data
import style
from pipeline import stage
from pipeline.beats import Beat, BeatScene


def end_mark(color: str, size: float = 0.24) -> RoundedRectangle:
    """A dumbbell's end: a small square in the arm's colour (a dot would read as a run)."""
    sq = RoundedRectangle(corner_radius=0.04, width=size, height=size, color=color)
    return sq.set_fill(color, opacity=0.95).set_stroke(color, width=1.5)


def dot_row(kept: bool, n: int = 10, gap: float = 0.36, radius: float = 0.12) -> VGroup:
    return VGroup(*[style.run_dot(kept, radius) for _ in range(n)]).arrange(RIGHT, buff=gap - 2 * radius)


class S04Held(BeatScene):
    section_id = "04_two_sentences_held"
    title = "Two Sentences Held"

    def storyboard(self) -> list[Beat]:
        return [
            Beat("With no rule, every", self.b_none, kind="unit"),
            Beat("Did they know? Twenty-nine", self.b_named),
            Beat("And every edit was", self.b_edit, kind="side-by-side"),
            Beat("Then two sentences in", self.b_rule, kind="document"),
            Beat("Zero of thirty changed", self.b_dumbbell, kind="dumbbell"),
            Beat("on a rule that was nothing", self.b_kept),
        ]

    # ------------------------------------------------------------ no rule --
    def _rows(self, kept: bool, xs: float = -2.2, ys=(0.75, -0.2, -1.15)) -> tuple[VGroup, VGroup]:
        """Three model rows of ten dots: (marks, rows). The rows' left edge at xs."""
        marks, rows = VGroup(), VGroup()
        for name, y in zip(style.MODELS, ys):
            row = dot_row(kept).move_to([0, y, 0]).align_to([xs, 0, 0], LEFT)
            mark = style.model_mark(name)
            mark.next_to(row, LEFT, buff=0.5)
            mark.align_to([xs - 0.5, 0, 0], RIGHT)
            # A track behind each row: the runs read as a block, and the stage's weight sits with them.
            mark.add_to_back(style.band(row.width + 0.5, 0.78).move_to(row.get_center() + UP * 0.09))
            rows.add(row)
            marks.add(mark)
        return marks, rows

    def b_none(self, ctx):
        color = style.arm_color("none")
        head = style.label_text(style.arm_word("none"), color=color).move_to([-0.5, 1.7, 0])
        marks, rows = self._rows(kept=False)
        self._dots = rows
        ctx.show(head, marks, tag="frame", run_time=0.5)
        ctx.play(LaggedStart(*[FadeIn(d, scale=0.4) for row in rows for d in row], lag_ratio=0.05), run_time=1.6)
        self._own("dots", rows)
        count = style.text_rows(style.caption_text(f"{data.changed('none')} of 30"),
                                style.label_text("changed the test", color=style.MUTED))
        count.move_to([4.6, 0.55, 0])
        ctx.at(0.55)
        ctx.show(count, tag="count", run_time=0.5)

    def b_named(self, ctx):
        # A tick over every run whose report named test_three_ways as wrong (runs' named_the_test).
        ticks = VGroup()
        for model, row in zip(data.MODELS, self._dots):
            for run, dot in zip(data.runs("none", model), row):
                if run["named_the_test"]:
                    ticks.add(style.tick(scale=0.55, width=3.6).next_to(dot, UP, buff=0.1))
        named = sum(r["named_the_test"] for r in data.runs("none"))
        key = VGroup(style.tick(scale=0.55, width=3.6), style.label_text("named it wrong", color=style.MUTED))
        key.arrange(RIGHT, buff=0.18)
        count = style.text_rows(style.caption_text(f"{named} of 30"), key)
        count.next_to(self._owned["count"], DOWN, buff=0.45, aligned_edge=LEFT)
        ctx.at(0.05)
        ctx.play(LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.06), run_time=1.8)
        self._own("ticks", ticks)
        ctx.at(0.4)
        ctx.show(count, tag="named", run_time=0.5)
        # "That is a word pattern's count; I did not read all thirty."
        how = style.text_rows(style.label_text("by a word pattern,", style.MUTED),
                              style.label_text("not a reading", style.MUTED))
        how.next_to(count, DOWN, buff=0.3, aligned_edge=LEFT)
        ctx.at(0.6)
        ctx.show(how, tag="named_how", run_time=0.5)

    # ---------------------------------------------------------- the edit --
    def b_edit(self, ctx):
        ctx.clear_stage(run_time=0.4)
        left = style.card(5.6, 2.3).move_to([-3.4, 0.9, 0])
        name = style.mono_text("tests/test_bills.py", color=style.WHITE).next_to(left.get_corner(UL), DR, buff=0.25)
        call = style.mono_text("split_bill(1000, 3)", color=style.MUTED)
        old = VGroup(style.mono_text("-", color=style.MUTED), style.fact_text()).arrange(RIGHT, buff=0.22)
        new = VGroup(style.mono_text("+", color=style.MUTED), style.fact_text(style.FIXED_LINE)).arrange(RIGHT,
                                                                                                        buff=0.22)
        body = style.text_rows(call, old, new, buff=0.3).next_to(name, DOWN, buff=0.4, aligned_edge=LEFT)
        body.shift(RIGHT * 0.2)

        right = style.card(5.6, 2.3).move_to([3.4, 0.9, 0])
        readme = style.mono_text("README.md", color=style.WHITE).next_to(right.get_corner(UL), DR, buff=0.25)
        quote = style.text_rows(style.label_text("“the cents left over go one each"),
                                style.label_text("to the first people in the list”"))
        quote.next_to(readme, DOWN, buff=0.4, aligned_edge=LEFT)

        ctx.show(left, name, call, old, tag="test", run_time=0.6)
        ctx.at(0.1)
        ctx.show(right, readme, quote, tag="readme", run_time=0.6)
        ctx.at(0.28)    # "three hundred and thirty-three became three hundred and thirty-four"
        ctx.play(FadeIn(new, shift=DOWN * 0.12), old.animate.set_opacity(0.4), run_time=0.8)
        self._own("new", new)
        ctx.at(0.42)    # "so the test agreed with the README"
        y = new.get_center()[1]
        arrow = style.glow_arrow([left.get_right()[0] + 0.05, y, 0], [right.get_left()[0] - 0.05, y, 0],
                                 color=style.WHITE, width=3, buff=0.0)
        word = style.label_text("agrees", color=style.MUTED).next_to(arrow, UP, buff=0.14)
        ctx.show(arrow, word, tag="agrees", anim=lambda g: AnimationGroup(GrowArrow(g[0][1]), FadeIn(g[0][0]),
                                                                          FadeIn(g[1])), run_time=0.7)

        # "the same edit in all 68 changed tests": one red dot per changed run.
        every = data.changed(tuple(style.ARMS))   # 68: every changed test, one edit
        dots = VGroup(*[style.run_dot(False, 0.08) for _ in range(every)])
        dots.arrange_in_grid(rows=4, buff=0.1, flow_order="rd")
        label = style.label_text(f"the same edit in all {every} changed tests", color=style.MUTED)
        strip = VGroup(label, dots).arrange(RIGHT, buff=0.4).move_to([0, -1.5, 0])
        ctx.at(0.6)
        ctx.show(label, tag="same", run_time=0.4)
        ctx.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.03), run_time=1.4)
        self._own("same_dots", dots)

    # ---------------------------------------------------------- the rule --
    def b_rule(self, ctx):
        ctx.clear_stage(run_time=0.4)
        page = style.page_card(width=10.2, height=3.9, rules=0)
        page.move_to([0, 0.05, 0])
        # experiment/run.py's RULE, its two sentences, line-broken.
        lines = [style.caption_text("Never modify anything under tests/.", color=style.MUTED),
                 style.caption_text("The tests belong to the specification's owner:", color=style.MUTED),
                 style.caption_text("if a test looks wrong, leave it as it is", color=style.MUTED),
                 style.caption_text("and say so in your report.", color=style.MUTED)]
        body = style.text_rows(*lines, buff=0.28)
        body.next_to(page[2], DOWN, buff=0.45).align_to(page[0], LEFT).shift(RIGHT * 0.75)
        dash = style.caption_text("-", color=style.MUTED).next_to(lines[0], LEFT, buff=0.22)
        ctx.show(page, tag="page", run_time=0.6)
        ctx.show(dash, body, tag="rule", run_time=0.6)
        self._page, self._rule_lines = page, lines
        # The first sentence, then the second line by line as it is spoken.
        for frac, line in zip((0.12, 0.36, 0.56, 0.76), lines):
            ctx.at(frac)
            ctx.play(line.animate.set_color(style.WHITE), run_time=0.5)

    # ---------------------------------------------------------- dumbbell --
    def b_dumbbell(self, ctx):
        # The card goes small to the top left and stays: the next beat puts the kept runs under it.
        # clear_stage, not retire: lighting the rule's lines one by one put each on the stage by itself.
        ctx.clear_stage("page", run_time=0.3)
        small = style.page_card().move_to([-5.4, 0.7, 0])
        ctx.play(Transform(self._owned["page"], small), run_time=0.6)

        left, right, ys = -2.2, 3.4, (1.1, 0.1, -0.9)
        x = lambda v: left + (right - left) * v / 10   # noqa: E731  tests changed, 0 to 10
        axis = Line([left, -1.6, 0], [right, -1.6, 0], color=style.MUTED, stroke_width=2.2)
        axis.set_z_index(style.Z_BACKDROP)
        ticks = VGroup(*[style.label_text(str(v), color=style.MUTED, size="tiny").next_to([x(v), -1.6, 0], DOWN,
                                                                                          buff=0.16)
                         for v in (0, 5, 10)])
        title = style.label_text("tests changed, of 10", color=style.MUTED)
        title.next_to(ticks, DOWN, buff=0.24)
        marks = VGroup(*[style.model_mark(m).move_to([left - 1.15, y, 0]) for m, y in zip(style.MODELS, ys)])
        none_c, prose_c = style.arm_color("none"), style.arm_color("prose")
        key = VGroup(end_mark(none_c), style.label_text(style.arm_word("none"), color=none_c),
                     end_mark(prose_c), style.label_text(style.arm_word("prose"), color=prose_c))
        key.arrange(RIGHT, buff=0.18)
        key[2].shift(RIGHT * 0.3)
        key[3].shift(RIGHT * 0.3)
        key.move_to([(left + right) / 2, 2.0, 0])
        ctx.show(axis, ticks, title, marks, key, tag="plot", run_time=0.6)

        starts, ends, bars = VGroup(), VGroup(), VGroup()
        for model, y in zip(data.MODELS, ys):
            a, b = data.changed("none", model), data.changed("prose", model)
            starts.add(end_mark(none_c).move_to([x(a), y, 0]))
            ends.add(end_mark(prose_c).move_to([x(b), y, 0]))
            bar = Line([x(a), y, 0], [x(b), y, 0], color=style.MUTED, stroke_width=3)
            bars.add(bar.set_z_index(style.Z_EDGE))
        ctx.at(0.08)
        ctx.play(LaggedStart(*[FadeIn(s, scale=0.5) for s in starts], lag_ratio=0.2), run_time=0.7)
        self._own("starts", starts)
        # "Zero of thirty changed the test": each model's run from 10 down to 0, in turn.
        ctx.at(0.18)
        ctx.play(LaggedStart(*[AnimationGroup(Create(bar), FadeIn(end, scale=0.5))
                               for bar, end in zip(bars, ends)], lag_ratio=0.45), run_time=1.6)
        self._own("bars", VGroup(bars, ends))
        self._ends = ends

        # "Zero of thirty changed the test": the count, at the right.
        count = style.text_rows(style.caption_text(f"{data.changed('prose')} of 30"),
                                style.label_text("with the rule", color=prose_c))
        count.move_to([5.2, ys[0], 0])
        ctx.at(0.38)
        ctx.show(count, tag="count", run_time=0.5)

        # "The thirtieth left the split bug in place": sonnet-prose-9, tests kept, split against the README.
        wrong = [r for r in data.runs("prose") if r["outcome"] == "left the split wrong"]
        if len(wrong) == 1:
            row = data.MODELS.index(wrong[0]["model"])
            note = style.text_rows(style.label_text("1 run left", color=style.MUTED),
                                   style.label_text("the split wrong,", color=style.MUTED),
                                   style.label_text("reported it", color=style.MUTED))
            note.move_to([5.2, ys[row] - 0.3, 0]).align_to(count, LEFT)
            ctx.at(0.68)
            ctx.play(*style.highlight(ends[row], style.WHITE), FadeIn(note), run_time=0.6)
            self._own("note", note)

    # ------------------------------------------------------------- kept --
    def b_kept(self, ctx):
        ctx.retire("plot", "starts", "note", "count", run_time=0.3)
        marks, rows = self._rows(kept=True, xs=-1.9, ys=(0.75, -0.15, -1.05))
        # Each model's prose end becomes its ten kept runs.
        bars = self._owned.pop("bars")[0]
        ctx.play(*[ReplacementTransform(end, row) for end, row in zip(self._ends, rows)],
                 *[FadeOut(b) for b in bars], FadeIn(marks), run_time=0.9)
        self._own("kept", VGroup(rows, marks))
        page = self._owned["page"]
        kept = len(data.runs("prose")) - data.changed("prose")
        label = style.text_rows(style.caption_text(f"{kept} of 30"),
                                style.label_text("the model’s call", color=style.arm_color("prose")))
        label.move_to([4.7, -0.15, 0])
        ctx.at(0.3)
        ctx.play(page.animate.move_to([-5.4, -0.15, 0]), FadeIn(label), run_time=0.7)
        self._own("label", label)
