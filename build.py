#!/usr/bin/env python3
"""
Builds index.html from plan.json.

The entire plan is written into the markup as static HTML, so the page is
fully readable with JavaScript disabled or blocked. JavaScript then upgrades
it into a single-week tracker with checkboxes, notes and saved progress.

Usage:  python3 build.py
"""
import json
import html
from pathlib import Path

HERE = Path(__file__).parent
data = json.loads((HERE / "plan.json").read_text())
WEEKS, PHASES, CERTS, RETIRED, LINKS = (
    data["WEEKS"], data["PHASES"], data["CERTS"], data["RETIRED"], data["LINKS"]
)

e = html.escape
SECTIONS = [("learn", "Microsoft Learn"), ("watch", "Watch"), ("build", "Build")]


def phase_of(pid):
    return next(p for p in PHASES if p["id"] == pid)


def week_items(w):
    """Every checkable id for a week, in render order."""
    ids = []
    for key, _ in SECTIONS:
        for i, _txt in enumerate(w.get(key) or []):
            ids.append(f"w{w['n']}.{key}.{i}")
    ids.append(f"w{w['n']}.cp")
    return ids


# ---------------------------------------------------------------- strip
def render_rail():
    cells = []
    for w in WEEKS:
        cls = "cell exam" if w.get("exam") else "cell"
        label = f"Week {w['n']} — {e(w['title'])}"
        cells.append(
            f'<a class="{cls}" href="#week-{w["n"]}" data-week="{w["n"]}" '
            f'title="{label}" aria-label="{label}">'
            f'<span class="fill"></span><span class="cell-n">{w["n"]}</span></a>'
        )
    brackets = "".join(
        f'<div class="brk" style="grid-column:span {len(p["weeks"])}"><span>{e(p["short"])}</span></div>'
        for p in PHASES
    )
    return "".join(cells), brackets


# ---------------------------------------------------------------- sidebar
def render_side():
    out = []
    for p in PHASES:
        rows = []
        for n in p["weeks"]:
            w = next(x for x in WEEKS if x["n"] == n)
            rows.append(
                f'<a class="wk-btn" href="#week-{n}" data-week="{n}">'
                f'<span class="tick" data-tick="{n}"></span>'
                f'<span class="wk-n">{n:02d}</span>'
                f'<span class="wk-t">{e(w["title"])}</span></a>'
            )
        out.append(
            f'<div class="phase-grp"><div class="phase-lab">'
            f'<span>{e(p["name"])}</span><span data-phasecount="{p["id"]}">0/{len(p["weeks"])}</span>'
            f'</div>{"".join(rows)}</div>'
        )
    return "".join(out)


# ---------------------------------------------------------------- panels
def render_item(item_id, text, extra_cls=""):
    return (
        f'<div class="item {extra_cls}" data-id="{item_id}" role="checkbox" '
        f'tabindex="0" aria-checked="false">'
        f'<span class="box"></span><span class="item-t">{e(text)}</span></div>'
    )


