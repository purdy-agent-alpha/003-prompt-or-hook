"""
Section 08: the close. The spine answered row by row; back to the opening's page card and hook, the hook's bar sliding
from the tool lane onto the folder itself; what is still open, each "not tested", and 0 of 10 as an interval reaching
the rate the narration says; and the repository, with the scorer typed and its table reproduced.
"""
from __future__ import annotations

from manim import *

import style
from pipeline import stage
from pipeline.beats import Beat, BeatScene

REPO_URL = "https://github.com/purdy-agent-alpha/003-prompt-or-hook"
# The upper end of 0 of 10's 95% interval, as the narration says it (script.md, section 8, line 3: "about thirty
# percent"; the exact bound is 30.8%, Wilson's 27.8%).
UPPER = 30
# The rule as every arm gives it (experiment/README.md).
RULE = "Never modify anything under tests/."


def phrase(*parts: tuple[str, str]) -> VGroup:
    """Words in their own colours on one baseline, separated by grey middle dots."""
    out = VGroup()
    for i, (text, color) in enumerate(parts):
        if i:
            out.add(style.label_text("·", style.MUTED))
        out.add(style.label_text(text, color))
    out.arrange(RIGHT, buff=0.22)
    y = style.baseline(out[0])
    for t in out[2::2]:
        style.sit(t, y)
    for dot in out[1::2]:          # a middle dot sits at the words' middle, not on their baseline
        dot.set_y(y + style.label_text("x").height / 2)
    return out


def underline(mob: Mobject, color: str) -> Line:
    return Line(mob.get_corner(DL), mob.get_corner(DR), color=color, stroke_width=3.5).shift(DOWN * 0.13)


