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
├── .Rprofile → renv         # renv.lock committed
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

Full resolved code→name mapping for all 51 is available (I already fetched them).

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
2. Add a belt-and-braces `.gitignore` rule in the public repo — `*_key.qmd` and `**/keys/` —
   so a stray key can't be committed by accident.
3. Because keys reference the same datasets, the private repo either duplicates the handful
   of CSVs it needs or points at the public site's `data/` URLs.

Worth deciding at the same time: whether the keys stay Quarto source or get rendered to
Canvas-hosted HTML. Keeping them as `.qmd` in a private repo means they re-render whenever
package versions shift, which is the same benefit `_freeze` gives the public site.

## 4. Work plan

### Phase 1 — Repo scaffolding
- `git init`; create `jmgirard/psyc790` on GitHub (does not exist yet); `main` default.
- Copy from data2/psyc894: `.gitignore`, `.nojekyll`, `.Rprofile`, `_common.R`,
  `format-outputs.html`, `_extensions/jmgirard/{details,honeypot,lordicon}`.
- `styles.css`: use data2's (it's the newest — has the output-block styling,
  `.slide-deck` iframe, `.my-title`/`.my-subtitle`, tachyons subset). Delete the four
  per-unit copies in `archive/`.
- `renv::init()` → `renv.lock`. Package set for this course is different from psyc894
  (easystats, no lme4-heavy stack).
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
  - **Readings:** Canvas links, psyc894-style —
    `- [View on Canvas](https://canvas.ku.edu/courses/<id>/pages/<slug>){target="_blank"}`.

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
| `_quarto.yml` | site title, her Canvas course ID + syllabus URL, footer |
| `index.qmd` | her name, class time/location, office hours, TA; attribution line under the course description |
| `README.md` | written for her (below) |

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

Also worth doing before handoff: `renv.lock` committed and a one-liner on `renv::restore()`
for the day she does need to render locally, plus confirming the lordicon `icons/` are
committed — since §3 moves them local, her site won't silently break if the CDN changes.

### Sequencing

Slots in as a new phase after Phase 6:

- **Phase 7** — copy `psyc790/` → `psyc790-hoemann/`, apply the four-file diff, add the
  workflow + README + LICENSE, create her GitHub repo, enable Pages, verify a test edit
  triggers a rebuild, then hand off.

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

- **Canvas course IDs** — needed for the reading links and the navbar Canvas / Syllabus
  entries, and now needed **twice**: yours for Fall 2025, and Katie's for her Fall 2026
  section. data2 uses `185369`, psyc894 uses `182539`. If the Fall 2025 psyc790 Canvas site is
  archived, those links may need to point somewhere else — and Katie's course won't exist in
  Canvas until closer to Fall 2026, so her copy likely ships with placeholder links she fills
  in later. Flag that in her README. This is the most likely thing to hold up her handoff.
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
