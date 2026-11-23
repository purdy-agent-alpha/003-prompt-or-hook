"""
Visual system for episode 003, "A rule an agent must never break: prompt or hook?". This docstring is the frame
review's rubric (pipeline/gemini_review.py reads it). One source of truth for palette, type scale and shape grammar:
scenes never hardcode a colour or a font size; they ask for a role, an arm or a kind.

The palette is Levi's video 2's. The grammar, for this episode (a shape and its colour mean one thing for the whole
video; emphasis brightens a shape in its own colour, never turns it into another kind):

    tests/      folder card (a tab on a rounded rectangle), white stroke, the word "tests/" in monospace; the bad
                line of the test, [333, 333, 333], is set in the monospace face and lit gold wherever it appears
    run         one dot per run of the agent: filled green when the test was kept, red when it was changed;
                never any other meaning
    lane        a route to the files: a grey track with its name, "Edit / Write" (the file-editing tools) or
                "shell"; a run that reaches the folder moves along its lane
    guard       drawn where it acts, in its ARM's colour:
                    the prose rule    a page card (CLAUDE.md) in front of the model
                    a hook            a bar across the lane it watches; a refusal flashes the bar
                    read-only         a lock on the folder itself
    arm         one colour per way the rule was given, the same in every figure (label, bar, card, dot ring)
                    no rule       grey          prose         blue
                    hook          violet        both          pale blue
                    stop message  pink          shell hook    cyan
                    read-only     lime
    model       white hexagon with the model's short name (Haiku, Sonnet, Opus); in a tight row or key, a small
                hexagon with the name beside it (model_mark)
    person      white circle (Levi, who directs); Alpha, the narrator, a white diamond
    spine       the episode's scorecard: three questions, one row each, filled in as the video answers them
                (spine() below); the row being asked is lit white, the others grey

Charts take the shape of their data (pipeline/charts.py): counts are runs out of ten or thirty, drawn as dots you
can count (a unit chart) or as stacked bars of kept and changed; before and after is a dumbbell; a flow of runs
is a sankey. A share from another study is drawn in grey and labelled with its source. A guide, a projection or
an illustration is dashed.

Claim kinds (rule 3.3), on a chip in the caption lane with the source:
    measured  green   counted by the scorer from the saved runs, or read from a run's transcript
    reported  grey    what a published study, page or issue says
    argued    grey    a reading of the data
    guess     amber   my inference, no measurement behind it
    levi      white   Levi's own words
Red is reserved for a changed test and for what was dropped: a red dot, a struck claim.
"""
from __future__ import annotations

from manim import *

# ---------------------------------------------------------------- palette ---
BG = "#00020A"
PANEL = "#070C1A"
PANEL_HI = "#0C1426"
GRID = "#1F2B42"
WHITE = "#F4F7FF"
MUTED = "#8791A8"
DIM = "#4A5468"

CYAN = "#20F7D2"
BLUE = "#4D8DFF"
VIOLET = "#B45CFF"
GOLD = "#FFCB4D"
RED = "#FF4D6D"
GREEN = "#49F28D"
AMBER = "#FF9E45"
PINK = "#FF7AD9"
PALE_BLUE = "#A9C8FF"
PALE_CYAN = "#9DFBEA"
LIME = "#C8F04A"

# Shape grammar: the contract the storyboard promises the viewer.
NODE_KINDS = {
    "model": {"color": WHITE, "shape": "hexagon"},
    "person": {"color": WHITE, "shape": "circle"},
    "agent": {"color": WHITE, "shape": "diamond"},
    "file": {"color": WHITE, "shape": "document"},
    "step": {"color": MUTED, "shape": "record"},
}

# The seven arms, in the order every figure lists them, with the word shown on screen.
ARMS = {
    "none": (MUTED, "no rule"),
    "prose": (BLUE, "prose"),
    "hook": (VIOLET, "hook"),
    "both": (PALE_BLUE, "both"),
    "hookstop": (PINK, "stop message"),
    "widehook": (CYAN, "shell hook"),
    "readonly": (LIME, "read-only"),
}
MODELS = ("Haiku", "Sonnet", "Opus")
KEPT = GREEN    # a run that left the test as it was
CHANGED = RED   # a run that changed the test
FACT = GOLD     # the bad line of the test, wherever it appears
BAD_LINE = "[333, 333, 333]"
FIXED_LINE = "[334, 333, 333]"

