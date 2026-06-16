#!/usr/bin/env python3
"""Assemble a library set from one or more raw agent JSON arrays, deduping answers.

config JSON:
{
  "set_id","topic","created","masthead":{...},"plan_note":"...",
  "sources": ["/tmp/a.json","/tmp/b.json"],   # each a raw array of question objs
  "answer_cap": 2,        # max times one answer may appear (default 2)
  "max": 50,              # cap total questions
  "drop_answers": [...]   # answers to exclude (case-insensitive)
}
Each source question obj uses agent fields: q, answer, detail, why, more, source, dimension (+ optional cat/archetype/mechanism).
"""
import json, sys, pathlib, re

def norm(s): return re.sub(r"\s+", " ", (s or "").strip().lower())

def main(cfgpath):
    cfg = json.load(open(cfgpath))
    sid, topic = cfg["set_id"], cfg["topic"]
    cap = cfg.get("answer_cap", 2)
    maxn = cfg.get("max", 9999)
    drop = {norm(a) for a in cfg.get("drop_answers", [])}
    acount, seenq, qs = {}, set(), []
    for src in cfg["sources"]:
        for q in json.load(open(src)):
            ans = (q.get("answer") or q.get("answer_subject") or q.get("state") or "").strip()
            ka, kq = norm(ans), norm(q.get("q"))
            if not ans or ka in drop or kq in seenq: continue
            if acount.get(ka, 0) >= cap: continue
            acount[ka] = acount.get(ka, 0) + 1
            seenq.add(kq)
            qs.append((q, ans))
            if len(qs) >= maxn: break
        if len(qs) >= maxn: break
    out_qs, dims = [], []
    for i, (q, ans) in enumerate(qs, 1):
        dim = q.get("dimension", "")
        dims.append(dim)
        out_qs.append({
            "id": f"{sid}-{i:02d}",
            "cat": q.get("cat") or f"{topic} · {dim}"[:60],
            "dimension": dim,
            "archetype": q.get("archetype") or (q.get("mechanism", "reasoning").split("/")[0].split("(")[0].strip()[:30]),
            "q": q["q"], "answer_subject": ans, "state": q.get("state") or ans,
            "detail": q.get("detail", ""), "why": q.get("why", ""),
            "more": q.get("more", ""), "source": q.get("source", ""),
        })
    plan = {"dimensions": dims, "unique_ratio": round(len(set(dims)) / len(dims), 2) if dims else 1.0,
            "doubled": [], "note": cfg.get("plan_note", "")}
    out = {"set_id": sid, "topic": topic, "created": cfg.get("created", "2026-06-16"),
           "masthead": cfg["masthead"], "plan": plan, "questions": out_qs}
    pathlib.Path("library/sets", f"{sid}.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {sid}: {len(out_qs)} questions, {len(acount)} distinct answers")

if __name__ == "__main__":
    main(sys.argv[1])
