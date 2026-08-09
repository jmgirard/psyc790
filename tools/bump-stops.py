#!/usr/bin/env python3
"""Step the font stop down one notch on every slide the last measurement found
overflowing, then re-render and measure again.

    python3 tools/bump-stops.py            # dry run
    python3 tools/bump-stops.py --apply
    python3 tools/bump-stops.py --min 10   # ignore overflow below 10px

`--min` exists because two image-driven slides sit at +1px and are documented as
acceptable in SLIDE-OVERFLOW.md; nothing is clipped at that margin. The earlier
sweep used >10px as its bar for the same reason.

Slides are addressed by their index among `## ` headings, which is what
measure-slides.mjs reports, so decks with repeated slide titles stay
unambiguous.

Prefer rewording over stepping down: removing one wrapped line frees about 46px
at .fs80, which is usually the whole deficit, and the house sizes are 40px and
32px. Reach for this when a slide is genuinely too dense for 32px, and record
the result in SLIDE-OVERFLOW.md's exceptions table.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
APPLY = "--apply" in sys.argv
MIN = int(sys.argv[sys.argv.index("--min") + 1]) if "--min" in sys.argv else 0
LADDER = ["none", "fs80", "fs70", "fs60", "fs50"]
FS = re.compile(r"\.fs\d+")
HEAD = re.compile(r"^(##)\s+(.*?)(?:\s*\{([^}]*)\})?\s*$")

report_path = ROOT / "tools/report.json"
if not report_path.exists():
    sys.exit("No tools/report.json. Run `node tools/measure-slides.mjs` first.")

report = json.load(open(report_path))
touched = []
for deck, r in report.items():
    if not any(x["o"] >= MIN for x in r["over"]):
        continue
    path = ROOT / f"{deck}_Slides.qmd"
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    h2 = [i for i, l in enumerate(lines) if l.startswith("## ")]
    for x in r["over"]:
        if x["o"] < MIN:
            continue
        if x["k"] < 0:
            print(f"  !! {deck} '{x['title']}' is not a level-2 slide; fix by hand (+{x['o']})")
            continue
        i = h2[x["k"]]
        m = HEAD.match(lines[i].rstrip("\n"))
        attrs = FS.sub("", m.group(3) or "").split()
        cur = x["stop"]
        nxt = LADDER[min(LADDER.index(cur) + 1, len(LADDER) - 1)]
        attrs.insert(0, f".{nxt}")
        lines[i] = f"{m.group(1)} {m.group(2)} {{{' '.join(attrs)}}}\n"
        touched.append((deck, x["title"], cur, nxt, x["o"]))
    if APPLY:
        path.write_text("".join(lines), encoding="utf-8")

for deck, title, cur, nxt, o in touched:
    print(f"  {deck} +{o:4}  .{cur} -> .{nxt}   {title[:46]}")
print(f"\n{len(touched)} slides stepped down" + ("" if APPLY else "  (dry run; pass --apply)"))
if touched:
    print("re-render: " + " ".join(f"quarto render {d}_Slides.qmd --to revealjs"
                                   for d in sorted({d for d, *_ in touched})))
