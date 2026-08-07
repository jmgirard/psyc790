# PSYC790 Modernization Plan

Bringing `psyc790` up to the pattern established in `jmgirard/data2` (last commit 2026-05-07)
and `jmgirard/psyc894` (last commit 2026-04-30).

---

## 1. What the target looks like

Both finished courses converged on the same architecture. Structurally, **psyc894 is the
closer template** (2 lectures/week, `a`/`b`), while **data2 is the more refined** (newer CSS,
output formatting, download links, honeypot, `c` lectures). Take structure from psyc894 and
polish from data2.

```
psyc790/
├── _quarto.yml              # website project; navbar w/ Canvas, Syllabus, Schedule, Unit menus
├── _slide-settings.yml      # shared revealjs metadata; `filters: [jmgirard/lordicon]`
├── _common.R                # knitr source hook (replace_path)
├── _extensions/jmgirard/    # details, honeypot, lordicon (+ shafayetshafee/downloadthis?)
├── _freeze/                 # COMMITTED (freeze: auto)
├── .nojekyll                # committed
├── install-packages.R       # unpinned package list; no renv, no .Rprofile
├── index.qmd                # course description, outcomes, instructor, times, office hours
├── schedule.qmd             # week-by-week list, links to each week index
├── 404.qmd                  # "still being developed" + progress checklist
├── styles.css               # single shared stylesheet (root only)
├── format-outputs.html      # JS that re-classes stderr → warning/message blocks
├── icons/*.json             # LOCAL lordicon lotties, semantic names
├── img/, data/
├── A/01/ A/02/ ...          # one folder per week, grouped by unit letter
│   ├── index.qmd            # hub page: Topics / Files / Readings / Slides iframe / Practice
│   ├── a_Slides.qmd         # revealjs, metadata-files: ../../_slide-settings.yml
│   ├── b_Slides.qmd
│   └── assignment.qmd
```

Publishing: `main` holds source; `quarto publish gh-pages` pushes the rendered site to a
`gh-pages` branch. `_site/` is gitignored, `_freeze/` is committed.

---

## 2. What we have now

`./archive/` is the Fall 2025 flat layout — no `_quarto.yml`, no website, self-contained
slide decks with `embed-resources: true`, a duplicated `styles.css` in every unit folder,
and data files duplicated between `data/` and each `Unit_*/`.

**Content inventory (23 slide decks):**

| Unit | Week | a | b | Activity | Assignment | Other |
|---|---|---|---|---|---|---|
| A | 01 | — | RStudio / Console / Scripts | 01b | — | |
| A | 02 | Projects / Quarto / Markdown | Assignment / Functions / Vectors | 02a, 02b | 02 + key | |
| A | 03 | Strings / Factors / Packages | Data Frames / Files / Exploration | 03a, 03b | 03 + key | |
| A | 04 | *project* | *project* | — | — | `04_Project.qmd` |
| B | 05 | Populations / Samples / Uncertainty | Estimates / Normality / Confidence | — | 05 + key | |
| B | 06 | Hypotheses / NHST / p-values | Covariances / Correlations / Inference | — | 06 + key | |
| B | 07 | t-tests / Effect Sizes / Paired Groups | One-way ANOVA / Effect Sizes / Contrasts | — | 07 + key | |
| B | 08 | Extensions / Translation / Review | — | — | — | |
| C | 09 | *fall break* | Regression / Inference / Centering | — | — | `09_Quiz_key.qmd` |
| C | 10 | Dummy Codes / Means / Contrasts | Multiple Regression / Partial Effects | — | 10 + key | |
| C | 11 | Continuous Moderation | Categorical Moderation | — | 11 + key | |
| C | 12 | Assumptions and Diagnostics I | Assumptions and Diagnostics II | — | 12 + key | |
| C | 13 | Polynomial Regression | *project work* | — | — | |
| C | 14 | *project work* | *project work* | — | — | |
| D | 15 | Best & Questionable Practices | *Thanksgiving break* | — | — | |
| D | 16 | Reporting & Reviewing | Translation Activity | — | 16 + key | |

**Resolved:** 09a was fall break, 15b Thanksgiving break, 13b/14a/14b Unit C project work,
and `04_Project.qmd` covers both 04a and 04b. This also settles the unit boundaries —
**week 14 belongs to Unit C, not D** (Unit C = 09–14, Unit D = 15–16), matching the archive
folders.

