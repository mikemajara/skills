/* scroll-presentation kit: a small scene system on top of GSAP + ScrollTrigger.
 * Exposes window.ScrollStory. Works without GSAP or with reduced motion: scenes then render as still frames.
 *
 *   ScrollStory.scene('#s-intro', {
 *     steps: [{dur:1, hold:.4}, {dur:1}],   // or just a number of steps; captions (.sp-cap) map 1:1 to steps
 *     render(t, p, step) { ... }            // t[k] = 0..1 progress of step k; p = whole scene 0..1
 *     still: [1, 1]                         // optional: which frame to show as the still (defaults to all steps done)
 *   });
 */
(function (global) {
  'use strict';
  var RM = global.matchMedia && global.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var HAS = typeof global.gsap !== 'undefined' && typeof global.ScrollTrigger !== 'undefined';
  if (HAS) { gsap.registerPlugin(ScrollTrigger); ScrollTrigger.config({ ignoreMobileResize: true }); }

  /* ---------------- small math + svg helpers ---------------- */
  var U = {
    clamp: function (v, a, b) { return Math.max(a, Math.min(b, v)); },
    lerp: function (a, b, t) { return a + (b - a) * t; },
    /** local 0..1 progress of p inside [a, b] */
    seg: function (p, a, b) { return U.clamp((p - a) / (b - a), 0, 1); },
    ease: {
      linear: function (t) { return t; },
      smooth: function (t) { return t * t * (3 - 2 * t); },
      out: function (t) { return 1 - Math.pow(1 - t, 3); },
      inOut: function (t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
    },
    /** create an SVG element: U.svg('circle', {cx:1, r:4}, parent) */
    svg: function (tag, attrs, parent) {
      var e = document.createElementNS('http://www.w3.org/2000/svg', tag);
      for (var k in attrs) e.setAttribute(k, attrs[k]);
      if (parent) parent.appendChild(e);
      return e;
    },
    /** seeded PRNG so example data is reproducible */
    rng: function (seed) { return function () { seed = (seed + 0x6D2B79F5) | 0; var t = Math.imul(seed ^ (seed >>> 15), 1 | seed); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; },
    /** linear scale: U.scale([d0,d1],[r0,r1])(v) */
    scale: function (d, r) { return function (v) { return r[0] + (v - d[0]) / (d[1] - d[0]) * (r[1] - r[0]); }; }
  };

  /* ---------------- scenes: pin + scrub + snap-to-step ---------------- */
  var scenes = [];
  /** Where to settle when scrolling stops at progress v.
   *  Inside a step's animation: forward -> that step's end state; backward -> the previous end state.
   *  Inside a hold (frame is already complete): stay on that end state. */
  function snapTarget(marks, v, dir) {
    var eps = 0.006;                                                 // absorbs scroll-pixel rounding
    for (var k = 0; k < marks.length; k++) {
      var m = marks[k], prevEnd = k ? marks[k - 1].e : 0;
      if (v < m.s + eps) return prevEnd;                             // in the hold before step k
      if (v < m.e - eps) return dir >= 0 ? m.e : prevEnd;            // mid-animation
      if (v <= m.e + eps) return m.e;                                // already at this end state
    }
    return v > (marks[marks.length - 1].e + 1) / 2 && dir >= 0 ? 1 : marks[marks.length - 1].e;  // final hold
  }
  var DEFAULT_STEP = { dur: 1, hold: 0.35 };

  function normSteps(steps, nCaps) {
    if (steps == null) steps = Math.max(1, nCaps);
    if (typeof steps === 'number') { var a = []; for (var i = 0; i < steps; i++) a.push({}); steps = a; }
    return steps.map(function (s) { return { dur: s.dur != null ? s.dur : DEFAULT_STEP.dur, hold: s.hold != null ? s.hold : DEFAULT_STEP.hold }; });
  }

  function scene(target, opts) {
    var el = typeof target === 'string' ? document.querySelector(target) : target;
    if (!el) throw new Error('ScrollStory.scene: no element for ' + target);
    opts = opts || {};
    var caps = Array.prototype.slice.call(el.querySelectorAll('.sp-cap'));
    var steps = normSteps(opts.steps, caps.length);
    var total = steps.reduce(function (s, x) { return s + x.dur + x.hold; }, 0);
    // marks: normalized [start, end] of each step's animation; label = end (the "anchored" state)
    var acc = 0, marks = steps.map(function (s) { var m = { s: acc / total, e: (acc + s.dur) / total }; acc += s.dur + s.hold; return m; });

    // step dots
    var dots = [], box = el.querySelector('.sp-steps');
    if (!box && opts.dots !== false && steps.length > 1) { box = document.createElement('div'); box.className = 'sp-steps'; (el.querySelector('.sp-caps') || el).appendChild(box); }
    if (box) { box.setAttribute('aria-hidden', 'true'); for (var i = 0; i < steps.length; i++) dots.push(box.appendChild(document.createElement('span'))); }

    var lastStep = -1;
    function stateAt(p) {
      var t = marks.map(function (m) { return U.clamp((p - m.s) / (m.e - m.s), 0, 1); });
      var k = 0; for (var j = 0; j < marks.length; j++) if (p >= marks[j].s - 1e-6) k = j;
      return { t: t, step: k };
    }
    function update(p) {
      var st = stateAt(p);
      opts.render && opts.render(st.t, p, st.step);
      if (st.step !== lastStep) {
        caps.forEach(function (c, j) { c.classList.toggle('is-on', j === st.step); });
        dots.forEach(function (d, j) { d.classList.toggle('is-on', j === st.step); d.classList.toggle('is-done', j < st.step); });
        lastStep = st.step;
      }
      el.dataset.spProgress = p.toFixed(3);
      el.dataset.spStep = st.step;
    }

    var s = { el: el, marks: marks, steps: steps, update: update, st: null, labels: [0].concat(marks.map(function (m) { return m.e; })).concat([1]) };
    scenes.push(s);

    if (RM || !HAS) {
      el.classList.add('sp-static');
      var still = opts.still || steps.map(function () { return 1; });
      opts.render && opts.render(still, 1, steps.length - 1);
      el.dataset.spProgress = 'static';
      return s;
    }

    update(0);
    var proxy = { p: 0 };
    var vh = opts.vhPerUnit != null ? opts.vhPerUnit : 0.55;   // scroll distance per (dur+hold) unit, in viewport heights
    var tl = gsap.timeline({
      defaults: { ease: 'none' },
      scrollTrigger: {
        trigger: el, start: 'top top',
        end: function () { return '+=' + Math.round(total * vh * global.innerHeight); },
        pin: true, scrub: opts.scrub != null ? opts.scrub : 0.6, anticipatePin: 1, invalidateOnRefresh: true,
        snap: opts.snap === false ? undefined : {
          // Anchored steps: when scrolling stops, ease ON (in the direction the reader was going) to the
          // nearest step end state, so nobody is left on a half-finished frame.
          snapTo: function (v, self) { return snapTarget(marks, v, self ? self.direction : 1); },
          duration: { min: 0.2, max: 0.7 }, delay: 0.08, ease: 'power2.inOut',
          inertia: false                          // no velocity projection: a fast flick must not skip past steps
        }
      }
    });
    tl.to(proxy, { p: 1, duration: 1, onUpdate: function () { update(proxy.p); } }, 0);
    tl.addLabel('start', 0);
    marks.forEach(function (m, k) { tl.addLabel('step' + k, m.e); });
    tl.addLabel('end', 1);
    s.st = tl.scrollTrigger; s.tl = tl;
    return s;
  }

  /* ---------------- live counters / readouts ---------------- */
  /** counter(el, {decimals, prefix, suffix, tone(v) -> 'good'|'bad'|''}) -> {set(v)}
   *  tone adds data-tone on the closest .sp-readout AND a symbol (✓ / ✗) so meaning never relies on color alone. */
  function counter(el, o) {
    el = typeof el === 'string' ? document.querySelector(el) : el;
    o = o || {};
    var wrap = el.closest('.sp-readout') || el, last = null;
    return {
      el: el,
      set: function (v) {
        var txt = o.format ? o.format(v) : (o.prefix || '') + Number(v).toFixed(o.decimals || 0) + (o.suffix || '');
        if (o.tone) {
          var tone = o.tone(v) || '';
          wrap.dataset.tone = tone;
          txt += tone === 'good' ? ' ✓' : tone === 'bad' ? ' ✗' : '';
        }
        if (txt !== last) { el.textContent = txt; last = txt; }
      }
    };
  }

  /* ---------------- morph: move a set of points from one layout to another ---------------- */
  /** morph(from[], to[], t, {stagger:0..0.9, arc:px, ease, xLead:0..1})
   *  returns [{x, y, t}] where t is each point's own eased progress.
   *  xLead > 0 lets x travel ahead of y, which reads better than a straight diagonal when rows fly into a chart. */
  function morph(from, to, t, o) {
    o = o || {};
    var n = from.length, st = o.stagger || 0, ez = o.ease || U.ease.smooth, arc = o.arc || 0, lead = o.xLead || 0;
    return from.map(function (a, i) {
      var b = to[i], start = n > 1 ? st * i / (n - 1) : 0;
      var lt = U.clamp((t - start) / (1 - st), 0, 1), e = ez(lt), ex = ez(U.clamp(lt / (1 - lead * .5), 0, 1));
      return { x: U.lerp(a.x, b.x, ex), y: U.lerp(a.y, b.y, e) - arc * Math.sin(Math.PI * e), t: e };
    });
  }
  /** place(elements, points): SVG circles get cx/cy, other SVG gets transform, HTML gets translate3d */
  function place(els, pts) {
    for (var i = 0; i < els.length; i++) {
      var e = els[i], p = pts[i]; if (!p) continue;
      if (e.tagName === 'circle' || e.tagName === 'ellipse') { e.setAttribute('cx', p.x); e.setAttribute('cy', p.y); }
      else if (e instanceof SVGElement) e.setAttribute('transform', 'translate(' + p.x + ',' + p.y + ')');
      else e.style.transform = 'translate3d(' + p.x + 'px,' + p.y + 'px,0)';
    }
  }
  /** centers of DOM elements expressed in an SVG's user coordinates (to fly HTML things into an SVG chart) */
  function pointsFromDOM(els, svgEl) {
    var inv = svgEl.getScreenCTM().inverse();
    return Array.prototype.map.call(els, function (e) {
      var r = e.getBoundingClientRect(), pt = svgEl.createSVGPoint();
      pt.x = r.left + r.width / 2; pt.y = r.top + r.height / 2; pt = pt.matrixTransform(inv);
      return { x: pt.x, y: pt.y };
    });
  }

  /* ---------------- touch-friendly drag handle ---------------- */
  /** dragHandle(box, {svg, get()->{x,y}, set({x,y}), axis:'x'|'y'|'both', label, keyStep, bounds:{x0,x1,y0,y1}})
   *  box = a .sp-dragbox wrapping the svg. The handle is an HTML <button> (touch-action:none works on it;
   *  it does NOT work on SVG <g>), positioned in % of the viewBox, so the rest of the chart still scrolls the page. */
  function dragHandle(box, o) {
    var svgEl = o.svg || box.querySelector('svg'), vb = svgEl.viewBox.baseVal;
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'sp-handle'; b.setAttribute('aria-label', o.label || 'Drag handle; arrow keys move it');
    box.appendChild(b);
    var axis = o.axis || 'both', B = o.bounds || { x0: vb.x, x1: vb.x + vb.width, y0: vb.y, y1: vb.y + vb.height }, dragging = false;
    function pos() { var q = o.get(); b.style.left = ((q.x - vb.x) / vb.width * 100) + '%'; b.style.top = ((q.y - vb.y) / vb.height * 100) + '%'; }
    function toSvg(e) { var pt = svgEl.createSVGPoint(); pt.x = e.clientX; pt.y = e.clientY; return pt.matrixTransform(svgEl.getScreenCTM().inverse()); }
    function apply(q) {
      var cur = o.get(), nx = axis === 'y' ? cur.x : U.clamp(q.x, B.x0, B.x1), ny = axis === 'x' ? cur.y : U.clamp(q.y, B.y0, B.y1);
      o.set({ x: nx, y: ny }); pos();
    }
    b.addEventListener('pointerdown', function (e) { dragging = true; b.classList.add('is-dragging'); b.setPointerCapture(e.pointerId); e.preventDefault(); });
    b.addEventListener('pointermove', function (e) { if (dragging) apply(toSvg(e)); });
    ['pointerup', 'pointercancel', 'lostpointercapture'].forEach(function (t) { b.addEventListener(t, function () { dragging = false; b.classList.remove('is-dragging'); }); });
    b.addEventListener('keydown', function (e) {
      var k = o.keyStep || vb.width / 60, c = o.get(), d = { ArrowLeft: [-k, 0], ArrowRight: [k, 0], ArrowUp: [0, -k], ArrowDown: [0, k] }[e.key];
      if (!d) return; e.preventDefault(); apply({ x: c.x + d[0], y: c.y + d[1] });
    });
    pos();
    return { el: b, update: pos };
  }

  /* ---------------- page chrome: progress bar, scroll cue, one-time reveals ---------------- */
  function chrome() {
    var bar = document.querySelector('.sp-progress'), cue = document.querySelector('.sp-cue');
    function onScroll() {
      var max = document.documentElement.scrollHeight - global.innerHeight, f = max > 0 ? global.scrollY / max : 0;
      if (bar) bar.style.transform = 'scaleX(' + f.toFixed(4) + ')';
      if (cue) cue.style.opacity = global.scrollY > 40 ? 0 : 1;
    }
    global.addEventListener('scroll', onScroll, { passive: true }); onScroll();
    if (!HAS || RM) return;
    gsap.utils.toArray('[data-sp-reveal]').forEach(function (e) {
      gsap.from(e, { y: 28, autoAlpha: 0, duration: .9, ease: 'power3.out', scrollTrigger: { trigger: e, start: 'top 88%', once: true } });
    });
  }

  function start() {
    chrome();
    if (HAS) global.addEventListener('load', function () { ScrollTrigger.refresh(); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();

  global.ScrollStory = { scene: scene, counter: counter, morph: morph, place: place, pointsFromDOM: pointsFromDOM, dragHandle: dragHandle, util: U, scenes: scenes, reducedMotion: RM, hasGsap: HAS };
})(window);
