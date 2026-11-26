// Video #7 "What If You Could Hear What People Really Think?"
// Load: scene.html, scenes20.js, scenes5.js, style2.js, assets/fx.js, assets/rig.js, scenes7.js
const ZT = { top: '#d9692a' };
const GIRL = { kind: 'mom', old: false, skin: '#a9b6c6', top: '#6f9fd8' };
const CROWD7 = ['#3d8bd0', '#5a9a4a', '#a07fd0', '#c9a06a', '#d0607a', '#4aa0a0'];
const backOut = k => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(k - 1, 3) + c1 * Math.pow(k - 1, 2); };

// ---------- thought bubbles ----------
// mode: 'blur' (unreadable scribbles), 'red' (imagined fear), 'clear' (real thought)
function thought(x, y, text, t, start, o = {}) {
  const k = clamp((t - start) / 0.4); if (k <= 0) return;
  const mode = o.mode || 'clear', size = o.size || 30, sc = 0.4 + 0.6 * backOut(k);
  ctx.save(); ctx.font = `bold ${size}px "DejaVu Sans"`;
  const lines = wrap(text, size, o.maxW || 380); ctx.font = `bold ${size}px "DejaVu Sans"`;
  const w = Math.max(...lines.map(l => ctx.measureText(l).width)) + 70, h = lines.length * size * 1.3 + 50;
  const jit = mode === 'red' ? Math.sin(t * 40) * 3 : 0;
  ctx.translate(x + jit, y); ctx.scale(sc, sc); ctx.globalAlpha = k * (o.a === undefined ? 1 : o.a);
  const fill = mode === 'red' ? '#2a080c' : '#fbfaf6', edge = mode === 'red' ? '#ff4a4a' : '#1a1a22';
  if (mode === 'red') glow(0, 0, w, 'rgba(255,60,60,0.35)'); else if (mode === 'clear') glow(0, 0, w * 0.8, 'rgba(160,220,255,0.25)');
  // cloud: main body + bumps
  const bumps = 9; ctx.beginPath();
  for (let i = 0; i < bumps; i++) { const a = i / bumps * Math.PI * 2; ctx.moveTo(Math.cos(a) * w * 0.42 + h * 0.3, Math.sin(a) * h * 0.4); ctx.arc(Math.cos(a) * w * 0.42, Math.sin(a) * h * 0.4, h * 0.3, 0, 7); }
  ctx.ellipse(0, 0, w / 2, h / 2, 0, 0, 7);
  ctx.fillStyle = fill; ctx.strokeStyle = edge; ctx.lineWidth = 5; ctx.stroke(); ctx.fill();
  ctx.beginPath(); ctx.ellipse(0, 0, w / 2 - 2, h / 2 - 2, 0, 0, 7); ctx.fill();
  // tail toward the head
  const tx = (o.tx === undefined ? 0 : o.tx - x) / sc, ty = (o.ty === undefined ? h : o.ty - y) / sc;
  for (const [f, r] of [[0.55, 16], [0.8, 10]]) { circle(tx * f, h / 2 + (ty - h / 2) * f, r); fs(fill, 4, edge); }
  // text
  if (mode === 'blur') { const r = rand(text.length * 7); lines.forEach((l, i) => { const yy = (i - (lines.length - 1) / 2) * size * 1.3; ctx.beginPath(); let xx = -w / 2 + 35; ctx.moveTo(xx, yy); while (xx < w / 2 - 35) { xx += 14; ctx.lineTo(xx, yy + (r() - 0.5) * 16); } ctx.lineWidth = 5; ctx.strokeStyle = '#9aa'; ctx.stroke(); }); }
  else lines.forEach((l, i) => textC(l, 0, (i - (lines.length - 1) / 2) * size * 1.3 + 2, size, mode === 'red' ? '#ff5a5a' : '#22222a'));
  ctx.restore();
}
function above(p, dy = 0) { return [p.hx + p.R * 0.3, p.hy - p.R - 110 + dy]; }
function thoughtOver(p, text, t, start, o = {}) { const [x, y] = above(p, o.dy || 0); thought(x + (o.dx || 0), y, text, t, start, Object.assign({ tx: p.hx, ty: p.hy - p.R }, o)); }

