#!/usr/bin/env python3
"""Build a static, mobile-first site of every trivia set for GitHub Pages.

Renders each ``library/sets/*.json`` into a self-contained field-guide page
under ``site/games/`` (reusing ``render.py`` so the output matches what you get
locally), then writes a gallery ``site/index.html`` that links to them all. The
whole ``site/`` tree is derived data — safe to delete and regenerate, and built
fresh by the Pages workflow, so it stays out of git.

Usage:
    python scripts/build_site.py
    python scripts/build_site.py --out site --base-url /trivia/
"""

import argparse
import glob
import html
import os
import sys

import render
import trivialib as T

DEFAULT_TEMPLATE = render.DEFAULT_TEMPLATE


def _esc(text):
    return html.escape(str(text or ""), quote=True)


def gallery_html(cards, title="Trivia Field Guides"):
    """A quiet, mobile-first index that links to every rendered game.

    Mirrors the field-guide palette (drafting paper + contour bistre, system
    fonts, dark-mode aware) so the gallery and the games feel like one object.
    """
    items = []
    for c in cards:
        items.append(
            '      <li class="card">\n'
            '        <a class="game" href="{href}">\n'
            '          <span class="cat">{eyebrow}</span>\n'
            '          <span class="title">{title}</span>\n'
            '          <span class="dek">{dek}</span>\n'
            '          <span class="meta">{topic} · {count} questions · {created}</span>\n'
            '        </a>\n'
            '      </li>'.format(
                href=_esc(c["href"]),
                eyebrow=_esc(c["eyebrow"]),
                title=_esc(c["title"]),
                dek=_esc(c["dek"]),
                topic=_esc(c["topic"]),
                count=c["count"],
                created=_esc(c["created"]),
            )
        )
    deck = "\n".join(items) if items else (
        '      <li class="empty">No games yet — generate a set, then rebuild.</li>')

    total = sum(c["count"] for c in cards)
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<style>
  :root{{
    --paper:#f1efe6; --card:#fbfaf4; --ink:#2a2823; --ink-2:#574f43;
    --muted:#8c8475; --contour:#8a5a2b; --line:rgba(42,40,35,.14);
    --line-soft:rgba(42,40,35,.08); --focus:#2f6db0;
    --serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,"Times New Roman",serif;
    --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,system-ui,sans-serif;
    --mono:ui-monospace,"SF Mono",SFMono-Regular,Menlo,Consolas,"Roboto Mono",monospace;
    --maxw:640px; --pad:clamp(16px,5vw,28px); --radius:14px;
  }}
  @media (prefers-color-scheme: dark){{
    :root{{
      --paper:#1b1a17; --card:#24231e; --ink:#ece7da; --ink-2:#bdb6a6;
      --muted:#8e8676; --contour:#cca067; --line:rgba(236,231,218,.16);
      --line-soft:rgba(236,231,218,.08); --focus:#7cb3e8;
    }}
  }}
  *{{box-sizing:border-box}} html{{-webkit-text-size-adjust:100%}}
  body{{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);
    font-size:17px;line-height:1.55;-webkit-font-smoothing:antialiased}}
  .wrap{{max-width:var(--maxw);margin:0 auto;
    padding:0 var(--pad) calc(64px + env(safe-area-inset-bottom))}}
  header{{padding:clamp(28px,8vw,52px) 0 18px;border-bottom:1px solid var(--line)}}
  .eyebrow{{font-family:var(--mono);font-size:.72rem;letter-spacing:.16em;
    text-transform:uppercase;color:var(--contour);margin:0 0 12px}}
  h1{{font-family:var(--serif);font-weight:600;font-size:clamp(1.9rem,8vw,2.7rem);
    line-height:1.08;letter-spacing:-.01em;margin:0 0 .5rem}}
  .dek{{color:var(--ink-2);font-size:1.02rem;margin:.35rem 0 0;max-width:46ch}}
  ol.deck{{list-style:none;margin:18px 0 0;padding:0}}
  .card{{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);
    margin:0 0 14px;overflow:hidden;box-shadow:0 1px 0 var(--line-soft)}}
  a.game{{display:block;text-decoration:none;color:inherit;padding:18px;
    -webkit-tap-highlight-color:transparent;min-height:44px}}
  a.game:active{{transform:translateY(1px)}}
  .cat{{font-family:var(--mono);font-size:.68rem;letter-spacing:.12em;
    text-transform:uppercase;color:var(--muted);display:block;margin:0 0 7px}}
  .title{{font-family:var(--serif);font-size:1.22rem;font-weight:600;
    line-height:1.3;color:var(--ink);display:block}}
  .dek{{display:block}}
  a.game .dek{{color:var(--ink-2);font-size:1rem;line-height:1.5;margin:6px 0 0}}
  .meta{{font-family:var(--mono);font-size:.72rem;letter-spacing:.02em;
    color:var(--muted);display:block;margin-top:12px}}
  a.game:focus-visible{{outline:3px solid var(--focus);outline-offset:2px;border-radius:12px}}
  .empty{{color:var(--muted);font-family:var(--mono);font-size:.85rem;
    list-style:none;padding:32px 0}}
  footer{{margin-top:28px;padding-top:18px;border-top:1px solid var(--line);
    font-family:var(--mono);font-size:.74rem;letter-spacing:.02em;
    color:var(--muted);line-height:1.7}}
</style>
</head>
<body>
  <div class="wrap">
    <header>
      <p class="eyebrow">Trivia Field Guide</p>
      <h1>{title}</h1>
      <p class="dek">Reasoning-driven games — narrow the set, place your bet, tap to check yourself. Pick one to play.</p>
    </header>
    <ol class="deck">
{deck}
    </ol>
    <footer>{ngames} games · {total} questions · answers hidden until you tap.</footer>
  </div>
</body>
</html>
""".format(title=_esc(title), deck=deck, ngames=len(cards), total=total)


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=None,
                    help="output directory (default: <repo>/site)")
    ap.add_argument("--template", default=None)
    ap.add_argument("--title", default="Trivia Field Guides")
    args = ap.parse_args()

    root = T.repo_root()
    out_dir = args.out or os.path.join(root, "site")
    games_dir = os.path.join(out_dir, "games")
    os.makedirs(games_dir, exist_ok=True)

    template_path = args.template or os.path.join(root, DEFAULT_TEMPLATE)
    with open(template_path, "r", encoding="utf-8") as fh:
        template_html = fh.read()

    cards = []
    set_paths = sorted(glob.glob(os.path.join(T.sets_dir(root), "*.json")))
    # Newest first in the gallery (filenames lead with the date).
    for path in reversed(set_paths):
        data = T.load_set(path)
        set_id = data.get("set_id")
        page = render.render(data, template_html)
        with open(os.path.join(games_dir, set_id + ".html"), "w",
                  encoding="utf-8") as fh:
            fh.write(page)

        m = data.get("masthead", {}) or {}
        cards.append({
            "href": "games/%s.html" % set_id,
            "eyebrow": m.get("eyebrow", "TRIVIA FIELD GUIDE"),
            "title": m.get("title_plain", data.get("topic", set_id)),
            "dek": m.get("dek", ""),
            "topic": data.get("topic", ""),
            "count": len(data.get("questions", [])),
            "created": data.get("created", ""),
        })

    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(gallery_html(cards, title=args.title))

    # GitHub Pages serves the artifact as-is; .nojekyll skips Jekyll processing.
    open(os.path.join(out_dir, ".nojekyll"), "w").close()

    print("Wrote %s: index.html + %d game page(s)" % (out_dir, len(cards)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
