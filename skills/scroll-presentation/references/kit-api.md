# Kit API (`assets/kit.js` → `window.ScrollStory`)

## `scene(selector, opts)`
Pins the section, scrubs a 0→1 progress with scroll, snaps to step end states, swaps captions, and builds step dots.

| option | default | meaning |
|---|---|---|
| `steps` | number of `.sp-cap` | a number, or an array of `{dur, hold}` (relative units). `dur` = animated part, `hold` = scroll distance where the finished frame stays. |
| `render(t, p, step)` | — | draw the frame. `t[k]` ∈ 0..1 is the progress of step k, `p` is the whole scene, `step` is the active step index. Must be **pure**: the same input gives the same frame, because scroll can go backwards. |
| `still` | all steps = 1 | the `t` array to render as the still frame (reduced motion / no GSAP). |
| `vhPerUnit` | `0.55` | viewport heights of scroll per unit of `dur + hold`. |
| `scrub` | `0.6` | ScrollTrigger scrub smoothing in seconds. |
| `snap` | on | `false` disables snapping for that scene. |
| `dots` | on | `false` hides the step dots. |

Returns `{el, marks, labels, st, tl}`. `st` is the ScrollTrigger and `labels` are the snap targets (0..1).
The DOM gets `data-sp-progress` and `data-sp-step` on the section (used by the test script).

Markup:
```html
<section class="sp-scene" id="s-x">
  <div class="sp-head"><p class="sp-eyebrow">2 / 5</p><h2>Headline</h2></div>
  <div class="sp-vis"><div class="sp-overlay">…readouts…</div><svg viewBox="0 0 360 300"></svg></div>
  <div class="sp-caps"><p class="sp-cap">Step 1</p><p class="sp-cap">Step 2</p></div>
</section>
```

## `counter(el, {decimals, prefix, suffix, format(v), tone(v)})` → `{set(v)}`
Writes only when the text changes. `tone` returns `'good' | 'bad' | ''`. It sets `data-tone` on the enclosing `.sp-readout` (colored by CSS) **and** appends ✓ / ✗.

## `morph(from, to, t, {stagger, arc, ease, xLead})` → `[{x, y, t}]`
Moves a point set from one layout to another. `stagger` (0–0.9) spreads the start times, `arc` (px) adds a hop, and `xLead` (0–1) lets x travel ahead of y.
## `place(elements, points)`
Puts circles at `cx/cy`, other SVG elements at `transform`, and HTML elements at `translate3d`.
## `pointsFromDOM(elements, svg)`
Returns element centers in SVG user units. Use it to fly HTML things into a chart.

## `dragHandle(box, {get, set, axis, bounds, keyStep, label, svg})`
Creates an HTML `<button class="sp-handle">` over the SVG and positions it in % of the viewBox. It uses pointer capture, `touch-action:none` and arrow keys.
`get()` returns `{x, y}` in SVG units, and `set({x, y})` receives the new position. Clamp or snap the position inside `set`.

## `util`
`clamp, lerp, seg(p, a, b), ease.{linear, smooth, out, inOut}, svg(tag, attrs, parent), rng(seed), scale(domain, range)`.

## Gotchas learned the hard way
- **`touch-action` does nothing on SVG `<g>`/`<circle>`.** Make handles HTML elements overlaid on the SVG. Otherwise dragging scrolls the page.
- Use `100svh` (with a `100vh` fallback) for pinned scenes, and `ScrollTrigger.config({ignoreMobileResize:true})` (the kit does this). Otherwise the iOS/Android URL bar resizes break pins.
- Text near the bottom edge of an SVG gets clipped. Leave about 12 units of margin in the `viewBox`, or set `overflow:visible`.
- Don't nest pinned scenes, and don't put a pinned scene inside a transformed parent.
- Precompute expensive things (curve samples, algorithm iterations) once. `render` should only interpolate and set attributes.
- Toggle classes only when the step changes. Set attributes every frame, but avoid layout reads (`getBoundingClientRect`) inside `render`.
- Call `ScrollTrigger.refresh()` after fonts or images change the layout (the kit does it on `load`).
