# Icons — resolved

All 51 icons verified: **no watermarks, none rendering Lordicon's green, all render.**

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

## The export gotcha

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
| legacy CDN files | ~35 | runtime remap via `colors=` (direct colour match) |
| older raw exports (`rulers`, `theater`, `caution`, `poetry`) | 4 | runtime remap via control-layer expressions |
| re-exported under the new UI | 12 | **baked in at export time**; `colors=` is inert |
| `quotation` | 1 | single-colour icon, no secondary layer — renders dark navy only |

The shortcodes stay uniform — `colors=secondary:#2a76dd` on all 70 call sites — even where
inert. Same rendered result, and if raw export ever returns it simply starts working again.

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

Open `icon-contact-sheet.html`, set every icon to `colors=secondary:#2a76dd`, and check
whether green survives in the shadow-DOM SVG. Static JSON inspection is **not** reliable —
legacy files legitimately contain `#08a88a` and render correctly, so only the browser check
distinguishes real failures.
