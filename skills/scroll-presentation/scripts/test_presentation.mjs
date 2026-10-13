#!/usr/bin/env node
/* Headless QA for a built scroll-presentation.
 *   node test_presentation.mjs <index.html> [--out <dir>] [--no-shots]
 * Needs `playwright` (bundled browsers) or `playwright-core` + a Chrome/Chromium (set CHROME_PATH).
 * Checks per viewport (phone 390x844 touch, desktop 1440x900, phone + reduced motion):
 *   - no page errors / console errors, no non-file network requests
 *   - every pinned scene reaches each step (data-sp-step) at its label
 *   - snapping: stopping mid-step settles on that step's end state
 *   - no horizontal overflow on phone
 *   - phone: the first .sp-handle can be touch-dragged, changes the nearest readout, and does not scroll the page
 * Screenshots: opening + each scene's final step (phone), first two scenes' final step (desktop),
 *   the hands-on moment (phone) and a reduced-motion still frame.
 */
import fs from 'node:fs'; import path from 'node:path'; import { createRequire } from 'node:module';
const require = createRequire(process.cwd() + '/');
const args = process.argv.slice(2); const file = path.resolve(args.find(a => !a.startsWith('--')) || 'index.html');
const outDir = path.resolve(args.includes('--out') ? args[args.indexOf('--out') + 1] : path.dirname(file));
const shots = !args.includes('--no-shots');
let pw; try { pw = require('playwright'); } catch { pw = require('playwright-core'); }
const guess = [process.env.CHROME_PATH, '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'].filter(Boolean).find(p => fs.existsSync(p));
const browser = await pw.chromium.launch({ executablePath: process.env.CHROME_PATH || (pw.chromium.executablePath && fs.existsSync(pw.chromium.executablePath()) ? undefined : guess), args: ['--no-sandbox'] });
const url = 'file://' + file; const fails = []; const log = (...a) => console.log(...a);
const VIEWS = [
  { name: 'phone', ctx: { viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true } },
  { name: 'desktop', ctx: { viewport: { width: 1440, height: 900 } } },
  { name: 'phone-reduced', ctx: { viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true, reducedMotion: 'reduce' } },
];
const sleep = ms => new Promise(r => setTimeout(r, ms));
for (const v of VIEWS) {
  const ctx = await browser.newContext(v.ctx); const pg = await ctx.newPage(); const errs = [], net = [];
  pg.on('pageerror', e => errs.push(e.message));
  pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  pg.on('request', r => { const u = r.url(); if (!/^(file|data|blob|about):/.test(u)) net.push(u); });
  await pg.goto(url); await sleep(800);
  const info = await pg.evaluate(() => (window.ScrollStory ? ScrollStory.scenes.map(s => ({ id: s.el.id, pinned: !!s.st, labels: s.labels, n: s.steps.length })) : null));
  if (!info) { fails.push(`${v.name}: window.ScrollStory missing`); await ctx.close(); continue; }
  log(`\n[${v.name}] scenes: ${info.map(s => `${s.id}(${s.n} steps${s.pinned ? '' : ', still'})`).join(', ')}`);
  if (shots && v.name === 'phone') await pg.screenshot({ path: path.join(outDir, `shot-phone-0-opening.png`) });
  const scrollToP = (id, p) => pg.evaluate(([id, p]) => { const s = ScrollStory.scenes.find(x => x.el.id === id); window.scrollTo(0, Math.round(s.st.start + p * (s.st.end - s.st.start))); }, [id, p]);
  const read = id => pg.evaluate(id => { const e = document.getElementById(id); return { p: e.dataset.spProgress, step: +e.dataset.spStep }; }, id);
  let sceneNo = 0;
  for (const s of info) {
    sceneNo++;
    if (!s.pinned) { if (v.name !== 'phone-reduced' && v.name !== 'none') fails.push(`${v.name}: ${s.id} not pinned`); continue; }
    for (let k = 0; k < s.n; k++) {                       // each anchored end state
      await scrollToP(s.id, s.labels[k + 1]); await sleep(1100);
      const r = await read(s.id);
      if (r.step !== k || Math.abs(+r.p - s.labels[k + 1]) > 0.02) fails.push(`${v.name}: ${s.id} step ${k} expected p=${s.labels[k + 1].toFixed(3)}, got step ${r.step} p=${r.p}`);
    }
    // snap: stop 40% into the last step's animation (scrolling forward) and expect it to settle on that step's end
    const k = s.n - 1, mid = s.labels[k] + (s.labels[k + 1] - s.labels[k]) * 0.4;
    await scrollToP(s.id, s.labels[k] + 0.001); await sleep(1300);
    await scrollToP(s.id, mid); await sleep(2200);
    const r = await read(s.id);
    const ok = Math.abs(+r.p - s.labels[k + 1]) < 0.02;
    log(`  ${s.id}: steps ok; snap from p=${mid.toFixed(3)} -> ${r.p} ${ok ? '(snapped)' : '(NOT snapped)'}`);
    if (!ok) fails.push(`${v.name}: ${s.id} did not snap (p=${r.p}, want ${s.labels[k + 1].toFixed(3)})`);
    if (shots && v.name === 'phone') await pg.screenshot({ path: path.join(outDir, `shot-phone-${sceneNo}-${s.id}.png`) });
    if (shots && v.name === 'desktop' && sceneNo <= 2) { await scrollToP(s.id, s.labels[s.n]); await sleep(1300); await pg.screenshot({ path: path.join(outDir, `shot-desktop-${sceneNo}-${s.id}.png`) }); }
  }
  if (v.name === 'phone' && await pg.$('.sp-handle')) {
    await pg.evaluate(() => { const h = document.querySelector('.sp-handle'); window.scrollTo(0, h.getBoundingClientRect().top + scrollY - innerHeight / 2); }); await sleep(900);
    const h = await pg.$('.sp-handle'); const bb = await h.boundingBox(); const cx = bb.x + bb.width / 2, cy = bb.y + bb.height / 2;
    const snap = () => pg.evaluate(() => ({ y: scrollY, txt: Array.from(document.querySelectorAll('.sp-section .sp-value')).map(e => e.textContent).join('|') }));
    const before = await snap(); const cdp = await ctx.newCDPSession(pg);
    await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: cx, y: cy }] });
    for (let i = 1; i <= 10; i++) await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: cx + 9 * i, y: cy - 6 * i }] });
    await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }); await sleep(300);
    const after = await snap();
    log(`  drag: readouts ${before.txt} -> ${after.txt}; page scrolled ${after.y - before.y}px`);
    if (before.txt === after.txt) fails.push('phone: dragging the handle did not change any readout');
    if (after.y !== before.y) fails.push('phone: dragging the handle scrolled the page');
    if (shots) await pg.screenshot({ path: path.join(outDir, 'shot-phone-hands-on.png') });
  }
  if (v.name.startsWith('phone')) { const ov = await pg.evaluate(() => document.documentElement.scrollWidth - innerWidth); if (ov > 0) fails.push(`${v.name}: horizontal overflow ${ov}px`); }
  if (v.name === 'phone-reduced') {
    const st = await pg.evaluate(() => ({ pins: ScrollTrigger.getAll().filter(t => t.pin).length, still: document.querySelectorAll('.sp-static').length, scenes: ScrollStory.scenes.length }));
    log(`  reduced motion: pins=${st.pins}, still scenes=${st.still}/${st.scenes}`);
    if (st.pins || st.still !== st.scenes) fails.push(`${v.name}: reduced motion should render still frames without pins`);
    if (shots) { await pg.evaluate(() => window.scrollTo(0, document.querySelector('.sp-scene').offsetTop)); await sleep(400); await pg.screenshot({ path: path.join(outDir, `shot-phone-reduced-motion.png`) }); }
  }
  log(`  errors: ${errs.length ? errs.join(' | ') : 'none'}; external requests: ${net.length ? net.join(', ') : 'none'}`);
  if (errs.length) fails.push(`${v.name}: JS errors`); if (net.length) fails.push(`${v.name}: network requests`);
  await ctx.close();
}
await browser.close();
log(fails.length ? `\nFAIL\n- ${fails.join('\n- ')}` : '\nPASS'); process.exit(fails.length ? 1 : 0);