CLAIM_KINDS = {
    "measured": GREEN,
    "reported": MUTED,
    "argued": MUTED,
    "guess": AMBER,
    "levi": WHITE,
}

# ------------------------------------------------------------- type scale ---
# Sizes are in Manim font_size units, tuned so the smallest is still legible
# after a 480p preview downscale. QA enforces MIN_FONT_SIZE.
TYPE = {
    "title": 40,
    "caption": 28,
    "label": 22,
    "node": 17,
    "field": 17,
    # 17, not 16. Pango's space advance rounds down a whole pixel below 17pt, so
    # every multi-word label set at 16 rendered with a ~3.5px word gap at review
    # size and read as one word — "makes an" as "makesan". At 17 the same phrases
    # come out at 6px. One point of type size, and a whole class of defect.
    "tiny": 17,
}
MIN_FONT_SIZE = 15
MONO = "DejaVu Sans Mono"

# Texts need air between them, not merely an absence of overlap. Below this gap
# two lines read as one block. Both the placement helper and the gate use this
# number, so a layout that satisfies the placer cannot fail the gate.
MIN_TEXT_GAP = 0.16

# The placer aims for MIN_TEXT_GAP + this, never for MIN_TEXT_GAP itself. Aiming
# exactly at a threshold lands on the wrong side of it about half the time once
# floating point is involved: the first version placed three labels at a
# computed 0.16 and the gate read all three back as 0.15999 and failed them.
PLACEMENT_MARGIN = 0.03

# ----------------------------------------------------------- draw layers ---
# Manim's renderer flattens the whole scene and sorts it by ``z_index`` with a
# *stable* sort, so a z_index is the only way to state a layering rule that
# holds across group boundaries. Sibling reordering cannot: an edge living
# inside a `chain` VGroup will always draw over a node that sits in a different
# top-level group, however carefully the two groups sort their own children.
# That is exactly the bug that put connectors on top of the code node for 23
# seconds in section 1.
#
# Lower draws earlier, i.e. further back.
Z_BACKDROP = -20   # zone bands, grids, anything content sits on top of
Z_EDGE = -10       # connectors: never in front of what they join
Z_NODE = 0         # shapes, cards, labels — the default
Z_SLATE = 50       # the review identifier, above everything


def _word_metrics(t: Text, source: str) -> tuple[float, float]:
    """
    (smallest gap between words, median gap between letters) — in scene units.

    Counting glyphs to find the word boundaries is the obvious approach and it is
    wrong: Pango ligates some pairs, so "verification" renders as eleven glyphs
    for twelve characters and every boundary after it is off by one. That made
    the check measure the gap between two letters and report the phrase as
    merged when it was fine.

    So don't rely on the mapping. There are exactly as many word gaps as there
    are spaces, and a word gap is normally wider than a letter gap — so take the
    N widest gaps as the word gaps. The estimate can only be too generous, which
    makes the check conservative: it under-reports rather than inventing faults.
    """
    import numpy as _np
    glyphs = [g for g in t.submobjects if len(g.get_all_points())]
    n_spaces = source.count(" ")
    if len(glyphs) < 2 or n_spaces == 0:
        return (99.0, 0.0)
    gaps = sorted(
        (glyphs[i + 1].get_left()[0] - glyphs[i].get_right()[0]
         for i in range(len(glyphs) - 1)), reverse=True)
    n = min(n_spaces, len(gaps))
    return (float(gaps[n - 1]), float(_np.median(gaps[n:])) if len(gaps) > n else 0.0)