// ---------- locations ----------
function bedroom7(t, light) {
  ctx.fillStyle = vgrad(0, H, [lerpCol('#1a1d33', '#5a4a52', light), lerpCol('#0c0e1a', '#2a2026', light)]); ctx.fillRect(0, 0, W, H);
  windowCity(1300, 120, 460, 380, t, light < 0.5);
  lightBeam(1530, 470, 520, 800, 'rgba(255,225,180,1)', 0.12 * light, 0.5);
  frames([[180, 180, 200, 260, '#5a6aa0'], [420, 220, 150, 190, '#c07a5a']]);
}
function streetDay(t, o = {}) {
  const { sunset = 0, pan = 0 } = o;
  skyline(t, { y: 780, layers: 3, seed: 61, pan, sky: [lerpCol('#7ab0e8', '#3a2a6a', sunset), lerpCol('#b8d8f0', '#e0705a', sunset), lerpCol('#f0e8d8', '#ffc080', sunset)], lit: 0.12 + sunset * 0.35, warm: true });
  if (!sunset) glow(1600, 150, 500, 'rgba(255,250,220,0.7)'); else { circle(W / 2, 700, 140); fs('#ffe0a0'); glow(W / 2, 700, 700, 'rgba(255,200,120,0.7)'); }
  ctx.fillStyle = sunset ? '#3a2a3a' : '#9a9a9e'; ctx.fillRect(0, 880, W, 200);
  ctx.fillStyle = sunset ? '#2a1e2a' : '#7a7a80'; ctx.fillRect(0, 880, W, 14);
  for (let i = 0; i < 8; i++) { const x = ((i * 300 - pan * 2) % 2400 + 2400) % 2400 - 200; ctx.fillStyle = 'rgba(0,0,0,0.08)'; ctx.fillRect(x, 960, 160, 8); }
}
function metro(t, k = 0) {
  ctx.fillStyle = vgrad(0, H, ['#1c2436', '#10141f']); ctx.fillRect(0, 0, W, H);
  for (let i = 0; i < 4; i++) { const x = 120 + i * 460; rr(x, 170, 380, 260, 30); fs('#05070c', 8);
    ctx.save(); ctx.beginPath(); ctx.roundRect(x, 170, 380, 260, 30); ctx.clip();
    for (let j = 0; j < 4; j++) { const lx = ((j * 260 - t * 1800 + i * 90) % 1040 + 1040) % 1040 - 200 + x; ctx.fillStyle = 'rgba(255,210,140,0.7)'; ctx.fillRect(lx, 280, 120, 8); glow(lx + 60, 284, 70, 'rgba(255,200,120,0.4)'); }
    ctx.restore(); }
  for (const x of [460, 1380]) { line([x, 0, x, 1000], 14, '#b8c0cc'); }
  ctx.fillStyle = '#2a3346'; ctx.fillRect(0, 760, W, 70); ctx.fillStyle = '#3a4560'; ctx.fillRect(0, 740, W, 30);
  ctx.fillStyle = '#151a26'; ctx.fillRect(0, 1000, W, 80);
  glow(W / 2, 60, 900, 'rgba(200,220,255,0.18)');
}
function office(t) {
  ctx.fillStyle = vgrad(0, H, ['#2a3040', '#1a1e2a']); ctx.fillRect(0, 0, W, H);
  windowCity(220, 120, 600, 380, t, false); windowCity(1100, 120, 600, 380, t, false);
  for (let i = 0; i < 6; i++) line([0, 560 + i * 3, W, 560 + i * 3], 1, 'rgba(255,255,255,0.03)');
  ctx.fillStyle = '#12151e'; ctx.fillRect(0, 1000, W, 80);
}
function desk(x, y, w, monitor = true) { if (monitor) { rr(x + w / 2 - 110, y - 170, 220, 140, 10); fs('#111', 6); rr(x + w / 2 - 100, y - 160, 200, 120, 4); fs('#3a6aa0'); glow(x + w / 2, y - 100, 220, 'rgba(110,160,255,0.3)'); line([x + w / 2, y - 30, x + w / 2, y], 10, '#222'); } rr(x, y, w, 30, 6); fs('#c9b49a', 6); rr(x + 10, y + 30, w - 20, 1000 - y - 30, 4); fs('#8a7a66', 5); }
function cafe(t) {
  ctx.fillStyle = vgrad(0, H, ['#4a3426', '#2a1d14']); ctx.fillRect(0, 0, W, H);
  ctx.globalAlpha = 0.06; for (let x = 0; x < W; x += 70) { ctx.fillStyle = '#ffd9a0'; ctx.fillRect(x, 0, 30, 900); } ctx.globalAlpha = 1;
  rr(1250, 120, 520, 280, 8); fs('#1d1a16', 8); textC('MENU', 1510, 170, 40, '#f3e9da'); ['Latte  3.5', 'Espresso  2', 'Cocoa  3'].forEach((m, i) => textC(m, 1510, 240 + i * 50, 28, '#d9c9a8', 'normal'));
  for (const x of [380, 760, 1140]) { line([x, 0, x, 120], 4, '#111'); ctx.beginPath(); ctx.moveTo(x - 60, 170); ctx.lineTo(x + 60, 170); ctx.lineTo(x + 30, 120); ctx.lineTo(x - 30, 120); ctx.closePath(); fs('#c58a3c', 6); glow(x, 220, 400, 'rgba(255,180,90,0.35)'); }
  plant(120, 1000, 1.3);
  ctx.fillStyle = '#1e140e'; ctx.fillRect(0, 1000, W, 80);
}
function table(x, y, w) { rr(x - w / 2, y, w, 26, 10); fs('#7a5a40', 6); line([x, y + 26, x, 1000], 14, '#4a3221'); rr(x - 70, 990, 140, 14, 6); fs('#4a3221', 4); }
function cup(x, y, s = 1) { rr(x - 22 * s, y - 40 * s, 44 * s, 42 * s, 8 * s); fs('#f2ede2', 4); ctx.beginPath(); ctx.arc(x + 26 * s, y - 20 * s, 12 * s, -1.2, 1.2); fs(null, 5, C.ink);
  for (let i = 0; i < 2; i++) { const yy = y - 50 * s - ((TIME * 30 + i * 20) % 40) * s; ctx.globalAlpha = 0.4; line([x - 6 * s + i * 12 * s, yy, x + i * 12 * s + Math.sin(TIME * 3 + i) * 6, yy - 20 * s], 4, '#eee'); ctx.globalAlpha = 1; } }

