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

## Re-measured: all 23 decks, current numbering

Full sweep at 1920×1080, 750 slides. **18 slides overflow, in 11 decks.** The other 12 decks
are clean. No slide anywhere still clips content inside a `<pre>`.

| deck | slide | over |
|---|---|---|
| `B/04/b` | A complication | +43 |
| `B/04/b` | Comparing CIs | +28 |
| `B/05/a` | What is a hypothesis? | +42 |
| `B/05/a` | The *p*-value of a test | +56 |
| `B/05/b` | Correlations | +44 |
| `B/05/b` | Another effect size | +45 |
| `B/06/a` | Paired samples *t*-test | +15 |
| `B/06/b` | Example dataset | +40 |
| `B/06/b` | The F distribution | +105 |
| `B/06/b` | Application and interpretation | +34 |
| `B/06/c` | Further partitioning | +49 (mermaid; scale-dependent, see above) |
| `C/07/a` | Standardized Slopes | +42 |
| `C/07/b` | Estimating means by hand | +68 |
| `C/07/b` | Effect sizes | +31 |
| `C/07/c` | Multiple regression | +101 |
| `C/07/c` | Controlling predictors | +22 |
| `C/08/b` | Proceed with caution | +56 |
| `D/10/a` | Assumption | +54 |

The old "remaining 4" list below is superseded — it used pre-restructure week ids and was
measured in a small window. Unit B and the first half of Unit C hold all but two of these.

### Titles that wrap to two lines

Five, all in Unit A, all `h2` content-slide titles at 64px against the 1050px canvas. Each
costs ~77px of vertical space on a slide that has room to spare, so they are a typography
problem rather than an overflow one.

| deck | title |
|---|---|
| `A/02/b` | Pitfall: Cannot Start with a Number or Underscore |
| `A/02/b` | Some Functions Transform Each Element |
| `A/02/b` | Other Functions Summarize the Whole Vector |
| `A/03/b` | Pitfall: Columns Must Be the Same Length |
| `A/03/b` | Covariation of Two Continuous Variables |

Roughly 40 characters is the limit at 64px. Divider (`#`) and title slides are excluded —
those are display type and are meant to wrap.

### Resolved

`C/09/a` was carried in `MAINTENANCE.md` §7 as a suspected two-slide overflow ("Motivation"
+144, "Power polynomials" +210), from a clone-based side measurement during the divider work.
Measured directly, both slides fit exactly; the clone numbers were an artifact. The direct
measurement did find one real overflow the clone had missed — "Adding moderation", +38 — fixed
by moving that slide from `.fs90` to `.fs80`. The deck is now 0 of 32.

`A/02/a` swept clean at every window size while actually hiding about half of three slides'
content inside `<pre>` scrollbars; see the clipping note above and `MAINTENANCE.md` §1.

## Three ways the measurement itself lies

All three were found re-measuring the current decks, and all three make the script below
report **fewer** problems than a projector shows. Fix them before trusting a sweep.

**Measure at presentation size.** Overflow is not scale-invariant. Reveal's canvas is a fixed
1050×700 no matter the window, so it *ought* to be — but `B/06/c`'s "Further partitioning"
reads 0 in a 744px-wide pane, +11 at 1050, +21 at 1280, and +49 at 1920×1080. The cause is
the deck's one **mermaid** diagram: mermaid lays itself out from unscaled device text metrics
while sitting inside reveal's CSS-transformed canvas, so its viewBox aspect changes with deck
scale (566×216 small, 955×274 at 1080p) and its height at a fixed 1050px width changes with
it. Only `B/06/c` has a mermaid diagram, so only that slide is affected today — but any new
one will behave the same way. Measure at 1920×1080, not in whatever window is open.

**`scrollHeight` misses content clipped *inside* a child.** A slide whose overflow is hidden
in a `<pre>`'s own scrollbar reports 0, because reveal's section fits fine. `A/02/a`'s three
"Live Coding" slides hid about half their steps that way and swept clean every time. Check
`pre.scrollHeight - pre.clientHeight` per slide as well.

**KaTeX breaks line counting.** Any check that counts line boxes in a heading must drop
`.katex-mathml` (a hidden duplicate of the whole expression — it doubles `innerText` too) and
then cluster the remaining rect tops by line-height, since sub/superscript boxes sit at their
own tops inside one visual line. Without both, every heading containing math reports as
wrapped: `B/05/a` alone gave eight false positives.

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
