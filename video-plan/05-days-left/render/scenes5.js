// Video #5 "What If You Could See How Many Days You Have Left?"
// Loaded after scene.html + 02-twenties/render/scenes20.js. Adds a floating "days left" counter above characters.

// remember every person drawn this frame so counters can be placed above their heads
let PEOPLE = [];
const _person = person;
person = function (o) { const p = _person(o); PEOPLE.push(Object.assign({ o }, p)); return p; };

function tag(p, val, opt = {}) {
  const s = p.R / 95, str = typeof val === 'number' ? val.toLocaleString('en-US') : String(val);
  const low = typeof val === 'number' && val < 1000;
  const col = opt.col || (low ? '#ff5a4a' : '#9fe7ff');
  const size = (opt.size || 46) * Math.max(0.7, s);
  const pulse = opt.pulse ? 1 + 0.08 * Math.max(0, Math.sin(opt.pulse * 6)) : 1;
  const y = p.hy - p.R - 55 * s - 20;
  ctx.save(); ctx.globalAlpha = opt.a === undefined ? 1 : opt.a; ctx.translate(p.hx, y); ctx.scale(pulse, pulse);
  ctx.font = `bold ${size}px "DejaVu Sans"`; const w = ctx.measureText(str).width + size * 0.9;
  glow(0, 0, w * 0.9, low ? 'rgba(255,80,60,0.45)' : 'rgba(120,220,255,0.4)');
  rr(-w / 2, -size * 0.75, w, size * 1.5, size * 0.75); fs('rgba(5,8,14,0.75)', 3, col);
  textC(str, 0, 2, size, col); ctx.restore();
}
// wrap an existing scene and put counters above the people it draws
function withTags(fn, specs) {
  return (t, d, f) => { PEOPLE = []; fn(t, d, f); specs.forEach(([i, v, opt]) => { const p = PEOPLE[i]; if (p) tag(p, typeof v === 'function' ? v(t, d) : v, typeof opt === 'function' ? opt(t, d) : opt); }); };
}
const tick = (start, per = 1.6) => (t) => start - Math.floor(t / per);