// ---------- Act 1: the gift ----------
S.wake7 = (t, d) => {
  PEOPLE = []; RIM = 'rgba(200,210,255,1)';
  bedroom7(t, 0.4);
  ctx.beginPath(); ctx.ellipse(760, 640, 260, 90, -0.05, 0, 7); fs('#e8e4da', 7);
  const up = prog(t, 0.6, 1.6);
  const p = person(Object.assign({}, ZT, { x: 820, y: lerp(1150, 1000, up), s: 1.45, expr: t < 3 ? 'tired' : 'shock', look: Math.sin(t * 1.5) * 0.7, hood: false }));
  ctx.beginPath(); ctx.moveTo(250, 860); ctx.quadraticCurveTo(900, 800, 1500, 880); ctx.lineTo(1500, 1080); ctx.lineTo(250, 1080); ctx.closePath(); fs('#4a5a8a', 8);
  // whispers: tiny blurred bubbles from the walls
  thought(300, 420, 'mmm whisper', t, 2.6, { mode: 'blur', size: 20, tx: 400, ty: 520, a: 0.7 });
  thought(1560, 620, 'whisper whisper', t, 3.6, { mode: 'blur', size: 20, tx: 1450, ty: 700, a: 0.7 });
  thought(1100, 260, 'psst', t, 4.4, { mode: 'blur', size: 20, tx: 1000, ty: 330, a: 0.6 });
};
S.streetMorning = (t, d) => {
  PEOPLE = []; RIM = 'rgba(255,220,180,1)';
  streetDay(t, { pan: t * 15 });
  const ppl = [[300, 0, -1], [620, 1, 1], [1500, 2, -1], [1750, 3, 1]];
  ppl.forEach(([x0, c, dir], i) => { const x = x0 + dir * t * 60; const p = figure({ x, y: 990, s: 0.85, top: CROWD7[c], pose: 'walk', phase: t * 0.8 + i, dir, expr: 'neutral', look: dir * 0.6, noBand: true, hood: true });
    thoughtOver(p, 'blah blah blah', t, 1 + i * 0.7, { mode: 'blur', size: 22 }); });
  figure(Object.assign({}, ZT, { x: lerp(800, 1040, t / d), y: 1000, s: 1.05, pose: 'walk', phase: t * 0.8, dir: 1, expr: t > 3 ? 'shock' : 'calm', look: Math.sin(t * 2) * 0.8 }));
};
S.title7 = (t, d) => { ctx.fillStyle = '#05060c'; ctx.fillRect(0, 0, W, H);
  thought(360, 260, 'hmm', t, 0.5, { mode: 'blur', size: 22, a: 0.35 }); thought(1560, 300, 'ugh', t, 1.0, { mode: 'blur', size: 22, a: 0.35 }); thought(1500, 840, 'what if', t, 1.5, { mode: 'blur', size: 22, a: 0.35 }); thought(420, 860, 'why', t, 2.0, { mode: 'blur', size: 22, a: 0.35 });
  glow(W / 2, H / 2, 700, 'rgba(120,180,255,0.18)'); };

