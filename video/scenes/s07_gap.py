"""
Section 07: closing the gap. The spine's third question; kept against changed, a bar of thirty per arm, filled arm by
arm until both, the shell hook and read-only stand at thirty of thirty; the strongest case against (widen the matcher)
on the lane diagram; how far it holds (the shell hook's list of write patterns, a sieve with a gap no run tried; which
lane needed guarding differs by model); and the limit, where the spellings multiply until the bar is a sandbox and
what is left is the lock on the folder and the page card in front of the model.

The bars' heights are the per-arm totals of results.json (edited the test, summed over the three models); the numbers
printed are the script's. The sieve's patterns are the shell hook's own (experiment/run.py, WRITES). The limit is an
illustration: its spellings are dashed, not data.
"""
from __future__ import annotations

from manim import *

import data
import style
from pipeline import stage
from pipeline.beats import Beat, BeatScene

ARMS = list(style.ARMS)          # none, prose, hook, both, hookstop, widehook, readonly
# The shell hook's write patterns as typed (run.WRITES: sed\s+-i, a redirect >, tee, cp, mv, open(... 'w')); one slot
# of the sieve is left open: the list can miss a spelling.
SIEVE = ("sed -i", "> file", "tee", "cp", None, "mv", "open(f, 'w')")
# Write spellings round the folder in the limit: an illustration of how many there are, not the hook's list.
SPELLINGS = ("sed -i", "tee", "cp", "mv", "> file", "dd of=", "perl -pi", "python3 -c", "git apply", "patch",
             "rsync", "ln -sf")


def bar_tiles(arm: str, x: float, base: float, unit: float, width: float) -> VGroup:
    """Kept (green, at the bottom) against changed (red, on top): one arm's thirty runs as a stacked bar."""
    out = VGroup()
    n_changed = data.changed(arm)
    n_kept = len(data.runs(arm)) - n_changed
    y = base
    for n, color in ((n_kept, style.KEPT), (n_changed, style.CHANGED)):
        if n:
            t = style.tile(width, n * unit, color, opacity=0.62).move_to([x, y, 0], aligned_edge=DOWN)
            out.add(t)
            y += n * unit
    return out


def chip(text: str, width: float, color: str) -> VGroup:
    """One write pattern of the sieve: its text in monospace inside a cell of the bar."""
    cell = style.card(width, 0.36, color, radius=0.05)
    words = style.mono_text(text, size="tiny").move_to(cell)
    return VGroup(cell, words)


def gap_cell(width: float, color: str) -> VGroup:
    """The slot the list leaves open: a dashed cell with nothing in it."""
    cell = RoundedRectangle(corner_radius=0.05, width=width, height=0.36, color=color)
    cell.set_fill(style.PANEL, opacity=0.96).set_stroke(width=0)
    edge = DashedVMobject(cell.copy().set_stroke(color, width=2.0), num_dashes=18)
    return VGroup(cell, edge)