def _stamp(t: Text, source: str | None = None) -> Text:
    """
    Remember how big this text was built, and how big its geometry was then.

    Manim computes ``Text.font_size`` from the mobject's height, which a 3D
    scene's upright rotation drives to zero. The pair recorded here lets QA
    recover the rendered size from the point cloud instead, which rotation
    cannot disturb and scaling still moves.
    """
    import numpy as _np
    pts = t.get_all_points()
    t.qa_pt0 = float(t.font_size)
    t.qa_diag0 = (float(_np.linalg.norm(pts.max(axis=0) - pts.min(axis=0)))
                  if len(pts) else 0.0)
    t.qa_word_gap0, t.qa_letter_gap0 = _word_metrics(t, source if source is not None else "")
    return t


def title_text(text: str) -> Text:
    return _stamp(Text(text, color=WHITE, font_size=TYPE["title"], weight=BOLD), text)


def caption_text(text: str, color: str = WHITE) -> Text:
    return _stamp(Text(text, color=color, font_size=TYPE["caption"], weight=MEDIUM), text)


def label_text(text: str, color: str = WHITE, size: str = "label") -> Text:
    return _stamp(Text(text, color=color, font_size=TYPE[size]), text)


def mono_text(text: str, color: str = WHITE, size: str = "field") -> Text:
    return _stamp(Text(text, font=MONO, color=color, font_size=TYPE[size]), text)


# ----------------------------------------------------------------- shapes ---
def _base_shape(kind: str, color: str, size: float) -> VMobject:
    shape_name = NODE_KINDS.get(kind, {}).get("shape", "record")
    if shape_name == "hexagon":
        shape = RegularPolygon(n=6, radius=size / 2, color=color)
    elif shape_name == "square":
        shape = Square(side_length=size, color=color)
    elif shape_name == "dashed_square":
        # A clone has the product's outline and none of its body: no fill, and a
        # dashed stroke. Returned early so the panel fill below never lands on it.
        return DashedVMobject(Square(side_length=size, color=color).set_stroke(color, width=2.6),
                              num_dashes=24)
    elif shape_name == "circle":
        shape = Circle(radius=size / 2, color=color)
    elif shape_name == "diamond":
        shape = Square(side_length=size * 0.8, color=color).rotate(PI / 4)
    elif shape_name == "document":
        shape = RoundedRectangle(corner_radius=0.05, width=size * 0.86, height=size * 1.1, color=color)
    else:
        shape = RoundedRectangle(corner_radius=0.07, width=size * 1.3, height=size * 0.8, color=color)
    # Filled in its own colour at 0.18 over an opaque panel: outlines alone on a
    # dark ground read as confetti (video 2, HANDOFF.md section 4).
    shape.set_fill(interpolate_color(ManimColor(PANEL), ManimColor(color), 0.18), opacity=0.96)
    shape.set_stroke(color, width=2.6)
    return shape


def node(kind: str, text: str = "", size: float = 1.0, color: str | None = None,
         font_size: int | None = None) -> VGroup:
    """
    An artifact node. Returns VGroup(aura, shape, label) — always that order, so
    highlight helpers can stroke the shape without mangling the label.

    The label is auto-fitted inside the shape; a label that cannot fit at the
    minimum legible size raises, rather than silently overflowing.
    """
    if kind not in NODE_KINDS:
        # A misspelt or foreign kind used to fall back to a white record without a
        # word, which is how the selftest's video-2 kinds silently stopped one check.
        raise ValueError(f"node kind {kind!r} is not in this video's grammar: {sorted(NODE_KINDS)}")
    color = color or NODE_KINDS[kind]["color"]
    shape = _base_shape(kind, color, size)
    aura = shape.copy().set_stroke(color, width=9, opacity=0.12).set_fill(opacity=0)
    group = VGroup(aura, shape)
    group.qa_role = "node"
    group.qa_kind = kind
    if text:
        fs = font_size or TYPE["node"]
        label = _stamp(Text(text, color=WHITE, font_size=fs, weight=MEDIUM), text)
        inner = shape.width * 0.78
        if label.width > inner:
            scale = inner / label.width
            if fs * scale < MIN_FONT_SIZE:
                raise ValueError(
                    f"node({kind!r}, {text!r}) cannot fit its label at >= "
                    f"{MIN_FONT_SIZE}pt inside size={size}. Shorten the label or grow the node."
                )
            label.scale(scale)
        label.move_to(shape)
        label.qa_role = "label"
        group.qa_label = label
        group.add(label)
    return group


