#!/usr/bin/env python3
"""Wrap a curated flat question list into a library set file.

Input JSON (a single object):
{
  "set_id": "...", "topic": "...", "created": "YYYY-MM-DD",
  "masthead": {...}, "plan": {...},
  "questions": [
    {"q": "...", "answer": "...",            # answer -> answer_subject + state
     "detail": "...", "why": "...", "more": "...", "source": "...",
     "dimension": "...", "cat": "...", "archetype": "..."},   # cat/archetype optional
    ...
  ]
}

Usage: python scripts/wrap_set.py <input.json>
Writes library/sets/<set_id>.json with ids added and only schema fields kept.
"""
import json, sys, pathlib

KEEP = ("id", "cat", "dimension", "archetype", "q", "answer_subject",
        "state", "detail", "why", "more", "source")

def main(path):
    d = json.load(open(path))
    sid = d["set_id"]
    topic = d["topic"]
    out_qs = []
    for i, q in enumerate(d["questions"], 1):
        ans = q.get("answer_subject") or q.get("answer") or q.get("state")
        nq = {
            "id": f"{sid}-{i:02d}",
            "cat": q.get("cat") or f"{topic} · {q.get('dimension','')}".strip(" ·"),
            "dimension": q.get("dimension", ""),
            "archetype": q.get("archetype", "best-without"),
            "q": q["q"],
            "answer_subject": ans,
            "state": q.get("state") or ans,
            "detail": q.get("detail", ""),
            "why": q.get("why", ""),
            "more": q.get("more", ""),
            "source": q.get("source", ""),
        }
        out_qs.append({k: nq[k] for k in KEEP})
    out = {
        "set_id": sid, "topic": topic, "created": d.get("created", "2026-06-16"),
        "masthead": d["masthead"], "plan": d.get("plan", {}), "questions": out_qs,
    }
    p = pathlib.Path("library/sets") / f"{sid}.json"
    p.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {p} ({len(out_qs)} questions)")

if __name__ == "__main__":
    main(sys.argv[1])
