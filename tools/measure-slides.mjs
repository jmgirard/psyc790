// Sweep every rendered deck in _site for the four layout faults that matter,
// and write the findings to tools/report.json for bump-stops.py and
// locate-widow.py to consume.
//
//   node tools/measure-slides.mjs            all decks
//   node tools/measure-slides.mjs C/08/b     one deck
//
// Runs against _site over file://, so nothing needs serving. Render first:
// stale HTML measures clean while the source is broken.
//
// Three ways this measurement lies, all of them learned the hard way and all
// written up in SLIDE-OVERFLOW.md. In short: measure at 1920x1080 because
// overflow is not scale-invariant; drop .katex-mathml and treat a whole .katex
// span as one token or every heading with math reports as wrapped; and check
// pre.scrollHeight too, because content clipped inside a child's own scrollbar
// leaves the section itself reporting a comfortable fit.
import { withBrowser } from "./cdp.mjs";
import { writeFileSync, readdirSync, existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join, resolve } from "node:path";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const SITE = join(ROOT, "_site");

function allDecks() {
  const out = [];
  for (const unit of readdirSync(ROOT).filter((d) => /^[A-E]$/.test(d))) {
    for (const chap of readdirSync(join(ROOT, unit)).sort()) {
      const dir = join(ROOT, unit, chap);
      let files = [];
      try { files = readdirSync(dir); } catch { continue; }
      for (const f of files.sort()) {
        const m = /^([a-z])_Slides\.qmd$/.exec(f);
        if (m) out.push(`${unit}/${chap}/${m[1]}`);
      }
    }
  }
  return out;
}

const decks = process.argv.slice(2).length ? process.argv.slice(2) : allDecks();
if (!existsSync(SITE)) {
  console.error(`No _site at ${SITE}. Run \`quarto render\` first.`);
  process.exit(1);
}

