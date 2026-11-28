// Production FX layer (load last): character life (blink, breathing), particles, light leaks, lightning,
// per-act colour grades, transitions (cut / whip / flash / zoom / fade), camera shake and kinetic captions.
// Requires: scene.html, scenes20.js, scenes5.js (tag/PEOPLE), style2.js (skyline, lightBeam, rim light).
let TIME = 0;

// ---------- character life ----------
const _pfx = person;
person = function (o) {
  o = Object.assign({}, o);
  if (o.bob === undefined) o.bob = Math.sin(TIME * 2.2 + (o.x || 0) * 0.01) * 2.5 * (o.s || 1);
  const p = _pfx(o);
  const e = o.expr || 'neutral';
  if (!o.noBlink && !['happy', 'shock', 'tired', 'calm'].includes(e)) {
    const ph = (TIME + (o.x || 0) * 0.0137) % 3.9;
    if (ph < 0.14) {
      const R = p.R, fx = p.hx + (o.look || 0) * R * 0.22, ey = p.hy - R * 0.02;
      for (const sd of [-1, 1]) { circle(fx + sd * R * 0.32, ey, R * 0.13); fs(o.skin || C.skin); line([fx + sd * R * 0.32 - R * 0.11, ey + R * 0.02, fx + sd * R * 0.32 + R * 0.11, ey + R * 0.02], 6 * R / 95); }
    }
  }
  return p;
};

// ---------- particles & light ----------
function rain(t, n = 260, a = 0.45) {
  const r = rand(123); ctx.save(); ctx.globalCompositeOperation = 'lighter';
  for (let i = 0; i < n; i++) {
    const sp = 1600 + r() * 900, x0 = r() * (W + 300), y = ((r() * 1300 + t * sp) % 1300) - 120, x = x0 - y * 0.18, len = 30 + r() * 30;
    line([x, y, x - len * 0.18, y + len], 2, `rgba(170,190,255,${a * (0.3 + r() * 0.7)})`);
  }
  for (let i = 0; i < n / 6; i++) { const k = (t * 3 + r()) % 1, x = r() * W, y = 930 + r() * 140; ctx.globalAlpha = (1 - k) * a; ctx.beginPath(); ctx.ellipse(x, y, 4 + k * 18, 1.5 + k * 4, 0, 0, 7); fs(null, 2, 'rgba(190,210,255,1)'); }
  ctx.restore();
}
function lightning(t, times) { let v = 0; for (const s of times) { const d = t - s; if (d > 0 && d < 0.5) v = Math.max(v, (d < 0.08 ? 1 : d < 0.16 ? 0.3 : d < 0.22 ? 0.9 : Math.max(0, 1 - (d - 0.22) / 0.28))); } return v; }
function fireflies(t, n, x, y, w, h, col = 'rgba(255,210,120,', seed = 3) {
  const r = rand(seed); ctx.save(); ctx.globalCompositeOperation = 'lighter';
  for (let i = 0; i < n; i++) {
    const px = x + r() * w + Math.sin(t * (0.5 + r()) + i) * 30, py = y + r() * h + Math.cos(t * (0.4 + r()) + i * 1.7) * 24, a = 0.4 + 0.6 * Math.abs(Math.sin(t * 2 + i));
    glow(px, py, 16 + r() * 14, col + (0.55 * a) + ')'); circle(px, py, 2.5); fs(col + a + ')');
  }
  ctx.restore();
}
function sparksRise(t, x, y, w, h, n, k, col = 'rgba(255,215,140,') {   // k: 0..1 dissolve progress
  const r = rand(55); ctx.save(); ctx.globalCompositeOperation = 'lighter';
  for (let i = 0; i < n; i++) {
    const st = r() * 0.8; if (k < st) continue; const q = clamp((k - st) / 0.6);
    const px = x + r() * w + Math.sin(t * 3 + i) * 20 * q, py = y + r() * h - q * (200 + r() * 300), a = (1 - q) * 0.9;
    glow(px, py, 18, col + (a * 0.6) + ')'); circle(px, py, 2 + r() * 2.5); fs(col + a + ')');
  }
  ctx.restore();
}
function lightLeak(t, col = 'rgba(255,150,80,', a = 0.35) {
  ctx.save(); ctx.globalCompositeOperation = 'lighter';
  const x = W * (0.85 + 0.12 * Math.sin(t * 0.3)), y = H * (0.2 + 0.15 * Math.cos(t * 0.23));
  const g = ctx.createRadialGradient(x, y, 0, x, y, 700); g.addColorStop(0, col + a + ')'); g.addColorStop(1, col + '0)');
  ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  const x2 = W * (0.05 + 0.08 * Math.cos(t * 0.27)), y2 = H * (0.9 - 0.1 * Math.sin(t * 0.31));
  const g2 = ctx.createRadialGradient(x2, y2, 0, x2, y2, 500); g2.addColorStop(0, col + (a * 0.6) + ')'); g2.addColorStop(1, col + '0)');
  ctx.fillStyle = g2; ctx.fillRect(0, 0, W, H); ctx.restore();
}

