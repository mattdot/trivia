#!/usr/bin/env python3
"""Show what the library already covers, so a new set can extend it.

Prints totals, the dimension histogram (which axes are over/under-used), and
the full list of answer subjects already taken. Run this *before* planning a
new set in library mode.

Usage:
    python scripts/stats.py
    python scripts/stats.py --topic "U.S. states"
"""

import argparse
import sys

import trivialib as T


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--topic", default=None, help="filter to one topic")
    args = ap.parse_args()

    questions = T.load_library()
    if args.topic:
        questions = [q for q in questions if q.get("topic") == args.topic]

    if not questions:
        print("Library is empty%s." % (" for that topic" if args.topic else ""))
        return 0

    dims = {}
    arches = {}
    subjects = {}
    topics = {}
    for q in questions:
        d = (q.get("dimension") or "(unset)").strip().lower()
        dims[d] = dims.get(d, 0) + 1
        a = (q.get("archetype") or "(unset)").strip().lower()
        arches[a] = arches.get(a, 0) + 1
        subjects[T.subject_fingerprint(q)] = q.get("answer_subject") or q.get("state")
        topics[q.get("topic", "")] = topics.get(q.get("topic", ""), 0) + 1

    print("Library: %d questions across %d topics" % (len(questions), len(topics)))
    print("Distinct answer subjects already used: %d" % len(subjects))
    print()
    print("Dimensions used (most to least) \u2014 prefer the unused/rare ones next:")
    for d, c in sorted(dims.items(), key=lambda kv: (-kv[1], kv[0])):
        print("  %-22s %d" % (d, c))
    print()
    print("Archetypes used:")
    for a, c in sorted(arches.items(), key=lambda kv: (-kv[1], kv[0])):
        print("  %-22s %d" % (a, c))
    print()
    print("Answer subjects already taken (off-limits for new questions):")
    for s in sorted(subjects.values(), key=lambda x: x.lower()):
        print("  - %s" % s)
    return 0


if __name__ == "__main__":
    sys.exit(main())
