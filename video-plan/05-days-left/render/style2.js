// "Ifverse-like" visual upgrade for video #5 (v2): rich layered backgrounds, city skylines with lit windows,
// volumetric light, rim-lit characters, per-shot camera moves and hard cuts.
// Load order: scene.html + scenes20.js + scenes5.js + style2.js

// ---------- rim light + volume on every character ----------
let RIM = 'rgba(255,170,90,1)', RIM_SIDE = 1;
const _p5 = person;
person = function (o) {
  const p = _p5(o); const { hx, hy, R } = p;
  ctx.save(); circle(hx, hy, R - 2); ctx.clip();
  let g = ctx.createRadialGradient(hx - R * 0.35, hy - R * 0.45, R * 0.1, hx, hy, R * 1.1);
  g.addColorStop(0, 'rgba(255,255,255,0.22)'); g.addColorStop(0.55, 'rgba(255,255,255,0)'); g.addColorStop(1, 'rgba(10,10,40,0.35)');
  ctx.fillStyle = g; ctx.fillRect(hx - R, hy - R, 2 * R, 2 * R);
  g = ctx.createRadialGradient(hx + RIM_SIDE * R * 1.15, hy - R * 0.1, R * 0.55, hx + RIM_SIDE * R * 1.15, hy, R);
  g.addColorStop(0, RIM); g.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.globalCompositeOperation = 'lighter'; ctx.globalAlpha = 0.3; ctx.fillStyle = g; ctx.fillRect(hx - R, hy - R, 2 * R, 2 * R);
  ctx.restore(); return p;
};

// ---------- building blocks ----------
function skyline(t, opt) {
  const { y = 760, layers = 3, seed = 1, pan = 0, sky = ['#0b1030', '#2a2060', '#7a4a8a'], lit = 0.45, warm = false } = opt;
  ctx.fillStyle = vgrad(0, y + 100, sky); ctx.fillRect(0, 0, W, y + 100);
  const r0 = rand(seed); for (let i = 0; i < 90; i++) { const sx = r0() * W, sy = r0() * y * 0.7; circle(sx, sy, 0.8 + r0() * 2); fs(`rgba(255,255,255,${0.3 + 0.5 * Math.abs(Math.sin(t * 0.8 + i))})`); }
  for (let L = 0; L < layers; L++) {
    const r = rand(seed * 10 + L), depth = (L + 1) / layers;
    const base = warm ? [[60, 40, 70], [90, 50, 70], [120, 60, 70]][L % 3] : [[30, 34, 70], [44, 46, 96], [60, 60, 120]][L % 3];
    const col = `rgb(${base[0]},${base[1]},${base[2]})`;
    let x = -100 - ((pan * (0.3 + depth)) % 400);
    while (x < W + 100) {
      const bw = 90 + r() * 140, bh = (140 + r() * 320) * (0.6 + depth * 0.7), top = y - bh + L * 50;
      ctx.fillStyle = col; ctx.fillRect(x, top, bw, y - top + 120);
      ctx.fillStyle = `rgba(255,255,255,${0.04 + 0.04 * depth})`; ctx.fillRect(x, top, bw, 6);
      for (let wy = top + 18; wy < y + 40; wy += 30) for (let wx = x + 12; wx < x + bw - 16; wx += 26) {
        if (r() < lit * (0.6 + depth * 0.4)) { ctx.fillStyle = r() < 0.25 ? 'rgba(160,210,255,0.85)' : 'rgba(255,214,140,0.9)'; ctx.fillRect(wx, wy, 12, 16); }
      }
      x += bw + 8 + r() * 30;
    }
  }
}
function lightBeam(x, y, w, len, col, a = 0.18, ang = 0) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(ang); ctx.globalAlpha = a; ctx.globalCompositeOperation = 'lighter';
  const g = ctx.createLinearGradient(0, 0, 0, len); g.addColorStop(0, col); g.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(-w * 0.2, 0); ctx.lineTo(w * 0.2, 0); ctx.lineTo(w, len); ctx.lineTo(-w, len); ctx.fill(); ctx.restore();
}
function windowCity(x, y, w, h, t, night = true) {
  ctx.save(); rr(x, y, w, h, 8); ctx.clip();
  ctx.translate(x, y); ctx.scale(w / W, h / H);
  skyline(t, { y: H * 0.75, seed: 7, sky: night ? ['#081030', '#1a1a50', '#4a2a6a'] : ['#ffb27a', '#ffd6a0', '#ffe8c0'], lit: night ? 0.5 : 0.15, warm: !night });
  ctx.restore(); rr(x, y, w, h, 8); fs(null, 12, '#1a1418'); line([x + w / 2, y, x + w / 2, y + h], 10, '#1a1418'); line([x, y + h * 0.45, x + w, y + h * 0.45], 10, '#1a1418');
}
function frames(list) { list.forEach(([x, y, w, h, c]) => { rr(x, y, w, h, 4); fs('#3a2a1e', 6); rr(x + 10, y + 10, w - 20, h - 20, 2); fs(c); }); }
function plant(x, y, s = 1) { rr(x - 40 * s, y - 70 * s, 80 * s, 70 * s, 10 * s); fs('#a0583a', 5); for (let i = 0; i < 5; i++) { ctx.save(); ctx.translate(x, y - 70 * s); ctx.rotate(-0.9 + i * 0.45); ctx.beginPath(); ctx.ellipse(0, -60 * s, 18 * s, 60 * s, 0, 0, 7); fs(i % 2 ? '#3f8a4a' : '#55a85a', 4); ctx.restore(); } }

