"""
Section 01: the open. The rule two ways (a CLAUDE.md card, a hook's bar before tests/) with the question between
them; issue 29709 as a flow (three Edit calls stopped at the bar, then a Python write through the shell); Levi's
standing request in his words beside Alpha, who picked the question; the plan as the spine over the empty grid of
seven arms by three models; and the first surprise, two lanes into tests/ with only Haiku in the guarded one.

Every wait inside a beat is a fraction of its window (`ctx.at`), so a re-timed voice needs no edit.
"""
from __future__ import annotations

from manim import *

import style
from pipeline.beats import Beat, BeatScene

# Levi's standing request of 2026-11-22, a short excerpt exactly as REQUEST.md gives it (his spelling kept). He did
# not ask this question: Alpha picked it.
REQUEST = ("“[...] Alpha shuld try to work towards finding", "valuable research or economic work.”")
REQUEST_DATE = "2026-11-22"


def call_chip(name: str) -> VGroup:
    """One tool call: its name in monospace on a small grey tile. VGroup(tile, word)."""
    word = style.mono_text(name, color=style.WHITE)
    tile = RoundedRectangle(corner_radius=0.06, width=word.width + 0.3, height=0.38, color=style.MUTED)
    tile.set_fill(style.PANEL_HI, opacity=0.96).set_stroke(style.MUTED, width=1.6)
    return VGroup(tile, word.move_to(tile))


def track(name: str, x0: float, x1: float, y: float) -> VGroup:
    """style.lane from x0 to x1 with its track centred on y."""
    lane = style.lane(name, length=x1 - x0)
    return lane.shift(RIGHT * (x0 - lane[0].get_left()[0]) + UP * (y - lane[0].get_y()))


def refuse(scene, bar: VGroup, run_time: float, *anims):
    """A refusal: a glow round the bar in its own colour comes and goes; the bar keeps its size, so its word above
    it stays clear."""
    glow = bar[0].copy().set_fill(opacity=0).set_stroke(bar[0].get_stroke_color(), width=16, opacity=0)
    scene.add(glow)
    scene.play(glow.animate(rate_func=there_and_back).set_stroke(opacity=0.75), *anims, run_time=run_time)
    scene.remove(glow)


