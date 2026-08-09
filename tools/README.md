# Slide QA tools

Layout faults in a reveal.js deck are properties of the *rendered* page, so they
cannot be found by reading the source. These measure the real thing.

No dependencies beyond Node and a Chrome that Puppeteer has already cached.
`cdp.mjs` drives it over the DevTools Protocol using Node's built-in WebSocket;
set `CHROME_PATH` if the binary lives somewhere unusual.

## The loop

```bash
quarto render                          # or one deck: quarto render C/08/b_Slides.qmd --to revealjs
node tools/measure-slides.mjs          # writes tools/report.json
python3 tools/locate-widow.py          # widows -> source lines, with a suggested cut
# reword, then render and measure again
```

`measure-slides.mjs` takes deck ids to narrow the sweep:
`node tools/measure-slides.mjs C/08/b D/10/a`. It reads `_site` over `file://`,
so nothing needs serving, but it measures whatever was last rendered: stale HTML
measures clean while the source is broken.

## What it reports

| | |
|---|---|
| `OVER` | slide taller than the 700px canvas |
| `CLIP` | content hidden inside a `<pre>`'s own scrollbar, which leaves the slide itself reporting a comfortable fit |
| `TITLE` | `h2` wrapping to two lines |
| `WIDOW` | a bullet or paragraph whose last line carries one or two words |

## Fixing what it finds

Reword first. Removing one wrapped line frees about 46px at `.fs80`, which is
usually the whole deficit, and the house sizes are 40px body text with 32px
(`.fs80`) for dense slides.

`bump-stops.py` is the fallback for a slide that is genuinely too dense for
32px. It steps the stop down one notch on everything currently overflowing;
record the result in `SLIDE-OVERFLOW.md`'s exceptions table.

## `section-art-map.tsv`

Not a measurement. It records which Lordicon illustration belongs on each of the
79 section-divider slides, one row per divider, and it is the checklist for
finishing that rollout.

Rows are keyed by deck and by the divider's 1-based index within that deck,
**not** by heading text, so a reworded section does not orphan its assignment.
The recorded title is carried anyway and checked against the deck, so a drift is
an error rather than a silently misplaced icon.

`source=catalog` rows are already wired. `source=new` names one icon in the
Wired / Outline family and `source=choose` names two or three, pipe-separated,
where nothing in the library is clearly right and it needs an eye. `key` is the
icon's code, so any candidate can be opened directly:
`lordicon.com/icon/<key>/wired/outline`.

Rows are marked `CLASH` when one of their candidates is the icon a *decided*
row already claims. Picking it anyway is allowed, but then the other row needs a
different icon: the point of the map is that no illustration opens two sections.

**Set secondary to `#2a76dd` in the customizer before exporting** or the icon
bakes in Lordicon's green with no way to recolour it at runtime -- see
`ICONS.md`, which is where that was learned the expensive way. Save it into
`icons/` under the row's `icon` name and add its code to `icon-map.json`.

The names and codes were read from `lordicon.com/api/library/icons?family=wired&style=outline`,
which is the same 3,676-icon list the site's own grid renders from. Searching it
offline beat searching the UI one concept at a time.

Two rows deliberately supersede the C/07/a pilot's choices: `map.json` is the
roadmap slide's recurring motif and should not also open a section, and
`location_pin.json` reads as a place rather than as re-centering an origin.

Adding an icon to `icons/` is all that a `new` row needs; nothing here has to be
edited to mark it done.

## Three ways the measurement lies

All three are written up at length in `SLIDE-OVERFLOW.md`. Briefly:

- **Measure at 1920×1080.** Overflow is not scale-invariant. One slide reads 0
  in a 744px pane and +49 at 1080p.
- **Do not probe font stops by toggling the class in the DOM.** It reports
  slides as fitting that are not, worst of all for slides carrying a Lottie
  icon, whose component never resizes. Thirteen slides passed a DOM probe and
  then overflowed by up to +457px once actually rendered. Change the source,
  render, measure that. These tools do.
- **Index slides by their position among `## ` headings.** A vertical stack is
  also `.level2` and owns no heading, so anything after it lands off by one.
  `measure-slides.mjs` filters on a direct `h2` child; `bump-stops.py` relies on
  that index to address the right line.
