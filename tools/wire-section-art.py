#!/usr/bin/env python3
"""Set each divider's icon from tools/section-art-map.tsv.

Only rows whose icon file actually exists in icons/ are wired; the rest keep
the placeholder until they are exported from Lordicon. Re-keys _freeze rather
than re-executing, per MAINTENANCE.md section 3.

Idempotent: run it again after dropping new icons into icons/ and it picks up
whatever has arrived.
"""
import hashlib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MAP = ROOT / "tools" / "section-art-map.tsv"
LIF = '{{< lif "../../icons/%s.json" colors=secondary:#2a76dd class=rc >}}'


def divider_indexes(lines):
    out = []
    in_fence = in_yaml = in_title = False
    for i, raw in enumerate(lines):
        s = raw.strip()
        if i == 0 and s == "---":
            in_yaml = True
            continue
        if in_yaml:
            if s == "---":
                in_yaml = False
            continue
        if s.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if s.startswith("::: {.t-title}"):
            in_title = True
        if re.match(r"^# (?!\s*$)", raw):
            if in_title:
                in_title = False
                continue
            out.append(i)
    return out


rows = [l.split("\t") for l in MAP.read_text().split("\n")
        if l.strip() and not l.startswith("#")]

have = {p.stem for p in (ROOT / "icons").glob("*.json")}
by_deck = {}
for deck, n, title, icon, source, _search, _note in rows:
    by_deck.setdefault(deck, []).append((int(n), title, icon, source))

wired = waiting = 0
for deck, entries in sorted(by_deck.items()):
    u, c, lec = deck.split("/")
    qmd = ROOT / u / c / f"{lec}_Slides.qmd"
    text = qmd.read_text(newline="")
    nl = "\r\n" if "\r\n" in text else "\n"
    lines = text.split(nl)
    idx = divider_indexes(lines)

    changes = []          # (heading line index, old icon, new icon)
    for n, title, icon, source in sorted(entries):
        if lines[idx[n - 1]].strip()[2:] != title:
            sys.exit(f"{deck} #{n}: expected '{title}', found "
                     f"'{lines[idx[n - 1]].strip()[2:]}'. Map is out of date.")
        if icon not in have:
            waiting += 1
            continue
        # The shortcode sits on the third line of the block under the heading.
        line_no = idx[n - 1] + 3
        m = re.search(r'icons/([a-z_0-9]+)\.json', lines[line_no])
        if not m:
            sys.exit(f"{deck} #{n}: no shortcode where one was expected "
                     f"(line {line_no + 1}).")
        if m.group(1) != icon:
            changes.append((line_no, m.group(1), icon))

    if not changes:
        continue

    for line_no, _old, icon in changes:
        lines[line_no] = LIF % icon
    new_text = nl.join(lines)
    qmd.write_text(new_text, newline="")
    wired += len(changes)
    print(f"  {deck}: " + ", ".join(f"{o} -> {i}" for _, o, i in changes))

    # Re-key the freeze with the same substitutions.
    frz = ROOT / "_freeze" / u / c / f"{lec}_Slides" / "execute-results" / "html.json"
    if not frz.exists():
        continue
    # Positional, not string replacement: the placeholder appears on several
    # dividers in a deck, so `icons/question.json` is not a unique needle.
    entry = json.loads(frz.read_text())
    md = entry["result"]["markdown"]
    md_nl = "\r\n" if "\r\n" in md else "\n"
    md_lines = md.split(md_nl)
    md_idx = divider_indexes(md_lines)
    if len(md_idx) != len(idx):
        sys.exit(f"{deck}: {len(idx)} dividers in source but {len(md_idx)} in "
                 "result.markdown.")
    for n, _title, icon, _source in sorted(entries):
        if icon not in have:
            continue
        line_no = md_idx[n - 1] + 3
        if f"icons/" not in md_lines[line_no]:
            sys.exit(f"{deck} #{n}: no shortcode in result.markdown at "
                     f"line {line_no + 1}.")
        md_lines[line_no] = LIF % icon
    entry["result"]["markdown"] = md_nl.join(md_lines)
    entry["hash"] = hashlib.md5(
        new_text.replace("\r\n", "\n").encode("utf-8")
    ).hexdigest()
    frz.write_text(json.dumps(entry, indent=2, ensure_ascii=False))

print(f"\nwired {wired}, still waiting on an export: {waiting}")
