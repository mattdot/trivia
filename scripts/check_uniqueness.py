#!/usr/bin/env python3
"""Check a candidate trivia set against the existing library.

Hard collisions (exit code 1):
  * a question stem that already appears in the library
  * an answer subject that has already been used (unless --allow-repeat-answers)
  * duplicate stems or answers *within* the candidate set itself

Warnings (exit code 0, but printed):
  * near-duplicate stems (token overlap >= --jaccard) against the library
  * the set's within-set dimension uniqueness falling below --min-unique

Usage:
    python scripts/check_uniqueness.py library/sets/2026-06-15-us-states.json
    python scripts/check_uniqueness.py my-draft.json --allow-repeat-answers
"""

import argparse
import sys

import trivialib as T


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("candidate", help="path to the candidate set JSON")
    ap.add_argument("--allow-repeat-answers", action="store_true",
                    help="downgrade repeated answer subjects to a warning")
    ap.add_argument("--jaccard", type=float, default=0.8,
                    help="token-overlap threshold for near-duplicate warnings")
    ap.add_argument("--min-unique", type=float, default=0.75,
                    help="minimum within-set dimension uniqueness before warning")
    args = ap.parse_args()

    data = T.load_set(args.candidate)
    cand_id = data.get("set_id")
    questions = data.get("questions", [])

    schema_problems = T.validate_set(data)
    if schema_problems:
        print("SCHEMA ERRORS:")
        for p in schema_problems:
            print("  - " + p)
        return 2

    # Library excluding the candidate (so re-checking an already-added set is fine).
    lib = T.load_library(exclude_set_id=cand_id)
    lib_stems = {T.stem_fingerprint(q): q for q in lib}
    lib_subjects = {}
    for q in lib:
        lib_subjects.setdefault(T.subject_fingerprint(q), q)

    hard = []
    warn = []

    seen_stems = {}
    seen_subjects = {}
    for i, q in enumerate(questions, 1):
        sfp = T.stem_fingerprint(q)
        subfp = T.subject_fingerprint(q)
        label = "Q%d (%s)" % (i, q.get("answer_subject") or q.get("state", "?"))

        # within-set duplicates
        if sfp in seen_stems:
            hard.append("%s repeats the stem of Q%d in this same set" % (label, seen_stems[sfp]))
        if subfp in seen_subjects:
            hard.append("%s reuses answer '%s' already used by Q%d in this set"
                        % (label, q.get("answer_subject"), seen_subjects[subfp]))
        seen_stems.setdefault(sfp, i)
        seen_subjects.setdefault(subfp, i)

        # against the library
        if sfp in lib_stems:
            other = lib_stems[sfp]
            hard.append("%s duplicates a question already in set '%s'" % (label, other.get("set_id")))
        if subfp in lib_subjects:
            other = lib_subjects[subfp]
            msg = "%s reuses answer '%s' already used in set '%s'" % (
                label, q.get("answer_subject"), other.get("set_id"))
            if args.allow_repeat_answers:
                warn.append(msg + " (allowed)")
            else:
                hard.append(msg)

        # near-duplicate stems (only worth checking if not already an exact hard dup)
        if sfp not in lib_stems:
            for other in lib:
                j = T.jaccard(q.get("q", ""), other.get("q", ""))
                if j >= args.jaccard:
                    warn.append("%s is %.0f%% similar to a question in set '%s'"
                                % (label, 100 * j, other.get("set_id")))
                    break

    ratio, counts = T.dimension_unique_ratio(questions)
    if ratio < args.min_unique:
        doubled = [d for d, c in counts.items() if c > 1]
        warn.append("within-set dimension uniqueness is %.0f%% (target >= %.0f%%); doubled: %s"
                    % (100 * ratio, 100 * args.min_unique, ", ".join(doubled) or "-"))

    over_cap = [d for d, c in counts.items() if c > 2]
    if over_cap:
        hard.append("dimension(s) used more than twice in one set: " + ", ".join(over_cap))

    # report
    print("Candidate: %s  (%d questions, %d already in library)" % (cand_id, len(questions), len(lib)))
    print("Within-set dimension uniqueness: %.0f%%" % (100 * ratio))
    if warn:
        print("\nWARNINGS:")
        for w in warn:
            print("  ! " + w)
    if hard:
        print("\nHARD COLLISIONS (must fix):")
        for h in hard:
            print("  x " + h)
        print("\nFAILED: regenerate the colliding questions and re-check.")
        return 1

    print("\nOK: no duplicate questions or answers against the library.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
