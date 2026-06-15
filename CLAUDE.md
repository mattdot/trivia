# CLAUDE.md

This repo is a growing **trivia library** plus the generator that fills it. The
goal is reasoning-driven questions and a guarantee that **no question or answer
is ever reused across games.**

## How questions are made

The `trivia-generator` skill lives in `.claude/skills/trivia-generator/` and
loads automatically. It governs the *style* of every question:

- All difficulty comes from **reasoning**, never obscurity. A sharp player should
  narrow a listable set to ~2-4 finalists and place a defensible bet — they won't
  always be right, and that residual doubt is the game.
- Within a set, **at least 75% of questions sit on a unique dimension** (the axis
  being measured — elevation, population, founding date), and no dimension is used
  more than twice.

## Library mode — always use it in this repo

Uniqueness across games is enforced by scripts, not by memory. When asked to
generate trivia here, follow this loop:

1. **Survey what's taken:** `python scripts/stats.py`
   (add `--topic "U.S. states"` to focus). Avoid answers and over-used dimensions
   it lists.
2. **Write the set** to `library/sets/<YYYY-MM-DD>-<slug>.json` in the schema
   described in `library/README.md`. Every question needs a normalized
   `dimension` and `answer_subject` — those are what dedup fingerprints.
3. **Check it:** `python scripts/check_uniqueness.py <path>.json`
   Non-zero exit = a hard collision (a repeated question stem or a reused answer).
   Regenerate only the colliding questions, then re-check until clean.
4. **File it:** `python scripts/add_to_library.py <path>.json`
   (re-runs the check, then rebuilds `library/index.jsonl` and `library/INDEX.md`).
5. **Render it:** `python scripts/render.py <path>.json` → playable HTML in
   `output/`.
6. **Commit** the new set file and the regenerated index.

Do not hand-edit `library/index.jsonl` or `library/INDEX.md`; they're rebuilt
from the set files. The set files in `library/sets/` are the source of truth.

## Tooling notes

- Python 3.8+, standard library only — no install step.
- Run scripts from the repo root so paths resolve.
- On Windows/PowerShell the commands are identical (`python scripts\stats.py`).