Break weeks get placeholder pages following the psyc894 convention (`C/09/index.qmd`,
`B/05/index.qmd`): a normal week `index.qmd` with `## [09a] Fall Break` / `No course meeting`
sections and the usual bottom nav, left unlinked in `schedule.qmd` the way data2 lists its
non-content weeks.

### Assessment pattern

Two meetings → assignment. One meeting → quiz. Checking that against the archive confirms
it exactly: assignments exist for **02, 03, 05, 06, 07, 10, 11, 12, 16** — precisely the
nine two-meeting weeks. The one-meeting weeks are **01, 08, 09, 13, 15**, and week 09's quiz
key is the only one that survived in the archive.

So `X/NN/assignment.qmd` for the nine assignment weeks, and the five quiz weeks need a
decision: a `quiz.qmd` stub on the week page, or just a note (quizzes may have been
Canvas-native). Weeks 04 and 14 are project weeks and take the project brief instead.

Also note: only Unit A has `*_Activity.qmd` files — Units B–D have no in-class practice
material to fold into their `index.qmd` **Practice** sections.

---

## 3. The lordicon migration (the "manual" piece — mostly automatable)

Archive uses **51 unique** `{{< li CODE ... >}}` shortcodes across 70 call sites, pulling
from `https://cdn.lordicon.com/CODE.json` at page load. Target uses
`{{< lif "../../icons/name.json" ... >}}` against committed local files.

**Good news: I verified all 51 codes still resolve on the CDN, and each downloaded lottie
carries a human-readable `nm` field** (e.g. `xtkehzkm` → `106-map-outline`,
`fdlimbxm` → `454-calculator-outline`). So the download + naming step can be scripted:

1. Extract all codes with their surrounding context (which slide, which section).
2. `curl https://cdn.lordicon.com/<code>.json -o icons/<slug>.json`.
3. Derive `<slug>` from the lottie's `nm` (strip the numeric ID and `-outline` suffix,
   snake_case it) — e.g. `781-rulers-outline` → `rulers.json`. That matches how the
   existing psyc894 `icons/` are named (`rulers.json`, `map.json`, `text_box.json`).
4. Reuse existing files where psyc790 and psyc894/data2 share an icon — several already
   exist (`map`, `rulers`, `text_box`, `books`, `poetry`, `theater`, `visa`, `box`,
   `blender`, `dice`, `genie`, `contacts`, `car`).
5. Rewrite the 70 shortcode call sites `li <code>` → `lif "../../icons/<slug>.json"`.
6. **Your manual step:** render a contact sheet of all 51 icons and eyeball the auto-derived
   names, renaming any that read badly in context. That's a review pass, not 51 downloads.

Full resolved code→name mapping for all 51 is available (I already fetched them), recorded in
`icon-map.json`.

### ⚠️ The CDN serves stale, sometimes watermarked revisions

Bulk-downloading from `cdn.lordicon.com/<code>.json` works, but returns **older revisions**
than the Lordicon web app gives a PRO account. Verified by rendering all 51 in a browser and
reading the resulting SVG fills:

- **10 contained a `watermark` layer** — free-preview versions. These would have shipped
  watermarked icons to a public course site.
- **9 used the old colour convention**, where `colors=secondary:#2a76dd` recolours the wrong
  layer and leaves Lordicon's green `#08a88a` behind — rendering blue+green instead of
  blue+black. (This is what Jeff spotted by eye on `caliper`, `magic_ball`, `people`.)

The two sets overlap; **12 icons** need replacing, tracked in `ICONS-TODO.md`. Four were
fixable by copying existing clean copies from data2/psyc894 (`rulers`, `theater`, `caution`,
`poetry` — all v5.12.1 with the modern `control`-layer structure).

Detection that worked: load `icon-contact-sheet.html`, set every icon to
`colors=secondary:#2a76dd`, and check whether `rgb(8,168,138)` survives in the shadow-DOM SVG.
Static JSON inspection is *not* reliable here — legacy-structured files can render correctly,
so the browser check is the source of truth. Re-run it after dropping in replacements.

### Animation: kill looping, hover only

The archive is **100% `trigger=loop`** (70/70, with `delay=5000` on 67 and `delay=3000` on 3).
Both modern repos converged on `trigger=hover` with no delay — psyc894 is 33/33 converted,
data2 is 95/97. Applying that here to minimize student distraction:

```
{{< li CODE trigger=loop delay=5000 colors=secondary:#2a76dd class=rc >}}
    ->
{{< lif "../../icons/<slug>.json" trigger=hover colors=secondary:#2a76dd class=rc >}}
```

