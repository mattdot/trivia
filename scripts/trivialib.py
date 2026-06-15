"""Shared helpers for the trivia question library.

Pure standard library (Python 3.8+). The library's source of truth is the
collection of per-game set files under ``library/sets/*.json``. Everything
else (the index, the uniqueness check, the stats) is derived from those.

A *set* file looks like::

    {
      "set_id": "2026-06-15-us-states",
      "topic": "U.S. states",
      "created": "2026-06-15",
      "masthead": { "eyebrow": "...", "title_html": "...",
                    "title_plain": "...", "dek": "...", "footer_html": "..." },
      "plan": { "dimensions": [...], "unique_ratio": 1.0, "doubled": [] },
      "questions": [
        {
          "id": "2026-06-15-us-states-01",
          "cat": "Geography \u00b7 Latitude",   # display eyebrow on the card
          "dimension": "latitude",               # normalized axis (for variety + dedup)
          "archetype": "extreme-north",          # optional ranking shape
          "q": "...",                            # the stem
          "answer_subject": "Olympia, Washington",  # normalized answer (for dedup)
          "state": "Olympia, Washington",        # display answer (template field)
          "detail": "...", "why": "...", "more": "...", "source": "..."
        }
      ]
    }
"""

import glob
import json
import os
import re

# Fields the HTML template consumes (keep in sync with assets/field-guide.html).
TEMPLATE_KEYS = ["cat", "q", "state", "detail", "why", "more", "source"]

# Fields every library question must carry.
REQUIRED_QUESTION_KEYS = ["q", "state", "dimension", "answer_subject"]

_WORD_RE = re.compile(r"[a-z0-9]+")


def repo_root(start=None):
    """Walk up from ``start`` (or this file) until we find a ``library`` dir."""
    here = os.path.abspath(start or os.path.dirname(__file__))
    cur = here
    while True:
        if os.path.isdir(os.path.join(cur, "library")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            # Fall back to one level above scripts/.
            return os.path.dirname(os.path.dirname(here))
        cur = parent


def sets_dir(root=None):
    return os.path.join(root or repo_root(), "library", "sets")


def load_set(path):
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    if "set_id" not in data:
        data["set_id"] = os.path.splitext(os.path.basename(path))[0]
    data.setdefault("questions", [])
    return data


def load_library(root=None, exclude_set_id=None):
    """Return a flat list of question dicts, each tagged with ``set_id``."""
    out = []
    for path in sorted(glob.glob(os.path.join(sets_dir(root), "*.json"))):
        data = load_set(path)
        if exclude_set_id and data.get("set_id") == exclude_set_id:
            continue
        for q in data.get("questions", []):
            q = dict(q)
            q["set_id"] = data.get("set_id")
            q["topic"] = data.get("topic", "")
            out.append(q)
    return out


# --- normalization & fingerprints -------------------------------------------

def normalize(text):
    """Lowercase, drop punctuation, collapse whitespace."""
    return " ".join(_WORD_RE.findall((text or "").lower()))


def stem_fingerprint(q):
    return normalize(q.get("q", ""))


def subject_fingerprint(q):
    return normalize(q.get("answer_subject") or q.get("state", ""))


def token_set(text):
    return set(_WORD_RE.findall((text or "").lower()))


def jaccard(a, b):
    sa, sb = token_set(a), token_set(b)
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def dimension_unique_ratio(questions):
    """Share of questions whose dimension is used by no other question here."""
    if not questions:
        return 1.0, {}
    counts = {}
    for q in questions:
        d = (q.get("dimension") or "").strip().lower()
        counts[d] = counts.get(d, 0) + 1
    unique = sum(1 for q in questions
                 if counts.get((q.get("dimension") or "").strip().lower(), 0) == 1)
    return unique / len(questions), counts


def validate_set(data):
    """Return a list of human-readable schema problems (empty == ok)."""
    problems = []
    if not data.get("set_id"):
        problems.append("missing set_id")
    qs = data.get("questions")
    if not isinstance(qs, list) or not qs:
        problems.append("no questions array")
        return problems
    for i, q in enumerate(qs, 1):
        for key in REQUIRED_QUESTION_KEYS:
            if not str(q.get(key, "")).strip():
                problems.append("question %d missing '%s'" % (i, key))
    return problems