// ---------- Act 2: the fear ----------
function metroScene(t, readable) {
  PEOPLE = []; RIM = 'rgba(170,200,255,1)'; metro(t);
  const sway = Math.sin(t * 2) * 4;
  const seat = [[250, 0, 'calm'], [1450, 2, 'tired'], [1770, 4, 'neutral']];
  const ps = seat.map(([x, c, e], i) => figure({ x, y: 990, s: 0.85, top: CROWD7[c], pose: 'sit', expr: e, look: i ? -0.5 : 0.5, noBand: true, kind: i === 2 ? 'mom' : undefined, skin: i === 2 ? '#a9b6c6' : undefined }));
  const st = figure({ x: 1200, y: 1000, s: 0.95, top: CROWD7[1], pose: 'pockets', expr: 'calm', look: -0.4, noBand: true });
  const z = figure(Object.assign({}, ZT, { x: 760 + sway, y: 1000, s: 1.05, pose: readable ? 'stand' : 'slump', expr: readable ? (t > 6 ? 'happy' : 'shock') : 'sad', look: readable ? 0 : Math.sin(t * 1.3) * 0.8 }));
  return { ps: [...ps, st], z };
}
S.metroFear = (t, d) => {
  const { ps } = metroScene(t, false);
  ps.forEach((p, i) => thoughtOver(p, 'thinking about him', t, 0.6 + i * 0.8, { mode: 'blur', size: 24, dy: [0, 0, -150, -60][i], dx: [60, -40, 0, -230][i] }));
};
S.fearClose = (t, d) => {
  PEOPLE = []; metro(t);
  ctx.fillStyle = 'rgba(10,12,20,0.5)'; ctx.fillRect(0, 0, W, H);
  const p = person(Object.assign({}, ZT, { x: 960, y: 1300, s: 2.4, expr: 'shock', look: Math.sin(t * 4) * 0.9 }));
  sweat(p.hx + p.R * 0.8, p.hy - p.R * 0.3, t);
  [[340, 300], [1580, 280], [300, 760], [1620, 760]].forEach(([x, y], i) => thought(x, y, 'whisper', t, 0.3 + i * 0.5, { mode: 'blur', size: 22, tx: x, ty: y + 120, a: 0.8 }));
};
S.office7 = (t, d, readable) => {
  PEOPLE = []; RIM = 'rgba(170,200,255,1)'; office(t);
  const cw = [[320, 0, 'tired'], [1560, 2, 'calm']];
  const ps = cw.map(([x, c, e]) => person({ x, y: 860, s: 1.0, top: CROWD7[c], expr: e, look: x < 960 ? 0.3 : -0.3, noBand: true }));
  desk(140, 830, 360); desk(1380, 830, 360);
  const z = person(Object.assign({}, ZT, { x: 960, y: 900, s: 1.15, expr: readable ? 'calm' : 'sad', look: Math.sin(t) * 0.5, bob: readable ? 0 : 12 }));
  desk(760, 880, 400);
  return { ps, z };
};
S.officeFear = (t, d) => { const { ps } = S.office7(t, d, false); ps.forEach((p, i) => thoughtOver(p, 'about him again', t, 1 + i * 1.2, { mode: 'blur', size: 22 })); };
S.cafe7 = (t, d, readable, hi) => {
  PEOPLE = []; RIM = 'rgba(255,190,120,1)'; cafe(t);
  const g = figure(Object.assign({}, GIRL, { x: 1300, y: 1000, s: 1.0, pose: 'sit', expr: hi ? 'happy' : 'calm', look: hi ? -0.8 : 0.2, blush: hi }));
  table(1300, 830, 300); cup(1360, 830, 1.0);
  const walk = hi ? prog(t, 0.3, 3.0) : 0;
  const z = figure(Object.assign({}, ZT, { x: hi ? lerp(500, 980, walk) : 640, y: 1000, s: 1.1, pose: hi ? (walk < 1 ? 'walk' : 'wave') : 'hold', phase: t * 0.8, dir: 1,
    expr: hi ? 'happy' : (t > d * 0.5 ? 'sad' : 'calm'), look: hi ? 0.8 : (t > d * 0.55 ? -0.6 : 0.8) }));
  if (!hi && z.hands.length) cup((z.hands[0][0] + z.hands[1][0]) / 2, (z.hands[0][1] + z.hands[1][1]) / 2, 0.8);
  return { g, z };
};
S.cafeFear = (t, d) => { S.cafe7(t, d, false); };
S.imagine = (t, d) => {
  PEOPLE = []; cafe(t); ctx.fillStyle = 'rgba(20,5,8,0.55)'; ctx.fillRect(0, 0, W, H);
  person(Object.assign({}, ZT, { x: 960, y: 1300, s: 2.4, expr: 'sad', look: Math.sin(t * 3) * 0.5 }));
  [['LOSER', 320, 260], ['LOOK AT HIM', 1560, 240], ['WEIRD', 300, 700], ['WHO IS THIS GUY?', 1580, 700], ['CRINGE', 960, 140]].forEach(([w, x, y], i) => thought(x, y, w, t, 0.4 + i * 0.7, { mode: 'red', size: 40 }));
};
S.mirror7 = (t, d) => {
  PEOPLE = []; ctx.fillStyle = vgrad(0, H, ['#1d2026', '#0e0f12']); ctx.fillRect(0, 0, W, H);
  rr(1000, 140, 700, 760, 20); fs('#4a4f58', 12);
  const e = ['happy', 'calm', 'happy', 'sad'][Math.floor(t / 2) % 4];
  ctx.save(); ctx.beginPath(); ctx.roundRect(1012, 152, 676, 736, 14); ctx.clip(); ctx.fillStyle = '#1d232b'; ctx.fillRect(1000, 140, 700, 760);
  person(Object.assign({}, ZT, { x: 1350, y: 1100, s: 1.4, expr: e, look: -0.5 })); ctx.restore();
  glow(1350, 120, 520, 'rgba(255,220,170,0.35)');
  const p = person(Object.assign({}, ZT, { x: 620, y: 1080, s: 1.65, expr: e, look: 0.6 }));
  thoughtOver(p, '"Hi, I\'m Zero..." no. "Hey!" no...', t, 1.0, { size: 26, maxW: 320, dx: 120 });
};
S.postDraft = (t, d) => {
  ctx.fillStyle = '#05060c'; ctx.fillRect(0, 0, W, H); glow(W / 2, H / 2, 650, 'rgba(100,140,255,0.3)');
  ctx.save(); ctx.translate(W / 2, H / 2 + 20); phone(0, 0, 2.0, '#0f1a2c');
  textC('New post', 0, -380, 36, '#fff'); rr(-190, -300, 380, 280, 16); fs('#e8e2d6'); circle(0, -170, 60); fs('#c4733a', 4); textC('♪', 0, -165, 70, '#fff');
  const msg = 'Learning guitar! Day 1'; const typed = t < 4 ? Math.floor(prog(t, 0.5, 3.2) * msg.length) : Math.floor((1 - prog(t, 4.6, 6.6)) * msg.length);
  rr(-190, 20, 380, 90, 20); fs('#1c2a42', 4, '#33476a'); textC(msg.slice(0, typed) + ((t * 2 | 0) % 2 ? '|' : ''), -170, 65, 28, '#fff', 'normal', 'left');
  rr(60, 150, 130, 60, 30); fs(typed ? '#3c7cf0' : '#2a3550'); textC('Post', 125, 180, 26, '#fff');
  if (t > 4.2) { ctx.globalAlpha = prog(t, 4.2, 4.6) * (1 - prog(t, 6.6, 7)); textC('Delete draft?', 0, 280, 34, '#ff6b6b'); ctx.globalAlpha = 1; }
  ctx.restore(); hand(W / 2 + 120, H / 2 + 420, 1.8, -2.2, C.skin);
};
S.smaller = (t, d) => {
  PEOPLE = []; RIM = 'rgba(140,170,255,1)'; bedroom7(t, 0);
  const shrink = 1.2 - prog(t, 0, d) * 0.25;
  rr(420, 900, 1000, 120, 20); fs('#3f4f7a', 8); rr(400, 860, 120, 160, 20); fs('#5a4a3a', 7);
  figure(Object.assign({}, ZT, { x: 900, y: 1000, s: shrink, pose: 'sit', expr: 'sad', look: 0.1 }));
  glow(900, 700, 300, 'rgba(110,140,255,0.2)');
};