// ---------- richer interiors (override the shared helpers, so every scene that uses them upgrades) ----------
kitchen = function (t, f) {
  ctx.fillStyle = vgrad(0, H, ['#3a2620', '#22150f']); ctx.fillRect(0, 0, W, H);
  ctx.globalAlpha = 0.06; for (let x = 0; x < W; x += 60) { ctx.fillStyle = '#ffd9a0'; ctx.fillRect(x, 0, 24, 960); } ctx.globalAlpha = 1;
  for (let i = 0; i < 4; i++) { rr(40 + i * 150, 120, 140, 220, 6); fs('#5a3a28', 6); circle(40 + i * 150 + 120, 300, 7); fs('#c9a14a'); }
  rr(30, 620, 620, 340, 6); fs('#4a3020', 6); rr(30, 600, 620, 30, 4); fs('#7a5a42', 5);
  windowCity(1250, 170, 480, 380, t, true);
  ctx.save(); ctx.beginPath(); ctx.rect(1255, 175, 470, 370); ctx.clip(); const r = rand(11);
  for (let i = 0; i < 60; i++) { const x = 1255 + r() * 470, sp = 500 + r() * 300, y = 175 + ((r() * 370 + t * sp) % 370); line([x, y, x - 6, y + 26], 2, 'rgba(160,190,230,0.45)'); } ctx.restore();
  frames([[860, 230, 150, 120, '#c98a6a'], [1040, 270, 110, 140, '#8aa0c0']]);
  plant(1800, 960, 1.2);
  line([700, 0, 700, 170], 5, '#111'); ctx.beginPath(); ctx.moveTo(620, 240); ctx.lineTo(780, 240); ctx.lineTo(735, 170); ctx.lineTo(665, 170); ctx.closePath(); fs('#c58a3c', 7);
  glow(700, 330, 800, 'rgba(255,170,80,0.55)'); lightBeam(700, 240, 420, 760, 'rgba(255,200,130,1)', 0.12);
  ctx.fillStyle = '#1b130d'; ctx.fillRect(0, 950, W, 130);
  for (let x = 0; x < W; x += 120) line([x, 950, x - 60, 1080], 3, 'rgba(0,0,0,0.3)');
};
bedroom = function () {
  ctx.fillStyle = vgrad(0, H, ['#121530', '#090a18']); ctx.fillRect(0, 0, W, H);
  windowCity(1300, 130, 460, 380, 0, true);
  for (let i = 0; i < 14; i++) { const x = 120 + i * 80, y = 90 + Math.sin(i * 0.9) * 18; circle(x, y, 8); fs(['#ffd27a', '#ff8ab0', '#8adfff'][i % 3]); glow(x, y, 40, 'rgba(255,210,140,0.5)'); }
  frames([[200, 200, 180, 240, '#3a4a8a'], [420, 230, 140, 180, '#8a3a5a']]);
};

