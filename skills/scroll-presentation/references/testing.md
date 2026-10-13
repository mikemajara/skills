# Testing checklist

## Automated (`scripts/test_presentation.mjs`)
```bash
npm i -D playwright-core           # or `playwright` with bundled browsers
CHROME_PATH=/path/to/chrome node scripts/test_presentation.mjs dist/index.html --out shots/
```
It runs three passes: phone 390×844 with touch, desktop 1440×900, and phone with `prefers-reduced-motion: reduce`.
- No page errors or console errors.
- **No network requests** other than `file:`/`data:`/`blob:`.
- Every pinned scene reaches every step: it scrolls to each label and checks `data-sp-step` and `data-sp-progress`.
- **Snap check**: it stops 40% into the last step and expects the scene to settle on that step's end.
- Phone: no horizontal overflow. It touch-drags the first `.sp-handle` and checks that a readout changed and the page didn't scroll.
- Reduced motion: zero pins, and every scene is a still frame.
- Screenshots: opening, each scene's final step (phone), the first two scenes (desktop), the hands-on moment, and a reduced-motion frame.

The script exits non-zero on any failure. It is safe to run in CI.

## By eye (open the screenshots)
- [ ] The phone headline fits in 3 lines or fewer and captions are fully visible above the step dots.
- [ ] Mid-morph frames look intentional. Scroll to roughly 30% and 60% of a step to check. No text overlaps a chart for long.
- [ ] The characters are recognizably the same objects from scene to scene.
- [ ] No more than 1 accent plus purposeful extra colors, each paired with a label or symbol.
- [ ] Counters and readouts are legible: tabular numbers, at least 22 px on a phone.
- [ ] Example data is labelled and nothing implies the numbers are real.
- [ ] Desktop: the visual fills the right column and the text column isn't sparse.
- [ ] Reduced motion: each still frame tells its scene's story with all captions listed.
- [ ] The hands-on handle is easy to grab with a thumb (48 px target) and the rest of the chart still scrolls the page.
- [ ] The opening scroll cue disappears after scrolling, and the progress bar reaches 100% at the footer.

## On a real phone (before publishing)
- iOS Safari and Android Chrome: the URL bar collapsing and expanding must not jump pinned scenes.
- A fast flick through a scene must not skip its final state permanently. Scrolling back must re-render correctly.
- Rotate the phone to landscape and back, and check that nothing breaks. Landscape phones use the stacked layout.