Rule: `trigger=loop` → `trigger=hover`, drop `delay=*` entirely, **preserve `colors` and
`class` verbatim**.

⚠️ **Do not normalize `class` to `rc`.** Both modern repos are 100% `class=rc`, which makes it
look like the house standard — but psyc790 uses two distinct patterns and they are not
interchangeable:

| Class | Count | Context | Size |
|---|---|---|---|
| `rc` | 25 | Big decorative icon in a 40% column (`::: {.column .tc .pv4}`) | 300×300 via `lord-icon.rc` |
| `tr` | 45 | Small corner accent in `::: {.absolute top=-33 right=0 width=100 height=100}` | 100×100 from the container; `.tr` is only `text-align: right` |

data2 and psyc894 are all-`rc` because they never used the corner-accent pattern, not because
`tr` was retired. Converting those 45 to `rc` would force 300×300 icons into 100×100 absolute
boxes and break the layout on more than half the decks.

`colors` also varies (`secondary:` on 65 call sites, `primary:` on 5) — those target different
Lottie layers, so preserve them verbatim as well.

### Also worth fixing in data2

`data2/A/04/a_Slides.qmd` lines 68 and 97 still have `trigger=loop delay=5000`
(`spreadsheet.json`, `light_bulb.json`) — the only two that escaped the hover conversion.
One-line fix each, unrelated to psyc790.

---

## 3b. Answer keys — keep them off GitHub

Confirmed: **neither data2 nor psyc894 has ever contained a key file**, in the working tree
or anywhere in git history. Separating them is already your established practice; psyc790 is
the only course that still has keys sitting next to the assignments.

There are two different things called "answer key" here, and only one is sensitive:

- **Practice answers** — the `{{< dstart summary="Answer key" >}}` … `{{< dstop >}}` blocks
  inside `*_Activity.qmd`. data2 publishes these openly (see `B/14/index.qmd`). These stay
  public and fold into each week's Practice section as planned.
- **Graded keys** — the 9 `*_Assignment_key.qmd` files and `09_Quiz_key.qmd`. These must not
  be published. They also **leak the honeypot design**: each key opens with a line like
  `> Honeypot Type: homoglyph "." (look for mid-dots: ·)`, which documents exactly how the
  `{{< hp >}}` LLM traps work across all 43 call sites. Publishing those would defeat the
  mechanism for all three courses, not just this one.

Recommended handling:

1. Move the 10 graded keys to a **separate private repo**, `jmgirard/psyc790-keys`, mirroring
   the week structure (`A/03/assignment_key.qmd`). A private repo keeps them versioned and
   backed up, which a gitignored local folder does not. If you'd rather have one place for
   all three courses, a single private `jmgirard/teaching-keys` with `psyc790/`, `data2/`,
   `psyc894/` subfolders works equally well and is probably tidier long-term.
2. Add `.gitignore` rules in the public repo so a stray key can't be committed by accident.

   ⚠️ **`*_key.qmd` alone is not enough — this actually bit us.** Quarto rendered the whole
   `archive/` tree (see below), which wrote the fully rendered answer keys — honeypot markers
   and all — into `_freeze/archive/**/execute-results/html.json`, plus figure PNGs and a stray
   `.html`. Those matched no `.qmd` rule and were committed across 16 commits before being
   caught. Nothing had been pushed (psyc790 had no remote yet), so history was rewritten with
   `git filter-branch` and the artifacts purged.

   The rules now cover derived artifacts, not just sources:
   ```gitignore
   *_key.qmd
   *_Key.qmd
   **/keys/
   *_key.*        # rendered html/json/png derived from a key
   *_Key.*
   *_key/
   *_Key/
   _freeze/archive/
   ```

   **Root cause:** a Quarto website project renders *every* `.qmd` it finds, including
   `archive/`. Fixed in `_quarto.yml`:
   ```yaml
   project:
     render:
       - "**/*.qmd"
       - "!archive/**"
   ```
   Note the glob-list form (`"A/**/*.qmd"`, …) did **not** exclude archive — only the `!`
   negation did. Verify with `quarto inspect`, which should report 51 input files and zero
   under `archive/`.

   Lesson for the keys repo: if graded keys are ever rendered, their `_freeze` output is just
   as sensitive as the source.
3. Because keys reference the same datasets, the private repo either duplicates the handful
   of CSVs it needs or points at the public site's `data/` URLs.

Worth deciding at the same time: whether the keys stay Quarto source or get rendered to
Canvas-hosted HTML. Keeping them as `.qmd` in a private repo means they re-render whenever
package versions shift, which is the same benefit `_freeze` gives the public site.

