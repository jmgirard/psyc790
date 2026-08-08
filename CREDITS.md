# Credits and Attributions

Third-party material used in this course site.

## Icons

Animated icons by [Lordicon](https://lordicon.com/), used under a paid (PRO) license.

## Illustrations

Hero and title-slide illustrations are from [unDraw](https://undraw.co/), which permits
free use without attribution. All are the "classic" unDraw generation (the `/illustrations/`
CDN path, not `/illustration/`) — mixing the two generations is what makes a set look
mismatched — and all were recoloured from unDraw's default `#6c63ff` accent to the site
blue `#2780E3`, which is what the filename suffix records.

| File | Used for | unDraw slug |
|---|---|---|
| `statistics_2780E3.svg` | site front page | `statistics_z6y6` |
| `exams_2780E3.svg` | assignment and practice pages | `exams` |
| `unit-a_2780E3.svg` | Unit A title slides | `source-code_m0vh` |
| `unit-b_2780E3.svg` | Unit B title slides | `percentages_wi9e` |
| `unit-c_2780E3.svg` | Unit C title slides | `growth-curve_kzjb` |
| `unit-d_2780E3.svg` | Unit D title slides | `inspection_tyum` |
| `unit-e_2780E3.svg` | Unit E title slides | `publish-article_u3z6` |

The five unit drawings were chosen as a set rather than one at a time: each is a single
standing figure beside a light panel or chart, at a similar visual weight, so the title
slides read as one family as a student moves through the course. They also track the
statistics — bars with markers for estimation in B, a fitted curve in C, the same curve
with a point sitting off it in D.

Retired in favour of the per-unit set: `statistics_2780E3.png` and `growth_curve_357EDD.png`
(the two illustrations every deck used to share) and `programmer_2780E3.svg` (already
unreferenced). They remain in git history.

## Figures

Provenance confirmed by Jeffrey Girard, 2026-08-07. Licenses below were verified against
each source's own license statement rather than assumed.

### Third-party, attribution required

| File | Used in | Source | License |
|---|---|---|---|
| `tidydata.png` | A/03b | Figure 5.1 of [*R for Data Science* (2e)](https://r4ds.hadley.nz/data-tidy.html), Wickham, Çetinkaya-Rundel & Grolemund | [CC BY-NC-ND 3.0 US](https://creativecommons.org/licenses/by-nc-nd/3.0/us/) |
| `nocorr.gif` | B/06b | [*Answering Questions with Data*](https://www.crumplab.com/statistics/13-Gifs.html) §13.1.3, Crump, Navarro & Suzuki (2019) | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) |
| `poscorr.gif` | B/06b | *Answering Questions with Data* §13.1.4, Crump, Navarro & Suzuki (2019) | CC BY-SA 4.0 |
| `breaking_bad_wikipedia.png` | A/03 index | Screenshot of a Wikipedia article table (table only; no cover art included) | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) |

Full citation for the CC BY-SA source:

- Crump, M. J. C., Navarro, D. J., & Suzuki, J. (2019). *Answering Questions with Data:
  Introductory Statistics for Psychology Students.* <https://doi.org/10.17605/OSF.IO/JZE52>

⚠️ **`tidydata.png` is NoDerivatives.** It may be redistributed with attribution for
non-commercial use, but must not be cropped, recoloured, or otherwise altered. It is used
here unmodified.

### Replaced by original ggplot figures (2026-08-07)

Six borrowed figures were redrawn from scratch as ggplot code in the decks that use them,
and the image files deleted. The statistical ideas are not copyrightable — only the
original renderings were — so these are now wholly original work with no attribution
owed, and they inherit each deck's theme instead of being frozen bitmaps.

| Was | Now drawn in | Replaced figure |
|---|---|---|
| `emprule.png` | `B/05/b_Slides.qmd` | Figure 9.8 of *Learning Statistics with R* v0.6, Navarro |
| `central_limit1.png` | `B/05/b_Slides.qmd` | Figure 10.8 (panels a–b), LSR v0.6 |
| `central_limit2.png` | `B/05/b_Slides.qmd` | Figure 10.8 (panels c–d), LSR v0.6 |
| `largenumbers.png` | `B/05/a_Slides.qmd` | Figure 10.4, LSR v0.6 |
| `between_within.png` | `B/07/b_Slides.qmd` | Figure 14.2 (p. 429), LSR v0.6 |
| `power.png` | `D/15/power_Slides.qmd` | source never identified |

The empirical-rule figure gained a third panel while being redrawn, so it now shows 1, 2
*and* 3 SD, matching what the slide text has always claimed.

For the record, the originals were: Navarro, D. J. (2015). *Learning Statistics with R: A
tutorial for psychology students and other beginners* (Version 0.6),
<https://old.learningstatisticswithr.com/> — CC BY-SA 4.0. Version 0.6 is the first
release Navarro placed under Creative Commons, and its figure numbers differ from the
current HTML edition. Note that the deleted files remain in this repository's **git
history**; only the working tree and the published site no longer carry them.

### Own work

| File | Used in | Notes |
|---|---|---|
| `tibble.png` | A/03b | Made by Jeffrey Girard from free stock imagery (possibly [Vecteezy](https://www.vecteezy.com/)) |
| `vectors.png` | A/03b | Made by Jeffrey Girard from free stock imagery |
| `traincar.png` | A/02b | Made by Jeffrey Girard from free stock imagery |
| `inference.png` | B/05a | Made by Jeffrey Girard from basic shapes in PowerPoint |
| `rstudio_labels.jpg` | A/01b | Screenshot of the RStudio IDE (Posit) with annotations added by Jeffrey Girard |
| `venn/*.png` | C/09b+ | Made by Jeffrey Girard (Illustrator `.ai` sources present) |

Note on the stock-sourced composites: Vecteezy's free tier requires attribution for some
assets. If the original downloads can be identified it is worth confirming whether a
credit line is owed; the composites themselves are original work.

### Still unresolved

None. Every figure on the site is either attributed above or original work.

`power.png` was the last unresolved item — a four-panel figure whose source could not be
found (it was not from LSR v0.6, whose power figures 11.6 and 11.7 are line plots). Rather
than publish material of unknown provenance, it was redrawn from scratch; see above.

## Data

Most teaching datasets are standard published examples. The ones with a traceable
external source are listed here.

| File | Used in | Source |
|---|---|---|
| `penguins.csv`, `penguins0.csv` | A/03b, B/06b+c, C/07b, C/09c | Generated from `datasets::penguins` (base R ≥ 4.5), which packages the Palmer Station LTER data of Gorman, Williams & Fraser (2014). `penguins0.csv` is the same data with the factors left as numeric codes so A/03b can teach `factor()`; both are written by a script, not edited by hand. |
| `prestige.csv` | B/06b+c, C/07b+c | Generated from `carData::Prestige` (Fox & Weisberg), 1971 Canadian census occupational data with Pineo-Porter prestige scores. The 4 rows with a missing `type` are dropped and the `census` code column omitted; factor levels are spelled out. |
| `screentime.csv` | C/08b, C/09a+b | A 3,000-row random subsample of the open data from Przybylski & Weinstein (2017), <https://doi.org/10.1177/0956797616678438>. See also `data/Przybylski2017/`. |
| `cereal.csv` | A/03b practice | Nutrition data for 77 breakfast cereals, obtained from the Kaggle "80 Cereals" dataset. ⚠️ **Provenance not fully verified.** The underlying data appears to originate from the cereals dataset circulated for the 1993 ASA Statistical Graphics exposition, but neither that chain nor the licence stated on the Kaggle page has been checked against a primary source. The file was renamed from `kaggle_cereal.csv` on 2026-08-08; the name previously implied Kaggle was the origin rather than the download point. Worth resolving or replacing before relying on it. |

Gorman, K. B., Williams, T. D., & Fraser, W. R. (2014). Ecological sexual dimorphism and
environmental variability within a community of Antarctic penguins (genus *Pygoscelis*).
*PLoS ONE, 9*(3), e90081. <https://doi.org/10.1371/journal.pone.0090081>

### Retired datasets

`salaries.csv`, `salaries0.csv`, `political.csv`, and `affairs.csv` are no longer
referenced by any page, so Quarto no longer copies them into the built site. The files
remain in `data/` because `archive/` still points at some of them. `salaries.csv` (which
was `carData::Salaries`) was dropped because every group comparison it supported was a
gender pay gap; `political.csv` and `affairs.csv` because every outcome they offered was
a 4- or 5-level ordinal being fed to a linear model.

## Shared files in other courses

These files are byte-identical to copies published in the `data2` site, so any correction
here applies there too: `tidydata.png`, `tibble.png`, `vectors.png`, `traincar.png`,
`inference.png`, `breaking_bad_wikipedia.png`, `rstudio_labels.jpg`. Of those, only
`tidydata.png` and `breaking_bad_wikipedia.png` are third-party and need attribution.
`rstudio_labels.jpg` is also published in `psyc894`.
