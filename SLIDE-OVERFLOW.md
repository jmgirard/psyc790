# Slides that overflow

Measured at the reveal.js logical slide size (**1050 × 700**), every slide visited in real
reveal state with `fragments: false` so all content is shown at once — i.e. worst case.

**55 of 602 slides overflow (9.1%).** Nine are severe (>200px, roughly a third of a slide
lost); most of the rest are minor.

## How this was measured

Do **not** measure by forcing `height: auto` on hidden sections — reveal resizes `.r-stretch`
images to fit, and overriding the layout defeats that, producing large false positives
(B/06/b "Scatterplots" measured +547px that way but is actually +1px).

The reliable method, in the browser console of a served deck:

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

## Note on one contributing cause (fixed)

Phase 1 replaced psyc790's per-unit `styles.css` with data2's, which defines only `.f3`. The
slides use `.f6` ×67, `.f5` ×50, `.f90` ×12 and `.f4` ×3, so 132 font-shrinking directives
were silently no-ops. Restored in `styles.css`. On `C/09/b` this alone took overflow from
16 slides / 2133px down to 13 / 1794px by the rough metric. **The remainder is pre-existing
content density**, not something the modernization introduced.

## Severe (>200px)

| deck | slide | overflow |
|---|---|---|
| C/09/b | Defining a Line in General | +481 |
| B/08/a | Further partitioning | +403 |
| B/07/b | The F distribution | +293 |
| C/12/b | Example: Assumption Met | +277 |
| C/12/b | Example: Assumption Violated | +251 |
| B/06/a | Reporting a significance test | +244 |
| B/05/b | Another example | +232 |
| C/13/a | Motivation | +206 |
| B/05/b | An example in R | +206 |

## Everything else, by deck

| deck | count | slides |
|---|---|---|
| B/05/a | 5 | Sample example (+90), Sampling error (+50), Sampling distributions (+35), Small population simulation (+28), Small population example (+19) |
| B/05/b | 8 | *(2 severe above)* + The normal distribution (+191), Comparing multipliers (+100), Reporting a CI (+95), Comparing CIs (+67), Sampling distribution (+35), A complication (+26) |
| B/06/a | 1 | *(severe above)* |
| B/06/b | 6 | Variance and covariance (+35), Test statistic (+31), Example dataset (+22), Pearson's correlation (+20), Another effect size (+19), Confidence intervals (+11) |
| B/07/b | 4 | *(1 severe)* + Application and interpretation (+61), The aov function (+55), Example dataset (+45) |
| B/08/a | 2 | *(1 severe)* + Post-hoc tests (+98) |
| C/09/b | 6 | *(1 severe)* + Standardized Slopes (+93), Centering a Predictor (+77), Adjusted R-Squared (+43), Example Dataset (+38), Defining Regression Residuals (+24) |
| C/10/a | 2 | Relation to Student's t-test (+84), Swapping the reference group (+11) |
| C/10/b | 8 | Plotting marginal effects (+144), Example zero-order effects (+111), Venn diagram for two predictors (+94), Two Types of Effects (+87), Plotting marginal effects (+71), Two Types of Effects (+35), Controlling predictors (+31), Multiple regression (+23) |
| C/11/a | 1 | Example dataset (+11) |
| C/11/b | 1 | Proceed with caution (+19) |
| C/12/a | 3 | Example with Collinearity (+27), Example with Multicollinearity (+27), Variance Inflation Factors (+16) |
| C/12/b | 2 | *(both severe above)* |
| C/13/a | 4 | *(1 severe)* + Number of bends (+145), Direction of curvature (+130), Visualizing the tangent line (+15) |
| D/15/power | 2 | Power analysis (+45), Linear model power (+14) |

Clean decks: **A/01/b, A/02/a, A/02/b, A/03/a, A/03/b, B/07/a, D/15/a, D/16/a, D/16/b.**

## Fixing them

Cheapest first:

1. **Drop the font size one step** — add or tighten `{.f5}` / `{.f6}` on the slide. Handles
   most of the 41 slides under +100px.
2. **Split the slide** — the honest fix for the severe ones, which are typically a formula
   plus a full bullet list plus a figure.
3. **Move content into a fragment-revealed second column** where the slide is already using
   `.columns`.

Unit A is entirely clean, so the pattern to imitate is already in the repo.