## 4. Work plan

### Phase 1 — Repo scaffolding
- `git init`; create `jmgirard/psyc790` on GitHub (does not exist yet); `main` default.
- Copy from data2/psyc894: `.gitignore`, `.nojekyll`, `_common.R`,
  `format-outputs.html`, `_extensions/jmgirard/{details,honeypot,lordicon}`.
  (Not `.Rprofile` — it only sourced `renv/activate.R`, and all three repos have
  since dropped renv. See below.)
- `styles.css`: use data2's (it's the newest — has the output-block styling,
  `.slide-deck` iframe, `.my-title`/`.my-subtitle`, tachyons subset). Delete the four
  per-unit copies in `archive/`.
- **No renv** (decided). `_freeze/` is the actual reproducibility mechanism
  here: frozen chunk results are committed, so package updates cannot change the live site
  until a page is deliberately re-rendered, and CI needs no R at all. renv would contribute
  nothing to the publish path while adding a `renv::restore()` step that is the single most
  likely thing to break Katie's handoff.
  - Replaced by `install-packages.R` — an unpinned list of the 18 CRAN packages the archive
    uses, plus `standist` from GitHub (`jmgirard/standist`, your own package, not on CRAN).
  - **Extended to all three courses (2026-08-07.)** This section originally said data2 and
    psyc894 would keep renv, on the grounds that they were finished courses and the
    inconsistency cost nothing. Both halves of that turned out to be wrong. psyc894 is being
    revised for a future offering, not finished; and the inconsistency did cost something —
    an upgrade to R 4.6.1 left psyc894's renv library stranded at R-4.5 (225 packages there,
    1 under R-4.6), so activation silently put an empty library on the path and every render
    failed at `library(here)`. A pinned environment that no longer resolves is worse than no
    pinning at all, because it fails at render time rather than at install time. Both repos
    now carry their own `install-packages.R` with lists derived from the `library()` and
    `::` calls in their course files.
  - Tradeoff accepted: no protection against a package update changing output on re-render.
    `freeze: auto` bounds this — only edited files re-execute, so drift is incremental and
    visible. Re-render everything before a semester to surface it deliberately.
- `psyc790.Rproj`.

### Phase 2 — Config
- `_quarto.yml`: website, `resources: ["icons/"]`, `freeze: auto`, navbar with Canvas /
  Syllabus / Schedule + four unit dropdown menus (bootstrap icon per week), footer,
  `theme: [cosmo, brand]`, `css: styles.css`.
  - ⚠️ Note: data2 and psyc894 both declare `theme: [cosmo, brand]` but **neither repo has a
    `_brand.yml`**. Worth confirming whether that's intentional before copying it forward.
- `_slide-settings.yml`: `pagetitle: "Statistical Methods in Psychology"`,
  `course: "PSYC 790"`, `semester: "Fall 2025"`, `instructor: "Jeffrey M. Girard"`,
  `attribution: ""`, `author-meta`, `filters: [jmgirard/lordicon]`, revealjs block copied
  from data2 (includes `code-annotations: hover`, which psyc894 lacks).
- `styles.css` gains an attribution rule, unused in your copy but present so both stay
  identical:
  ```css
  .my-attrib {
    padding-top: 1.5em !important;
    color: #AAAAAA;
    font-size: 0.55em !important;
    font-style: italic;
  }
  .my-attrib:empty, .my-attrib p:empty { display: none; }
  ```
  ⚠️ Verify at first render that an empty `attribution` collapses cleanly — Quarto may emit
  `<p></p>` inside the div, which `:empty` won't match on the parent alone.

### Phase 3 — Restructure content
For each week `NN` in unit `X`:
- `archive/Unit_X/NNa_Slides.qmd` → `X/NN/a_Slides.qmd`, and rewrite the YAML header:
  strip the giant inline `format:` block, replace with
  ```yaml
  lecture: "NNa"
  metadata-files:
    - ../../_slide-settings.yml
  format:
    revealjs:
      theme: default
  ```
