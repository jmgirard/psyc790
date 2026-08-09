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
_extensions/jmgirard/  details, lordicon
_freeze/               COMMITTED (freeze: auto) -- this is the reproducibility mechanism
.nojekyll              committed
CNAME                  stats.jmgirard.com
install-packages.R     unpinned CRAN list + standist from GitHub
index.qmd              front door; contents.qmd is the chapter index; 404.qmd
styles.css             single shared stylesheet, root only
icons/ img/ data/
A/ ... E/              one folder per unit
  _metadata.yml        `unit` letter and `unit-art` (that unit's title-slide illustration)
A/01/ ... E/15/        one folder per chapter, grouped by unit letter
  _metadata.yml        `chapter` number
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

### Title slides

Every deck opens with the same block, and only the heading differs:

```markdown
::: {.t-title}
::: {.t-eyebrow}
{{< meta course >}}
:::

# Working in RStudio

::: {.t-rule}
:::

::: {.t-meta}
Unit {{< meta unit >}} · Chapter {{< meta chapter >}} · Lecture {{< meta chapter >}}{{< meta lecture >}}
:::

::: {.t-attrib}
{{< meta attribution >}}
:::

![]({{< meta unit-art >}}){.t-art}
:::
```

Everything except the heading is metadata, so the *design* lives entirely in the `.t-*`
rules in `styles.css` and can be changed without touching 23 files. Two things follow from
that and are worth not undoing:

- **The topic is the `h1`, not the course name.** The course name is the eyebrow. The old
  layout gave the largest type on every deck to the one line that never changed.
- **`unit-art` is in the *unit's* `_metadata.yml`, not the deck's front matter.** Moving a
  chapter to a different unit stays a directory move with no file edits, and the deck
  front matter stays untouched — which is also what makes the freeze re-key below possible.

Changing this block is a **purely textual** edit: `{{< meta >}}` shortcodes are resolved
after knitr, so the frozen chunk output is unaffected. Rather than re-executing 22 decks
(and inviting package drift), re-key the freeze instead — see §3.

### Code slides show code *and* results

Unit A used to teach from "Live Coding" slides: one `eval: false` chunk holding a 50-line
lesson script, displayed as an unreadable scrollbox with no output. Those are gone —
each idea now gets its own slide with a small executed chunk, so the result appears under
the code. Three rules make this work here, and all three are easy to get wrong:

- **Every chunk needs an explicit `#| echo: true`.** This repo deliberately does not set
  `echo` globally (§6), so a chunk without it renders *output with no code*, which is worse
  than the scrollbox. This is also why slides cannot be copied from `data2` verbatim —
  `data2` relies on the global setting.
- **Parse errors cannot be executed at all.** `heart rate <- 93`, `1_heart_rate`,
  `_heart_rate`, `10 x 3`, `10 \ 3`, `9,876,543`, and `x <- 4 9 16 25` are syntax errors,
  so `#| error: true` does not help — the render fails. These stay `eval: false` with the
  expected message as a comment. *Runtime* errors (`average(x)`, `dyes + 1`,
  `str_to_title()` before loading stringr) do execute under `#| error: true` and show their
  real message, which is the better lesson.
- **Watch for chunks with side effects.** `install.packages()`, `browseVignettes()`, and
  `write_csv()` must stay `eval: false` or a render will install packages, open a browser,
  or write stray files into the chapter folder.

### The anatomy of a Unit A code slide

Unit A's code slides follow one shape. It was arrived at by measuring: 82 of them
filled anywhere from 0.18 to 0.94 of the canvas, and three different conventions were
in use for showing a failure.

```
## Title (≤ ~35 characters, or it wraps to two lines at 64px)

  code card  →  output card        one or more, knitr emits one pair per statement

::: {.takeaway}
One or two sentences naming the lesson.
:::
```

**Order is code, then result, then lesson.** The result is the punchline, so a lead-in
sentence above the code gives it away. Both placements were tried in the browser before
this was settled.

**`.takeaway`, not `::: aside`.** An aside is absolutely positioned near the slide
bottom, so the sentence explaining the code floated ~200px below it in grey small print
while the middle of the slide stayed empty — and it was only present on some slides.
`aside` is still right for a genuine footnote ("repeat this every 4–5 months"); it is
not right for the point of the slide. Figure slides are exempt: they already fill their
space, and a plot title carries the lesson.

**One slide per *idea*, not per line.** The rule was over-applied — `10 ^ 2` had a slide
to itself at 0.25 fill. Related variations belong on one slide as stacked cards; aim for
0.5–0.9 fill. Unit A is 143 slides where it was 154, and no code slide is under 0.38.

**Failures use one visual language.** Three treatments used to coexist:

| kind | how | result |
|---|---|---|
| runtime error | `#| error: true` | R's own message, pink card — **correct** |
| parse error | `#| error: true` | renders, but as knitr's `Error in parse(text = input): <text>:1:2:` wrapper, which no student ever sees |
| parse error | `eval: false` + `# Error:` comment | no card at all, so a failing line looked exactly like working code that was not run |

Runtime errors keep `error: true`. Parse errors use `eval: false` plus a `.r-error`
block holding the **console-accurate** message (see the block comment in `styles.css`).
Verify each message by running the line in a fresh R session — do not copy knitr's.

Note that the old list of "parse errors" was partly wrong: `heart-rate <- 93` and
`age@time2 <- 12` parse fine and fail at runtime with "object not found", so they are
real executed errors. `_heart_rate` gives "unexpected symbol", not "unexpected input".

Two things worth not undoing. `qplot()` is deprecated and warns, but it is kept because
`A/03/b_assignment.qmd` instructs students to use it — replacing it is a teaching-content
decision (§3). The warning fires once per session, so it appears on the first plot slide
only, which is exactly what a student sees in their own console. And chunks that read data
carry `#| replace_path: ["../../data/", ""]` so the slide shows `read_csv("penguins0.csv")`
while the render reads the real path; keep it on any data-reading chunk you add.

`A/02/a`'s three "Live Coding" slides are now gone too, and no deck has one. They had been
left alone on the theory that a UI walkthrough has no code to run and no output to show, so
the name was accurate. What that missed is that they had the *same* defect as the code ones:
each was a single 4-space-indented block holding 20-plus steps, so it rendered as a pale
grey `<pre>` with its own scrollbar and roughly half the steps cut off. `.instructions`,
the class wrapping them, had **no CSS anywhere** — not here, not in any of the four archive
unit stylesheets — so it never did anything. The class is now unused; do not reintroduce it.

They were unrolled into nine slides in the `A/01/b` idiom (`## Creating a Project`, bullets,
`[File > New Project...]{.b .blue}`, `<kbd>` for keystrokes, `.fragment` reveals) — which is
what `A/01/b` had already done to the same content when it came over from data2. Do not
"fix" these by copying data2's version: data2 still uses the 50-line `eval: false` scrollbox
this repo removed (§6).

Splitting freed enough room that none of the nine needs a font stop, so none carries one.

### Chapter-page resource lists

A lecture section on a chapter page offers up to four kinds of resource — **Files**,
**Readings**, **Practice**, **Assignment** — and each is opted into its styling from the
`.qmd`, as `### Files {.res-files}` and so on. Four rules to keep:

- **Add the class when you add the heading.** An unclassed `### Assignment` silently falls
  back to a plain grey bullet list and stops matching the other three.
- **Don't match on heading text or on ids.** Quarto numbers repeated ids down a page
  (`#files`, `#files-1`, `#files-2`), so an id-based rule would style the first lecture only.
- **The class lands on the wrapping `<section>`**, not the `h3` — that is Pandoc's
  section-divs behaviour, and the selectors in `styles.css` depend on it.
- **Readings entries are not all links.** Paywalled textbook chapters are deliberately plain
  text (§5), so the styling has to look right with no `<a>` inside the `li`.

Icons come from Bootstrap Icons, which Quarto already loads on every page because the navbar
uses `icon: list-ul`. No new dependency.

### Slide footers

Two things about `.reveal .footer` that are easy to break:

- **It lives outside reveal's scaled canvas.** Quarto attaches it to `.reveal`, not to
  `.slides`, so anything sized in px there ignores the deck scale — a flat `0.5em` (20px)
  stayed 20px while the slide text shrank, and in the embedded chapter-page iframe (scale
  ≈0.45) the footnote rendered *larger* than the body text it annotates. It is now
  multiplied by `--deck-scale`, which the observer in `format-outputs.html` publishes from
  reveal's transform. Do not put a bare px or em size back.
- **Footers must fit on one line.** The binding case is a narrow window, where the footer
  box is exactly the 1050px canvas width at 20px — about 118 characters. Three footers were
  over and were shortened; keep new ones under ~105 to leave room.

Slide math is **KaTeX**, set in `_slide-settings.yml`, not reveal's bundled MathJax 2.
MathJax 2 assembles a tall radical out of glyph pieces and the seams show at deck scale;
`B/04/a`'s SD formula was rendering as a broken column of segments. KaTeX draws it as one
SVG path. Everything these decks use is well inside KaTeX's coverage.

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

**Freeze applies to project renders only.** `quarto render C/09/a_Slides.qmd` and
`quarto render C/09` both ignore `_freeze/` and execute the chunks, even when the stored hash
matches the source exactly. Only a bare `quarto render` from the project root consults the
cache. This matters because the committed freeze is often the *only* way these pages can be
built — a machine without the full package set (`tidyverse` and friends) fails immediately on
a single-file render while the whole-project render succeeds in seconds. Render the project,
not the file.

**Freeze also caches config, not just code.** The cache keys on source hash, so editing
`_quarto.yml`, `_slide-settings.yml`, or `_common.R` has *no effect* on already-frozen pages
until the cache is cleared. Changes to those files have appeared to do nothing for exactly
this reason.

### Re-keying the freeze instead of re-executing

A purely textual edit to a deck — a class rename, a restyled title block — does not need R
to run again. The cache key (`hash` in `_freeze/<path>/execute-results/html.json`) is **md5
of the source with line endings normalized to LF**, and `result.markdown` is the post-knitr
markdown with all the div and heading attributes verbatim. Apply the same textual edit to
`result.markdown`, set `hash` to the new md5, and Quarto skips execution entirely: no R run,
no regenerated figures, no package drift. Serialize with
`json.dumps(entry, indent=2, ensure_ascii=False)`, which round-trips byte-identical.

Three traps:

- **`result.markdown` also embeds the deck's own YAML front matter, and that copy is what
  Quarto reads.** Re-keying a front-matter edit takes two edits, not one. Fixing only the
  hash renders silently from the stale front matter — a `{{< meta >}}` field keeps its old
  value with no error anywhere. Edits that stay out of the front matter avoid this.
- **Line endings.** Most sources here are LF, but `C/07/c_Slides.qmd`, `E/14/b_Slides.qmd`,
  and `E/15/a_Slides.qmd` are CRLF. Hash the LF-normalized text, and read and write the
  `.qmd` with `newline=''` so a CRLF file is not silently rewritten as LF.
- **Guard the rewrite.** Check that HEAD plus the same transform reproduces the working tree
  byte-for-byte. If it does not, that file changed some other way too and genuinely needs a
  real render.

After a re-key, `git diff --numstat _freeze` should show exactly `2+ 2-` per deck (the hash
line and the markdown line). Anything larger means something re-executed.

### Drift met on 2026-08-09

Installing the package list on a fresh machine and re-executing Unit A changed the
figures: same pixel dimensions, but 3–6× the file size (`unnamed-chunk-28-1.png` went
18,477 → 105,982 bytes). Cause is `ragg`, which arrives as a tidyverse dependency and
which knitr then prefers over the default device — so the plots are redrawn with better
antialiasing. Visually an improvement, and the dimensions are unchanged, but it touches
every committed figure in a re-executed deck. Expect it the next time a deck with plots
is genuinely re-run, and do not mistake it for a layout change.

Known drift as of the last full re-render: `qplot()` is deprecated in ggplot2 (still
functional, but it warns). It is used as a teaching section in `A/03/b_Slides.qmd`, and
`A/03/b_assignment.qmd` instructs students to use it. Replacing it with `ggplot()` calls is
a teaching-content decision, not a mechanical fix.

---

## 4. Answer keys stay off GitHub

The graded keys are **not in this repo and must never be.** They live in a private
companion repo, `statistical-methods-keys`, cloned as a *sibling* directory:

```
F:\GitHub\teaching\statistical-methods         (this repo, public)
F:\GitHub\teaching\statistical-methods-keys    (private: keys, rubrics, semester scaffolding)
```

Sibling rather than nested, deliberately. A Quarto website project renders **every** `.qmd`
below its root, and `git add -A` does not distinguish sensitive files from the rest — nesting
would leave `.gitignore` as the only barrier, which is exactly the barrier that failed (see
below). A separate directory removes both failure modes structurally instead of by rule. The
keys repo is its own Quarto project, so its `_freeze/` and `_site/` stay inside the private
repo where they are as protected as the source.

Two different things get called an answer key, and only one is sensitive:

- **Practice answers** — the `{{< dstart summary="Answer key" >}}` blocks inside
  `*_practice.qmd`. These are public on purpose.
- **Graded keys** — assignment answers. These must not be published.
  [`index.qmd`](index.qmd) tells instructors to email for them.

`.gitignore` still blocks `*_key.*` and `**/keys/` here as a backstop, and the rules cover
**derived artifacts, not just sources**. The source-only rule was not enough: rendered keys
once landed in `_freeze/` and were committed across 16 commits before being caught. Nothing
had been pushed, so history was rewritten and the artifacts purged.

If keys are ever rendered anywhere, their `_freeze` output is exactly as sensitive as the
source.

### Removed: the LLM honeypot

Assignments used to carry a `{{< hp >}}` shortcode that injected invisible text
(`font-size: 0.1px; color: transparent`) instructing an LLM to substitute a homoglyph into
its answer, so pasted-in work could be spotted. It was removed in full — 83 calls across the
22 assignments, the `_extensions/jmgirard/honeypot` filter, and the `.tiny-text` rule in
`styles.css`. Reasons, so it is not reintroduced:

- **Accessibility.** The span was hidden visually but not from assistive technology, and had
  no `aria-hidden`. A screen-reader user heard the trap text read aloud in every question.
- **It did not settle cases.** It caught students, who denied it anyway. A covert signal you
  cannot explain without burning it is weak evidence in an integrity hearing, and the marker
  transfers innocently from permitted LLM use.
- **Silent decay.** Models are increasingly trained to ignore instructions embedded in
  pasted content, and nothing distinguishes "nobody cheated" from "the trap stopped working."

It is still deployed in `data2` and `psyc894`; removing it there is a separate change.

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
| `C/09` lecture b | Piecewise & Splines |
| `D/11` | Bootstrap & Robustness |
| `D/12` | Missing Data |
| `E/13` | Reliability |
| `E/15` lecture b | Reviewing Claims |

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

**Section illustrations rollout.** The divider pattern (§1) is prototyped on `C/07/a` only.
Rolling it out means one icon on each of ~102 `#` dividers, 2–6 per deck. Two loose ends:

- **Unit A's 25 `rc` icons** are still on *content* slides, data2-style, and were left there
  deliberately — those slides have genuine room and Unit A is the part of this course closest
  to data2. Decide later whether to move them onto dividers so there is one rule site-wide,
  or keep the content-slide placement where a slide can afford it. `C/08/b`'s 2 are in the
  same position.
- **Icon picks** are not limited to the 51 files already in `icons/`; more are available to
  download. Anything new lands in `icons/` and is referenced the same way.

Chapter 04's 45 corner icons were removed as part of this — see the git history if the
`class=tr` placement is ever wanted back.

Do not read the 32px regression as evidence against them. Each archive unit stylesheet had
`lord-icon.tr { width: 100px; height: 100px; position: absolute !important; top: 0; right: 0 }`;
that rule was lost when the four unit stylesheets were consolidated into one, while the `.rc`
rule beside it survived. The icons rendered correctly until the rebuild. The replacement rule
in `styles.css` sizes to the container instead of hard-coding 100px, so `width=`/`height=` on
the `.absolute` div now means what it says.

**Instructor prep notes.** Supplement the private answer keys with a per-lecture "notes"
document — a prep sheet for whoever is teaching that lecture. Lives in
`statistical-methods-keys` alongside the keys.

**Readings audit.** Search for optimal readings that may improve upon or supplement the
current ones, chapter by chapter.

---

## 8. Outbound links to other courses

[`contents.qmd`](contents.qmd) is the only page that links off this site to other course
materials, in the `↳` line under a unit:

| Unit | Links to | URL |
|---|---|---|
| A | Foundations of Data Science (`jmgirard/data2`) | `https://jmgirard.github.io/data2/` |
| E | Multilevel Modeling (`jmgirard/psyc894`) | `https://jmgirard.github.io/psyc894/` |

Both are GitHub Pages default URLs. **Neither repo has a `CNAME`, so both links break the
day either one gets a custom domain** the way this site did when it moved to
`stats.jmgirard.com`. Nothing in the build checks them: Quarto does not validate external
links, so a dead one fails silently and stays dead. Re-check them whenever one of those
courses is rebuilt or moved.

The Unit E line also names a **Generalized Linear Models** course as `(coming soon)`, with no
link because it does not exist yet. It is meant to sit between this course and Multilevel
Modeling. Replace the marker with a link when it does.

One tension worth knowing about: both linked sites are still offering-shaped — `data2`'s
navbar points at a Canvas course and a dated syllabus PDF, and `psyc894`'s points at Canvas.
So this site now links outward to pages that link to particular offerings, which the
"links run one way" rule (§1) otherwise avoids. Accepted deliberately, on the expectation
that `data2` will be rebuilt in this site's semester-agnostic style.