const PAGE_FN = `(async () => {
  Reveal.configure({ transition: 'none', fragments: false });
  const H = Reveal.getConfig().height;

  // A vertical stack is also .level2 but owns no heading of its own, so indexing
  // on the raw list puts every slide after it off by one. Require a direct h2:
  // this index is what addresses a slide back in the source, as the k-th "## ".
  const level2 = [...document.querySelectorAll('.reveal .slides section.level2')]
    .filter(s => s.querySelector(':scope > h2'));

  function tokens(node, acc) {
    for (const n of node.childNodes) {
      if (n.nodeType === 3) {
        const re = /\\S+/g; let m;
        while ((m = re.exec(n.nodeValue))) {
          const r = document.createRange();
          r.setStart(n, m.index); r.setEnd(n, m.index + m[0].length);
          const b = r.getBoundingClientRect();
          if (b.width > 0.5 && b.height > 0.5)
            acc.push({ w: m[0], top: b.top, bottom: b.bottom, left: b.left, right: b.right });
        }
      } else if (n.nodeType === 1) {
        const t = n.tagName;
        if (t === 'UL' || t === 'OL' || t === 'ASIDE' || t === 'PRE') continue;
        if (n.classList.contains('katex-mathml')) continue;
        if (n.classList.contains('katex')) {
          const b = n.getBoundingClientRect();
          if (b.width > 0.5)
            acc.push({ w: 'M', display: !!n.closest('.katex-display'),
                       top: b.top, bottom: b.bottom, left: b.left, right: b.right });
          continue;
        }
        const cs = getComputedStyle(n);
        if (cs.display === 'none' || cs.visibility === 'hidden') continue;
        tokens(n, acc);
      }
    }
  }

  function lines(el) {
    const acc = []; tokens(el, acc);
    if (!acc.length) return [];
    const lh = parseFloat(getComputedStyle(el).lineHeight) || 20;
    const tol = Math.max(4, lh * 0.5);
    acc.sort((a, b) => (a.top + a.bottom) / 2 - (b.top + b.bottom) / 2 || a.left - b.left);
    const out = []; let cur = null;
    for (const t of acc) {
      const mid = (t.top + t.bottom) / 2;
      if (!cur || Math.abs(mid - cur.mid) > tol) { cur = { mid, toks: [t] }; out.push(cur); }
      else cur.toks.push(t);
    }
    for (const l of out) l.toks.sort((a, b) => a.left - b.left);
    return out;
  }

  const out = { over: [], clipped: [], wrapTitles: [], widows: [], slides: 0 };
  for (const s of [...document.querySelectorAll('.reveal .slides section')]
        .filter(s => !s.querySelector(':scope > section'))) {
    const i = Reveal.getIndices(s);
    Reveal.slide(i.h, i.v);
    await new Promise(r => setTimeout(r, 25));
    const cur = Reveal.getCurrentSlide();
    out.slides++;
    const k = level2.indexOf(cur);                       // -1 for level-1 dividers
    const title = (cur.querySelector('h1,h2,h3')?.innerText || '(untitled)')
                    .trim().replace(/\\s+/g, ' ');
    const stop = [...cur.classList].find(c => /^fs\\d+$/.test(c)) || 'none';
    const base = { k, title, stop };

    const o = Math.round(cur.scrollHeight - H);
    if (o > 0) out.over.push({ ...base, o });
    for (const pre of cur.querySelectorAll('pre')) {
      const hidden = Math.round(pre.scrollHeight - pre.clientHeight);
      if (hidden > 10) { out.clipped.push({ ...base, hidden }); break; }
    }
    const h2 = cur.querySelector('h2');
    if (h2 && lines(h2).length > 1) out.wrapTitles.push(base);

    for (const el of cur.querySelectorAll('li, p')) {
      if (el.closest('aside.notes, pre, .katex-display, figcaption')) continue;
      if (el.tagName === 'P' && el.closest('li')) continue;
      const cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden') continue;
      const ls = lines(el);
      if (ls.length < 2) continue;
      const last = ls[ls.length - 1];
      if (last.toks.length > 2) continue;
      // A display equation alone on a centred line is not a widow, and neither
      // is a last line still filling half its column, which is what an inline
      // formula as wide as the column produces.
      if (last.toks.every(t => t.display)) continue;
      const box = el.getBoundingClientRect();
      const px = last.toks[last.toks.length - 1].right - last.toks[0].left;
      if (px / box.width >= 0.5) continue;
      out.widows.push({ ...base,
        widow: last.toks.map(t => t.w).join(' '),
        lastPx: Math.round(px), boxPx: Math.round(box.width),
        text: ls.map(l => l.toks.map(t => t.w).join(' ')).join(' ') });
    }
  }
  return out;
})()`;

const report = {};
let slides = 0;
await withBrowser(async (page) => {
  for (const deck of decks) {
    const file = join(SITE, `${deck}_Slides.html`);
    if (!existsSync(file)) { console.error(`  missing render: ${deck}`); continue; }
    await page.goto("file://" + file);
    await page.eval("new Promise(r => setTimeout(r, 900))");   // let MathJax/KaTeX settle
    report[deck] = await page.eval(PAGE_FN);
    slides += report[deck].slides;
    process.stderr.write(".");
  }
});

writeFileSync(join(ROOT, "tools/report.json"), JSON.stringify(report, null, 1));
const n = (f) => Object.values(report).reduce((a, r) => a + r[f].length, 0);
console.log(`\n${slides} slides | overflow ${n("over")} | clipped ${n("clipped")} | ` +
            `wrapping titles ${n("wrapTitles")} | widows ${n("widows")}`);
for (const [deck, r] of Object.entries(report)) {
  for (const x of r.over) console.log(`  OVER  ${deck} h2#${x.k} .${x.stop} +${x.o}  ${x.title}`);
  for (const x of r.wrapTitles) console.log(`  TITLE ${deck} h2#${x.k} .${x.stop}  ${x.title}`);
  for (const x of r.clipped) console.log(`  CLIP  ${deck} h2#${x.k} +${x.hidden}  ${x.title}`);
  for (const x of r.widows)
    console.log(`  WIDOW ${deck} h2#${x.k} «${x.widow}» ${x.lastPx}/${x.boxPx}px  ${x.title}`);
}
