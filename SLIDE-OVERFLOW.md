# Slide overflow — resolved

## Two font sizes (current)

Body text is **40px everywhere except dense slides, which are 32px (`.fs80`)**. Nine slides
keep a smaller stop as documented exceptions. Measured at 1920×1080 over 676 slides:

| body size | slides | |
|---|---|---|
| 40px (no stop) | 556 | |
| 32px (`.fs80`) | 111 | |
| 28px (`.fs70`) | 7 | exceptions, listed below |
| 24px (`.fs60`) | 2 | exceptions, listed below |

Before this pass the decks used five sizes: 516 slides at 40px, 83 at `.fs90`, 4 at
`.fs80`, 70 at `.fs70`, 3 at `.fs60`. **`.fs90` and the old `.fs60` uses are gone.** The
classes still exist in `styles.css` and are still correct to use; they are simply not the
house sizes.

Fifty-five of the scaled slides did not need scaling at all and went to full size. That was
the largest single win, and it suggests the stops had accumulated from the modernization
overflow described below and were never revisited after the stylesheet fixes removed the
cause.

**The exceptions**, all genuinely too dense for 32px:

| deck | slide | stop |
|---|---|---|
| `A/01/b` | Communicating with R | `.fs70` |
| `A/02/a` | File Management | `.fs70` |
| `A/02/b` | Vectors | `.fs70` |
| `A/03/a` | Strings | `.fs70` |
| `A/03/a` | Packages | `.fs70` |
| `A/03/b` | Data Visualization | `.fs70` |
| `C/08/b` | Predicting energy expenditure | `.fs70` |
| `C/08/b` | Interpreting coefficients | `.fs60` |
| `C/08/b` | Proceed with caution | `.fs60` |

Everything else that did not fit at 32px was reworded rather than shrunk, mostly by
tightening bullets that wrapped a word or two onto a second line. Removing one such wrapped
line frees about 46px at `.fs80`, which is usually the whole deficit.

Two slides sit at **+1px**, `A/03/b` Tidy Data and Tidying Example 3. Both are image-driven
and nothing is clipped. The sweep below used >10px as the bar for the same reason.

⚠️ **Do not probe font stops by toggling the class in the DOM.** It reports slides as
fitting that do not. Slides carrying a Lottie icon (`{{< lif ... >}}`) were the worst
offenders: the component does not resize on a class change, so the measurement misses the
height the real render produces. Thirteen slides passed a DOM probe and then overflowed by
up to +457px once actually rendered. Change the source, render, and measure that.

⚠️ **Index slides by their position among `## ` headings, not by title.** Several decks
repeat a title, and reading the title out of the DOM also drags in KaTeX's duplicate math
text and smart quotes. The rendered `section.level2` list is the right key, but a vertical
**stack** is also `.level2` and owns no heading, so filter on a direct `h2` child or every
slide after the stack is off by one.

---

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

## Resolved: 0 overflowing slides in all 23 decks

Swept at 1920×1080, 743 slides, **0 overflowing and 0 wrapping titles.** The old
"remaining 4" list below is superseded: it used pre-restructure week ids and was measured
in a small window.

Eighteen slides were over. Seventeen were fixed with a **font stop**, chosen per slide as
the largest stop that reaches 0 rather than the smallest that looked safe:

| deck | slide | was | stop |
|---|---|---|---|
| `B/04/b` | A complication | +43 | `.fs80` |
| `B/04/b` | Comparing CIs | +28 | `.fs90` |
| `B/05/a` | What is a hypothesis? | +42 | `.fs90` |
| `B/05/a` | The *p*-value of a test | +56 | `.fs90` |
| `B/05/b` | Correlations | +44 | `.fs90` |
| `B/05/b` | Another effect size | +45 | `.fs90` |
| `B/06/a` | Paired samples *t*-test | +15 | `.fs90` |
| `B/06/b` | Example dataset | +40 | `.fs90` |
| `B/06/b` | The F distribution | +105 | `.fs90` |
| `B/06/b` | Application and interpretation | +34 | `.fs90` |
| `C/07/a` | Standardized Slopes | +42 | `.fs90` |
| `C/07/b` | Estimating means by hand | +68 | `.fs80` |
| `C/07/b` | Effect sizes | +31 | `.fs90` |
| `C/07/c` | Multiple regression | +101 | `.fs80` |
| `C/07/c` | Controlling predictors | +22 | `.fs90` |
| `C/08/b` | Proceed with caution | +56 | `.fs60` (was already `.fs70`) |
| `D/10/a` | Assumption | +54 | `.fs90` |

The two worst, at +105 and +101, had been expected to need splitting. They did not: both
clear at `.fs80`. Measuring every stop before choosing beat guessing from the size of the
overflow.

**`B/06/c` "Further partitioning" (+49) is the exception** and got a CSS fix instead,
because a font stop would not have held. Its overflow comes from the mermaid diagram, whose
height is scale-dependent (see above), not from the text a font stop shrinks. `styles.css`
now caps `svg.mermaid-js` at 210 slide-px with `width: auto`, which pins it at that height
from 1050×700 through 2560×1440. Verified at four viewports.

Three titles are ambiguous in source and must be located by **ordinal**, not by text:
`C/07/b` has two "Estimating means by hand" and three "Effect sizes"; `D/10/a` has five
"Assumption". Only one of each was over.

⚠️ **Hard-won: the browser caches `styles.css` across iframe loads.** After a stylesheet
change the sweep reported `B/06/c` still at +49 while the rule was present in `_site` and
worked when injected live. Append a cache-busting query when re-measuring after a CSS edit,
or the result is stale and looks like the fix failed.

### Titles that wrap to two lines — none

Swept all 23 decks: **0 wrapping `h2` titles.** The five that were found (all in Unit A)
have been reworded:

| deck | was | now |
|---|---|---|
| `A/02/b` | Pitfall: Cannot Start with a Number or Underscore | Pitfall: Names Must Start with a Letter |
| `A/02/b` | Some Functions Transform Each Element | Functions That Transform |
| `A/02/b` | Other Functions Summarize the Whole Vector | Functions That Summarize |
| `A/03/b` | Pitfall: Columns Must Be the Same Length | Pitfall: Unequal Column Lengths |
| `A/03/b` | Covariation of Two Continuous Variables | Two Continuous Variables |

**About 35 characters is the limit** at 64px against the 1050px canvas — the shortest
that wrapped was 37, the longest that did not was 31. A wrap costs ~77px, which is
usually free space rather than overflow, so this is a typography rule and not a layout
bug. Divider (`#`) and title slides are excluded: those are display type and are meant
to wrap.

Note the last two rewordings above: `Functions That Transform` / `Functions That
Summarize` keep the contrast the pair was built on while dropping the
`Some…`/`Other…` scaffolding, and `Two Continuous Variables` works because the
surrounding slides already establish that the section is about covariation.

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
