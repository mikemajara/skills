# Design principles

These are defaults, not dogma. Break one when the story needs it, and say why in a comment in the source.

## 1. Objects as characters (strong default)

The audience remembers *things that change*. Pick 1–3 objects that stay on stage across scenes and transform them.
Wiping the screen and drawing something new is a weaker move.

- Table rows fly into scatter-plot dots. The same dots then get a line, the line's misses become bars, and the bars become squares.
- 23 dots queue up, form a circle, then sprout pair lines.
- A product's three features start as cards, collapse into icons, then dock onto a diagram of the product.
- Pipeline stages start as boxes in a row. Each one lights up as a "packet" dot travels through.

How to carry an object across two pinned scenes: draw it in **identical coordinates** in both SVGs (same viewBox, same positions). Then make scene A's final frame equal scene B's first frame. The reader sees one continuous object even though they are two elements.

Some things are not characters: decorative particles, floating blobs, and parallax background shapes. They add motion without meaning.

## 2. Color restraint

The palette is chosen per presentation. The rule is about **restraint**, not about specific colors.

- Default: neutral ink and background, plus **one accent** for the characters.
- Add color only when it does a practical job:
  - **good vs. bad** (`--good` / `--bad`), e.g. a passing vs. failing approach;
  - **one color per data series** when a chart plots several (train vs. test, before vs. after);
  - **the highlighted one** (`--accent-2`): the single matching pair, the outlier, the chosen option.
- Avoid rainbow palettes, badly combined hues, decorative gradients, glows, gradient text, and colored backgrounds on every card.
- **Always pair color with a non-color cue**: a label, a ✓/✗ symbol (`counter({tone})` adds one), a dashed vs. solid line, or a size difference. About 1 in 12 men has a color-vision deficiency, and phone screens in sunlight wash out hue.
- Contrast: body text ≥ 4.5:1 and large numbers ≥ 3:1 against the background.

## 3. Context keepers

A pinned page can disorient people ("is this stuck?"). Four small instruments prevent that:

- an **opening scroll cue** (`.sp-cue`) that fades after the first scroll;
- an **overall progress bar** (`.sp-progress`) across the top;
- **step dots** inside each scene (added automatically), where the current step is long and done steps are filled;
- **live counters / readouts** (`ScrollStory.counter`) that update as objects move. Counters make the transformation *quantitative*: "pairs: 253", "error: 25.5", "chance: 50.7%".

## 4. Anchored steps

Every step ends on a **meaningful finished frame**: a result is shown, a chart is complete, a caption is fully in.
When scrolling stops mid-step, the page eases *on* to that step's end in the direction the reader was going. In a hold, it stays put. The reader never rests on a half-morphed frame. The details are in `snapping.md`.

## 5. Mobile first, and other defaults

- **Portrait phone is the primary canvas.** Each scene is laid out as headline (top), visual (middle, SVG `viewBox` around 360 wide), and caption (bottom). Desktop ≥ 900 px wide automatically gets two columns: text left, visual right.
- **Tight scenes.** Each step is about 0.5–0.6 viewport heights of scroll (`vhPerUnit`). A whole presentation should be about 8–20 screens. Long scroll distances feel like scroll-jacking.
- **One hands-on moment**, where it helps understanding: drag a line, a point or a slider. Put it in a *normal* (unpinned) section so touch-dragging never fights the scroll.
- **Reduced motion**: no pins, no scrub, no snap. Each scene is a still frame of its end state with all captions listed. The kit does this automatically.
- **Offline single file.** No CDN, no web fonts fetched, no analytics. `sp.py build` enforces this.
- **Synthetic data is labelled** ("Example data, made up") in the scene or footer. Real data needs a source line.
- **Short text.** Headline ≤ 8 words. Each caption ≤ 25 words with one idea. Bold the one phrase that matters.
- **Typography.** System UI stack, or Inter/Geist if locally installed. Use 1–2 weights and tabular numbers for counters.
- **Motion.** Use `power2/3` and smoothstep eases. No bounce, elastic or spring. Scrubbed motion is linear to scroll, and the easing lives inside `render` via `util.ease`.

## Avoid

- Busy pill or badge labels on everything. One small "Example data" note is enough.
- Parallax or particles that teach nothing.
- More than three things moving at once.
- Text that animates in word by word inside scrubbed scenes, because it is unreadable mid-scrub.
- Hiding essential information only in hover states, since phones have none.
