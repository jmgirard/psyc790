# Icons — remaining work

## Status

- ✅ **Watermarks gone.** All 51 files are clean (the CDN bulk download had served 10
  free-preview versions carrying a `watermark` layer).
- ✅ **No stale colour convention.** Nothing renders Lordicon's green `#08a88a` because the
  remap hit the wrong layer.
- ⚠️ **12 icons ignore the `colors=` shortcode** — see below.

## The remaining issue

Lordicon's export UI changed. It used to offer a **raw** Lottie (colours wired to a `control`
layer through expressions, so `colors=secondary:#2a76dd` works at runtime) and a
**customized** Lottie (colours flattened to static values at export time). Now it appears to
export only the customized form.

Measured across the 51 files:

| group | control layer | colour expressions | `colors=` works? |
|---|---|---|---|
| `rulers`, `theater`, `caution`, `poetry` (older exports, from data2/psyc894) | yes | 6–8 | **yes** |
| the 12 re-exported under the new UI | yes | **0** | no — inert |
| the other 35 (legacy CDN files) | no | n/a | yes, via direct colour match |

The 12 have a `control` layer that nothing listens to, so the shortcode updates it and nothing
downstream changes. Removing the orphaned control layer does **not** restore runtime control
(tested).

## Fix: set the colour before exporting — ✅ VERIFIED

For each icon below, open it in Lordicon, set **secondary → `#2a76dd`** in the customizer,
then export the Lottie JSON and overwrite the file in `icons/` keeping the filename.

**Confirmed working on `avatar_search.json`.** After re-export it contains `#2a76dd` (x3) and
`#121331` (x3) with no `#08a88a`, comes back with modern `wired-outline-*` naming, and renders
blue + dark navy — an identical colour profile to the known-good `rulers.json`.

Verification for each: the exported JSON should contain `#2a76dd` where it previously had
`#08a88a`. Reload `icon-contact-sheet.html`; every icon should render blue + near-black.

| file | lordicon page |
|---|---|
| ~~`avatar_search.json`~~ | ✅ done |
| `caliper.json` | https://lordicon.com/icons/wired/outline/1749-vernier-caliper |
| `edit_doc.json` | https://lordicon.com/icons/wired/outline/245-edit-document |
| `equalizer.json` | https://lordicon.com/icons/wired/outline/1080-rhythm-audio-equalizer |
| `funnel.json` | https://lordicon.com/icons/wired/outline/736-funnel-tools-utensils |
| `magic_ball.json` | https://lordicon.com/icons/wired/outline/1114-magic-ball |
| `muscle.json` | (replaces the retired `649-jump`) |
| `newspaper.json` | https://lordicon.com/icons/wired/outline/411-news-newspaper |
| `people.json` | https://lordicon.com/icons/wired/outline/275-female-and-two-males |
| `privacy_policy.json` | https://lordicon.com/icons/wired/outline/966-privacy-policy |
| `target.json` | https://lordicon.com/icons/wired/outline/458-goal-target |
| `test_tubes.json` | https://lordicon.com/icons/wired/outline/1221-test-tubes |

## Leave the shortcodes alone

Keep `colors=secondary:#2a76dd` on all 70 call sites even though it is inert for these 12.
The source stays uniform, the rendered result is identical either way, and if Lordicon ever
restores raw export the shortcode simply starts working again.

## Consequence worth knowing

For export-customized icons the accent colour is **fixed at export time**. If the course ever
changes its accent colour, those icons must be re-exported — the shortcode won't move them.
Worth a line in Katie's README, since over time more icons will end up in this category as
they get replaced.