S.title5 = (t, d) => {
  ctx.fillStyle = '#050403'; ctx.fillRect(0, 0, W, H);
  const a = prog(t, 0.4, 1.6) * (1 - prog(t, d - 1, d));
  glow(W / 2, H / 2, 700, 'rgba(120,200,255,0.25)', a);
  ctx.globalAlpha = a; textC('WHAT IF YOU COULD SEE', W / 2, H / 2 - 70, 96, '#f3e9da'); textC('HOW MANY DAYS YOU HAVE LEFT?', W / 2, H / 2 + 50, 80, '#9fe7ff');
  ctx.globalAlpha = a * 0.6; textC('an animated short film', W / 2, H / 2 + 180, 36, '#d9a070', 'normal'); ctx.globalAlpha = 1;
};
S.wake5 = (t, d, f) => {
  PEOPLE = [];
  ctx.fillStyle = vgrad(0, H, ['#c9a27a', '#8a6a52']); ctx.fillRect(0, 0, W, H);
  rr(1300, 120, 460, 400, 8); fs('#fff4d6', 10); glow(1530, 320, 600, 'rgba(255,240,200,0.6)');
  const up = prog(t, 0.6, 1.6);
  const p = person({ x: 820, y: lerp(1150, 1000, up), s: 1.45, expr: t < 4 ? 'tired' : t < 7 ? 'shock' : 'calm', look: t > 4 ? 0 : 0.4, hood: false });
  ctx.beginPath(); ctx.moveTo(250, 860); ctx.quadraticCurveTo(900, 800, 1500, 880); ctx.lineTo(1500, 1080); ctx.lineTo(250, 1080); ctx.closePath(); fs('#5a6a8a', 8);
  if (t < 3) hand(900, lerp(1000, 640, prog(t, 1.4, 2.2)) , 1.2, -0.6, C.skin);
  if (t > 3.2) tag(p, 17412, { a: prog(t, 3.2, 4.2), pulse: t < 5 ? t : 0 });
};
S.mirror5 = (t, d) => {
  PEOPLE = [];
  ctx.fillStyle = vgrad(0, H, ['#1d2026', '#0e0f12']); ctx.fillRect(0, 0, W, H);
  rr(1000, 140, 700, 760, 20); fs('#4a4f58', 12);
  ctx.save(); ctx.beginPath(); ctx.roundRect(1012, 152, 676, 736, 14); ctx.clip(); ctx.fillStyle = '#1d232b'; ctx.fillRect(1000, 140, 700, 760);
  const r = person({ x: 1350, y: 1100, s: 1.4, expr: 'shock', look: -0.5 }); tag(r, 17412); ctx.restore();
  glow(1350, 120, 520, 'rgba(255,220,170,0.35)');
  const p = person({ x: 620, y: 1080, s: 1.65, expr: 'shock', look: 0.6 });
  hand(760, lerp(900, 420, prog(t, 2, 3.5)), 1.3, -0.5, C.skin);
  tag(p, 17412);
};
const CROWD = [[300, '#3d8bd0', 21903, 'zero'], [620, '#5a9a4a', 9120, 'zero'], [960, '#a07fd0', 30455, 'zero'], [1290, '#7a5a3c', 12, 'dad'], [1620, '#c9733a', 4310, 'mom']];
S.street = (t, d) => {
  PEOPLE = [];
  ctx.fillStyle = vgrad(0, H, ['#8aa0b8', '#d9c9b0']); ctx.fillRect(0, 0, W, H);
  for (let i = 0; i < 6; i++) { rr(i * 340 - 40, 200 + (i % 3) * 60, 300, 700, 6); fs(['#7a6a62', '#8a7a6a', '#6a6a72'][i % 3], 6); for (let w = 0; w < 6; w++) { rr(i * 340 + (w % 2) * 130, 260 + (i % 3) * 60 + Math.floor(w / 2) * 150, 80, 90, 4); fs('#3a4452', 4); } }
  ctx.fillStyle = '#5c5a5a'; ctx.fillRect(0, 900, W, 180);
  const pan = prog(t, 0, d) * 0;
  CROWD.forEach(([x, top, n, kind], i) => {
    const old = kind === 'dad' || kind === 'mom';
    const p = person({ x: x + pan, y: 1040, s: 0.95, top, expr: i === 3 ? 'calm' : 'neutral', kind: kind === 'zero' ? undefined : kind, old, skin: old ? (kind === 'dad' ? C.dadSkin : C.momSkin) : C.skin, hood: kind === 'zero', noBand: true, look: (i - 2) * 0.2 });
    tag(p, n, { a: prog(t, 1 + i * 0.6, 2 + i * 0.6), pulse: i === 3 && t > 7 ? t : 0 });
  });
  tint('#3a4a66', 0.15, 'color');
};
S.gaming5 = withTags(S.gaming, [[0, tick(17402, 1.2)]]);
S.scroll5 = withTags(S.scroll, [[0, tick(17320, 0.9)]]);
S.phone5 = (t, d, f) => { S.phone(t, d, f); ctx.save(); ctx.globalAlpha = 0.9; rr(W / 2 - 170, 70, 340, 80, 40); fs('rgba(5,8,14,0.75)', 3, '#9fe7ff'); textC('17,288', W / 2, 112, 44, '#9fe7ff'); ctx.restore(); };
S.doorMom = (t, d, f) => {
  PEOPLE = [];
  ctx.fillStyle = vgrad(0, H, ['#4a3426', '#2c1f15']); ctx.fillRect(0, 0, W, H);
  rr(900, 120, 700, 900, 10); fs('#f2c88a'); glow(1250, 450, 650, 'rgba(255,200,130,0.55)'); rr(900, 120, 700, 900, 10); fs(null, 16, '#5a3a24');
  const m = person({ x: 1250, y: 1040, s: 1.3, kind: 'mom', old: true, skin: C.momSkin, top: '#d8c3a0', expr: 'happy', look: -0.6, blush: true });
  const z = person({ x: 520, y: 1080, s: 1.45, expr: t > 4.5 ? 'shock' : 'happy', look: 0.8 });
  tag(z, 17201, { a: 0.8 });
  if (t > 3.5) tag(m, 214, { a: prog(t, 3.5, 4.2), pulse: t, size: 58 });
};
S.grid214 = (t, d) => {
  ctx.fillStyle = '#050505'; ctx.fillRect(0, 0, W, H);
  const cols = 31, sz = 34, gap = 40, x0 = (W - cols * gap) / 2, y0 = 330;
  const shown = Math.floor(prog(t, 0.5, 3.0) * 214);
  for (let i = 0; i < shown; i++) { const x = x0 + (i % cols) * gap, y = y0 + Math.floor(i / cols) * gap; const sunday = i % 7 === 6;
    ctx.fillStyle = sunday && t > 5 ? '#ff8a3c' : '#2e2e2e'; ctx.fillRect(x, y, sz, sz); }
  ctx.globalAlpha = prog(t, 0.3, 1.0); textC('214 days.', W / 2, 200, 90, '#f3e9da'); ctx.globalAlpha = 1;
};
S.cry5 = (t, d) => {
  PEOPLE = [];
  ctx.fillStyle = '#07060a'; ctx.fillRect(0, 0, W, H); glow(W / 2, 600, 700, 'rgba(255,150,80,0.3)');
  const p = person({ x: W / 2, y: 1400, s: 2.6, expr: 'cry', tear: prog(t, 0.5, 4) });
  tag(p, 17201, { a: 0.5 });
};
S.stars = (t, d) => {
  PEOPLE = [];
  ctx.fillStyle = vgrad(0, H, ['#0a0e22', '#1a1a3a', '#2a2040']); ctx.fillRect(0, 0, W, H);
  const r = rand(8); for (let i = 0; i < 120; i++) { circle(r() * W, r() * 700, 1 + r() * 2.5); fs(`rgba(255,255,255,${0.4 + 0.6 * Math.abs(Math.sin(t + i))})`); }
  ctx.fillStyle = '#0c0c18'; ctx.beginPath(); ctx.ellipse(W / 2, 1200, 1200, 380, 0, 0, 7); ctx.fill();
  const p = person({ x: W / 2, y: 1000, s: 1.4, expr: 'calm', look: 0 });
  tag(p, 17190 - Math.floor(t / 3));
};
S.dinner5 = withTags(S.dinner, [[0, tick(150, 3)], [1, 17110], [2, 3105]]);
S.album5 = withTags(S.album, [[0, tick(96, 3)], [1, 17050]]);
S.mom5 = withTags(S.mom, [[0, tick(60, 3)]]);
S.cook = (t, d, f) => {
  PEOPLE = [];
  kitchen(t, f);
  rr(1050, 760, 500, 200, 8); fs('#3a3a3a', 7); rr(1150, 720, 220, 40, 10); fs('#222', 6); line([1370, 740, 1480, 720], 14, '#222');
  for (let i = 0; i < 3; i++) { const y = 700 - ((t * 45 + i * 40) % 120); ctx.globalAlpha = 0.5; line([1200 + i * 50, y, 1210 + i * 50 + Math.sin(t * 3 + i) * 10, y - 40], 6, '#eee'); ctx.globalAlpha = 1; }
  const m = person({ x: 820, y: 1000, s: 1.25, kind: 'mom', old: true, skin: C.momSkin, top: '#d8c3a0', expr: 'happy', look: 0.6, bob: Math.abs(Math.sin(t * 3)) * -5 });
  const z = person({ x: 1250, y: 1000, s: 1.3, expr: t % 4 > 2 ? 'happy' : 'calm', look: -0.4 });
  hand(1180, 740, 1.1, -0.3, C.skin);
  tag(m, 120 - Math.floor(t / 3)); tag(z, 16990, { a: 0.7 });
};
S.walkMom = (t, d) => {
  PEOPLE = [];
  const scroll = t * 90;
  ctx.fillStyle = vgrad(0, H, ['#f2a35e', '#e8875a', '#f4c08a']); ctx.fillRect(0, 0, W, H);
  ctx.fillStyle = '#b07a4a'; ctx.beginPath(); ctx.ellipse(800 - scroll * 0.4, 1200, 1400, 420, 0, 0, 7); ctx.fill();
  for (let i = 0; i < 8; i++) { const tx = ((i * 380 - scroll * 0.7) % 3040 + 3040) % 3040 - 300; rr(tx - 18, 560, 36, 220, 10); fs('#5a3a24', 6); circle(tx, 520, 120); fs('#d9732e', 7); circle(tx - 70, 580, 80); fs('#e8a03a', 7); }
  ctx.fillStyle = '#a07a52'; ctx.fillRect(0, 900, W, 180);
  const b = i => Math.abs(Math.sin(t * 3 + i)) * -8;
  const m = person({ x: 800, y: 1010, s: 1.1, kind: 'mom', old: true, skin: C.momSkin, top: '#d8c3a0', expr: 'happy', look: 0.7, bob: b(0) });
  const z = person({ x: 1100, y: 1010, s: 1.2, expr: 'happy', look: -0.7, bob: b(1.5) });
  hand(950, 830, 1, 0.2, C.skin);
  tag(m, 30 - Math.floor(t / 2)); tag(z, 16890, { a: 0.7 });
};
S.bench5 = (t, d) => {
  const z = 1.1 - prog(t, 0, d) * 0.1;
  ctx.save(); ctx.translate(W / 2, H / 2); ctx.scale(z, z); ctx.translate(-W / 2, -H / 2);
  ctx.fillStyle = vgrad(0, H, ['#3a2a5a', '#d4584a', '#ffa64d', '#ffd08a']); ctx.fillRect(0, 0, W, H);
  const sy = 600 + prog(t, 0, d) * 90; circle(W / 2, sy, 150); fs('#ffe1a0'); glow(W / 2, sy, 700, 'rgba(255,200,120,0.8)');
  ctx.fillStyle = '#1a1020'; ctx.beginPath(); ctx.ellipse(W / 2, 1180, 1300, 420, 0, 0, 7); ctx.fill();
  ctx.fillStyle = '#120a14'; ctx.fillRect(760, 820, 400, 22); ctx.fillRect(790, 842, 16, 80); ctx.fillRect(1115, 842, 16, 80);
  for (const [x, r, b] of [[870, 52, 110], [1050, 60, 130]]) { rr(x - b / 2 - 10, 820 - b, b + 20, b, 30); ctx.fill(); circle(x, 820 - b - r * 0.7, r); ctx.fill(); }
  ctx.restore();
  tag({ hx: W / 2 + (870 - W / 2) * z, hy: H / 2 + (820 - 110 - 52 * 0.7 - H / 2) * z, R: 52 * z }, t < d / 2 ? 2 : 1, { size: 50 });
};
S.emptyChair = (t, d, f) => {
  PEOPLE = [];
  kitchen(t, f);
  rr(380, 720, 1000, 34, 8); fs('#6a4a30', 7); line([440, 754, 440, 960], 14, '#4a3221'); line([1320, 754, 1320, 960], 14, '#4a3221');
  rr(1180, 560, 30, 400, 8); fs('#4a3221', 6); rr(1060, 760, 160, 26, 6); fs('#4a3221', 6);
  const p = person({ x: 640, y: 740, s: 1.05, expr: t > d * 0.6 ? 'calm' : 'sad', look: 0.9 });
  ctx.save(); ctx.translate(1020, 640); ctx.rotate(0.05); rr(-70, -90, 140, 180, 6); fs('#f2e8d6', 5); rr(-55, -72, 110, 130, 4); fs('#d9b98a'); circle(0, -20, 26); fs(C.momSkin, 3); circle(4, -50, 12); fs('#c4c4c4', 3); rr(-30, 6, 60, 50, 10); fs('#d8c3a0', 3); ctx.restore();
  ctx.beginPath(); ctx.ellipse(780, 712, 95, 24, 0, 0, 7); fs('#efe9de', 6);
  tag(p, 16702 - Math.floor(t / 3));
};
S.closeup5 = (t, d) => {
  PEOPLE = [];
  ctx.fillStyle = '#060507'; ctx.fillRect(0, 0, W, H); glow(W / 2, 560, 700, 'rgba(255,150,70,0.35)');
  const p = person({ x: W / 2, y: 1420, s: 2.6, expr: t > d * 0.5 ? 'determined' : 'calm' });
  tag(p, 16700, { a: 1 - prog(t, d * 0.35, d * 0.65) });
};

Object.assign(ZOOM, { wake5: [1.0, 1.06], mirror5: [1.0, 1.08], street: [1.0, 1.05], doorMom: [1.0, 1.1], cry5: [1.0, 1.08], stars: [1.0, 1.05],
  cook: [1.0, 1.05], emptyChair: [1.0, 1.08], closeup5: [1.0, 1.1], gaming5: [1.0, 1.06], scroll5: [1.0, 1.07] });
LOOK.grid214 = { noVig: 1 };