// ---------- new / upgraded shots ----------
S.cityOpen = (t, d) => {
  skyline(t, { y: 820, layers: 4, seed: 3, pan: t * 30, sky: ['#1a1440', '#5a3a7a', '#e08a6a'], lit: 0.4 });
  glow(W * 0.7, 760, 600, 'rgba(255,170,110,0.5)');
  ctx.fillStyle = '#0e0c1a'; ctx.fillRect(0, 900, W, 180);
  for (let i = 0; i < 8; i++) { const x = ((i * 300 + t * 220) % (W + 300)) - 150; ctx.fillStyle = 'rgba(255,90,70,0.8)'; ctx.fillRect(x, 980, 60, 5); ctx.fillStyle = 'rgba(255,240,200,0.8)'; ctx.fillRect(W - x, 1010, 60, 5); }
};
S.wake5 = (t, d, f) => {
  PEOPLE = []; RIM = 'rgba(255,200,140,1)';
  ctx.fillStyle = vgrad(0, H, ['#3a2a3a', '#1a1220']); ctx.fillRect(0, 0, W, H);
  windowCity(1300, 120, 460, 400, t, false);
  lightBeam(1530, 470, 520, 800, 'rgba(255,220,170,1)', 0.16, 0.5);
  frames([[180, 180, 200, 260, '#5a6aa0'], [420, 220, 150, 190, '#c07a5a']]);
  rr(150, 760, 260, 200, 10); fs('#3a2a22', 6); rr(220, 690, 120, 70, 10); fs('#222', 5); textC('6:47', 280, 725, 34, '#7fd');
  const up = prog(t, 0.6, 1.6);
  const p = person({ x: 820, y: lerp(1150, 1000, up), s: 1.45, expr: t < 4 ? 'tired' : t < 7 ? 'shock' : 'calm', look: t > 4 ? 0 : 0.4, hood: false });
  ctx.beginPath(); ctx.moveTo(250, 860); ctx.quadraticCurveTo(900, 800, 1500, 880); ctx.lineTo(1500, 1080); ctx.lineTo(250, 1080); ctx.closePath(); fs('#4a5a8a', 8);
  for (let i = 0; i < 6; i++) line([350 + i * 190, 880, 380 + i * 190, 1080], 4, 'rgba(0,0,0,0.15)');
  if (t > 3.2) tag(p, 17412, { a: prog(t, 3.2, 4.2), pulse: t < 5 ? t : 0 });
};
const _street = S.street;
S.street = (t, d) => {
  PEOPLE = []; RIM = 'rgba(150,200,255,1)';
  skyline(t, { y: 800, layers: 4, seed: 9, pan: t * 12, sky: ['#0a0e2a', '#25205a', '#5a3a7a'], lit: 0.5 });
  ctx.fillStyle = '#16142a'; ctx.fillRect(0, 880, W, 200);
  for (let i = 0; i < 10; i++) { ctx.fillStyle = 'rgba(255,255,255,0.12)'; ctx.fillRect(i * 200 + 40, 960, 110, 14); }
  for (const lx of [150, 1780]) { line([lx, 900, lx, 380], 10, '#222'); line([lx, 380, lx + (lx < W / 2 ? 80 : -80), 380], 10, '#222'); glow(lx + (lx < W / 2 ? 80 : -80), 400, 300, 'rgba(255,210,140,0.55)'); lightBeam(lx + (lx < W / 2 ? 80 : -80), 395, 200, 520, 'rgba(255,210,140,1)', 0.15); }
  CROWD.forEach(([x, top, n, kind], i) => {
    const old = kind === 'dad' || kind === 'mom';
    const p = person({ x, y: 1040, s: 0.95, top, expr: i === 3 ? 'calm' : 'neutral', kind: kind === 'zero' ? undefined : kind, old, skin: old ? (kind === 'dad' ? C.dadSkin : C.momSkin) : C.skin, hood: kind === 'zero', noBand: true, look: (i - 2) * 0.2 });
    tag(p, n, { a: prog(t, 0.6 + i * 0.4, 1.4 + i * 0.4), pulse: i === 3 && t > 4 ? t : 0 });
  });
};
function gamerRoom(t, f) {
  ctx.fillStyle = vgrad(0, H, ['#0c0e22', '#05060e']); ctx.fillRect(0, 0, W, H);
  windowCity(120, 140, 420, 360, t, true);
  ctx.fillStyle = 'rgba(160,80,255,0.9)'; ctx.fillRect(0, 70, W, 6); glow(W / 2, 70, 900, 'rgba(150,80,255,0.25)');
  frames([[1450, 200, 200, 260, '#2a4a8a'], [1690, 240, 150, 190, '#8a2a5a']]);
}
S.gaming5 = withTags((t, d, f) => { RIM = 'rgba(120,160,255,1)'; gamerRoom(t, f);
  const fl = 0.75 + 0.25 * Math.sin(f * 0.9) * Math.sin(f * 0.37);
  glow(W / 2, 420, 900, `rgba(70,120,255,${0.35 * fl})`);
  rr(0, 930, W, 160, 0); fs('#14161f');
  const p = person({ x: W / 2, y: 1010, s: 1.55, expr: 'tired', bob: Math.sin(t * 2) * 3 });
  ctx.beginPath(); ctx.arc(p.hx, p.hy, p.R * 1.12, Math.PI * 1.08, Math.PI * 1.92); fs(null, 22, '#222');
  for (const sd of [-1, 1]) { rr(p.hx + sd * p.R * 1.05 - 28, p.hy - 40, 56, 100, 22); fs('#2a2a2a', 7); }
  rr(W / 2 - 150, 860, 300, 110, 50); fs('#25262e', 7);
  hand(W / 2 - 135, 900, 1.3, 0.3, C.skin); hand(W / 2 + 135, 900, 1.3, -0.3 + Math.PI, C.skin);
  for (const [cx, rot] of [[430, 0], [520, 0.3], [1420, -0.2]]) { ctx.save(); ctx.translate(cx, 900); ctx.rotate(rot); rr(-28, -90, 56, 110, 10); fs('#2b9b5a', 5); ctx.restore(); }
}, [[0, tick(17402, 1.2)]]);
S.doorMom = (t, d, f) => {
  PEOPLE = []; RIM = 'rgba(255,190,120,1)';
  ctx.fillStyle = vgrad(0, H, ['#2a1c24', '#140c12']); ctx.fillRect(0, 0, W, H);
  ctx.globalAlpha = 0.07; for (let x = 0; x < W; x += 70) { ctx.fillStyle = '#ffcf9a'; ctx.fillRect(x, 0, 26, 960); } ctx.globalAlpha = 1;
  rr(900, 120, 700, 900, 10); fs('#ffd9a0'); glow(1250, 450, 750, 'rgba(255,200,130,0.6)');
  frames([[1000, 200, 140, 110, '#c98a6a'], [1360, 220, 130, 150, '#8aa0c0']]);
  lightBeam(1250, 140, 520, 950, 'rgba(255,220,170,1)', 0.12);
  rr(900, 120, 700, 900, 10); fs(null, 18, '#3a2418');
  plant(1700, 1000, 1.1);
  const m = person({ x: 1250, y: 1040, s: 1.3, kind: 'mom', old: true, skin: C.momSkin, top: '#d8c3a0', expr: 'happy', look: -0.6, blush: true });
  RIM_SIDE = -1;
  const z = person({ x: 520, y: 1080, s: 1.45, expr: t > 4.5 ? 'shock' : 'happy', look: 0.8 });
  RIM_SIDE = 1;
  tag(z, 17201, { a: 0.8 });
  if (t > 2.0) tag(m, 214, { a: prog(t, 2.0, 2.6), pulse: t, size: 58 });
};
S.bus5 = withTags((t, d, f) => { RIM = 'rgba(255,190,140,1)'; S.bus(t, d, f); }, [[0, 17240]]);