def highlight(n: Mobject, color: str = GOLD):
    """
    Animations that light a mobject without touching any text inside it.

    Nodes made by `node()` are VGroup(aura, shape, label) and get the aura
    treatment; anything else — a plain rectangle, a packet outline — just gets a
    heavier stroke. Assuming the node shape and indexing blindly turned every
    highlight on a plain shape into a render-time crash.
    """
    if getattr(n, "qa_role", None) == "node" and len(n.submobjects) >= 2:
        return [
            n[0].animate.set_stroke(color, width=13, opacity=0.6),
            n[1].animate.set_stroke(color, width=4),
        ]
    # Never stroke text. `set_stroke` on a group reaches the glyphs too, and a
    # 5-wide stroke on a letterform closes up its counters — the text goes bold,
    # muddy and harder to read, which is the opposite of highlighting it.
    targets = [s for s in n.get_family()
               if not _is_text_like(s) and len(getattr(s, "points", []))]
    if not targets:
        return [n.animate.set_color(color)]
    return [s.animate.set_stroke(color, width=5) for s in targets]


def _is_text_like(mob: Mobject) -> bool:
    if getattr(mob, "text", None) is not None:
        return True
    parent_text = getattr(mob, "qa_role", None) == "label"
    return parent_text or type(mob).__name__.startswith("VMobjectFromSVGPath")


def glow_arrow(start, end, color: str = CYAN, width: float = 3.4, buff: float = 0.16,
               tip: float | None = None) -> VGroup:
    # Manim thins a short arrow's stroke to a share of its length; no cap, so one width draws at one weight
    # (the quality pass of 2026-11-20 found 05 b09's two arrows at different weights). It shrinks the head the same
    # way: `tip` fixes the head's length too, for arrows side by side (05 b09, quality pass 2, 2026-11-21).
    heads = dict(tip_length=tip, max_tip_length_to_length_ratio=1000) if tip else {}
    aura = Arrow(start, end, color=color, stroke_width=width * 2.6, buff=buff,
                 max_stroke_width_to_length_ratio=1000, **heads).set_opacity(0.16)
    core = Arrow(start, end, color=color, stroke_width=width, buff=buff, max_stroke_width_to_length_ratio=1000,
                 **heads)
    group = VGroup(aura, core)
    # Tag only the stroke that actually has points. The wrapping VGroup has none,
    # and asking it for an endpoint raises.
    core.qa_role = "edge"
    group.qa_layer = "edge"      # the stage sends these to the back on show
    # Belt and braces: the back-seating below is a scene-order fix, this is a
    # renderer-order fix, and only the second one survives being re-parented
    # into somebody else's VGroup.
    group.set_z_index(Z_EDGE, family=True)
    return group


def connect(a: Mobject, b: Mobject, color: str = CYAN, width: float = 3.4) -> VGroup:
    """
    Arrow between two mobjects, anchored on the line between their centres so the
    head always lands on the boundary it is pointing at — never inside the label.
    """
    start = a.get_center()
    end = b.get_center()
    direction = end - start
    norm = np.linalg.norm(direction)
    if norm < 1e-6:
        raise ValueError("connect() needs two mobjects at different positions")
    unit = direction / norm
    return glow_arrow(
        a.get_boundary_point(unit) + unit * 0.06,
        b.get_boundary_point(-unit) - unit * 0.06,
        color=color, width=width, buff=0.0,
    )


def text_rows(*mobs: Mobject, buff: float | None = None, align=LEFT) -> VGroup:
    """
    Stack label rows with a gap the crowding check will accept.

    Writing `arrange(DOWN, buff=MIN_TEXT_GAP)` looks exactly right and fails:
    the rows land at precisely the threshold, and the gate reads the same
    distance back as 0.15999. Rows built through here clear the bar instead of
    balancing on it.
    """
    if buff is None:
        buff = MIN_TEXT_GAP + PLACEMENT_MARGIN
    return VGroup(*mobs).arrange(DOWN, buff=buff, aligned_edge=align)


