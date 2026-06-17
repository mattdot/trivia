#!/usr/bin/env python3
"""Extract the final JSON question-array from a subagent transcript (.output JSONL).

Reads the transcript IN-SCRIPT (never to stdout, so it won't flood a context),
finds fenced ```json blocks in assistant text, keeps arrays of question objects
(dicts with a 'q' key), and writes the LAST/strongest such array to <out>.

Usage: python scripts/extract_agent_json.py <transcript.output> <out.json>
"""
import json, sys, re

def texts_from(obj):
    """Yield any assistant text strings found in a parsed JSONL record."""
    if isinstance(obj, dict):
        c = obj.get("content")
        if isinstance(c, str):
            yield c
        elif isinstance(c, list):
            for b in c:
                if isinstance(b, dict) and isinstance(b.get("text"), str):
                    yield b["text"]
        # nested message
        m = obj.get("message")
        if isinstance(m, dict):
            yield from texts_from(m)

def main(src, out):
    blocks = []
    with open(src, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except Exception:
                continue
            for t in texts_from(rec):
                for m in re.findall(r"```json\s*(.*?)```", t, re.DOTALL):
                    try:
                        arr = json.loads(m)
                    except Exception:
                        continue
                    if isinstance(arr, list) and arr and isinstance(arr[0], dict) and "answer" in arr[0]:
                        # keep well-formed candidate dicts (skip 'REMOVED' placeholders)
                        good = [q for q in arr if q.get("answer") and q.get("detail") and "REMOV" not in str(q.get("answer", "")).upper()]
                        if good:
                            blocks.append(good)
    if not blocks:
        print(f"!! no question array found in {src}")
        sys.exit(2)
    best = max(blocks, key=len)  # the full final array
    json.dump(best, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{src.split('/')[-1]} -> {out}: {len(best)} questions")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