- Retitle the title slide to the data2/psyc894 `.my-title` pattern, and **parameterize the
  instructor and attribution** (see §6 — this is what makes Katie's version a 4-file change
  rather than a fork):
  ```
  ::: {.my-title}
  # [Statistical Methods]{.blue}
  Strings / Factors / Packages

  ::: {.my-grey}
  [{{< meta semester >}} | Course {{< meta course >}}]{}<br />
  [{{< meta instructor >}} | Lecture {{< meta lecture >}}]{}
  :::

  ::: {.my-attrib}
  {{< meta attribution >}}
  :::

  ![](../../img/statistics_2780E3.png){.absolute bottom=30 right=0 width="400"}
  :::
  ```
  Note both finished repos hardcode `Jeffrey M. Girard` on every title slide while
  parameterizing `semester` and `course`. Swapping in `{{< meta instructor >}}` costs nothing
  now and is the difference between one edit and 23.
- Fix asset paths: `../img/` → `../../img/`, `../data/` → `../../data/`, bare `"foo.csv"` →
  `"../../data/foo.csv"`.
- `archive/Unit_X/NN_Assignment.qmd` → `X/NN/assignment.qmd`. The matching `*_key.qmd` goes
  to the private keys repo (§3b), never here.
- Fold `*_Activity.qmd` content into the week's `index.qmd` **Practice** section using
  `{{< dstart summary="Answer key" >}}` … `{{< dstop >}}`, matching data2's B/14 pattern.
  (Unit A only — B–D have no activity files.)
- Write each `X/NN/index.qmd`: Topics, File Downloads, Readings, Slides iframe + hamburger
  note, Practice, bottom prev/next nav buttons.
  - **Downloads:** plain links, data2-style —
    `- [foo.csv](../../data/foo.csv){download="foo.csv"}`. No `downloadthis` extension.
  - **Readings:** Canvas **file** links (not Canvas pages — psyc790's readings are PDFs in
    Canvas Files), in this shape:
    ```
    - [BST (2E) Ch. 5](https://canvas.ku.edu/courses/{{< meta canvas-id >}}/files/folder/Unit%20B?preview={{< meta readings.bst-2e-ch5 >}}){target="_blank"}
    ```
    with the file ids collected in one block at the top of `_quarto.yml`:
    ```yaml
    canvas-id: "164756"
    readings:
      bst-2e-ch5: "14592426"
    ```
    Verified: `{{< meta >}}` expands inside link URLs, dotted paths resolve, hyphenated keys
    work, and `_quarto.yml` metadata is inherited by every page.

    **Why the map, rather than inlining the ids:** a Canvas file preview id (`14592426`) is
    opaque and *per-file, per-course*. When Katie copies the course, every PDF gets a new id,
    so `canvas-id` alone cannot carry reading links across. Without the map she'd be editing
    ~20–30 links spread over 16 files; with it she edits one block and the week pages stay
    identical. It should also degrade gracefully — a stale `?preview=` id is expected to fall
    back to the folder listing, which is still the right place (worth confirming once in
    Canvas).

    ⚠️ **These PDFs are textbook chapters and must stay behind Canvas authentication.** Do
    not commit them to this repo or copy them into `data/` — the site is public, and Canvas
    is the access-controlled home for them. Link only.

### Phase 4 — Assets
- Consolidate all CSVs into a single root `data/`. Currently duplicated across
  `archive/data/` and each `Unit_*/`. Four files are referenced but missing:
  `breaking_bad.csv`, `gradebook.csv`, plus `depression.csv`/`water0.csv` which live only
  in a unit folder.
- Copy `archive/img/` → `img/`; keep `img/venn/`.
- Run the lordicon migration from §3.

### Phase 5 — Top-level pages
- `index.qmd`: course description, learning outcomes, textbook links, instructor/TA,
  class time & location, office hours, hero image (`img/statistics_2780E3.svg`).
- `schedule.qmd`: 16 weeks, `a`/`b` sub-items, links to each `X/NN/index.qmd`.
- `404.qmd`: progress checklist.

### Phase 6 — Build & publish
- `quarto render` locally, fix path/render errors, commit `_freeze/`.
- `quarto publish gh-pages`; enable Pages on the `gh-pages` branch.
- Update the Canvas course link and syllabus URL in the navbar.

---

## 6. Katie Hoemann's Fall 2026 version

Built **after** the psyc790 rebuild and derived from it, so the archive→website conversion
happens once. Lives at `F:/GitHub/teaching/psyc790-hoemann/`, pushed to its own GitHub repo
with its own Pages site so she can maintain it independently.

### What actually differs

Because §4 parameterizes the instructor and attribution, the derived copy differs in
**four files**. Every `.qmd` is byte-identical.

