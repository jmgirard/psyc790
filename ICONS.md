# Icons — resolved

All 121 icons verified: **no watermarks, all render, and only two carry Lordicon's
green** (both quarantined, see *Three exceptions* below).

## Raw export works again

The section below records a period when Lordicon's UI appeared to export only
*customized* Lottie, with colours flattened at export time, which is why 12 icons
have their accent baked in and ignore `colors=`. **That is no longer the case.**
The 70 icons added for the section dividers are raw: each carries a `control` layer
whose colour slots are wired through live expressions, so `colors=secondary:#2a76dd`
is applied at runtime and the accent can be changed later by editing the shortcodes.

The house convention a raw file should follow is `primary=#121331` (dark navy) and
`secondary=#08a88a` (the green placeholder that `colors=` remaps to blue). 67 of the
70 follow it exactly.

### Three exceptions, and how to spot them

Read the defaults out of the `control` layer rather than trusting the rendering
to look right in a thumbnail:

| file | slots | what happens |
|---|---|---|
| `wired-outline-1378-3-d` | primary=**green**, secondary=navy | Slots are **swapped**, so `colors=secondary` recolours the navy and the green survives. This is the same fault as the 9 legacy CDN files below. |
| `wired-outline-451-bolt` | primary=green, **no secondary** | `colors=secondary` is inert and the icon renders entirely green. |
| `parabola.json` (square-root), `puzzle_fit.json` (puzzle-piece) | no usable secondary | Renders flat navy with no accent, like `quotation.json`. Cosmetic, not a fault. |

The first two are **not wired to any slide.** An icon with a swapped or missing
secondary slot needs either a per-call `colors=primary:...` override, which breaks
the uniform shortcode, or a different icon.

## What went wrong, and why it's worth remembering

The initial bulk download pulled every icon from `cdn.lordicon.com/<code>.json`. That endpoint
serves **older revisions** than a PRO account gets from the web app, and it introduced two
problems that only showed up on screen:

1. **Watermarks.** 10 files carried a `watermark` layer — free-preview versions that would
   have shipped watermarked icons to a public course site.
2. **Wrong colour convention.** 9 files recoloured the wrong layer, leaving Lordicon's green
   `#08a88a` visible and rendering blue+green instead of blue+black.

Four were fixed by copying existing clean copies out of data2/psyc894 (`rulers`, `theater`,
`caution`, `poetry`). The rest were re-exported from the Lordicon UI.

## The export gotcha (historical)

This is what was true for a while, and it is why 12 icons still have their accent
baked in. Raw export is available again; see the top of this file.

Lordicon's export UI changed. It used to offer a **raw** Lottie, whose colours are wired to a
`control` layer through expressions so `colors=secondary:#2a76dd` works at runtime. It now
appears to export only a **customized** Lottie, with colours flattened to static values at
export time. A first round of re-exports came back with a `control` layer and **zero** colour
expressions — a control layer nothing listens to, so the shortcode was inert and the icons
stayed green. (Removing the orphaned control layer does not restore runtime control; tested.)

**The fix that works:** set **secondary → `#2a76dd`** in the Lordicon customizer *before*
exporting. The blue is then baked in as a static value and renders correctly.

## Current state

| group | count | how colour is applied |
|---|---|---|
| raw exports for the section dividers | 70 | runtime remap via `colors=`, control-layer expressions |
| legacy CDN files | ~35 | runtime remap via `colors=` (direct colour match) |
| older raw exports (`rulers`, `theater`, `caution`, `poetry`) | 4 | runtime remap via control-layer expressions |
| re-exported under the new UI | 12 | **baked in at export time**; `colors=` is inert |
| `quotation` | 1 | single-colour icon, no secondary layer — renders dark navy only |

The shortcodes stay uniform — `colors=secondary:#2a76dd` on all 106 call sites — even where
inert. Same rendered result, and for the 70 raw exports it is doing real work again.

## Maintenance note

For the 12 export-customized icons the accent colour is **fixed at export time**. If the
course ever changes its accent colour, those must be re-exported from Lordicon — a
find-and-replace on the shortcodes will not move them. Expect this group to grow as icons get
replaced over time.

**AEP / MOGRT** downloads are not usable here: AEP is an After Effects project, MOGRT a
Premiere Pro template, and `<lord-icon>` reads only Lottie JSON. (An AEP *could* be re-exported
via After Effects + Bodymovin to restore runtime colour control, but that's a large workflow
for a capability worth almost nothing here.)

## How to re-verify

Static JSON inspection is **not** reliable on its own: legacy files legitimately
contain `#08a88a` and render correctly, so only a browser check distinguishes real
failures. Two passes, and both are quick to script rather than eyeball:

**Colour, in the browser.** Render every icon at `colors=secondary:#2a76dd`, then walk
each one's shadow-DOM SVG and collect the computed `fill` and `stroke` of every node.
Lordicon's green is `rgb(8, 168, 138)` and the course accent is `rgb(42, 118, 221)`;
an icon that shows the first, or never shows the second, is the one to look at.
`icon-contact-sheet.html` is the manual version of the same thing.

**Slots, from the JSON.** The `control` layer's effects give the default value of each
colour slot, which is what says whether `colors=secondary` will do anything at all.
That is how the three exceptions above were found, and a thumbnail would not have
shown two of them.

One trap worth knowing: both passes read `_site/icons/`, which Quarto only refreshes
on a render. Dropping new files into `icons/` and testing immediately reports every
one of them as failing to render, which looks alarming and means nothing.

For the divider illustrations specifically, `tools/section-art-map.tsv` records which
icon belongs on which slide and `tools/wire-section-art.py` puts them there.