def render_week(w):
    ph = phase_of(w["phase"])
    total = len(week_items(w))
    h = [f'<section class="panel wk-panel" id="week-{w["n"]}" data-week="{w["n"]}" tabindex="-1">']

    h.append('<div class="p-head"><div class="p-meta">')
    h.append(f'<span class="badge dark">Week {w["n"]}</span>')
    h.append(f'<span class="badge">{e(ph["name"])}</span>')
    if w.get("exam"):
        h.append(f'<span class="badge hl">Exam &middot; {e(w["exam"])}</span>')
    if w.get("aka"):
        h.append(f'<span class="badge">{e(w["aka"])}</span>')
    h.append(f'<span class="sect-count" data-wkcount="{w["n"]}">0 / {total}</span>')
    h.append("</div>")
    h.append(f'<h2>{e(w["title"])}</h2>')
    if w.get("intent"):
        h.append(f'<p class="p-intent">{e(w["intent"])}</p>')
    h.append("</div>")

    if w.get("trial"):
        h.append(f'<div class="callout"><span class="eyebrow">Licensing</span>{e(w["trial"])}</div>')
    if w.get("note"):
        h.append(f'<div class="callout"><span class="eyebrow">Note</span>{e(w["note"])}</div>')

    for key, label in SECTIONS:
        items = w.get(key) or []
        if not items:
            continue
        h.append(
            f'<div class="sect"><div class="sect-h"><h3>{label}</h3>'
            f'<span class="sect-count" data-seccount="w{w["n"]}.{key}">0/{len(items)}</span></div>'
        )
        for i, txt in enumerate(items):
            h.append(render_item(f'w{w["n"]}.{key}.{i}', txt))
        h.append("</div>")

    if w.get("ai"):
        h.append('<div class="sect"><div class="sect-h"><h3>AI drill</h3></div>')
        h.append(f'<p class="ai-txt">{e(w["ai"])}</p></div>')

    h.append('<div class="sect"><div class="sect-h"><h3>Checkpoint</h3></div>')
    h.append(f'<div class="cp" data-cp="{w["n"]}">')
    h.append(render_item(f'w{w["n"]}.cp', w["checkpoint"]))
    h.append("</div>")
    h.append('<p class="cp-hint">Can&rsquo;t produce it? Repeat the week. Ticking this marks the week done.</p>')
    h.append("</div>")

    h.append('<div class="sect js-only"><div class="sect-h"><h3>Notes</h3></div>')
    h.append(
        f'<textarea class="notes" data-notes="w{w["n"]}" '
        f'placeholder="What broke, what clicked, what to revisit&hellip;"></textarea></div>'
    )

    h.append('<div class="nav js-only">')
    if w["n"] > 0:
        h.append(f'<a class="navbtn" href="#week-{w["n"]-1}" data-week="{w["n"]-1}">&larr; Week {w["n"]-1}</a>')
    else:
        h.append("<span></span>")
    if w["n"] < 24:
        h.append(f'<a class="navbtn" href="#week-{w["n"]+1}" data-week="{w["n"]+1}">Week {w["n"]+1} &rarr;</a>')
    else:
        h.append("<span></span>")
    h.append("</div>")

    h.append("</section>")
    return "".join(h)


# ---------------------------------------------------------------- reference
def render_ref():
    certs = "".join(
        f'<div class="ref-row"><span class="code">{e(c["code"])}</span><span>{e(c["name"])}'
        f'<br><span class="muted">'
        f'{("Week " + str(c["week"])) if c["week"] is not None else "Beyond week 24"}'
        f'{" &middot; optional" if c["status"] == "optional" else ""}</span></span></div>'
        for c in CERTS
    )
    retired = "".join(
        f'<div class="ref-row"><span class="code gone">{e(r["code"])}</span>'
        f'<span class="muted">{e(r["when"])}</span></div>'
        for r in RETIRED
    )
    links = "".join(
        f'<div class="ref-row"><span class="code">{e(l["code"])}</span>'
        f'<a href="{e(l["url"])}" target="_blank" rel="noopener">{e(l["label"])}</a></div>'
        for l in LINKS
    )
    return certs, retired, links


rail, brackets = render_rail()
side = render_side()
panels = "".join(render_week(w) for w in WEEKS)
ref_certs, ref_retired, ref_links = render_ref()
phase_json = json.dumps([{"id": p["id"], "weeks": p["weeks"]} for p in PHASES], separators=(",", ":"))
items_json = json.dumps({str(w["n"]): week_items(w) for w in WEEKS}, separators=(",", ":"))

template = (HERE / "template.html").read_text()
out = (
    template.replace("<!--RAIL-->", rail)
    .replace("<!--BRACKETS-->", brackets)
    .replace("<!--SIDE-->", side)
    .replace("<!--PANELS-->", panels)
    .replace("<!--REFCERTS-->", ref_certs)
    .replace("<!--REFRETIRED-->", ref_retired)
    .replace("<!--REFLINKS-->", ref_links)
    .replace("/*PHASEDATA*/", phase_json)
    .replace("/*ITEMDATA*/", items_json)
)

(HERE / "index.html").write_text(out)
total_items = sum(len(week_items(w)) for w in WEEKS)
print(f"Built index.html — {len(WEEKS)} weeks, {total_items} checkable items, {len(out):,} bytes")