// ---------- Act 3: the truth ----------
S.metroTruth = (t, d) => {
  const { ps, z } = metroScene(t, true);
  const said = ['Did I lock the door?', 'I hope my boss isn\'t mad.', 'Do I look tired today?', 'I forgot my lunch...'];
  ps.forEach((p, i) => thoughtOver(p, said[i], t, 0.8 + i * 1.3, { size: 30, maxW: 300, dy: [0, 0, -150, -60][i], dx: [60, -40, 0, -230][i] }));
};
S.officeTruth = (t, d) => { const { ps, z } = S.office7(t, d, true);
  thoughtOver(ps[0], 'What if they find out I\'m not good enough?', t, 0.6, { size: 30, maxW: 340, dx: 80 });
  thoughtOver(ps[1], 'Everyone here is smarter than me.', t, 1.8, { size: 30, maxW: 340, dx: -80 }); };
S.cafeTruth = (t, d) => { const { g } = S.cafe7(t, d, false); thoughtOver(g, 'I wish someone would just say hi.', t, 1.0, { size: 32, maxW: 340, dx: -60 }); };
S.strangers = (t, d) => {
  PEOPLE = []; streetDay(t, { pan: t * 10 });
  const ppl = [[260, 0, 'I miss my dad.'], [640, 3, 'Am I a good mom?', 'mom'], [1280, 4, 'Rent is due Friday.'], [1660, 5, 'Nobody texts me back.']];
  ppl.forEach(([x, c, txt, kind], i) => { const p = figure({ x, y: 990, s: 0.85, top: CROWD7[c], pose: 'stand', expr: 'calm', look: (i - 1.5) * 0.3, noBand: true, kind, skin: kind ? '#a9b6c6' : undefined });
    thoughtOver(p, txt, t, 0.6 + i * 1.1, { size: 28, maxW: 260, dy: i % 2 ? -110 : 0 }); });
  figure(Object.assign({}, ZT, { x: 960, y: 1000, s: 1.0, pose: 'stand', expr: t > 4 ? 'sad' : 'calm', look: Math.sin(t) * 0.8 }));
};
S.laugh = (t, d) => {
  PEOPLE = []; RIM = 'rgba(255,200,130,1)'; streetDay(t, {});
  person(Object.assign({}, ZT, { x: 960, y: 1300, s: 2.4, expr: t > 1 ? 'happy' : 'shock', bob: t > 1 ? Math.abs(Math.sin(t * 8)) * -14 : 0 }));
  fireflies(t, 25, 200, 100, 1500, 800, 'rgba(255,230,160,', 2);
};

