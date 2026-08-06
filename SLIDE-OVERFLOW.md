# Slide overflow — a regression from the modernization

**Jeff's instinct was right: the original Fall 2025 decks did not have this problem.** The
overflow was introduced by adopting data2's `styles.css` wholesale in Phase 1, not by
pre-existing content density.

## The evidence

Original archive decks were re-rendered against their own per-unit stylesheets and measured
identically (reveal logical size 1050 × 700, every slide visited, `fragments: false`):

| deck | ORIGINAL | after modernization | after fixes |
|---|---|---|---|
| B/05/b | **0 slides, 0px** | 7 slides, 546px | 3 slides, 192px |
| B/07/b | **0 slides, 0px** | 4 slides, 454px | 1 slide, 235px |
| C/09/b | 1 slide, 57px | 6 slides, 756px | 3 slides, 500px |
| B/08/a | 2 slides, 97px | 2 slides, 501px | 2 slides, 396px |

## What caused it

data2's stylesheet was written for data2's slides, which are far less dense. Three separate
problems came across with it:

1. **Missing font utilities.** psyc790's per-unit stylesheets define `.f4`, `.f5`, `.f6`,
   `.f90`; data2's defines only `.f3`. The slides use those **132 times**, so every one was a
   silent no-op and text rendered at full size. *(Also lost: `.pb4`, `.full-width`,
   `.tiny-text`.)*
2. **`.reveal h2 { margin-bottom: 0.75em }`** — applies to every slide heading. Accounted for
   **~50%** of the remaining overflow on B/05/b.
3. **`.reveal div.sourceCode` padding (10px) and margin-bottom (1rem)** — psyc790 carries far
   more code per slide than data2. Accounted for **~39%**.

Isolated by A/B on B/05/b (baseline 7 slides / 546px):

| disabled | overflowing | total px |
|---|---|---|
| baseline | 7 | 546 |
| `.reveal h2` margin | 4 | 273 |
| sourceCode padding | 6 | 334 |
| cell-output padding | 7 | 546 *(no effect)* |
| all three | 2 | 135 |

## Fixes applied

- Restored `.f4` / `.f5` / `.f6` / `.f90` (and `.pb4`, `.full-width`, `.tiny-text`) with the
  values all four archive stylesheets agreed on.
- Dropped `.reveal h2 { margin-bottom }` and `.reveal h4 { margin-top }` — back to reveal
  defaults, as the originals had.
- Reduced sourceCode padding `10px` → `4px 10px` and margin-bottom `1rem` → `0.4rem`.

The cell-output colour styling from data2 (warning/message/error blocks, paired with
`format-outputs.html`) is **kept** — it costs no vertical space and is a genuine improvement.

## Where it stands

Sampled decks after the fixes:

| deck | before fixes | after |
|---|---|---|
| B/06/b | 6 | **0** |
| B/05/a | 5 | 1 (+13px) |
| C/10/b | 8 | 2 (worst +53) |
| B/05/b | 8 | 3 (worst +133) |
| B/07/b | 4 | 1 (+235) |
| C/09/b | 6 | 3 (worst +423) |
| C/13/a | 4 | 3 (worst +153) |
| B/08/a | 2 | 2 (worst +346) |

A handful of genuinely dense slides remain — these are the ones that were *also* slightly over
in the original (e.g. C/09/b "Defining a Line in General", B/08/a "Further partitioning").
Those are content problems, best fixed by splitting the slide or stepping the font down with
`{.f5}` / `{.f6}`.

## How to measure

Do **not** measure by forcing `height: auto` on hidden sections — reveal resizes `.r-stretch`
images to fit, and overriding the layout defeats that, giving large false positives (B/06/b
"Scatterplots" measured +547px that way; it was actually +1px).

In the browser console of a served deck:

```js
Reveal.configure({transition:'none', fragments:false});
const H = Reveal.getConfig().height;
for (const s of [...document.querySelectorAll('.reveal .slides section')]
       .filter(s => !s.querySelector(':scope > section'))) {
  const i = Reveal.getIndices(s); Reveal.slide(i.h, i.v);
  const cur = Reveal.getCurrentSlide(), o = cur.scrollHeight - H;
  if (o > 10) console.log(o, cur.querySelector('h1,h2,h3')?.innerText);
}
```

## Lesson for Katie's copy

Do not sync `styles.css` from data2 or psyc894. Each course's slides are authored against
their own spacing, and these stylesheets are not interchangeable.