def cursor_for(mob: Mobject, color: str = GOLD, width: float = 4.0,
               pad: float = 0.22) -> Circle:
    """
    A ring that actually goes round the thing it marks.

    A fixed-radius circle marks a one-word node and cuts straight through a
    longer one — "traversal" spent fifteen seconds with a gold line through the
    middle of it. Size the ring from the node, not from a constant.
    """
    r = max(mob.width, mob.height) / 2 + pad
    ring = Circle(radius=r, color=color, stroke_width=width)
    ring.move_to(mob.get_center())
    return ring


def allow_overlap(mob: Mobject, *others: Mobject, reason: str = ""):
    """
    Declare that `mob` is *meant* to sit over `others`.

    A stamp landing across a quote is a deliberate composition, not a layout bug.
    Declaring it keeps the overlap checker strict everywhere else instead of
    forcing the tolerance up globally, which is how these checks stop working.
    """
    def texts(m):
        return [str(getattr(s, "text", "")) for s in m.get_family()
                if getattr(s, "text", None)]

    mine = texts(mob)
    theirs = [t for o in others for t in texts(o)]
    for sub in mob.get_family():
        if getattr(sub, "text", None):
            sub.qa_allow_overlap = theirs
            sub.qa_allow_reason = reason
    for o in others:
        for sub in o.get_family():
            if getattr(sub, "text", None):
                sub.qa_allow_overlap = mine
                sub.qa_allow_reason = reason
    return mob


def strip_labels(*nodes: Mobject) -> None:
    """
    Remove the text from nodes, immediately and permanently.

    Deliberately not an animation. Two reasons, both learned the hard way:

    * `FadeOut` on a label is a no-op that then *restores* the opacity, because
      the label is a submobject the scene does not hold directly.
    * Returning `.animate` chains puts two animations on one family; the group's
      own `.animate.scale(...)` captured its target before the opacity changed,
      so it faithfully restored every label it was supposed to remove.

    Call this immediately before the play that moves or scales the node, so the
    text goes as the shape transforms. A label evaporating off a shape that then
    sits still reads as a rendering glitch — and the QA gate will say so.
    """
    for node in nodes:
        for sub in node.get_family():
            if getattr(sub, "text", None):
                sub.set_opacity(0)


def restroke(mob: Mobject, color: str, width: float = 3.0):
    """
    Change a mobject's stroke without touching any text inside it.

    `mob.animate.set_stroke(...)` reaches every submobject, so calling it on a
    node group strokes the label as well and thickens the letterforms until they
    are hard to read. Use this anywhere a group might contain text.
    """
    targets = [s for s in mob.get_family()
               if not _is_text_like(s) and len(getattr(s, "points", []))]
    if not targets:
        return [mob.animate.set_color(color)]
    return [s.animate.set_stroke(color, width=width) for s in targets]


# ------------------------------------------------------------ this video ---
def claim_footer(kind: str, source: str = "") -> VGroup:
    """
    A dot in the claim kind's colour, then one line: the kind word in that
    colour, a middle dot, the short source name in grey.

    One Text, not a chip plus a label: the caption lane holds one thing at a
    time (the gate's caption_stack). No pill round the word: any outline round
    part of a Text runs through the Text's box (outline_over_text). Set at the
    caption size: at 17 and 22 the word gaps of a source name merged.
    """
    color = CLAIM_KINDS[kind]
    word = "Levi's view" if kind == "levi" else kind
    # Single spaces only: the gate finds word gaps by counting spaces.
    text = f"{word} · {source}" if source else word
    line = _stamp(Text(text, color=MUTED, font_size=TYPE["caption"]), text)
    VGroup(*line[:len(word.replace(" ", ""))]).set_color(color if kind in ("measured", "guess") else WHITE)
    dot = RoundedRectangle(corner_radius=0.06, width=0.24, height=0.24)
    dot.set_fill(color, opacity=1.0).set_stroke(width=0)
    return VGroup(dot, line).arrange(RIGHT, buff=0.22)


