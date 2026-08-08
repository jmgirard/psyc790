# Maintaining this site

Operational notes for whoever is keeping these materials up to date. The *content*
decisions live in the pages themselves; this file records the things that are easy to
get wrong and expensive to rediscover.

Companion files: [`ICONS.md`](ICONS.md) (Lordicon workflow), [`SLIDE-OVERFLOW.md`](SLIDE-OVERFLOW.md)
(slide layout regressions), [`CREDITS.md`](CREDITS.md) (third-party figures, data, licenses).

---

## 1. Layout

```
_quarto.yml            website project; navbar with one dropdown per unit
_slide-settings.yml    shared revealjs metadata; `filters: [jmgirard/lordicon]`
_common.R              knitr source hook (replace_path)
_extensions/jmgirard/  details, honeypot, lordicon
_freeze/               COMMITTED (freeze: auto) -- this is the reproducibility mechanism
.nojekyll              committed
CNAME                  stats.jmgirard.com
install-packages.R     unpinned CRAN list + standist from GitHub
index.qmd              front door; schedule.qmd is the chapter index; 404.qmd
styles.css             single shared stylesheet, root only
icons/ img/ data/
A/01/ ... E/15/        one folder per chapter, grouped by unit letter
  index.qmd            chapter hub: per lecture -- Topics / Files / Readings / Slides iframe
  a_Slides.qmd         revealjs; metadata-files: ../../_slide-settings.yml
  a_practice.qmd       in-class practice, answers in {{< dstart >}} blocks (public)
  a_assignment.qmd     three questions, each naming its own dataset and model
  translation.qmd      unit-closing activity (B/06, C/09, D/10 only)
archive/               pre-modernization Fall 2025 source; excluded from the render
```

Vocabulary is **Unit → Chapter → Lecture**. A lecture is one ~90-minute block, which is a
content constraint worth keeping. Assignments attach to lectures rather than chapters, so a
skipped lecture drops its assignment and nothing cascades.

### Two rules the structure depends on

**Semester-agnostic.** Nothing on the site names a semester, meeting time, office hour, due
date, grade, or prerequisite-as-policy. Those belong to whoever is running the course. This
is why `_slide-settings.yml` carries `attribution` but no `semester`, `course`, or
`instructor`.

**Links run one way.** An LMS links *in*; nothing here links back out to a particular course
site. There is deliberately no `canvas-id`, no LMS navbar entry, and no "download this from
Canvas" — datasets are served from this site's own `data/`.

---

## 2. Building and publishing

```bash
quarto render
```

```bash
quarto publish gh-pages
```

`main` holds the source; `quarto publish gh-pages` pushes the rendered site to the
`gh-pages` branch, which Pages serves at `stats.jmgirard.com`. `_site/` is gitignored,
`_freeze/` is committed. There is no CI workflow — publishing is a local command.

Three things that have bitten before:

- **`CNAME` must reach the published branch on every deploy**, or Pages drops the custom
  domain and falls back to `github.io`. It is listed under `project: resources:` for that
  reason; don't remove it.
- **`quarto publish --no-render` uploads `_site/` as-is.** If a page or asset was deleted
  since the last full render, the stale copy is still sitting in `_site/` and gets
  republished. Re-render before publishing whenever anything was removed.
- **`archive/` must stay out of the render.** A Quarto website project renders *every*
  `.qmd` it finds. Only the `!archive/**` negation in `_quarto.yml` excludes it — the
  glob-list form does not. Verify with `quarto inspect`, which should report zero inputs
  under `archive/`. This is not cosmetic: it once wrote fully rendered answer keys into
  `_freeze/archive/`.

---

## 3. Packages and freeze

**No renv, deliberately.** `_freeze/` is the reproducibility mechanism: frozen chunk results
are committed, so a package update cannot change the live site until a page is deliberately
re-rendered. renv was dropped from all three courses after an R 4.6.1 upgrade stranded a
renv library at R-4.5 — activation silently put an empty library on the path and every
render failed at `library(here)`. A pinned environment that no longer resolves is worse than
no pinning, because it fails at render time rather than install time.

`install-packages.R` replaces it: an unpinned list of the CRAN packages the course uses,
plus `standist` from GitHub. It is served from the site so setup instructions can point at
`/install-packages.R`.

### Freeze hides package drift, by design

`freeze: auto` re-executes only when the **source** changes, never when packages update.
That is what keeps the published site stable, but it also means drift stays invisible until
execution is forced. There is no `--no-freeze` flag; clear the cache instead:

```bash
rm -rf _freeze && quarto render
```

Worth doing once before each offering, so drift is met deliberately rather than by a student
mid-semester.

**Freeze also caches config, not just code.** The cache keys on source hash, so editing
`_quarto.yml`, `_slide-settings.yml`, or `_common.R` has *no effect* on already-frozen pages
until the cache is cleared. Changes to those files have appeared to do nothing for exactly
this reason.

