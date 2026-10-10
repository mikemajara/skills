---
name: scroll-presentation
description: Build a scroll-driven story page in the style of an Apple product page, where sections pin, objects morph from one form to the next, and every step snaps to a finished frame. The result is one offline HTML file that works on phones first. Use it to explain a concept, product, idea, process, or curiosity to any audience, for example a customer pitch, a product explainer, an internal walkthrough, or a class. Also use it when someone asks for a "scrollytelling" or "scroll story" page, or for a deck rebuilt as a scrolling page. Don't use it for slide decks (.pptx) or long text documents.
---

# Scroll presentation

The output is one self-contained HTML page. The story plays as you scroll: scenes pin in place, the same objects transform from scene to scene, and live counters and step dots keep the audience oriented. When scrolling stops, the animation eases to the nearest finished frame. The page works offline and on a phone in portrait first. With reduced motion, it degrades to still frames.

## Workflow

1. **Pick the one idea.** Write the takeaway in one sentence. If you need two sentences, make two presentations or cut one idea.
2. **Find the characters and the key transformation.** Characters are the objects the audience follows, such as rows, dots, people, or a line. The key transformation is the moment the idea clicks. Examples: table rows fly into a chart, 23 dots form 253 pairs, a cloud of points collapses into a line. Characters move and morph across scenes. Don't wipe the screen. See `references/design-principles.md`.
3. **Storyboard 2 to 8 scenes.** For each scene, write the headline, the characters on stage, and its steps. Give each step a caption of 25 words or less and a **snap end state**: the finished frame the reader lands on when they stop scrolling. Mark at most one hands-on moment, where the audience drags something. Pick patterns from `references/scene-patterns.md`.
4. **Scaffold and build from the template.**
   `python3 scripts/sp.py new <dir> --title "…"` creates `<dir>/index.src.html` and `<dir>/kit/`. Each scene is a `<section class="sp-scene">` with one `.sp-cap` per step, plus one `ScrollStory.scene()` call whose `render(t)` draws step progress `t[k]`. The kit handles pinning, scrub, snap, step dots, captions, the progress bar, the scroll cue and still frames. API and gotchas: `references/kit-api.md`. Snap tuning: `references/snapping.md`.
5. **Bundle.** Run `python3 scripts/sp.py build <dir>/index.src.html -o <dir>/index.html`. It inlines the CSS, the JS and the vendored GSAP, and fails if any external URL remains.
6. **Test** at phone (390×844, touch), desktop (1440×900) and phone with reduced motion. Run `node scripts/test_presentation.mjs <dir>/index.html --out <dir>`. It needs `playwright` or `playwright-core` plus Chrome. It checks for JS errors and network requests, confirms every step and the snap behavior, tests the drag handle, and takes screenshots. Then look at the screenshots yourself against `references/testing.md`.
7. **Publish.** The output is one static file. Any static host works (object storage, GitHub Pages, Netlify, an intranet share), or you can send the file itself. No build step or server is needed.

## Defaults (taste, not dogma)

- **Objects as characters.** Carry the same objects through scenes and transform them.
- **Flat, restrained color.** Use neutral ink plus one accent, picked per presentation. No rainbow palettes, decorative gradients or glows. Add a second color only when it has a job, such as good vs. bad or one color per data series. Always pair color with a label or a ✓/✗ symbol.
- **Context keepers.** Use an opening scroll cue, an overall progress bar, step dots inside each scene, and live counters that move with the objects.
- **Anchored steps.** Snap to step end states. Never leave the reader on a half-finished frame.
- **Mobile first.** Design for portrait phone first; desktop gets two columns automatically. Touch targets are at least 44 px. Keep scenes tight: about 0.5 to 0.6 viewport heights of scroll per step.
- **Honest data.** Label synthetic data as example data on the page.
- **Short text.** One idea per caption. Use system fonts or a clean sans (Inter or Geist if installed). Eases should be smooth, never bouncy.
- **Avoid** busy pill and badge labels, parallax that explains nothing, long scroll distances, and more than one hands-on moment.

## Files

- `assets/template.html` is the starter page: an opening, one example scene, one hands-on section and a footer.
- `assets/kit.js` is the scene system (`window.ScrollStory`): `scene`, `counter`, `morph`, `place`, `pointsFromDOM`, `dragHandle`, plus helpers in `util`.
- `assets/kit.css` holds the layout, captions, step dots, readouts, progress bar, scroll cue, drag handle and still-frame styles. Palette lives in CSS variables.
- `assets/vendor/` holds GSAP and ScrollTrigger 3.15.0. `VENDOR.md` has the license, checksums, a pinned CDN fallback and update steps. Lenis is optional and not bundled.
- `references/design-principles.md`, `scene-patterns.md`, `kit-api.md`, `snapping.md`, `testing.md`, `worked-example.md`.
- `scripts/sp.py` scaffolds and bundles (stdlib Python). `scripts/test_presentation.mjs` runs the headless QA.
