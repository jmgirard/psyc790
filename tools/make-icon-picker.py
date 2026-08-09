#!/usr/bin/env python3
"""Write _site/icon-picker.html: every candidate in section-art-map.tsv, rendered.

Deciding 21 open rows in the Lordicon UI means 50 tabs. This puts the
candidates for each slot side by side with the section they would open and the
reason they are on the shortlist.

Previews load from cdn.lordicon.com, which per ICONS.md serves OLDER revisions
than the PRO web app and sometimes watermarked ones. That is fine for deciding
and wrong for downloading: export the pick from the Lordicon UI instead, with
secondary set to #2a76dd before exporting.

Output goes to _site/ because it is disposable and _site is gitignored. It is
also what the local preview server serves:

    python3 tools/make-icon-picker.py     # then open /icon-picker.html
"""
import html
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
rows = [l.split("\t") for l in (ROOT / "tools" / "section-art-map.tsv").read_text().split("\n")
        if l.strip() and not l.startswith("#")]
choose = [r for r in rows if r[4] == "choose"]
decided = [r for r in rows if r[4] == "new"]


def card(name, key):
    return (f'<figure><lord-icon src="https://cdn.lordicon.com/{key}.json" '
            f'colors="secondary:#2a76dd" trigger="loop" delay="1200"></lord-icon>'
            f'<figcaption><a href="https://lordicon.com/icon/{key}/wired/outline" '
            f'target="_blank">{html.escape(name)}</a></figcaption></figure>')


def block(r, cls):
    names, keys = r[5].split("|"), r[6].split("|")
    return (f'<section class="{cls}"><h3>{html.escape(r[0])} &middot; {html.escape(r[2])}'
            f'<span class="slug">{html.escape(r[3])}.json</span></h3>'
            f'<p class="note">{html.escape(r[7])}</p><div class="row">'
            + "".join(card(n, k) for n, k in zip(names, keys)) + "</div></section>")


doc = f"""<!doctype html><meta charset="utf-8"><title>Divider icon picker</title>
<script src="https://cdn.lordicon.com/lordicon.js"></script>
<style>
 body{{font:16px/1.5 system-ui,sans-serif;margin:0;padding:2rem 2.5rem;color:#212529;max-width:1100px}}
 h1{{font-size:1.6rem;margin:0 0 .3rem}} h2{{margin:2.5rem 0 .5rem;font-size:1.15rem;
   border-bottom:2px solid #2780e3;padding-bottom:.3rem}}
 .lede{{color:#495057;margin:0 0 1.5rem}}
 section{{border:1px solid #e9ecef;border-left:3px solid #2780e3;border-radius:5px;
   padding:.9rem 1.1rem;margin:.9rem 0;background:#fff}}
 section.clash{{border-left-color:#b03a2e}}
 h3{{margin:0;font-size:1rem}} .slug{{color:#6c757d;font-weight:400;font-size:.85rem;margin-left:.6rem}}
 .note{{color:#495057;font-size:.9rem;margin:.35rem 0 .6rem}}
 .row{{display:flex;gap:1.4rem;flex-wrap:wrap}}
 figure{{margin:0;text-align:center;width:130px}}
 lord-icon{{width:110px;height:110px}}
 figcaption{{font-size:.78rem;word-break:break-word}}
 figcaption a{{color:#2780e3;text-decoration:none}} figcaption a:hover{{text-decoration:underline}}
 .decided .row figure{{width:110px}} .decided lord-icon{{width:90px;height:90px}}
</style>
<h1>Divider icon picker</h1>
<p class="lede">Previews come from the CDN, which per <code>ICONS.md</code> serves older
revisions than the PRO web app: fine for deciding, <strong>not</strong> for downloading.
Export the one you pick from the Lordicon UI with secondary set to <code>#2a76dd</code>.
Names link to the icon page.</p>
<h2>Open choices ({len(choose)})</h2>
{"".join(block(r, 'clash' if 'CLASH' in r[7] else '') for r in choose)}
<h2>Already decided ({len(decided)}) &mdash; sanity check these too</h2>
<div class="decided">{"".join(block(r, '') for r in decided)}</div>
"""

out = ROOT / "_site" / "icon-picker.html"
out.parent.mkdir(exist_ok=True)
out.write_text(doc)
print(f"wrote {out}: {len(choose)} open, {len(decided)} decided")