// ---------- grades ----------
const GRADES = {
  night: () => { tint('#2a3a9a', 0.22, 'soft-light'); },
  cold: () => { ctx.save(); ctx.globalCompositeOperation = 'saturation'; ctx.globalAlpha = 0.45; ctx.fillStyle = '#808080'; ctx.fillRect(0, 0, W, H); ctx.restore(); tint('#20305a', 0.18, 'multiply'); },
  memory: () => { tint('#704214', 0.3, 'color'); tint('#ffc080', 0.3, 'soft-light'); },
  warm: () => { tint('#ffb46a', 0.28, 'soft-light'); },
  dawn: () => { tint('#ff9a6a', 0.22, 'soft-light'); tint('#6a5aff', 0.08, 'soft-light'); },
  none: () => {},
};

// ---------- kinetic captions (*word* = highlighted key word) ----------
function caption(time, sc) {
  const list = TL.captions.filter(c => time >= c.start && time < c.end);
  for (const c of list) {
    const center = c.scene === 'card' || c.scene.startsWith('title'), size = center ? 92 : 58, font = center ? `${size}px Lucky` : `bold ${size}px "DejaVu Sans"`;
    ctx.font = font;
    const words = c.en.split(' '), plain = words.map(w => w.replace(/\*/g, ''));
    const lines = []; let cur = [], curW = 0, maxW = center ? 1500 : 1550, sp = ctx.measureText(' ').width;
    plain.forEach((w, i) => { const ww = ctx.measureText(w).width; if (cur.length && curW + sp + ww > maxW) { lines.push(cur); cur = []; curW = 0; } cur.push(i); curW += (cur.length > 1 ? sp : 0) + ww; });
    lines.push(cur);
    const lh = size * 1.25, y0 = center ? H / 2 - (lines.length - 1) * lh / 2 : H - 125 - (lines.length - 1) * lh;
    const out = clamp((c.end - time) / 0.4);
    lines.forEach((ln, li) => {
      const lw = ln.reduce((s, i, k) => s + ctx.measureText(plain[i]).width + (k ? sp : 0), 0);
      let x = W / 2 - lw / 2;
      ln.forEach(i => {
        const ws = c.start + i * 0.11, a = clamp((time - ws) / 0.28) * out, key = words[i].includes('*'), ww = ctx.measureText(plain[i]).width;
        if (a > 0) {
          ctx.save(); ctx.globalAlpha = a; ctx.font = font; ctx.textAlign = 'left'; ctx.textBaseline = 'middle';
          const yy = y0 + li * lh + (1 - a) * 18; ctx.translate(x + ww / 2, yy); ctx.scale(0.88 + 0.12 * a, 0.88 + 0.12 * a); ctx.translate(-ww / 2, 0);
          // cheap look: offset soft shadow + outline + (for key words) a wide translucent glow stroke
          ctx.lineJoin = 'round';
          ctx.fillStyle = 'rgba(0,0,0,0.45)'; ctx.fillText(plain[i], 4, 6);
          if (key) { ctx.lineWidth = 22; ctx.strokeStyle = 'rgba(255,200,60,0.22)'; ctx.strokeText(plain[i], 0, 0); ctx.lineWidth = 12; ctx.strokeStyle = 'rgba(255,200,60,0.3)'; ctx.strokeText(plain[i], 0, 0); }
          if (!center) { ctx.lineWidth = 9; ctx.strokeStyle = 'rgba(0,0,0,0.85)'; ctx.strokeText(plain[i], 0, 0); }
          ctx.fillStyle = key ? '#ffd23a' : (center ? '#f3e9da' : '#fff'); ctx.fillText(plain[i], 0, 0);
          ctx.restore();
        }
        x += ww + sp;
      });
    });
  }
}

