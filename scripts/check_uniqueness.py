#!/usr/bin/env python3
"""Check a candidate trivia set against the existing library.

Uniqueness model (per the game's rules):
  * The same QUESTION must never be reused. A stem that already appears in the
    library — or repeats within the candidate set — is a hard collision.
  * The same ANSWER *may* be reused across different games/sets. Reusing an
    answer subject that appears in another set is fine (reported as info only).
  * Within a single set/session, no single answer may make up more than ~8% of
    the questions (so a 20-question run is effectively all-distinct answers, but
    a larger session may repeat an answer a couple of times).

Hard collisions (exit code 1):
  * a question stem that already appears in the library
  * a question stem repeated within the candidate set
  * an answer subject used more than 8% of the time within the candidate set
  * a dimension used more than twice within the candidate set

Warnings (exit code 0, but printed):
  * near-duplicate stems (token overlap >= --jaccard) against the library
  * the set's within-set dimension uniqueness falling below --min-unique

Usage:
    python scripts/check_uniqueness.py library/sets/2026-06-15-us-states.json
"""

import argparse
import sys
from collections import Counter

import trivialib as T


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("candidate", help="path to the candidate set JSON")
    ap.add_argument("--jaccard", type=float, default=0.8,
                    help="token-overlap threshold for near-duplicate (same-question) warnings")
    ap.add_argument("--min-unique", type=float, default=0.75,
                    help="minimum within-set dimension uniqueness before warning")
    ap.add_argument("--answer-cap", type=float, default=0.08,
                    help="max share of a session any single answer may occupy")
    args = ap.parse_args()

    data = T.load_set(args.candidate)
    cand_id = data.get("set_id")
    questions = data.get("questions", [])
    n = len(questions)

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
    info = []

    seen_stems = {}
    subj_counts = Counter()
    subj_label = {}
    for i, q in enumerate(questions, 1):
        sfp = T.stem_fingerprint(q)
        subfp = T.subject_fingerprint(q)
        label = "Q%d (%s)" % (i, q.get("answer_subject") or q.get("state", "?"))

        # --- QUESTIONS must be unique (within set + across library) ---
        if sfp in seen_stems:
            hard.append("%s repeats the stem of Q%d in this same set" % (label, seen_stems[sfp]))
        seen_stems.setdefault(sfp, i)
        if sfp in lib_stems:
            other = lib_stems[sfp]
            hard.append("%s duplicates a question already in set '%s'" % (label, other.get("set_id")))
        elif args.jaccard < 1.0:
            for other in lib:
                j = T.jaccard(q.get("q", ""), other.get("q", ""))
                if j >= args.jaccard:
                    warn.append("%s is %.0f%% similar to a question in set '%s' — make sure it isn't the same question"
                                % (label, 100 * j, other.get("set_id")))
                    break

        # --- ANSWERS may repeat across sets (info only); track within-set frequency ---
        subj_counts[subfp] += 1
        subj_label.setdefault(subfp, q.get("answer_subject") or q.get("state", "?"))
        if subfp in lib_subjects:
            info.append("%s answer also appears in set '%s' (allowed — answers may repeat across games)"
                        % (label, lib_subjects[subfp].get("set_id")))

    # within-set answer-frequency cap (~8% of the session, but always allow at least 1)
    allowed = max(1, int(args.answer_cap * n))
    for subfp, c in subj_counts.items():
        if c > allowed:
            hard.append("answer '%s' appears %d times — over the %.0f%% per-session cap (max %d of %d here)"
                        % (subj_label[subfp], c, 100 * args.answer_cap, allowed, n))

    ratio, counts = T.dimension_unique_ratio(questions)
    if ratio < args.min_unique:
        doubled = [d for d, c in counts.items() if c > 1]
        warn.append("within-set dimension uniqueness is %.0f%% (target >= %.0f%%); doubled: %s"
                    % (100 * ratio, 100 * args.min_unique, ", ".join(doubled) or "-"))

    over_cap = [d for d, c in counts.items() if c > 2]
    if over_cap:
        hard.append("dimension(s) used more than twice in one set: " + ", ".join(over_cap))

    # report
    print("Candidate: %s  (%d questions, %d already in library)" % (cand_id, n, len(lib)))
    print("Within-set dimension uniqueness: %.0f%%" % (100 * ratio))
    print("Distinct answers: %d of %d  (per-session cap: %d each)" % (len(subj_counts), n, allowed))
    if info:
        print("\nINFO (answers shared with other sets — allowed):")
        for m in info:
            print("  - " + m)
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

    print("\nOK: no repeated questions, and no answer over the per-session cap.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