// ---------- camera: per-shot framing from the timeline (cam: [cx0, cy0, z0, cx1, cy1, z1]) ----------
window.drawFrame = function (frame, fps) {
  const time = frame / fps;
  const sc = TL.scenes.find(s => time >= s.start && time < s.end) || TL.scenes[TL.scenes.length - 1];
  const t = time - sc.start, d = sc.end - sc.start, L = LOOK[sc.id] || {};
  RIM = 'rgba(255,170,90,1)'; RIM_SIDE = 1;
  ctx.save();
  if (sc.cam) { const k = ease(clamp(t / d)), c = sc.cam; const cx = lerp(c[0], c[3], k), cy = lerp(c[1], c[4], k), z = lerp(c[2], c[5], k);
    ctx.translate(W / 2, H / 2); ctx.scale(z, z); ctx.translate(-cx, -cy); }
  else { const z = ZOOM[sc.id]; if (z) { const k = lerp(z[0], z[1], clamp(t / d)); ctx.translate(W / 2, H / 2); ctx.scale(k, k); ctx.translate(-W / 2, -H / 2); } }
  const t0 = sc.t0 || 0; S[sc.id](t + t0, d + t0, frame);
  ctx.restore();
  if (L.warm) { tint('#ffb46a', 0.3, 'soft-light'); }
  else if (!L.noVig) { tint('#3a2a7a', 0.12, 'soft-light'); }
  if (!L.noVig) vignette(0.6);
  applyGrain(frame, 0.05);
  const fa = sc.cut ? 0 : Math.max(1 - clamp(t / 0.4), 1 - clamp((d - t) / 0.4));
  if (fa > 0) { ctx.fillStyle = `rgba(0,0,0,${fa})`; ctx.fillRect(0, 0, W, H); }
  caption(time, sc);
};