// ---------- frame: camera, transitions, shake, grade, leaks ----------
let TMP = null;
window.drawFrame = function (frame, fps) {
  const time = frame / fps; TIME = time;
  const sc = TL.scenes.find(s => time >= s.start && time < s.end) || TL.scenes[TL.scenes.length - 1];
  const t = time - sc.start, d = sc.end - sc.start, L = LOOK[sc.id] || {};
  RIM = sc.rim || 'rgba(255,170,90,1)'; RIM_SIDE = 1;
  const tr = sc.trans || 'cut';
  ctx.save();
  // shake
  let sh = 0; if (sc.shake) sh = sc.shake * Math.max(0, 1 - t / 0.6); if (sc.flashes) sh = Math.max(sh, 10 * lightning(t, sc.flashes));
  if (sh) ctx.translate(Math.sin(time * 90) * sh, Math.cos(time * 77) * sh);
  // whip / zoom-in entry
  if (tr === 'whip' && t < 0.3) ctx.translate((1 - ease(t / 0.3)) * -W * 0.35, 0);
  let zin = 1; if (tr === 'zoom' && t < 0.45) zin = 1 + 0.35 * (1 - ease(t / 0.45));
  // camera
  if (sc.cam) { const k = ease(clamp(t / d)), c = sc.cam; const z = Math.max(1, lerp(c[2], c[5], k) * zin);
    // keep the view inside the scene (no empty edges)
    const cx = clamp(lerp(c[0], c[3], k), W / (2 * z), W - W / (2 * z)), cy = clamp(lerp(c[1], c[4], k), H / (2 * z), H - H / (2 * z));
    ctx.translate(W / 2, H / 2); ctx.scale(z, z); ctx.translate(-cx, -cy); }
  else if (zin !== 1) { ctx.translate(W / 2, H / 2); ctx.scale(zin, zin); ctx.translate(-W / 2, -H / 2); }
  const t0 = sc.t0 || 0; S[sc.id](t + t0, d + t0, frame);
  ctx.restore();
  (GRADES[sc.grade || 'none'] || GRADES.none)();
  if (sc.leak) lightLeak(time, sc.leak, 0.3);
  if (sc.flashes) { const v = lightning(t, sc.flashes); if (v) { ctx.fillStyle = `rgba(200,210,255,${v * 0.55})`; ctx.fillRect(0, 0, W, H); } }
  if (!L.noVig) vignette(0.55);
  applyGrain(frame, 0.045);
  // whip motion smear
  if (tr === 'whip' && t < 0.3) {
    if (!TMP) { TMP = document.createElement('canvas'); TMP.width = cv.width; TMP.height = cv.height; }
    const g = TMP.getContext('2d'); g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, TMP.width, TMP.height); g.drawImage(cv, 0, 0);
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); const k = 1 - t / 0.3;
    for (let i = 1; i <= 6; i++) { ctx.globalAlpha = 0.22 * k; ctx.drawImage(TMP, -i * 45 * k, 0); }
    ctx.restore();
  }
  if (tr === 'flash' && t < 0.4) { ctx.fillStyle = `rgba(255,250,240,${Math.pow(1 - t / 0.4, 2) * 0.95})`; ctx.fillRect(0, 0, W, H); }
  if (tr === 'zoom' && t < 0.45) { ctx.fillStyle = `rgba(255,255,255,${(1 - t / 0.45) * 0.25})`; ctx.fillRect(0, 0, W, H); }
  if (tr === 'fade' || sc.id === 'card') { const fa = Math.max(1 - clamp(t / 0.45), 1 - clamp((d - t) / 0.45)); if (fa > 0) { ctx.fillStyle = `rgba(0,0,0,${fa})`; ctx.fillRect(0, 0, W, H); } }
  if (sc.fadeOut) { const fa = 1 - clamp((d - t) / 0.6); if (fa > 0) { ctx.fillStyle = `rgba(0,0,0,${fa})`; ctx.fillRect(0, 0, W, H); } }
  caption(time, sc);
};
