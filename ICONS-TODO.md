# Icons to re-download from Lordicon

The bulk download pulled these from `cdn.lordicon.com`, which serves older revisions.
Two problems, overlapping:

- **watermark** — the JSON contains a `watermark` layer (free-preview version).
- **colour** — uses the old colour convention, so `colors=secondary:#2a76dd` leaves the
  green `#08a88a` in place and recolours the wrong layer. Renders blue+green, not blue+black.

Fix: download each from your Lordicon PRO account (Lottie JSON) and overwrite the file
in `icons/`. Keep the filename exactly as listed. Then re-open `icon-contact-sheet.html`
and I can re-verify all 51 in one pass.

| file | problem | lordicon page | used in |
|---|---|---|---|
| `avatar_search.json` | watermark | https://lordicon.com/icons/wired/outline/288-avatar-man-search | A/03/b |
| `caliper.json` | watermark, colour | https://lordicon.com/icons/wired/outline/1749-vernier-caliper | B/05/b |
| `edit_doc.json` | watermark | https://lordicon.com/icons/wired/outline/245-edit-document | B/05/b |
| `equalizer.json` | watermark | https://lordicon.com/icons/wired/outline/1080-rhythm-audio-equalizer | B/05/a, B/05/b |
| `funnel.json` | colour | https://lordicon.com/icons/wired/outline/736-funnel-tools-utensils | B/05/a |
| `jump.json` | colour | https://lordicon.com/icons/wired/outline/649-jump | A/01/b |
| `magic_ball.json` | watermark, colour | https://lordicon.com/icons/wired/outline/1114-magic-ball | B/05/b |
| `newspaper.json` | colour | https://lordicon.com/icons/wired/outline/411-news-newspaper | B/05/b |
| `people.json` | watermark, colour | https://lordicon.com/icons/wired/outline/275-female-and-two-males | B/05/a |
| `privacy_policy.json` | watermark | https://lordicon.com/icons/wired/outline/966-privacy-policy | B/05/a |
| `target.json` | colour | https://lordicon.com/icons/wired/outline/458-goal-target | B/05/b |
| `test_tubes.json` | watermark | https://lordicon.com/icons/wired/outline/1221-test-tubes | B/05/a |

## Already fixed

Copied from your existing repos (all v5.12.1, clean, modern structure):
`rulers.json`, `theater.json` (psyc894) and `caution.json`, `poetry.json` (data2).