def tile(width: float, height: float, color: str, opacity: float = 0.18) -> Rectangle:
    """A bar or panel filled in its own colour, never a bare outline."""
    r = Rectangle(width=width, height=height, color=color)
    r.set_fill(color, opacity=opacity).set_stroke(color, width=2.2)
    return r


def strike(mob: Mobject, color: str = RED, width: float = 5.0) -> Line:
    """A red line through a moat that dies. The shape stays what it was."""
    line = Line(mob.get_corner(DL) + LEFT * 0.08, mob.get_corner(UR) + RIGHT * 0.08,
                color=color, stroke_width=width)
    return line


# ------------------------------------------------------------- episode 003 ---
def arm_color(key: str) -> str:
    return ARMS[key][0]


def arm_word(key: str) -> str:
    return ARMS[key][1]


def fact_text(text: str = BAD_LINE, size: str = "field") -> Text:
    """The bad line of the test (or what it became): monospace, gold, wherever it appears."""
    return mono_text(text, color=FACT, size=size)


def baseline(t: Text) -> float:
    """Where a line of text sits: the median of its glyphs' bottoms, which descenders (p, g, y) do not move.
    Centring words by their boxes makes a row of them jitter by their descenders (quality pass, 2026-11-20)."""
    import numpy as _np
    return float(_np.median([g.get_bottom()[1] for g in t.submobjects if len(g.get_all_points())]))


def sit(t: Text, y: float) -> Text:
    """Move a text up or down so its baseline is at y."""
    return t.shift(UP * (y - baseline(t)))


def page_card(title: str = "CLAUDE.md", width: float = 1.5, height: float = 1.9, rules: int = 5,
              color: str | None = None) -> VGroup:
    """The prose rule's file: a portrait card tinted blue, ruled lines inside, its file name in monospace above the
    lines. VGroup(card, lines, name)."""
    color = color or arm_color("prose")
    card = RoundedRectangle(corner_radius=0.08, width=width, height=height, color=color)
    card.set_fill(interpolate_color(ManimColor(PANEL), ManimColor(color), 0.18), opacity=0.96)
    card.set_stroke(color, width=2.6)
    name = mono_text(title, color=color, size="tiny")
    if name.width > width * 0.86:
        name.scale_to_fit_width(width * 0.86)
    name.next_to(card.get_top(), DOWN, buff=0.16)
    top = name.get_bottom()[1] - 0.16
    gap = (top - card.get_bottom()[1]) / (rules + 1)
    lines = VGroup(*[Line(LEFT * width * 0.32, RIGHT * width * (0.32 if i % 3 else 0.12), color=color,
                          stroke_width=2, stroke_opacity=0.55)
                     .move_to([card.get_center()[0], top - gap * (i + 1), 0])
                     .align_to(card.get_left() + RIGHT * width * 0.18, LEFT)
                     for i in range(rules)])
    return VGroup(card, lines, name)


def folder(name: str = "tests/", width: float = 1.9, height: float = 1.3, color: str = WHITE) -> VGroup:
    """The tests: a folder card (a tab on a rounded body) with its name in monospace. VGroup(body, tab, name)."""
    body = RoundedRectangle(corner_radius=0.08, width=width, height=height, color=color)
    body.set_fill(PANEL_HI, opacity=0.96).set_stroke(color, width=2.6)
    tab = RoundedRectangle(corner_radius=0.05, width=width * 0.42, height=0.22, color=color)
    tab.set_fill(PANEL_HI, opacity=0.96).set_stroke(color, width=2.6)
    tab.next_to(body, UP, buff=-0.05).align_to(body, LEFT)
    word = mono_text(name, color=color, size="label")
    word.move_to(body)
    group = VGroup(body, tab, word)
    group.qa_role = "node"
    return group


def hook_bar(key: str = "hook", height: float = 1.0, label: bool = True) -> VGroup:
    """A hook: a bar across the lane it watches, in its arm's colour, with the word "hook" above it. VGroup(bar[,
    word]). A refusal flashes the bar (highlight it), never changes its colour."""
    color = arm_color(key)
    bar = RoundedRectangle(corner_radius=0.05, width=0.16, height=height, color=color)
    bar.set_fill(color, opacity=0.85).set_stroke(color, width=2.0)
    group = VGroup(bar)
    if label:
        word = label_text("hook", color=color, size="tiny")
        word.next_to(bar, UP, buff=0.12)
        group.add(word)
    return group