class S07Gap(BeatScene):
    section_id = "07_closing_the_gap"
    title = "Closing the Gap"

    # The bars: seven columns, a run is UNIT high.
    XS = [-5.7 + 1.88 * i for i in range(7)]
    BASE, UNIT, BAR_W = -1.3, 0.093, 0.78
    # The lanes: the file tools above, the shell below, both into tests/ at the right.
    TOOL_Y, SHELL_Y, LANE_X0, LANE_X1, BAR_X = 1.45, -0.55, -3.7, 4.3, 1.6

    def storyboard(self) -> list[Beat]:
        return [
            Beat("What closes the gap, then", self.b_spine, kind="scorecard"),
            Beat("Prose and hook together", self.b_bars, kind="stacked"),
            Beat("A hook that also screens", self.b_shell, kind="~"),
            Beat("Read-only tests, with no", self.b_readonly, kind="~"),
            Beat("The strongest case against", self.b_counter, kind="diagram"),
            Beat("That is partly right", self.b_sieve, kind="~"),
            Beat("Push it to the limit", self.b_limit, kind="limit"),
        ]

    # -------------------------------------------------------------- 1 spine --
    def b_spine(self, ctx):
        ctx.waive("text_too_brief", "the spine's first two rows were read in section 06, where they stood for a "
                  "minute; here they return for the 3.8 s before the bars (the line before them was shortened)")
        rows = style.spine(lit=2, answers={0: "prose: 30 of 30", 1: "0 of 52"}, width=11.0)
        stage.fit(rows, stage.STAGE)
        ctx.play(FadeIn(rows[0]), FadeIn(rows[1]), run_time=0.3)
        self._owned["asked"] = VGroup(rows[0], rows[1])
        # The third row arrives, lit.
        ctx.at(0.3)
        ctx.play(FadeIn(rows[2], shift=UP * 0.25), run_time=0.6)
        self._owned["third"] = rows[2]
        ctx.at(0.65)
        ctx.play(rows[2][2].animate.set_stroke(style.WHITE, width=3.2), run_time=0.4)

    # --------------------------------------------------------------- 2 bars --
    def _bar(self, arm: str) -> VGroup:
        x = self.XS[ARMS.index(arm)]
        tiles = bar_tiles(arm, x, self.BASE, self.UNIT, self.BAR_W)
        word = style.label_text(style.arm_word(arm), style.arm_color(arm)).move_to([x, self.BASE - 0.38, 0])
        style.sit(word, self.BASE - 0.5)
        return VGroup(tiles, word)

    def _grow(self, bar: VGroup) -> list:
        return [GrowFromEdge(t, DOWN) for t in bar[0]] + [FadeIn(bar[1])]

    def _thirty(self, arm: str) -> Text:
        x = self.XS[ARMS.index(arm)]
        return style.label_text("30 of 30").move_to([x, self.BASE + 30 * self.UNIT + 0.3, 0])

    def b_bars(self, ctx):
        # The spine stays a moment into this line: its questions need four seconds to read.
        ctx.at(0.42)
        ctx.clear_stage(run_time=0.3)
        axis = Line([self.XS[0] - 0.7, self.BASE, 0], [self.XS[-1] + 0.7, self.BASE, 0], color=style.MUTED,
                    stroke_width=2.2).set_z_index(style.Z_BACKDROP)
        key = VGroup(*[VGroup(style.run_dot(k, radius=0.1), style.label_text(w, style.MUTED)).arrange(RIGHT, buff=0.16)
                       for k, w in ((True, "kept"), (False, "changed"))])
        key.arrange(RIGHT, buff=0.45).move_to([self.XS[0] - 0.4, 2.08, 0], aligned_edge=LEFT)
        first = [self._bar(a) for a in ("none", "prose", "hook", "hookstop")]
        ctx.play(Create(axis), FadeIn(key), *[a for b in first for a in self._grow(b)], run_time=1.0)
        self._owned["axis"] = VGroup(axis, key)
        for arm, b in zip(("none", "prose", "hook", "hookstop"), first):
            self._owned[arm] = b
        # Both together: all thirty kept.
        ctx.at(0.5)
        both = self._bar("both")
        ctx.play(*self._grow(both), run_time=0.7)
        self._owned["both"] = both
        ctx.at(0.72)
        mark = self._thirty("both")
        ctx.play(FadeIn(mark, shift=DOWN * 0.1), *style.highlight(both[0][0], style.KEPT), run_time=0.5)
        self._owned["both_mark"] = mark

    # ---------------------------------------------------------- 3 shell hook --
    def b_shell(self, ctx):
        bar = self._bar("widehook")
        ctx.play(*self._grow(bar), run_time=0.8)
        self._owned["widehook"] = bar
        ctx.at(0.3)
        mark = self._thirty("widehook")
        ctx.play(FadeIn(mark, shift=DOWN * 0.1), run_time=0.4)
        self._owned["widehook_mark"] = mark
        # "This one every model met": a refusal mark, a small bar in the arm's colour, beside each of its thirty runs.
        ctx.at(0.6)
        color = style.arm_color("widehook")
        x = self.XS[ARMS.index("widehook")] + self.BAR_W / 2 + 0.14
        marks = VGroup()
        for i in range(30):
            r = RoundedRectangle(corner_radius=0.02, width=0.05, height=0.2, color=color)
            r.set_fill(color, opacity=0.9).set_stroke(color, width=1)
            marks.add(r.move_to([x + 0.1 * (i % 3), self.BASE + 0.16 + 0.27 * (i // 3), 0]))
        word = style.label_text("refused", color, "tiny")
        style.sit(word.move_to([self.XS[ARMS.index("widehook")], 0, 0]), self.BASE - 0.92)
        ctx.play(LaggedStart(*[FadeIn(m, scale=0.5) for m in marks], lag_ratio=0.05), FadeIn(word), run_time=1.2)
        self._owned["refused"] = VGroup(marks, word)

    # ----------------------------------------------------------- 4 read-only --
    def b_readonly(self, ctx):
        bar = self._bar("readonly")
        ctx.play(*self._grow(bar), run_time=0.7)
        self._owned["readonly"] = bar
        ctx.at(0.35)
        lock = style.lock("readonly", size=0.42).move_to(bar[0][0].get_top() + DOWN * 0.45)
        mark = self._thirty("readonly")
        ctx.play(FadeIn(lock, scale=0.8), FadeIn(mark, shift=DOWN * 0.1), run_time=0.5)
        self._owned["readonly_mark"] = VGroup(lock, mark)

    # ------------------------------------------------------------- 5 counter --
    def _lanes(self) -> dict:
        """The lane diagram: models at the left, the two lanes, tests/ at the right."""
        length = self.LANE_X1 - self.LANE_X0
        mid = (self.LANE_X0 + self.LANE_X1) / 2
        tool = style.lane("Edit / Write", length=length).move_to([mid, self.TOOL_Y, 0], aligned_edge=DOWN)
        tool.shift(UP * (self.TOOL_Y - tool[0].get_center()[1]))
        shell = style.lane("shell", length=length)
        shell.shift(UP * (self.SHELL_Y - shell[0].get_center()[1]) + RIGHT * (mid - shell[0].get_center()[0]))
        tool.shift(RIGHT * (mid - tool[0].get_center()[0]))
        folder = style.folder(width=1.7, height=2.75)
        folder.move_to([self.LANE_X1 + 0.95, (self.TOOL_Y + self.SHELL_Y) / 2 - 0.08, 0])
        haiku = style.model_mark("Haiku").move_to([-5.45, self.TOOL_Y, 0])
        sonnet = style.model_mark("Sonnet").move_to([-5.45, self.SHELL_Y + 0.28, 0])
        opus = style.model_mark("Opus").move_to([-5.45, self.SHELL_Y - 0.3, 0])
        for m in (sonnet, opus):
            m.align_to(haiku, LEFT)
        hook = style.hook_bar("hook", height=0.85).move_to([self.BAR_X, self.TOOL_Y + 0.15, 0])
        hook.shift(UP * (self.TOOL_Y - hook[0].get_center()[1]))
        return dict(tool=tool, shell=shell, folder=folder, models=VGroup(haiku, sonnet, opus), hook=hook)

    def b_counter(self, ctx):
        ctx.clear_stage(run_time=0.4)
        d = self._lanes()
        ctx.play(FadeIn(d["tool"]), FadeIn(d["shell"]), FadeIn(d["folder"]), FadeIn(d["models"]), run_time=0.7)
        ctx.play(GrowFromEdge(d["hook"][0], DOWN), FadeIn(d["hook"][1]), run_time=0.4)
        for k, v in d.items():
            self._owned[k] = v
        self._d = d
        # The gap: a run in the shell lane goes past the hook into the folder.
        ctx.at(0.22)
        dot = style.run_dot(False, radius=0.11).move_to([self.LANE_X0 + 0.25, self.SHELL_Y, 0])
        ctx.play(FadeIn(dot, scale=0.5), run_time=0.3)
        ctx.play(dot.animate.move_to([self.LANE_X1 + 0.5, self.SHELL_Y, 0]), run_time=1.6, rate_func=linear)
        self._owned["gap_run"] = dot
        # "widen it": the hook's bar across the shell lane too.
        ctx.at(0.6)
        wide = style.hook_bar("widehook", height=0.85, label=False)
        wide.move_to([self.BAR_X, self.SHELL_Y, 0])
        ctx.play(FadeOut(dot), GrowFromEdge(wide[0], UP), run_time=0.7)
        self._owned.pop("gap_run")
        self._owned["wide"] = wide
        ctx.at(0.72)
        words = style.label_text("widen the matcher", style.arm_color("widehook"))
        words.move_to([self.BAR_X + 1.25, (self.TOOL_Y + self.SHELL_Y) / 2 - 0.05, 0])
        ctx.play(FadeIn(words, shift=UP * 0.1), run_time=0.5)
        self._owned["widen"] = words

    # --------------------------------------------------------------- 6 sieve --
    def b_sieve(self, ctx):
        color = style.arm_color("widehook")
        width = 1.75
        cells = VGroup(*[chip(p, width, color) if p else gap_cell(width, color) for p in SIEVE])
        cells.arrange(DOWN, buff=0.07).move_to([self.BAR_X, self.SHELL_Y, 0])
        # The bar becomes the sieve: it stretches to the sieve's height while the words leave.
        wide = self._owned.pop("wide")
        frame = RoundedRectangle(corner_radius=0.06, width=width + 0.16, height=cells.height + 0.16, color=color)
        frame.set_fill(style.PANEL, opacity=0.96).set_stroke(color, width=2.4).move_to(cells)
        ctx.retire("widen", run_time=0.3)
        ctx.play(ReplacementTransform(wide, frame), run_time=0.8)
        self._owned["frame"] = frame
        # The patterns, one cell at a time: "its list of write commands is a list".
        ctx.at(0.06)
        ctx.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.12) for c in cells], lag_ratio=0.35), run_time=2.6)
        self._owned["cells"] = cells
        # "and a list can miss one": the open slot.
        ctx.at(0.3)
        gap = cells[SIEVE.index(None)]
        ring = SurroundingRectangle(gap, color=style.WHITE, buff=0.035, corner_radius=0.07, stroke_width=3)
        ctx.play(Create(ring), run_time=0.6)
        self._owned["ring"] = ring
        # "no refused agent here tried another spelling": runs come down the shell lane and stop at the sieve.
        ctx.at(0.42)
        stop = frame.get_left()[0] - 0.2
        dots = VGroup(*[style.run_dot(True, radius=0.11).move_to([self.LANE_X0 + 0.25, self.SHELL_Y, 0])
                        for _ in range(3)])
        self.add(*dots)
        ctx.play(LaggedStart(*[d.animate.move_to([stop - 0.3 * i, self.SHELL_Y, 0]) for i, d in enumerate(dots)],
                             lag_ratio=0.3), run_time=1.8)
        self._owned["stopped"] = dots
        ctx.at(0.56)
        ctx.play(*style.highlight(frame, color), run_time=0.4)
        # "And which tool needed guarding changed from model to model."
        ctx.at(0.72)
        models = self._owned["models"]
        span = DoubleArrow([-6.42, self.TOOL_Y + 0.1, 0], [-6.42, self.SHELL_Y - 0.45, 0], color=style.MUTED,
                           stroke_width=2.4, buff=0, tip_length=0.16)
        words = style.label_text("differs by model", style.WHITE)
        words.move_to([0, self.SHELL_Y - 1.0, 0]).align_to(span, LEFT)
        ctx.play(GrowFromCenter(span), FadeIn(words, shift=UP * 0.1), run_time=0.6)
        self._owned["differs"] = VGroup(span, words)
        ctx.at(0.84)
        ctx.play(*[a for m in models for a in style.highlight(m[0], style.WHITE)], run_time=0.5)

    # --------------------------------------------------------------- 7 limit --
    def b_limit(self, ctx):
        ctx.clear_stage(run_time=0.4)
        center = np.array([1.9, 0.25, 0])
        agent = style.node("model", "agent", size=1.15).move_to([-5.1, 0.25, 0])
        folder = style.folder(width=1.7, height=1.2).move_to(center)
        ctx.play(FadeIn(agent), FadeIn(folder), run_time=0.5)
        self._owned["agent"], self._owned["folder"] = agent, folder
        # The spellings multiply round the folder: an illustration, so dashed underlines and grey type.
        rx, ry = 3.25, 1.72
        words = VGroup()
        for i, s in enumerate(SPELLINGS):
            a = PI / 2 + TAU * i / len(SPELLINGS)
            w = style.mono_text(s, color=style.MUTED, size="tiny")
            w.move_to(center + np.array([rx * np.cos(a), ry * np.sin(a), 0]))
            words.add(w)
        ctx.at(0.04)
        order = [0, 6, 3, 9, 1, 7, 4, 10, 2, 8, 5, 11]      # round the ring, top and bottom in turn
        ctx.play(LaggedStart(*[FadeIn(words[i], shift=(center - words[i].get_center()) * 0.08) for i in order],
                             lag_ratio=0.4), run_time=3.6)
        self._owned["spellings"] = words
        # Refusing one command: a small bar in front of each spelling, between it and the folder.
        color = style.arm_color("widehook")
        ctx.at(0.27)
        bars = VGroup()
        for w in words:
            v = (center - w.get_center())
            p = w.get_center() + v * 0.36
            b = RoundedRectangle(corner_radius=0.03, width=0.1, height=0.42, color=color)
            b.set_fill(color, opacity=0.85).set_stroke(color, width=1.5)
            b.rotate(np.arctan2(v[1], v[0])).move_to(p)
            bars.add(b)
        ctx.play(LaggedStart(*[GrowFromCenter(b) for b in bars], lag_ratio=0.15), run_time=1.6)
        # ... until the bars close into a box: a sandbox.
        ctx.at(0.45)
        box = RoundedRectangle(corner_radius=0.12, width=3.0, height=2.0, color=color).move_to(center)
        box.set_stroke(color, width=3)
        pieces = VGroup(*[box.get_subcurve(i / len(bars), (i + 1) / len(bars)) for i in range(len(bars))])
        ctx.play(*[ReplacementTransform(b, p) for b, p in zip(bars, pieces)], run_time=1.6)
        sandbox = style.label_text("sandbox", color).next_to(box, UP, buff=0.16)
        ctx.play(FadeIn(sandbox), run_time=0.4)
        self._owned["sandbox"] = VGroup(pieces, sandbox)
        # At the limit: the spellings and the box recede; the lock on the folder and the page card in front of the
        # model are what is left.
        ctx.at(0.66)
        ctx.recede("spellings", "sandbox", opacity=0.14, run_time=0.6)
        lock = style.lock("readonly", size=0.46).next_to(folder[0], RIGHT, buff=-0.3).align_to(folder[0], DOWN)
        lock.shift(DOWN * 0.18)
        card = style.page_card(width=1.5, height=1.8).move_to([-3.35, 0.25, 0])
        ctx.play(FadeIn(lock, scale=0.7), FadeIn(card, shift=LEFT * 0.15), run_time=0.7)
        self._owned["lock"], self._owned["card"] = lock, card
        ctx.at(0.8)
        effect = style.label_text("the effect", style.arm_color("readonly")).next_to(folder, DOWN, buff=0.42)
        wants = style.label_text("what it wants", style.arm_color("prose")).next_to(card, DOWN, buff=0.3)
        ctx.play(FadeIn(effect, shift=UP * 0.1), FadeIn(wants, shift=UP * 0.1), run_time=0.6)
        self._owned["left"] = VGroup(effect, wants)