| File | Change |
|---|---|
| `_slide-settings.yml` | `semester: "Fall 2026"`, `instructor: "Katie Hoemann"`, `attribution: "Course originally developed by Jeffrey M. Girard"` |
| `_quarto.yml` | `canvas-id: "198405"` (confirmed), the `readings:` file-id map, navbar Canvas + syllabus hrefs, footer |
| `index.qmd` | her name, class time/location, office hours, TA; attribution line under the course description |
| `README.md` | written for her (below) |

Because `canvas-id` lives in `_quarto.yml` and the week pages reference it as
`{{< meta canvas-id >}}`, all 16 week `index.qmd` files carry over untouched. The navbar
hrefs in `_quarto.yml` use the literal id — shortcodes aren't processed in project YAML, but
that file is already part of the per-instructor diff so it costs nothing.

Footer becomes something like
`"Copyright 2026 &copy; Katie Hoemann &middot; Originally developed by Jeffrey Girard"`.

The attribution renders as a small italic grey line beneath the semester/instructor block on
all 23 title slides — present but unobtrusive, matching the existing `.my-grey` treatment.

Worth deciding: whether to add a `LICENSE` (CC BY-SA or similar) so the terms of reuse are
explicit rather than implied by the footnote alone.

### Adapting to her expertise

Since she doesn't have your R/Quarto/GitHub background, the goal is that **she never has to
run `quarto publish` or manage renv**. Two things make that work:

1. **Commit `_freeze/` and let CI publish.** With `freeze: auto` and frozen results committed,
   a GitHub Action needs only Quarto — **no R, no renv restore** — because no code re-executes.
   She edits a `.qmd` (even in the GitHub web editor), pushes, and the site rebuilds itself.
   This is the officially recommended Quarto pattern for exactly this situation.

   ```yaml
   # .github/workflows/publish.yml
   on:
     push:
       branches: [main]
   jobs:
     build-deploy:
       runs-on: ubuntu-latest
       permissions:
         contents: write
       steps:
         - uses: actions/checkout@v4
         - uses: quarto-dev/quarto-actions/setup@v2
         - uses: quarto-dev/quarto-actions/publish@v2
           with:
             target: gh-pages
           env:
             GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
   ```

   Caveat to flag for her: if she edits an R **code chunk**, the frozen result goes stale and
   CI can't regenerate it without R. That's the one case where she needs to render locally —
   or send it back to you.

2. **A task-oriented `README.md`**, not a technical one. Sections along the lines of:
   "Change the semester or your name" (→ `_slide-settings.yml`, 3 lines), "Change your office
   hours" (→ `index.qmd`), "Edit a lecture" (→ `X/NN/a_Slides.qmd`), "Add a reading link"
   (→ `X/NN/index.qmd`), "Where the answer keys are" (→ not here; see §3b), and "What to do
   if the site doesn't update" (→ check the Actions tab).

Also worth doing before handoff: a one-liner on `source("install-packages.R")` for the day
she does need to render locally, plus confirming the lordicon `icons/` are committed —
since §3 moves them local, her site won't silently break if the CDN changes.

(This previously suggested committing `renv.lock` and pointing her at `renv::restore()`.
That contradicted the "No renv" decision in Phase 1, and renv has since been dropped from
all three courses — `install-packages.R` is the one command she needs.)

### Sequencing

Slots in as a new phase after Phase 6:

- **Phase 7** — copy `psyc790/` → `psyc790-hoemann/`, apply the four-file diff, add the
  workflow + README + LICENSE, create her GitHub repo, enable Pages, verify a test edit
  triggers a rebuild, then hand off.

---

## 6b. Package drift

Checked against the versions installed 2026-08-06 (easystats 0.7.6, ggplot2 4.0.3,
tidyverse 2.0.0, marginaleffects 0.32.0, emmeans 2.0.4, dplyr 1.2.1). The full site
re-executed every chunk with **zero errors**, so nothing in the Fall 2025 code is broken by
current packages.

One genuine deprecation:

- **`qplot()`** — deprecated in ggplot2 3.4.0, still functional in 4.0.3 but it warns. Used
  ~8 times as a teaching section in `A/03/b_Slides.qmd`, and `A/03/assignment.qmd`
  **instructs students to use it** (Q4a/b). Students on current ggplot2 will see a
  deprecation warning that the Fall 2025 cohort did not. Replacing it with `ggplot()` calls
  is a teaching-content decision, not a mechanical fix.

Three decks suppress warnings (`B/05/b`, `B/07/a`, `B/08/a`, mostly around
`model_parameters()` / `estimate_means()` / `visualisation_recipe()`). These were re-rendered
with `warning: true` to check for drift hiding behind the suppression — **zero deprecations
found** — then restored.