def lock(key: str = "readonly", size: float = 0.5) -> VGroup:
    """Read-only on disk: a padlock (a shackle arc over a body) in the read-only arm's colour. VGroup(shackle,
    body)."""
    color = arm_color(key)
    body = RoundedRectangle(corner_radius=0.05, width=size, height=size * 0.78, color=color)
    body.set_fill(interpolate_color(ManimColor(PANEL), ManimColor(color), 0.35), opacity=0.96)
    body.set_stroke(color, width=2.6)
    shackle = Arc(radius=size * 0.3, start_angle=0, angle=PI, color=color, stroke_width=4)
    shackle.next_to(body, UP, buff=-0.02)
    return VGroup(shackle, body)


def lane(name: str, length: float = 6.0, color: str = MUTED) -> VGroup:
    """A route to the files: a grey track with its name at the left end, above it, at the label size (at the tiny
    size the gate read "Edit / Write" as one word). VGroup(track, word)."""
    track = card(length, 0.5, color, radius=0.12).set_stroke(width=1.8).set_z_index(Z_BACKDROP)
    word = label_text(name, color=color)
    word.next_to(track, UP, buff=0.12).align_to(track, LEFT).shift(RIGHT * 0.12)
    return VGroup(track, word)


def card(width: float, height: float, color: str = MUTED, radius: float = 0.1, dashed: bool = False) -> VMobject:
    """A page, step or panel filled in its own colour over the panel, never a bare outline; dashed, unfilled, when
    it is a gap, not a thing."""
    box = RoundedRectangle(corner_radius=radius, width=width, height=height, color=color)
    if dashed:
        return DashedVMobject(box.set_stroke(color, width=2.2), num_dashes=44)
    box.set_fill(interpolate_color(ManimColor(PANEL), ManimColor(color), 0.14), opacity=0.96)
    return box.set_stroke(color, width=2.2)


def band(width: float, height: float) -> RoundedRectangle:
    """A table's row behind its marks: faint, on the backdrop, so an empty table reads as one to fill."""
    row = RoundedRectangle(corner_radius=0.08, width=width, height=height, color=GRID)
    return row.set_fill(PANEL_HI, opacity=0.9).set_stroke(GRID, width=1.4).set_z_index(Z_BACKDROP)


def boxed(words: Mobject, color: str = MUTED, pad: tuple[float, float] = (0.5, 0.36)) -> VGroup:
    """Words centred on a card in their colour. VGroup(card, words)."""
    box = card(words.width + pad[0], words.height + pad[1], color)
    return VGroup(box, words.move_to(box))


def tick(color: str = WHITE, scale: float = 1.0, width: float = 5.0) -> VMobject:
    """A check mark: a kept item, a source that measured it, a table that matches."""
    return VMobject(color=color, stroke_width=width).set_points_as_corners(
        [LEFT * 0.16 + UP * 0.02, DOWN * 0.13 + LEFT * 0.03, RIGHT * 0.19 + UP * 0.18]).scale(scale)


def ignore(mob: Mobject) -> Mobject:
    """A ghost in passing (a copy flying into a card): not part of the composition the gate judges."""
    for sub in mob.get_family():
        sub.qa_ignore = True
    return mob


def run_dot(kept: bool, radius: float = 0.09) -> Dot:
    """One run of the agent: green when the test was kept, red when it was changed."""
    return Dot(radius=radius, color=KEPT if kept else CHANGED)


def run_grid(kept: int, changed: int, cols: int = 10, radius: float = 0.09, gap: float = 0.08) -> VGroup:
    """Runs as a block of dots you can count, kept first then changed, `cols` to a row, filled row by row."""
    dots = VGroup(*[run_dot(i < kept, radius) for i in range(kept + changed)])
    dots.arrange_in_grid(cols=cols, buff=gap, flow_order="rd")
    return dots


