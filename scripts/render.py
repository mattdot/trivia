#!/usr/bin/env python3
"""Render a trivia set into a self-contained, tap-to-reveal HTML field guide.

Uses the bundled template at
``.claude/skills/trivia-generator/assets/field-guide.html``. Each question is
server-rendered into a native ``<details>`` card (so the page needs **no
JavaScript** to play — it works in script-blocked viewers like in-app
previews), and the four masthead strings are substituted. The output stays
self-contained: system fonts, no storage, no external assets.

Usage:
    python scripts/render.py library/sets/2026-06-15-us-states.json
    python scripts/render.py my-set.json --out output/custom.html
"""

import argparse
import html
import os
import sys

import trivialib as T


def _esc(text):
    return html.escape("" if text is None else str(text), quote=True)


def _field(label, body, cls=""):
    cls_attr = (' class="%s"' % cls) if cls else ""
    return ('<span class="label">%s</span>'
            '<div class="field"><p%s>%s</p></div>'
            % (_esc(label), cls_attr, _esc(body)))


def card_html(item, i):
    """One <details> card. All question text is HTML-escaped."""
    out = ['<details class="card">',
           '<summary class="q-toggle">',
           '<span class="medallion" aria-hidden="true">%d</span>' % (i + 1),
           '<span class="q-main">']
    if item.get("cat"):
        out.append('<span class="cat">%s</span>' % _esc(item["cat"]))
    out.append('<span class="q-text">%s</span>' % _esc(item.get("q", "")))
    out.append('<span class="hint">'
               '<span class="lbl lbl-closed">Tap to reveal</span>'
               '<span class="lbl lbl-open">Hide answer</span>'
               '<span class="chev" aria-hidden="true"></span></span>')
    out.append('</span>')  # .q-main
    out.append('</summary>')
    out.append('<div class="answer-pad">')
    out.append('<span class="label">Answer</span>')
    out.append('<span class="ans-main">%s</span>' % _esc(item.get("state", "")))
    if item.get("detail"):
        out.append('<span class="ans-detail">%s</span>' % _esc(item["detail"]))
    if item.get("why"):
        out.append(_field("Why it’s interesting", item["why"]))
    if item.get("more"):
        out.append(_field("Follow-on", item["more"]))
    if item.get("source"):
        out.append(_field("Source", item["source"], "source-text"))
    out.append('</div>')  # .answer-pad
    out.append('</details>')
    return "\n".join(out)

DEFAULT_TEMPLATE = os.path.join(
    ".claude", "skills", "trivia-generator", "assets", "field-guide.html")


def render(data, template_html):
    questions = data.get("questions", [])
    if questions:
        cards = "\n".join(card_html(q, i) for i, q in enumerate(questions))
    else:
        cards = '<p class="empty">No questions loaded.</p>'

    html = template_html.replace("<!--__CARDS__-->", cards)

    m = data.get("masthead", {}) or {}
    topic = data.get("topic", "Trivia")
    repl = {
        "__EYEBROW__": m.get("eyebrow", "TRIVIA FIELD GUIDE"),
        "__TITLE_HTML__": m.get("title_html", m.get("title_plain", topic)),
        "__TITLE_PLAIN__": m.get("title_plain", topic),
        "__DEK__": m.get("dek", "Reason it through, then tap to check yourself."),
        "__FOOTER_HTML__": m.get("footer_html", "Sources noted per question."),
    }
    for k, v in repl.items():
        html = html.replace(k, v)
    return html


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("set_json")
    ap.add_argument("--template", default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    root = T.repo_root()
    template_path = args.template or os.path.join(root, DEFAULT_TEMPLATE)
    with open(template_path, "r", encoding="utf-8") as fh:
        template_html = fh.read()

    data = T.load_set(args.set_json)
    html = render(data, template_html)

    out = args.out or os.path.join(root, "output", "%s.html" % data.get("set_id"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("Wrote %s (%d questions)" % (out, len(data.get("questions", []))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