class S08Close(BeatScene):
    section_id = "08_close"
    title = "Close"

    def storyboard(self) -> list[Beat]:
        return [
            Beat("So, prompt or hook?", self.b_spine, kind="scorecard"),
            Beat("Back to the hook from", self.b_back, kind="side-by-side"),
            Beat("Still open: a task with", self.b_open, kind="ledger"),
            Beat("Everything is in the repository", self.b_repo, kind="repository"),
        ]

    # -------------------------------------------------------------- 1 spine --
    def b_spine(self, ctx):
        rows = style.spine(lit=None, width=12.4)
        rows.arrange(DOWN, buff=0.62, aligned_edge=LEFT)
        stage.fit(rows, stage.STAGE)
        ctx.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15), run_time=0.8)
        self._owned["spine"] = rows
        answers = (
            phrase(("two sentences: 30 of 30", style.arm_color("prose")), ("hook: where it fired",
                                                                           style.arm_color("hook"))),
            phrase(("0 of 52 went around", style.WHITE)),
            phrase(*[(style.arm_word(k), style.arm_color(k)) for k in ("both", "widehook", "readonly")]),
        )
        self._answers = answers
        for i, (row, answer, frac) in enumerate(zip(rows, answers, (0.08, 0.2, 0.32))):
            ctx.at(frac)
            slot = row[2]
            answer.move_to(slot).align_to(slot, RIGHT)
            dy = style.baseline(row[1]) - style.baseline(answer[0])
            answer.shift(UP * dy)
            row.remove(slot)           # out of its row, so fading it removes it from the stage
            self.add(slot)
            ctx.play(FadeOut(slot), FadeIn(answer, shift=LEFT * 0.15), run_time=0.6)
            self._owned[f"answer{i}"] = answer
        # "Write the rule down: here two sentences did nearly all the work."
        ctx.at(0.5)
        first = answers[0][0]
        line = underline(first, style.arm_color("prose"))
        ctx.play(Create(line), run_time=0.6)
        self._owned["u_prose"] = line
        # "Then enforce the effect, not a tool: the shell too, or the files themselves."
        ctx.at(0.74)
        lines = VGroup(underline(answers[2][2], style.arm_color("widehook")),
                       underline(answers[2][4], style.arm_color("readonly")))
        ctx.play(*[Create(l) for l in lines], run_time=0.6)
        self._owned["u_effect"] = lines

    # --------------------------------------------------------------- 2 back --
    def b_back(self, ctx):
        ctx.clear_stage(run_time=0.4)
        # The left: the rule, written down, in front of the model.
        card = style.page_card(width=1.7, height=2.15).move_to([-4.6, 0.45, 0])
        first, _, rest = RULE.partition(" under ")
        quote = style.text_rows(style.label_text(f"“{first}"), style.label_text(f"under {rest}”"), align=ORIGIN)
        quote.next_to(card, DOWN, buff=0.3)
        # The right: the two lanes into tests/, the hook on the tool lane.
        x0, x1, ty, sy = -1.6, 3.7, 1.0, -0.75
        length = x1 - x0
        tool = style.lane("Edit / Write", length=length)
        tool.shift([(x0 + x1) / 2 - tool[0].get_center()[0], ty - tool[0].get_center()[1], 0])
        shell = style.lane("shell", length=length)
        shell.shift([(x0 + x1) / 2 - shell[0].get_center()[0], sy - shell[0].get_center()[1], 0])
        folder = style.folder(width=1.55, height=2.6).move_to([x1 + 0.95, (ty + sy) / 2 - 0.1, 0])
        hook = style.hook_bar("hook", height=0.85)
        hook.shift([1.0 - hook[0].get_center()[0], ty - hook[0].get_center()[1], 0])
        ctx.play(FadeIn(card), FadeIn(quote), run_time=0.5)
        ctx.play(FadeIn(tool), FadeIn(shell), FadeIn(folder), GrowFromEdge(hook[0], DOWN), FadeIn(hook[1]),
                 run_time=0.6)
        for k, v in dict(card=card, quote=quote, tool=tool, shell=shell, folder=folder, hook=hook).items():
            self._owned[k] = v
        # "The hooks that failed here were never in the way": a run goes down the shell lane, past the hook, into
        # the folder, the hook never flashing.
        ctx.at(0.2)
        dot = style.run_dot(False, radius=0.11).move_to([x0 + 0.25, sy, 0])
        ctx.play(FadeIn(dot, scale=0.5), run_time=0.3)
        ctx.play(dot.animate.move_to([x1 + 0.45, sy, 0]), run_time=1.8, rate_func=linear)
        ctx.play(FadeOut(dot), run_time=0.3)
        # The answer, once the line has been spoken to its end (quality passes 1 and 2): the guard moves from the
        # tool onto the folder itself, across both lanes, and a run down the shell lane now meets it.
        run_time = ctx.after_line(0.4)
        bar = hook[0]
        target = bar.copy().stretch_to_fit_height(folder[0].height - 0.2)
        target.move_to([folder[0].get_left()[0] - 0.22, folder[0].get_center()[1], 0])
        word = hook[1].copy().next_to(target, DOWN, buff=0.12).align_to(target, RIGHT)
        ctx.play(Transform(bar, target), FadeOut(hook[1]), FadeIn(word), run_time=run_time)  # the word does not cross
        self._owned["hook_word"] = word
        run_time = ctx.at(0.0, 0.3)     # at once, in what is left of the window
        dot2 = style.run_dot(True, radius=0.11).move_to([target.get_left()[0] - 0.25, sy, 0])
        ctx.play(FadeIn(dot2, scale=0.5), *style.highlight(bar, style.arm_color("hook")), run_time=run_time)
        self._owned["met"] = dot2

    # --------------------------------------------------------------- 3 open --
    def b_open(self, ctx):
        ctx.lopsided("the ledger fills from the top, one open question as each is spoken; its first rows sit high "
                     "until the rest and the interval below them arrive")
        ctx.at(0.03)                   # the answer above holds a moment before the ledger replaces it
        ctx.clear_stage(run_time=0.4)
        questions = ("a task with no honest way out", "a deadline, or a reward for green tests",
                     "other vendors' agents", "an agent that really wants the write")
        rows = VGroup()
        for q in questions:
            band = style.tile(10.4, 0.52, style.GRID, opacity=0.3)
            text = style.label_text(q).move_to(band).align_to(band.get_left() + RIGHT * 0.35, LEFT)
            chip_text = style.label_text("not tested", style.MUTED)
            chip = RoundedRectangle(corner_radius=0.08, width=chip_text.width + 0.4, height=0.42,
                                    color=style.MUTED, stroke_width=2)
            chip_text.move_to(chip)
            VGroup(chip, chip_text).move_to(band).align_to(band.get_right() + LEFT * 0.25, RIGHT)
            rows.add(VGroup(band, text, VGroup(chip, chip_text)))
        rows.arrange(DOWN, buff=0.14).move_to([0, 0.5, 0])
        for i, (row, frac) in enumerate(zip(rows, (0.0, 0.12, 0.27, 0.38))):
            ctx.at(frac)
            ctx.play(FadeIn(row[0]), FadeIn(row[1], shift=RIGHT * 0.15), run_time=0.45)
            ctx.play(FadeIn(row[2], scale=0.9), run_time=0.3)
            self._owned[f"row{i}"] = row
        # "ten runs a cell can't rule out a rare failure": a rate's axis, 0 of 10 at zero.
        ctx.at(0.55)
        x0, x1, y = -2.6, 4.6, -1.75
        axis = Line([x0, y, 0], [x1, y, 0], color=style.MUTED, stroke_width=2.2).set_z_index(style.Z_BACKDROP)
        ends = VGroup(style.label_text("0%", style.MUTED, "tiny").next_to([x0, y, 0], DOWN, buff=0.2),
                      style.label_text("100%", style.MUTED, "tiny").next_to([x1, y, 0], DOWN, buff=0.2))
        title = style.label_text("true rate", style.MUTED, "tiny").next_to([x1, y, 0], UP, buff=0.2)
        title.align_to([x1, y, 0], RIGHT)
        count = style.label_text("0 of 10").next_to([x0, y, 0], LEFT, buff=0.55)
        point = [x0, y, 0]
        dot = Dot(point, radius=0.12, color=style.WHITE)
        ctx.play(Create(axis), FadeIn(ends), FadeIn(title), FadeIn(count), GrowFromCenter(dot), run_time=0.7)
        self._owned["axis"] = VGroup(axis, ends, title, count, dot)
        # "zero of ten fits a true rate up to about twenty-eight percent".
        ctx.at(0.74)
        hi = [x0 + (x1 - x0) * UPPER / 100, y, 0]
        span = style.interval(point, point, hi, style.WHITE)[0]
        cap = Line([hi[0], y - 0.16, 0], [hi[0], y + 0.16, 0], color=style.WHITE, stroke_width=4)
        upper = style.label_text(f"about {UPPER}%").next_to(cap, UP, buff=0.2)
        ctx.play(Create(span), run_time=1.0)
        ctx.play(Create(cap), FadeIn(upper, shift=DOWN * 0.1), run_time=0.5)
        self._owned["interval"] = VGroup(span, cap, upper)

    # --------------------------------------------------------------- 4 repo --
    def b_repo(self, ctx):
        ctx.clear_stage(run_time=0.4)
        url = style.mono_text(REPO_URL, size="label").move_to([0, 1.95, 0])
        term = style.tile(6.1, 2.4, style.MUTED, opacity=0.08).move_to([3.35, -0.55, 0])
        ctx.play(FadeIn(url, shift=DOWN * 0.1), FadeIn(term), run_time=0.6)
        self._owned["url"], self._owned["term"] = url, term
        # What is in it, as the narration lists it.
        tree = (("experiment/fixture/", "the library"), ("experiment/run.py", "the seven arms"),
                ("experiment/score.py", "the scorer"), ("experiment/runs/", "every transcript"),
                ("report/report.pdf", "the PDF"))
        files = VGroup()
        for i, (name, what) in enumerate(tree):
            y = 0.75 - 0.5 * i
            f = VGroup(style.mono_text(name).move_to([-6.3, y, 0], aligned_edge=LEFT),
                       style.label_text(what, style.MUTED).move_to([-6.3, y - 0.26, 0], aligned_edge=LEFT))
            files.add(f)
        for f in files:      # names on one pitch, their descriptions beside them
            f[1].next_to(f[0], RIGHT, buff=0.3)
            style.sit(f[1], style.baseline(f[0]))
        for i, (f, frac) in enumerate(zip(files, (0.06, 0.13, 0.2, 0.27, 0.34))):
            ctx.at(frac)
            ctx.play(FadeIn(f, shift=RIGHT * 0.15), run_time=0.4)
            self._owned[f"file{i}"] = f
        # "Rerun it and see if you get my numbers": the scorer, typed, and its table out again.
        ctx.at(0.45)
        cmd = VGroup(style.mono_text("$ cd experiment"), style.mono_text("$ python3 score.py 2026-11-22"))
        cmd.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        cmd.move_to(term).align_to(term.get_left() + RIGHT * 0.3, LEFT).shift(UP * 0.62)
        ctx.play(AddTextLetterByLetter(cmd[0]), run_time=0.6)
        ctx.play(AddTextLetterByLetter(cmd[1]), run_time=1.0)
        self._owned["cmd"] = cmd
        ctx.at(0.64)
        out = style.mono_text("| model | arm | n | kept | ...", color=style.MUTED)
        out.align_to(cmd, LEFT).set_y(cmd.get_bottom()[1] - 0.42)
        ok = VGroup(style.tick(style.GREEN, scale=1.15), style.mono_text("same as results.md", color=style.GREEN))
        ok.arrange(RIGHT, buff=0.25).align_to(cmd, LEFT).set_y(out.get_bottom()[1] - 0.45)
        ctx.play(FadeIn(out), run_time=0.4)
        ctx.play(Create(ok[0]), FadeIn(ok[1]), run_time=0.6)
        self._owned["ok"] = VGroup(out, ok)
        # "If you find a mistake, open an issue there": back to the address.
        ctx.at(0.84)
        under = underline(url, style.WHITE)
        ctx.play(Create(under), run_time=0.6)
        self._owned["under"] = under
