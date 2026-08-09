# Slide overflow — resolved

**The original Fall 2025 decks did not have this problem.** The overflow was introduced by
importing data2's configuration wholesale in Phase 1. It is now fixed.

| | overflowing slides (of 602) |
|---|---|
| original Fall 2025 decks | ~2 (sampled) |
| after modernization | 55 |
| after stylesheet fixes | 21 |
| **after `echo` fix (current)** | **4** |

Remaining: `B/08/a` Post-hoc tests (+50), `C/10/b` Example zero-order effects (+53),
`C/10/a` Relation to Student's t-test (+26), `B/08/a` Further partitioning (+16). All minor —
a line or two each. 20 of 24 decks are completely clean.

⚠️ Every deck id on this page is from the **pre-restructure week numbering**, which the
Unit → Chapter → Lecture renumbering has since replaced. Treat them as historical labels; the
counts above have not been re-measured against the current chapters.

## Re-measured decks

`C/09/a` — **clean**, 0 of 32 slides overflowing. It was carried in `MAINTENANCE.md` §7 as a
suspected two-slide overflow ("Motivation" +144, "Power polynomials" +210), from a clone-based
side measurement during the divider work. Measured directly with the script below, both slides
fit exactly; the clone numbers were an artifact. What the direct measurement *did* find was one
real overflow the clone had missed — "Adding moderation", +38px — fixed by moving that slide
from `.fs90` to `.fs80` (`.fs70` was not needed; either stop brings it to 0).

## What went wrong

data2's config is written for a coding course with sparse slides. This is a stats course with
dense slides. Three separate settings came across that shouldn't have:

### 1. `echo: true` in `_quarto.yml` — the big one

data2 sets this because showing code *is* the lesson there. It overrides revealjs's default of
`echo: false`, exposing plumbing code these slides were written to hide.

Verified defaults by rendering a bare chunk: **html → code shown, revealjs → code hidden.**

| deck | original visible code blocks | with `echo: true` |
|---|---|---|
| C/09/b | 33 | 57 |
| B/05/b | 24 | 48 |
| B/07/b | 33 | 45 |
| B/08/a | 24 | 33 |

Fixed by *removing* the line rather than setting `echo: false`, so each format uses its own
default: slides hide code unless a chunk opts in with `#| echo: true`, while HTML week pages
and assignments still show it. All four decks above now match their originals exactly.

### 2. Missing font utilities in `styles.css`

The archive's per-unit stylesheets define `.f4`, `.f5`, `.f6`, `.f90`; data2's defines only `.f3`.
The slides use them **132 times**, so every one was a silent no-op. Also lost: `.pb4`,
`.full-width`, `.tiny-text`. Restored with the values all four archive stylesheets agreed on.

### 3. Spacing rules in `styles.css`

- `.reveal h2 { margin-bottom: 0.75em }` — every slide heading, ~50% of the remaining overflow
- `.reveal div.sourceCode` padding `10px` + margin-bottom `1rem` — ~39%

Dropped the h2/h4 margins; reduced padding to `4px 10px` and margin to `0.4rem`. data2's
cell-output colour styling is **kept** — it costs no vertical space and is a real improvement.

## Two traps worth remembering

**Freeze caches config, not just code.** `_freeze` keys on source hash, so changing
`_quarto.yml`, `_slide-settings.yml`, or `_common.R` has **no effect** until you clear it. The
`echo` fix appeared to do nothing until:

```bash
rm -rf _freeze && quarto render
```

**Measure after MathJax typesets.** Raw LaTeX wraps taller than rendered math, so measuring too
early reports phantom overflow — B/07/a appeared to have a +288px slide that is actually 0.
Wait for typesetting before measuring.

## How to measure

Do **not** force `height: auto` on hidden sections — reveal resizes `.r-stretch` images to fit,
and overriding layout defeats that (B/06/b "Scatterplots" measured +547px that way; actually
+1px). In the console of a served deck, after the page has fully settled:

```js
Reveal.configure({transition:'none', fragments:false});
const H = Reveal.getConfig().height;
for (const s of [...document.querySelectorAll('.reveal .slides section')]
       .filter(s => !s.querySelector(':scope > section'))) {
  const i = Reveal.getIndices(s); Reveal.slide(i.h, i.v);
  await new Promise(r => setTimeout(r, 12));
  const cur = Reveal.getCurrentSlide(), o = cur.scrollHeight - H;
  if (o > 10) console.log(o, cur.querySelector('h1,h2,h3')?.innerText);
}
```

## The lesson

**Do not sync `styles.css` or `_quarto.yml` from data2 or psyc894.** Each course's slides are
authored against their own spacing and echo conventions. The files share names and lineage but
are not interchangeable — that assumption caused every problem on this page.