Known drift as of the last full re-render: `qplot()` is deprecated in ggplot2 (still
functional, but it warns). It is used as a teaching section in `A/03/b_Slides.qmd`, and
`A/03/b_assignment.qmd` instructs students to use it. Replacing it with `ggplot()` calls is
a teaching-content decision, not a mechanical fix.

---

## 4. Answer keys stay off GitHub

The graded keys are **not in this repo and must never be.** They are handled privately;
[`index.qmd`](index.qmd) tells instructors to email for them.

Two different things get called an answer key, and only one is sensitive:

- **Practice answers** — the `{{< dstart summary="Answer key" >}}` blocks inside
  `*_practice.qmd`. These are public on purpose.
- **Graded keys** — assignment answers. These must not be published. They also **leak the
  honeypot design**: each key opens with a line naming the trap it uses (e.g. a homoglyph
  mid-dot), which documents exactly how the `{{< hp >}}` LLM traps work across all three
  courses.

`.gitignore` blocks them, and the rules cover **derived artifacts, not just sources**
(`*_key.*`, `_freeze/archive/`, …). The source-only rule was not enough: rendered keys —
honeypot markers and all — once landed in `_freeze/` and were committed across 16 commits
before being caught. Nothing had been pushed, so history was rewritten and the artifacts
purged.

If keys are ever rendered anywhere, their `_freeze` output is exactly as sensitive as the
source.

---

## 5. Copyright

`.gitignore` also blocks `*.pdf`/`*.epub`/`*.docx`/`*.pptx` and `readings/`. Course readings
that are copyrighted textbook chapters must never be committed — this repo and its site are
both public. Chapter pages link to open-access sources directly; anything paywalled is the
LMS's job.

Everything else is settled and recorded in [`CREDITS.md`](CREDITS.md): four attributed
third-party figures, six borrowed figures redrawn as original ggplot code, unDraw
illustrations (no attribution required), and the Lordicon PRO license, which explicitly
permits self-hosting the Lottie JSON.

One open item, carried in `CREDITS.md`: `traincar.png` and the other stock-sourced
composites may owe a Vecteezy credit if the original downloads can be identified.

---

## 6. Do not sync config from `data2` or `psyc894`

The three course repos share names and lineage but their configs are **not
interchangeable**. Importing `data2`'s wholesale is what caused every problem recorded in
[`SLIDE-OVERFLOW.md`](SLIDE-OVERFLOW.md) — 55 overflowing slides, from three settings:

- **`echo: true` in `_quarto.yml`** — right for a coding course, wrong here. It overrides
  revealjs's `echo: false` and exposes plumbing code these slides were written to hide. It
  is deliberately *absent* rather than set to `false`, so each format keeps its own default.
- **Missing font utilities in `styles.css`** — `.f4`/`.f5`/`.f6`/`.f90` are used 132 times
  here and did not exist in data2's stylesheet, so every call was a silent no-op.
- **Spacing rules** — heading margins and `sourceCode` padding differ on purpose, because
  these decks carry more code per slide.

`styles.css` carries comments at each of these points explaining why the value differs.
Leave them there.

---

## 7. Still to do

**Unbuilt chapters.** Numbered and placeholdered so adding them needs no renumber; each
`index.qmd` carries the intended outline.

| | |
|---|---|
| `C/09` lecture b | Piecewise and Spline Regression |
| `D/11` | Bootstrap and Robust Inference |
| `D/12` | Missing Data |
| `E/13` | Reliability and Measurement Error |

When these land, [`index.qmd`](index.qmd)'s "About the Course" paragraph and the learning
outcomes list both need updating — they currently describe only the built material.

**Dataset refresh — tail.** Reuse is the design, not the problem: a dataset that carries
five chapters is one students orient to once. The *spine* is done (`penguins` replaced the
retired `salaries.csv` rung for rung). What is left is nine datasets used exactly once each,
which is where the real orient-once-per-lecture tax lives.

- `gpa.csv` and `gradebook.csv` sit in `data/` referenced by nothing.
- `yearspubs.csv` (C/07c, C/09b) still regresses academic `salary` on `sex` — the same
  contentiousness that retired `salaries.csv`. Flagged, deliberately not changed.
- Ruled out as spines, with numbers, so they are not re-tested: `exercise.csv` (negative
  `expenditure` values, no sex effect, main effects near zero — built for the C/08
  interaction only) and `psych::bfi` (non-monotonic education effect, R² = .02, gender its
  only dichotomous variable).
- Adding `carData`/`psych` built-ins was considered and rejected: it *adds* datasets to
  learn. Consolidate onto existing ones instead.

**Factorial ANOVA vocabulary bridge.** Factorial ANOVA is already taught, as
categorical-by-categorical moderation in the GLM. What is missing is two slides of
vocabulary plus Type I/II/III sums of squares (`afex` is already a dependency and already
defaults to Type III).

**`_brand.yml`.** `_quarto.yml` declares `theme: [cosmo, brand]` but no `_brand.yml` exists,
here or in the other two repos. It renders fine; worth confirming it is intentional.