// ---------- Act 4: freedom ----------
S.freeWalk = (t, d) => {
  PEOPLE = []; RIM = 'rgba(255,210,150,1)'; streetDay(t, { pan: t * 40 });
  const z = figure(Object.assign({}, ZT, { x: 900, y: 1000, s: 1.15, pose: t % 4 > 3 ? 'armsUp' : 'walk', phase: t * 0.9, dir: 1, expr: 'happy', look: 0.5 }));
  ctx.beginPath(); ctx.arc(z.hx, z.hy, z.R * 1.12, Math.PI * 1.08, Math.PI * 1.92); fs(null, 18, '#222');
  for (const sd of [-1, 1]) { rr(z.hx + sd * z.R * 1.05 - 24, z.hy - 34, 48, 86, 20); fs('#ff8a3c', 6); }
  for (let i = 0; i < 4; i++) { const k = (t * 0.6 + i / 4) % 1; ctx.save(); ctx.globalAlpha = Math.sin(k * Math.PI); textC(i % 2 ? '♪' : '♫', z.hx + 160 + Math.sin(k * 6) * 30, z.hy - 60 - k * 300, 56, '#ffd08a'); ctx.restore(); }
};
S.parkDraw = (t, d) => {
  PEOPLE = []; RIM = 'rgba(255,220,160,1)';
  park(t, 200);
  rr(700, 850, 560, 26, 8); fs('#6a4a30', 6); line([740, 876, 740, 990], 12, '#4a3221'); line([1220, 876, 1220, 990], 12, '#4a3221');
  const w = figure({ x: 1900 - t * 40, y: 930, s: 0.7, top: CROWD7[2], pose: 'walk', phase: t * 0.8, dir: -1, expr: 'calm', look: -0.6, noBand: true });
  thoughtOver(w, 'Did I leave the oven on?', t, 1.5, { size: 28, maxW: 260 });
  const z = figure(Object.assign({}, ZT, { x: 960, y: 1000, s: 1.05, pose: 'hold', expr: 'happy', look: 0.2 }));
  if (z.hands.length) { const hx = (z.hands[0][0] + z.hands[1][0]) / 2, hy = (z.hands[0][1] + z.hands[1][1]) / 2; rr(hx - 90, hy - 110, 180, 130, 6); fs('#f6efdf', 5); const k = prog(t, 0.5, d - 0.5); ctx.save(); ctx.beginPath(); ctx.rect(hx - 85, hy - 105, 170 * k, 120); ctx.clip(); circle(hx - 30, hy - 60, 22); fs('#ffd27a', 3); line([hx - 80, hy, hx - 20, hy - 30, hx + 30, hy - 10, hx + 80, hy - 40], 4, '#3d8bd0'); ctx.restore(); }
};
S.openMic = (t, d) => {
  PEOPLE = []; RIM = 'rgba(255,200,120,1)';
  ctx.fillStyle = vgrad(0, H, ['#1a1018', '#0a070c']); ctx.fillRect(0, 0, W, H);
  lightBeam(960, 0, 380, 1000, 'rgba(255,230,180,1)', 0.25); glow(960, 700, 500, 'rgba(255,200,130,0.35)');
  rr(500, 900, 920, 60, 6); fs('#3a2418', 6);
  const z = figure(Object.assign({}, ZT, { x: 900, y: 900, s: 1.1, pose: 'hold', expr: t < d * 0.4 ? 'shock' : 'happy', look: 0.1 }));
  line([1080, 900, 1080, 620], 8, '#222'); circle(1080, 600, 22); fs('#444', 5);
  ctx.save(); ctx.translate(900, 780); ctx.rotate(-1.2); ctx.scale(0.9, 0.9); rr(-14, -330, 28, 260, 6); fs('#4a2e1c', 5); ctx.beginPath(); ctx.ellipse(0, -40, 75, 70, 0, 0, 7); fs('#c4733a', 6); ctx.beginPath(); ctx.ellipse(0, 70, 100, 95, 0, 0, 7); fs('#c4733a', 6); circle(0, 15, 28); fs('#1a1a1a', 4); ctx.restore();
  // audience silhouettes, clapping later
  for (let i = 0; i < 7; i++) { const x = 160 + i * 270, b = t > d * 0.6 ? Math.abs(Math.sin(t * 8 + i)) * -10 : 0; ctx.fillStyle = '#05040a'; circle(x, 990 + b, 70); ctx.fill(); rr(x - 90, 1040 + b, 180, 80, 30); ctx.fill(); }
  if (t > d * 0.6) thought(1560, 560, 'He\'s brave.', t, d * 0.65, { size: 28, tx: 1700, ty: 940 });
};
S.sayHi = (t, d) => { const { g } = S.cafe7(t, d, false, true); if (t > 3.4) thoughtOver(g, 'Finally!', t, 3.6, { size: 30, dx: -40 }); };
S.finalCrowd = (t, d) => {
  PEOPLE = []; RIM = 'rgba(255,190,120,1)'; streetDay(t, { sunset: 1 });
  const ppl = [[240, 0, 'What\'s for dinner?'], [560, 2, 'I hope she calls.'], [1360, 4, 'Tired...'], [1680, 5, 'Am I enough?']];
  ppl.forEach(([x, c, txt], i) => { const p = figure({ x, y: 990, s: 0.85, top: CROWD7[c], pose: 'stand', expr: 'calm', look: x < 960 ? 0.4 : -0.4, noBand: true }); thoughtOver(p, txt, t, 0.5 + i * 0.6, { size: 28, maxW: 240, dy: i % 2 ? -110 : 0 }); });
  const z = figure(Object.assign({}, ZT, { x: 960, y: 1000, s: 1.15, pose: t > 5 ? 'armsUp' : 'stand', expr: 'happy' }));
  thoughtOver(z, 'I\'m free.', t, 4.0, { size: 40, dy: -20 });
  fireflies(t, 20, 300, 200, 1300, 600, 'rgba(255,220,150,', 6);
};
Object.assign(LOOK, { title7: { noVig: 1 } });
