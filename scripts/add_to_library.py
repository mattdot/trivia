#!/usr/bin/env python3
"""Add a candidate set to the library, but only if it passes the uniqueness check.

Steps: validate schema -> run check_uniqueness -> copy into library/sets/ ->
rebuild the index. Refuses to overwrite an existing set file unless --force.

Usage:
    python scripts/add_to_library.py my-draft.json
"""

import argparse
import json
import os
import shutil
import sys

import trivialib as T
import check_uniqueness
import build_index


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("candidate")
    ap.add_argument("--force", action="store_true",
                    help="overwrite an existing set file with the same id")
    args = ap.parse_args()

    data = T.load_set(args.candidate)
    set_id = data.get("set_id")

    # Run the same uniqueness check the user would run by hand.
    saved = sys.argv
    sys.argv = ["check_uniqueness.py", args.candidate]
    try:
        rc = check_uniqueness.main()
    finally:
        sys.argv = saved
    if rc != 0:
        print("\nNot added: fix the issues above first.")
        return rc

    dest = os.path.join(T.sets_dir(), "%s.json" % set_id)
    if os.path.abspath(dest) != os.path.abspath(args.candidate):
        if os.path.exists(dest) and not args.force:
            print("Refusing to overwrite existing %s (use --force)." % dest)
            return 3
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copyfile(args.candidate, dest)
        print("Filed set as %s" % dest)
    else:
        print("Candidate already lives in library/sets/.")

    build_index.main()
    print("\nAdded '%s' to the library." % set_id)
    return 0


if __name__ == "__main__":
    sys.exit(main())
