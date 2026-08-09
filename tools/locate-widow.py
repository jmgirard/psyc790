#!/usr/bin/env python3
"""Match each widow from the last measurement back to its line in the deck
source, with an estimate of how many characters need to come out.

    python3 tools/locate-widow.py

The estimate divides the widow's rendered width by its character count, which
is the local average character width for that element's font and size, then
asks for the widow plus a small margin. It is a starting point, not a promise:
re-measure after editing.
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent


def norm(s):
    s = re.sub(r"\$[^$]*\$", " M ", s)                    # inline math -> placeholder
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)        # links -> label
    s = re.sub(r"\[([^\]]*)\]\{[^}]*\}", r"\1", s)        # spans -> content
    s = re.sub(r"[`*_{}\[\]()#|\\]", " ", s)
    s = s.replace("‘", "'").replace("’", "'")
    s = s.replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", s).strip().lower()


report_path = ROOT / "tools/report.json"
if not report_path.exists():
    raise SystemExit("No tools/report.json. Run `node tools/measure-slides.mjs` first.")

report = json.load(open(report_path))
found = 0
for deck, r in report.items():
    if not r["widows"]:
        continue
    src = ROOT / f"{deck}_Slides.qmd"
    lines = src.read_text(encoding="utf-8").splitlines()
    for w in r["widows"]:
        found += 1
        target = norm(w["text"])
        words = [x for x in target.split() if len(x) > 3]
        best_i, best_score = None, 0
        for i, line in enumerate(lines, 1):
            n = norm(line)
            if not n:
                continue
            score = sum(1 for x in words if x in n)
            if score > best_score:
                best_score, best_i = score, i
        per_char = w["lastPx"] / max(1, len(w["widow"]))
        cut = int((w["lastPx"] + 25) / per_char)
        confidence = "" if best_score / max(1, len(words)) > 0.75 else "   <<< weak match"
        print(f"{deck}:{best_i}  cut >= {cut} chars  widow=«{w['widow']}» "
              f"{w['lastPx']}/{w['boxPx']}px{confidence}")
        if best_i:
            print(f"    {lines[best_i - 1].strip()[:120]}")
print(f"\n{found} widows")