def arm_grid(sandboxes: bool = False) -> tuple[VGroup, VGroup, VGroup]:
    """The plan as a table to fill: seven arms down, three models across, ten empty runs a cell (an arm-coloured ring
    each, in a grey square when each run's own sandbox matters), each arm's row on a faint band. (heads, bands, rows),
    each row VGroup(arm word, cells)."""
    def empty_run(color: str) -> VMobject:
        ring = Circle(radius=0.065 if sandboxes else 0.07).set_stroke(color, width=1.8)
        if not sandboxes:
            return ring.set_fill(PANEL, opacity=1)
        box = Square(side_length=0.2).set_stroke(DIM, width=1.2).set_fill(PANEL_HI, opacity=1)
        return VGroup(box, ring.move_to(box))

    heads, rows, gap = VGroup(*[model_mark(m) for m in MODELS]), VGroup(), 0.03 if sandboxes else 0.07
    for key in ARMS:
        cells = VGroup(*[VGroup(*[empty_run(arm_color(key)) for _ in range(10)]).arrange(RIGHT, buff=gap)
                         for _ in MODELS]).arrange(RIGHT, buff=0.7)
        rows.add(VGroup(label_text(arm_word(key), color=arm_color(key)), cells))
    rows.arrange(DOWN, buff=0.2)
    left = rows[0][1].get_left()[0] - 0.5 - max(r[0].width for r in rows)
    for row in rows:
        row[1].align_to(rows[0][1], LEFT)
        row[0].move_to(RIGHT * left + UP * row[1].get_y(), aligned_edge=LEFT)
    bands = VGroup(*[band(rows.width + 0.6, 0.4).move_to(RIGHT * rows.get_x() + UP * row.get_y()) for row in rows])
    for h, c in zip(heads, rows[0][1]):
        h.next_to(c, UP, buff=0.3)
    return heads, bands, rows


def model_mark(name: str) -> VGroup:
    """A model as a small white hexagon with its short name beside it, for rows and keys too tight for node()."""
    hexagon = RegularPolygon(n=6, radius=0.17, color=WHITE).set_stroke(WHITE, width=2.4)
    hexagon.set_fill(PANEL_HI, opacity=0.96)
    return VGroup(hexagon, label_text(name)).arrange(RIGHT, buff=0.16)


def interval(lo, value, hi, color: str, radius: float = 0.11) -> VGroup:
    """A rate with its 95% interval: a bar from lo to hi (scene points) and a dot at the value. VGroup(bar, dot)."""
    bar = Line(lo, hi, color=color, stroke_width=6, stroke_opacity=0.55)
    dot = Dot(value, radius=radius, color=color)
    return VGroup(bar, dot)


SPINE = (
    "Does the rule hold?",
    "Once refused, does it go around?",
    "What closes the gap?",
)


def spine(lit: int | None = None, answers: dict[int, str] | None = None, width: float = 10.0,
          rows_shown: int = 3) -> VGroup:
    """The episode's scorecard: one row per question in SPINE (0-based; the first `rows_shown`), its answer, if
    given, at the right; the row `lit` in white and the rest grey, or all white with none lit. VGroup of rows, each
    VGroup(number, question, answer slot), so a beat can light or fill one row."""
    answers = answers or {}
    rows = VGroup()
    for i, question in enumerate(SPINE[:rows_shown]):
        on = lit is None or lit == i
        color = WHITE if on else MUTED
        number = mono_text(f"{i + 1}", color=color, size="label")
        q = label_text(question, color=color)
        if i in answers:
            slot = label_text(answers[i], color=color)
        else:
            slot = DashedVMobject(RoundedRectangle(corner_radius=0.06, width=2.6, height=0.42, color=color)
                                  .set_stroke(color, width=1.6), num_dashes=22)
        row = VGroup(number, q, slot)
        number.move_to(LEFT * width / 2, aligned_edge=LEFT)
        sit(q.next_to(number, RIGHT, buff=0.4), baseline(number))
        slot.move_to(RIGHT * width / 2, aligned_edge=RIGHT)
        rows.add(row)
    rows.arrange(DOWN, buff=0.34, aligned_edge=LEFT)
    return rows