### ⚠️ Freeze hides future drift, by design

`freeze: auto` re-executes only when the **source** changes, never when packages update. That
is exactly what keeps the published site stable — but it also means package drift stays
invisible until execution is forced. There is no `--no-freeze` flag; force it by clearing the
cache:

```bash
rm -rf _freeze && quarto render
```

Worth doing once before each offering. That is the moment drift surfaces, and it is much
better to meet it deliberately than to have a student hit it mid-semester. Note this also
applies to Katie's CI setup: because her GitHub Action reuses committed freeze output and
never runs R, it can never surface drift — someone has to run a full local re-render.

---

## 6c. Audit of everything imported from data2

Phase 1 copied data2's config wholesale. That caused two real defects (see
`SLIDE-OVERFLOW.md`), so everything else copied has now been checked against the archive
originals. **Result: the two known defects were the only ones.**

| imported | verdict |
|---|---|
| `styles.css` | **2 defects, fixed.** See below. |
| `_quarto.yml` `echo: true` | **1 defect, fixed.** Overrode revealjs's `echo: false`. |
| `_slide-settings.yml` | clean — 4 added options, all verified benign |
| chunk options | identical to archive, apart from the intentional `replace_path` |
| `_extensions/` | correct — the archive has no `_extensions`, so the decks always relied on repo-root copies |
| `_common.R` | additive only; the `replace_path` hook is inert unless a chunk sets it |
| `format-outputs.html` | inert — **0** real `cell-output-stderr` blocks across all 24 decks |

### styles.css, checked three ways

1. **Do the four archive unit stylesheets conflict with each other?** No — they are supersets
   of one another, identical values for every shared selector. Merging was safe.
2. **Do any selectors present in both archive and data2 carry different values?** None
   remaining (this is the check that should have been run in Phase 1 — the original comparison
   only looked at selector *names*, which is how the `.f4`/`.f5`/`.f6`/`.f90` loss slipped
   through).
3. **Did any shared selector lose a property?** None.

### `_slide-settings.yml` additions, each verified

- `code-line-numbers: false` — **no-op here**; rendered markup is byte-identical to the
  original (`<span id="cbN-M">` anchors either way).
- `controls: true` — already the reveal default.
- `code-annotations: hover` — psyc790 uses no code annotations.
- `include-after-body: format-outputs.html` — inert, per the table above.

Options *dropped* from the archive headers (`author-meta`, `course`, `lecture`, `pagetitle`,
`semester`) all moved to the top level of `_slide-settings.yml` and are still applied;
`embed-resources`/`self-contained` were correctly dropped for a website build.

---

## 7. Copyright audit

Since the repo and the Pages site are both public, here's what's actually in scope. Not legal
advice — flagging what's worth a decision.

### Clean

- **No PDFs, docs, or slides decks anywhere** in the repo. The textbook chapters live only on
  Canvas, which is the correct arrangement. `.gitignore` now blocks `*.pdf`/`*.epub`/`*.docx`/
  `*.pptx` as a safety net so a stray copy can't be committed during Phase 3/4.
- **Datasets** are the standard teaching corpus (`affairs`, `teaching_ratings`, `salaries`,
  `cigarettes`, …) plus `Przybylski2017`, which is published open research data. Low concern.
- **unDraw illustrations** (`*_2780E3.svg`, `*_357EDD.svg`, `proud_coder`, `programmer`,
  `statistics`) — unDraw's license permits free use without attribution. Fine.

### Worth attention

**1. Textbook figures with no attribution.** ✅ **Resolved — see `CREDITS.md` and the
decision below.** The guesses recorded here were only partly right, which is why they were
checked rather than acted on: `vectors.png`, `traincar.png` and `tibble.png` are **not** R4DS
figures at all but Jeff's own composites from stock imagery, while `emprule.png`,
`central_limit1/2.png`, `largenumbers.png` and `between_within.png` came from Navarro's
*Learning Statistics with R* v0.6 (CC BY-SA 4.0), not R4DS. Only `tidydata.png` is R4DS
(Figure 5.1, CC BY-NC-ND 3.0 US — note 3.0 US, not 4.0). `breaking_bad_wikipedia.png` is a
table screenshot with no cover art.

Context that matters: all six I hashed are **byte-identical to files already published in
data2**, so psyc790 adds no new exposure — but it does mean the question spans all three
courses. BY-NC-ND permits educational redistribution *with attribution*, so the cheap fix is
a credit line under each figure (or a central `CREDITS.md`) rather than removing anything.