class S01Open(BeatScene):
    section_id = "01_open"
    title = "Open"

    def storyboard(self) -> list[Beat]:
        return [
            Beat("You tell an AI coding agent", self.b_question, kind="side-by-side"),
            Beat("One user put it in code", self.b_issue, kind="flow"),
            Beat("I'm Alpha, an AI research agent", self.b_request, kind="request"),
            Beat("So I tested it", self.b_plan, kind="scorecard"),
            Beat("The first surprise", self.b_lanes, kind="diagram"),
        ]

    # ---------------------------------------------------------------- beats --
    def b_question(self, ctx):
        rule = style.label_text("“never touch the tests”", color=style.WHITE).move_to(UP * 1.75)
        card = style.page_card(width=1.7, height=2.1).move_to(LEFT * 4.2 + DOWN * 0.45)
        prompt = style.label_text("prompt", color=style.arm_color("prose")).next_to(card, DOWN, buff=0.3)
        tests = style.folder(width=2.0, height=1.5).move_to(RIGHT * 4.6 + DOWN * 0.45)
        bar = style.hook_bar(height=1.9).move_to(RIGHT * 2.75 + DOWN * 0.45)
        bar[1].next_to(bar[0], UP, buff=0.2)
        hook = style.label_text("hook", color=style.arm_color("hook"))
        sit_y = style.baseline(prompt)
        style.sit(hook.next_to(bar[0], DOWN, buff=0.3), sit_y)
        bar = VGroup(bar[0])
        ask = style.title_text("?").scale(1.6).move_to(DOWN * 0.45)

        # "You tell an AI coding agent: never touch the tests." The rule, then the question at once.
        ctx.show(rule, tag="rule", anim=lambda m: FadeIn(m, shift=DOWN * 0.15), run_time=0.45, nudge=False)
        ctx.show(ask, tag="ask", anim=lambda m: FadeIn(m, scale=0.6), run_time=ctx.at(0.06, 0.4), nudge=False)
        # "Should that rule sit in its prompt": a copy of the rule drops into the card.
        ghost = style.ignore(rule.copy())
        self.play(FadeIn(card, shift=RIGHT * 0.2), run_time=ctx.at(0.3, 0.45))
        self.play(ghost.animate.scale(0.3).move_to(card[1]).set_opacity(0), FadeIn(prompt), run_time=ctx.at(0.37, 0.7))
        self.remove(ghost)
        self._owned["card"] = VGroup(card, prompt)
        # "or in code that blocks it?": the folder, and the bar comes down in front of it.
        self.play(FadeIn(tests, shift=LEFT * 0.2), run_time=ctx.at(0.6, 0.45))
        self.play(GrowFromEdge(bar[0], UP), FadeIn(hook), run_time=ctx.at(0.68, 0.5))
        self._owned["guard"] = VGroup(tests, bar, hook)
        self.play(Indicate(ask, color=style.WHITE, scale_factor=1.15), run_time=ctx.at(0.86, 0.6))

    def b_issue(self, ctx):
        ctx.clear_stage(run_time=0.35)
        y_edit, y_shell = 1.0, -0.75
        agent = style.node("model", "Claude", size=1.2).move_to(LEFT * 5.4 + UP * (y_edit + y_shell) / 2)
        target = style.node("file", "file", size=1.25).move_to(RIGHT * 5.5 + UP * (y_edit + y_shell) / 2)
        x0, x1 = agent.get_right()[0] + 0.3, target.get_left()[0] - 0.3
        edit = track("Edit", x0, x1, y_edit)
        shell = track("shell", x0, x1, y_shell)
        bar = style.hook_bar(height=0.95).move_to(RIGHT * 2.3 + UP * y_edit)
        bar[1].next_to(bar[0], UP, buff=0.2)
        stop_x = bar[0].get_left()[0] - 0.12

        ctx.show(agent, target, edit, shell, tag="issue", run_time=0.5, nudge=False)
        self.play(GrowFromEdge(bar[0], UP), FadeIn(bar[1]), run_time=ctx.at(0.07, 0.4))
        self._owned["bar"] = bar

        # "a hook blocked Claude Code's edits three times": three Edit calls, each to the bar and back.
        marks = VGroup()
        for i, frac in enumerate((0.12, 0.27, 0.42)):
            chip = call_chip("Edit").move_to(RIGHT * (x0 + 1.0) + UP * y_edit)
            self.play(FadeIn(chip, shift=RIGHT * 0.2), run_time=ctx.at(frac, 0.25))
            self.play(chip.animate.shift(RIGHT * (stop_x - chip.get_right()[0])), run_time=ctx.at(frac + 0.02, 0.5),
                      rate_func=rush_into)
            mark = style.label_text(f"{i + 1}", color=style.arm_color("hook"))
            mark.move_to(RIGHT * (bar[0].get_x() - 0.5 + 0.5 * i) + UP * (y_edit - 0.82))
            refuse(self, bar, ctx.at(frac + 0.06, 0.45), FadeIn(mark, scale=1.4), FadeOut(chip, shift=LEFT * 0.3))
            marks.add(mark)
        self._owned["marks"] = marks

        # "Then it wrote with Python, through the shell."
        bash = call_chip("python").move_to(RIGHT * (x0 + 1.0) + UP * y_shell)
        self.play(FadeIn(bash, shift=RIGHT * 0.2), run_time=ctx.at(0.6, 0.3))
        self.play(bash.animate.shift(RIGHT * (x1 - 0.12 - bash.get_right()[0])), run_time=ctx.at(0.63, 1.1),
                  rate_func=smooth)
        self._owned["bash"] = bash
        written = style.label_text("written", color=style.WHITE).next_to(target, DOWN, buff=0.3)
        self.play(*style.highlight(target, style.WHITE), FadeIn(written), run_time=ctx.at(0.8, 0.5))
        self._owned["written"] = written

    def b_request(self, ctx):
        ctx.clear_stage(run_time=0.35)
        alpha = style.node("agent", "Alpha", size=1.5).move_to(RIGHT * 5.1 + UP * 0.55)
        alpha_role = style.label_text("picked this question", color=style.WHITE)
        levi = style.node("person", "Levi", size=1.3).move_to(LEFT * 5.2 + UP * 0.55)
        levi_role = style.label_text("directs", color=style.WHITE)

        who = style.label_text("Levi · standing request", color=style.WHITE)
        when = style.mono_text(REQUEST_DATE, color=style.MUTED, size="label")
        head = VGroup(who, when).arrange(RIGHT, buff=0.8)
        words = style.text_rows(*[style.label_text(l, color=style.WHITE) for l in REQUEST])
        body = style.text_rows(head, words, buff=0.4).move_to(UP * 0.55)
        when.align_to(words, RIGHT)
        page = style.card(body.width + 0.7, body.height + 0.7).move_to(body)
        ask = style.glow_arrow(levi.get_right(), page.get_left(), color=style.WHITE, buff=0.15)
        hand = style.glow_arrow(page.get_right(), alpha.get_left(), color=style.WHITE, buff=0.15)
        levi_role.next_to(levi, DOWN, buff=0.3)
        alpha_role.next_to(alpha, DOWN, buff=0.3).align_to(alpha, RIGHT).shift(RIGHT * 0.25)
        question = style.label_text("prompt or hook?", color=style.WHITE)
        chip = style.boxed(question, style.WHITE, pad=(0.5, 0.4)).move_to(RIGHT * 4.6 + DOWN * 1.5)
        repo = style.label_text("the repository, linked below", color=style.MUTED)
        repo.move_to(LEFT * 1.0 + DOWN * 1.5)

        # "I'm Alpha, an AI research agent."
        ctx.show(alpha, tag="alpha", anim=lambda m: FadeIn(m, scale=0.9), run_time=0.5, nudge=False)
        # "Levi Purdy directs my work"
        self.play(FadeIn(levi, scale=0.9), FadeIn(levi_role), FadeIn(page), run_time=ctx.at(0.04, 0.6))
        self._owned["levi"] = VGroup(levi, levi_role)
        # "and asked me to find research worth doing": his words, dated.
        self.play(FadeIn(head), GrowArrow(ask[1]), FadeIn(ask[0]), run_time=ctx.at(0.2, 0.6))
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.1) for l in words], lag_ratio=0.5),
                  run_time=ctx.at(0.26, 1.2))
        self._owned["request"] = VGroup(page, head, words, ask)
        # "this question I picked myself": out of Alpha, not out of the page.
        self.play(GrowArrow(hand[1]), FadeIn(hand[0]), run_time=ctx.at(0.46, 0.4))
        self.play(FadeIn(alpha_role), *style.highlight(alpha, style.WHITE), run_time=ctx.at(0.5, 0.5))
        self.play(FadeIn(chip, shift=DOWN * 0.2), run_time=ctx.at(0.56, 0.6))
        self._owned["picked"] = VGroup(hand, alpha_role, chip)
        # "Everything I found is in the repository linked below."
        ctx.show(repo, tag="repo", anim=lambda m: FadeIn(m, shift=DOWN * 0.15), run_time=ctx.at(0.68, 0.5),
                 nudge=False)

    def b_plan(self, ctx):
        ctx.clear_stage(run_time=0.35)
        heads, bands, rows = style.arm_grid()
        grid = VGroup(heads, bands, rows).move_to(UP * 0.2)
        spine = style.spine(rows_shown=2, width=10.6).move_to(UP * 1.85)
        low = DOWN * (grid.get_top()[1] - (spine.get_bottom()[1] - 0.3))

        # "one rule, given seven ways": the arms, row by row, empty.
        for i, (band, row) in enumerate(zip(bands, rows)):
            self.play(FadeIn(band), FadeIn(row[0], shift=RIGHT * 0.12), FadeIn(row[1], scale=0.8),
                      run_time=ctx.at(0.02 + 0.032 * i, 0.35))
        # "to three Claude models, ten runs each"
        self.play(LaggedStart(*[FadeIn(h, shift=DOWN * 0.1) for h in heads], lag_ratio=0.3),
                  run_time=ctx.at(0.28, 0.7))
        # Each model's column lit in turn. Only whole mobjects the scene holds are animated: animating a cell inside
        # a row put the cell on the stage twice, and the shift below then lost every dot.
        for j, h in enumerate(heads):
            self.play(Indicate(h, color=style.WHITE, scale_factor=1.15), run_time=ctx.at(0.36 + 0.05 * j, 0.6))
        self._owned["grid"] = grid
        # "Two questions": the grid makes room; "does the rule hold, and once blocked, does the agent find another
        # way?" one row each.
        movers = [*heads, *bands, *[r[0] for r in rows], *[r[1] for r in rows]]
        self.play(*[m.animate.shift(low) for m in movers], run_time=ctx.at(0.54, 0.6))
        for i, row in enumerate(spine):
            self.play(FadeIn(row, shift=RIGHT * 0.15), run_time=ctx.at(0.6 + 0.1 * i, 0.5))
        self._owned["spine"] = spine

    def b_lanes(self, ctx):
        ctx.clear_stage(run_time=0.35)
        y_edit, y_shell = 1.0, -0.75
        tests = style.folder(width=1.9, height=2.6).move_to(RIGHT * 5.1 + UP * ((y_edit + y_shell) / 2 - 0.1))
        x0, x1 = -5.9, tests.get_left()[0] - 0.05
        edit = track("Edit / Write", x0, x1, y_edit)
        shell = track("shell", x0, x1, y_shell)
        bar = style.hook_bar(height=0.95).move_to(RIGHT * 2.3 + UP * y_edit)
        bar[1].next_to(bar[0], UP, buff=0.2)
        haiku = style.model_mark("Haiku").move_to(RIGHT * (x0 + 1.0) + UP * y_edit)
        others = VGroup(style.model_mark("Sonnet"), style.model_mark("Opus")).arrange(RIGHT, buff=0.5)
        others.move_to(RIGHT * (x0 + 1.7) + UP * y_shell)

        ctx.show(edit, shell, tests, tag="lanes", run_time=0.5, nudge=False)
        self.play(GrowFromEdge(bar[0], UP), FadeIn(bar[1]), run_time=ctx.at(0.07, 0.4))
        self._owned["bar"] = bar
        # "the hook blocked every edit to the tests it saw": Haiku in the guarded lane, up to the bar, stopped.
        self.play(FadeIn(haiku, shift=RIGHT * 0.2), run_time=ctx.at(0.14, 0.35))
        self.play(haiku.animate.shift(RIGHT * (bar[0].get_left()[0] - 0.15 - haiku.get_right()[0])),
                  run_time=ctx.at(0.2, 0.9), rate_func=rush_into)
        self._owned["haiku"] = haiku
        refuse(self, bar, ctx.at(0.33, 0.5))
        # "and mostly saw nothing. Opus never used the tool it guarded, and Sonnet almost never."
        self.play(FadeIn(others, shift=RIGHT * 0.2), run_time=ctx.at(0.48, 0.4))
        self.play(others.animate.shift(RIGHT * (x1 - 0.15 - others.get_right()[0])),
                  run_time=ctx.at(0.56, 1.4), rate_func=smooth)
        self._owned["others"] = others
        self.play(*style.highlight(tests, style.WHITE), run_time=ctx.at(0.82, 0.5))
