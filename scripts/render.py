#!/usr/bin/env python3
"""Render a trivia set into a self-contained, tap-to-reveal HTML field guide.

Uses the bundled template at
``.claude/skills/trivia-generator/assets/field-guide.html``. Only the question
array and the four masthead strings are substituted; the template's CSS/JS are
untouched, so the output stays self-contained (system fonts, no storage).

Usage:
    python scripts/render.py library/sets/2026-06-15-us-states.json
    python scripts/render.py my-set.json --out output/custom.html
"""

import argparse
import json
import os
import sys

import trivialib as T

DEFAULT_TEMPLATE = os.path.join(
    ".claude", "skills", "trivia-generator", "assets", "field-guide.html")


def render(data, template_html):
    questions = data.get("questions", [])
    # Keep only the keys the template consumes; preserve order.
    objs = []
    for q in questions:
        objs.append({k: q.get(k, "") for k in T.TEMPLATE_KEYS})
    body = ",\n".join(json.dumps(o, ensure_ascii=False) for o in objs)
    # Guard against an accidental </script> inside question text.
    body = body.replace("</", "<\\/")

    html = template_html.replace("/*__QUESTIONS__*/", body)

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