**2. Lordicon.** ✅ **Proceed with the `li` → `lif` migration.** You hold a PRO license, and
PRO *explicitly permits* the thing we're doing: it names as a supported integration the use of
"icons in the static or Lottie JSON format that are hosted on the User's servers." Self-hosting
the Lottie files is a sanctioned path, not a workaround.

An earlier draft of this section overstated the risk by quoting only the prohibition. For
accuracy, what PRO actually bars is:

> "Resell, trade, rent, lend, assign, gift, sublicense, or otherwise distribute the icons in
> their original or modified form as standalone files, whether for free or for profit"

and using them "as the core feature of a product, such as an icon library or icon pack."
A course site using icons decoratively is neither.

**Remaining gray area (thin):** Lordicon's terms are silent on public source repositories.
But since PRO permits serving the JSON from your own site — which inherently makes every file
fetchable by any visitor — a public repo doesn't meaningfully expand what's obtainable.
Gitignoring `icons/` would reduce apparent exposure without reducing actual exposure, and
would break Katie's build. Not worth it.

If you want certainty, one clarifying email to Lordicon support would settle the repo
question. Recorded in `CREDITS.md` either way.

### Decisions taken

- ~~**Figure credits:** add a source caption under each third-party figure, plus
  `CREDITS.md`.~~ **Resolved 2026-08-07.** Provenance was confirmed for all 15 figures and
  `CREDITS.md` now records verified sources and licences rather than guesses. Six borrowed
  figures (`emprule`, `central_limit1/2`, `largenumbers`, `between_within`, `power`) were
  **redrawn from scratch as ggplot code** in the decks that use them and the image files
  deleted, so no attribution is owed for those at all. Four third-party items remain and are
  attributed in `CREDITS.md`: `tidydata.png` (R4DS 2e, CC BY-NC-ND 3.0 US), `nocorr.gif` and
  `poscorr.gif` (Crump, Navarro & Suzuki, CC BY-SA 4.0), and `breaking_bad_wikipedia.png`
  (Wikipedia, CC BY-SA 4.0). Per-slide source captions were **not** added; the central
  `CREDITS.md` is the record.
  - Still to carry back: `data2` publishes `tidydata.png` and `breaking_bad_wikipedia.png`
    and has no `CREDITS.md` of its own.

---

## 5. Decisions I need from you

1. ~~Which semester?~~ **Fall 2025** — not teaching this term, so the site reproduces the
   last offering as-is.
2. ~~Missing weeks?~~ **Resolved** (see §2): 09a fall break, 15b Thanksgiving break,
   13b/14a/14b Unit C project work, `04_Project.qmd` covers 04a + 04b.
3. ~~Answer keys?~~ **Off GitHub entirely** — see §3b for the split between publishable
   practice answers and the 10 private graded keys.
4. ~~`04_Project.qmd`?~~ Becomes the `A/04/index.qmd` content, covering both meetings.
   `09_Quiz_key.qmd` is a graded key → private repo.
5. ~~Readings?~~ **Canvas links**, psyc894-style:
   `- [View on Canvas](https://canvas.ku.edu/courses/<id>/pages/...){target="_blank"}`.
   The PDFs live on Canvas rather than being linked out to publisher sites.
6. ~~`downloadthis`?~~ No preference stated → **use data2's plain `{download=}` links**
   and skip the extension. One less dependency, and it matches the newest repo.

### Still open

- ~~Canvas course ids?~~ Settled: **164756** (yours, Fall 2025) and **198405** (Katie,
  Fall 2026), both recorded.
- **Canvas file ids** — the `readings:` map has to be populated during Phase 3 by collecting a
  preview link per PDF from your Canvas Files. Katie will need to regenerate the whole map
  against her own course once her files exist; flag it in her README as the one real setup
  task she can't skip.
- **Does Katie get the answer keys?** She'll need them to teach from, and that's a separate
  transfer from the public repo (private repo access, or sent directly). Note they document
  the honeypot design per §3b, so it's a deliberate decision rather than a copy-paste.
- **Quiz weeks (01, 08, 09, 13, 15)** — a `quiz.qmd` on the week page, or just a note if
  quizzes were Canvas-native? Only week 09's key survived in the archive, which hints they
  may have been Canvas quizzes.
- **Keys repo shape** — `jmgirard/psyc790-keys` vs. one private `jmgirard/teaching-keys`
  covering all three courses.
- **`_brand.yml`** — both existing repos declare `theme: [cosmo, brand]` with no
  `_brand.yml` present. Intentional?
