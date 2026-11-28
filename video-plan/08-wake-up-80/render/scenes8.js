// Video #8 "What If You Woke Up At 80?"
// Load: scene.html, scenes20.js, scenes5.js, style2.js, assets/fx.js, assets/rig.js, 07-hear-thoughts/render/scenes7.js, scenes8.js
const YOUNG = { top: '#d9692a' };
const OLD = { kind: 'dad', old: true, band: true, top: '#a8582a', skin: '#a3b3c6' };
const MOM8 = { kind: 'mom', old: true, skin: '#a9b6c6', top: '#d8c3a0' };

function oldF(o) {
  const s = o.s || 1, p = figure(Object.assign({}, OLD, { lean: 0.1 }, o));
  if (o.cane !== false && p.hands.length) { const [hx, hy] = p.hands[1]; line([hx + 6 * s, hy, hx + 26 * s, o.y + 4], 10 * s, '#5a3a22'); circle(hx + 6 * s, hy - 4 * s, 10 * s); fs('#5a3a22', 3); }
  return p;
}
function clockWall(x, y, r, h, m) {
  circle(x, y, r); fs('#f2ede2', 7); for (let i = 0; i < 12; i++) { const a = i / 12 * Math.PI * 2; line([x + Math.sin(a) * r * 0.8, y - Math.cos(a) * r * 0.8, x + Math.sin(a) * r * 0.9, y - Math.cos(a) * r * 0.9], 4); }
  const ha = h / 12 * Math.PI * 2, ma = m / 60 * Math.PI * 2;
  line([x, y, x + Math.sin(ha) * r * 0.5, y - Math.cos(ha) * r * 0.5], 8); line([x, y, x + Math.sin(ma) * r * 0.75, y - Math.cos(ma) * r * 0.75], 5); circle(x, y, 6); fs(C.ink);
}
function couch8(x, y, col = '#4a5070') { rr(x - 420, y - 250, 840, 160, 50); fs(shade(col, 0.1), 8); rr(x - 440, y - 120, 880, 140, 40); fs(col, 8); rr(x - 470, y - 200, 90, 220, 40); fs(col, 8); rr(x + 380, y - 200, 90, 220, 40); fs(col, 8); }
function livingRoom(t, o = {}) {
  const { dusty = 0, light = 0, future = false } = o;
  ctx.fillStyle = vgrad(0, H, [lerpCol('#1e2034', '#6a5450', light), lerpCol('#0e0f1a', '#2e2220', light)]); ctx.fillRect(0, 0, W, H);
  if (future) { ctx.save(); rr(1280, 110, 520, 420, 8); ctx.clip(); ctx.translate(1280, 110); ctx.scale(520 / W, 420 / H); futureCity(t, { noPods: false }); ctx.restore(); rr(1280, 110, 520, 420, 8); fs(null, 12, '#1a1418'); }
  else windowCity(1280, 110, 520, 420, t, light < 0.5);
  if (light > 0.3) lightBeam(1540, 500, 560, 800, 'rgba(255,225,180,1)', 0.15 * light, 0.5);
  frames([[180, 170, 200, 260, dusty ? '#6a6a6a' : '#5a6aa0'], [420, 210, 150, 190, dusty ? '#7a7270' : '#c07a5a']]);
  plant(1150, 980, dusty ? 0.8 : 1.1);
  ctx.fillStyle = '#100c0c'; ctx.fillRect(0, 980, W, 100);
  if (dusty) {
    for (const [cx, cy] of [[0, 0], [W, 0]]) { const sd = cx ? -1 : 1; for (let k = 0; k < 6; k++) line([cx, cy, cx + sd * Math.cos(k * 0.28) * 260, cy + Math.sin(k * 0.28) * 260], 1.5, 'rgba(220,220,220,0.4)'); for (let r = 50; r < 260; r += 45) { ctx.beginPath(); ctx.arc(cx, cy, r, cx ? Math.PI / 2 : 0, cx ? Math.PI : Math.PI / 2); fs(null, 1.5, 'rgba(220,220,220,0.35)'); } }
    dust(t, 60, 'rgba(230,220,200,0.35)');
  }
}
function futureCity(t, o = {}) {
  skyline(t, { y: 800, layers: 4, seed: 88, pan: t * 8, sky: ['#060a24', '#2a1a5a', '#8a3a8a'], lit: 0.55 });
  // holographic billboards
  [[300, 300, '#38e8ff', 'SMART LIFE'], [1500, 260, '#ff4ad8', '2081'], [980, 420, '#7aff9a', 'NEURO+']].forEach(([x, y, c, txt], i) => {
    const fl = 0.75 + 0.25 * Math.sin(t * 6 + i * 2);
    ctx.save(); ctx.globalAlpha = fl; rr(x - 150, y - 55, 300, 110, 10); fs('rgba(10,10,30,0.4)', 4, c); glow(x, y, 260, c.replace('#', '#') + '55'); textC(txt, x, y + 4, 46, c); ctx.restore();
  });
  if (!o.noPods) for (let i = 0; i < 7; i++) {
    const sp = 140 + i * 40, y = 160 + (i * 97) % 420, x = ((i * 430 + t * sp * (i % 2 ? 1 : -1)) % (W + 400) + W + 400) % (W + 400) - 200;
    rr(x - 70, y - 20, 140, 40, 20); fs('#d8e0f0', 4); rr(x - 40, y - 34, 70, 22, 10); fs('#5aa8ff', 3);
    glow(x - 70 * (i % 2 ? 1 : -1), y, 60, 'rgba(120,220,255,0.6)');
  }
}

// ---------- Act 1 ----------
S.couchNight = (t, d) => {
  PEOPLE = []; RIM = 'rgba(120,160,255,1)'; livingRoom(t, {});
  clockWall(780, 220, 70, 2.2, 14 + t * 0.5);
  couch8(960, 980);
  const z = figure(Object.assign({}, YOUNG, { x: 960, y: 980, s: 1.05, pose: 'sit', expr: t > d * 0.6 ? 'tired' : 'calm', look: 0, bob: t > d * 0.7 ? (t - d * 0.7) * 6 : 0 }));
  const hx = z.hx, hy = z.hy + z.R * 1.9; ctx.save(); ctx.translate(hx, hy); phone(0, 0, 0.32, '#2a3d66'); ctx.restore();
  hand(hx - 60, hy + 30, 1.0, 0.4, C.skin); hand(hx + 60, hy + 30, 1.0, Math.PI - 0.4, C.skin); glow(hx, hy - 80, 300, 'rgba(110,150,255,0.45)');
};
S.timeWarp = (t, d) => {
  ctx.fillStyle = '#04040a'; ctx.fillRect(0, 0, W, H);
  const r = rand(9); ctx.save(); ctx.globalCompositeOperation = 'lighter';
  for (let i = 0; i < 220; i++) { const a = r() * Math.PI * 2 + t * (1 + r() * 2), rad = ((r() * 900 - t * 600 * (0.5 + r())) % 900 + 900) % 900; const x = W / 2 + Math.cos(a) * rad, y = H / 2 + Math.sin(a) * rad * 0.7;
    line([x, y, x + Math.cos(a + 1.5) * 20, y + Math.sin(a + 1.5) * 14], 3, `rgba(${150 + r() * 100},${170 + r() * 80},255,${0.3 + r() * 0.5})`); }
  ctx.restore();
  glow(W / 2, H / 2, 500, 'rgba(140,180,255,0.4)');
  clockWall(W / 2, H / 2 - 40, 150, t * 40, t * 480);
  textC(String(2026 + Math.floor(prog(t, 0.3, d - 0.4) * 55)), W / 2, H / 2 + 200, 110, '#e8ecff');
};
S.wake80 = (t, d) => {
  PEOPLE = []; RIM = 'rgba(255,220,170,1)'; livingRoom(t, { dusty: 1, light: 0.7, future: true });
  clockWall(780, 220, 70, 7, 40);
  couch8(960, 980, '#5a5a62');
  oldF({ x: 960, y: 980, s: 1.05, pose: t < 3 ? 'slump' : 'think', expr: t < 2.5 ? 'tired' : 'shock', look: Math.sin(t) * 0.6, cane: false });
};
S.hands80 = (t, d) => {
  ctx.fillStyle = vgrad(0, H, ['#3a2a26', '#1a1210']); ctx.fillRect(0, 0, W, H); glow(W / 2, 400, 700, 'rgba(255,200,150,0.35)');
  for (const sd of [-1, 1]) {
    const x = W / 2 + sd * 260 + Math.sin(t * 30 + sd) * 4, y = 560 + Math.cos(t * 27) * 3;
    ctx.save(); ctx.translate(x, y); ctx.scale(sd, 1);
    ctx.beginPath(); ctx.ellipse(0, 0, 170, 200, 0, 0, 7); fs(OLD.skin, 9);
    for (let i = 0; i < 4; i++) { rr(-150 + i * 72, -330, 62, 190, 31); fs(OLD.skin, 8); for (let k = 0; k < 3; k++) line([-140 + i * 72, -250 + k * 22, -100 + i * 72, -246 + k * 22], 3, 'rgba(60,70,90,0.5)'); }
    rr(150, -120, 70, 160, 35); fs(OLD.skin, 8);
    for (let k = 0; k < 5; k++) { ctx.beginPath(); ctx.arc(-40 + k * 20, 40 + k * 8, 60, 3.6, 5.2); fs(null, 3, 'rgba(60,70,90,0.45)'); }
    circle(-60, 80, 10); fs('rgba(120,90,70,0.4)'); circle(40, -40, 7); fs('rgba(120,90,70,0.35)');
    ctx.restore();
  }
};
S.mirror80 = (t, d) => {
  PEOPLE = []; ctx.fillStyle = vgrad(0, H, ['#22252c', '#101114']); ctx.fillRect(0, 0, W, H);
  rr(1000, 140, 700, 760, 20); fs('#4a4f58', 12);
  ctx.save(); ctx.beginPath(); ctx.roundRect(1012, 152, 676, 736, 14); ctx.clip(); ctx.fillStyle = '#1d232b'; ctx.fillRect(1000, 140, 700, 760);
  person(Object.assign({}, OLD, { x: 1350, y: 1100, s: 1.4, expr: t > 2 ? 'shock' : 'calm', look: -0.5 })); ctx.restore();
  for (let i = 0; i < 6; i++) line([1040 + i * 110, 160, 1100 + i * 120, 880], 2, 'rgba(255,255,255,0.05)');
  glow(1350, 120, 520, 'rgba(255,220,170,0.35)');
  person(Object.assign({}, OLD, { x: 620, y: 1080, s: 1.65, expr: t > 2 ? 'shock' : 'calm', look: 0.6 }));
  hand(760, lerp(1000, 520, prog(t, 3, 4.5)), 1.3, -0.5, OLD.skin);
};
S.title8 = (t, d) => { ctx.fillStyle = '#05040a'; ctx.fillRect(0, 0, W, H); const r = rand(3); for (let i = 0; i < 60; i++) { circle(r() * W, (r() * H + t * 20) % H, 2); fs('rgba(255,230,200,0.4)'); } glow(W / 2, H / 2, 700, 'rgba(255,170,80,0.18)'); };

// ---------- Act 2 ----------
S.cal2081 = (t, d) => {
  ctx.fillStyle = vgrad(0, H, ['#2a2422', '#141110']); ctx.fillRect(0, 0, W, H); glow(800, 450, 600, 'rgba(255,200,150,0.25)');
  rr(560, 180, 520, 600, 16); fs('#e8e0d0', 8); rr(560, 180, 520, 130, 16); fs('#4a8ad0', 8);
  textC('JUNE', 820, 245, 54, '#fff'); textC(prog(t, 0.5, 1.5) < 1 ? String(2026 + Math.floor(prog(t, 0.3, 1.5) * 55)) : '2081', 820, 520, 150, '#222');
  ctx.save(); ctx.translate(1380, 620); ctx.rotate(0.12); phone(0, 0, 0.9, '#111'); textC('NO SIGNAL', 0, 0, 26, '#666'); ctx.restore();
  dust(t, 40, 'rgba(230,220,200,0.3)');
};
S.futureStreet = (t, d) => {
  PEOPLE = []; RIM = 'rgba(200,120,255,1)'; futureCity(t);
  ctx.fillStyle = '#12102a'; ctx.fillRect(0, 880, W, 200); for (let i = 0; i < 12; i++) { ctx.fillStyle = 'rgba(80,220,255,0.35)'; ctx.fillRect(((i * 180 - t * 220) % W + W) % W, 960, 90, 5); }
  [[200, 4, 1], [600, 0, -1], [1500, 2, 1], [1800, 5, -1]].forEach(([x0, c, dir], i) => figure({ x: x0 + dir * t * 200, y: 990, s: 0.85, top: CROWD7[c], pose: 'walk', phase: t * 1.4 + i, dir, expr: 'calm', look: dir * 0.6, noBand: true }));
  oldF({ x: 760 + t * 25, y: 1000, s: 1.05, pose: 'walk', phase: t * 0.45, dir: 1, expr: 'sad', look: Math.sin(t * 0.7) * 0.8 });
};
S.futureLookUp = (t, d) => {
  PEOPLE = []; RIM = 'rgba(200,120,255,1)'; futureCity(t * 1.3);
  person(Object.assign({}, OLD, { x: 960, y: 1360, s: 2.3, expr: 'shock', look: Math.sin(t * 0.8) * 0.6 }));
};
S.friendsHouse = (t, d) => {
  PEOPLE = []; RIM = 'rgba(255,200,140,1)'; streetDay(t, { sunset: 0.4 });
  rr(980, 260, 620, 620, 6); fs('#8a6a5a', 8); rr(1180, 560, 220, 320, 6); fs('#4a3226', 7);
  rr(1220, 470, 140, 50, 6); fs('#e8e0d0', 4); textC('The Novaks', 1290, 497, 22, '#333');
  for (const [x, y] of [[1030, 330], [1440, 330]]) { rr(x, y, 120, 120, 4); fs('#ffe8b5', 6); }
  oldF({ x: 700, y: 1000, s: 1.05, pose: 'stand', expr: 'sad', look: 0.8 });
};

// ---------- Act 3 ----------
S.tryRun = (t, d) => {
  PEOPLE = []; RIM = 'rgba(255,200,140,1)'; park(t, 120);
  const running = t < 3.2;
  figure({ x: 1900 - t * 150, y: 930, s: 0.7, top: CROWD7[1], pose: 'run', phase: t * 1.2, dir: -1, expr: 'happy', look: -0.6, noBand: true });
  const p = oldF({ x: 600 + Math.min(t, 3.2) * 60, y: 1000, s: 1.05, pose: running ? 'run' : 'slump', phase: t * 0.5, dir: 1, expr: running ? 'determined' : 'tired', look: 0.6, cane: !running });
  if (!running) { sweat(p.hx + 100, p.hy - 30, t); line([p.hx - 40, p.hy + 120, p.hx + 40, p.hy + 120], 0.1); }
};
S.tryGuitar = (t, d) => {
  PEOPLE = []; RIM = 'rgba(255,200,140,1)'; livingRoom(t, { dusty: 0.6, light: 0.5, future: true });
  person(Object.assign({}, OLD, { x: 900, y: 1060, s: 1.5, expr: t > d * 0.5 ? 'sad' : 'determined' }));
  ctx.save(); ctx.translate(960, 880); ctx.rotate(-1.2); ctx.scale(1.1, 1.1); rr(-14, -330, 28, 260, 6); fs('#4a2e1c', 5); ctx.beginPath(); ctx.ellipse(0, -40, 75, 70, 0, 0, 7); fs('#8a6a4a', 6); ctx.beginPath(); ctx.ellipse(0, 70, 100, 95, 0, 0, 7); fs('#8a6a4a', 6); circle(0, 15, 28); fs('#1a1a1a', 4); ctx.restore();
  hand(940 + Math.sin(t * 25) * 6, 860 + Math.sin(t * 31) * 6, 1.2, 0.3, OLD.skin); hand(1320 + Math.sin(t * 22) * 6, 680, 1.1, -1.2, OLD.skin);
  for (let i = 0; i < 4; i++) { const k = (t * 0.4 + i / 4) % 1; ctx.save(); ctx.globalAlpha = Math.sin(k * Math.PI) * 0.8; textC(i % 2 ? '?' : '♪', 520 + i * 70 + Math.sin(t * 20 + i) * 12, 760 - k * 400, 56, '#9aa'); ctx.restore(); }
};
S.callMom80 = (t, d) => {
  ctx.fillStyle = '#05060a'; ctx.fillRect(0, 0, W, H); glow(W / 2, H / 2, 650, 'rgba(110,150,255,0.3)');
  ctx.save(); ctx.translate(W / 2 + Math.sin(t * 28) * 3, H / 2 + 20); phone(0, 0, 2.0, '#0f1a2c');
  circle(0, -250, 80); fs('#c87a4a'); textC('M', 0, -248, 80, '#fff'); textC('Mom ❤', 0, -120, 60, '#fff');
  if (t < 4) { textC('Calling' + '.'.repeat(1 + Math.floor(t * 2) % 3), 0, -40, 36, '#9fe0b8', 'normal'); }
  else { ctx.globalAlpha = prog(t, 4, 4.6); textC('The number you have dialed', 0, -40, 28, '#ff8a8a', 'normal'); textC('is no longer in service.', 0, 0, 28, '#ff8a8a', 'normal'); ctx.globalAlpha = 1; }
  circle(0, 280, 60); fs('#e04848'); textC('✕', 0, 282, 50, '#fff');
  ctx.restore();
  hand(W / 2 - 200 + Math.sin(t * 30) * 4, H / 2 + 300, 1.9, 0.4, OLD.skin);
};
S.photoWall = (t, d) => {
  PEOPLE = []; RIM = 'rgba(255,210,160,1)'; ctx.fillStyle = vgrad(0, H, ['#3a2e2a', '#1e1714']); ctx.fillRect(0, 0, W, H);
  glow(1100, 300, 800, 'rgba(255,200,150,0.25)');
  const labels = ['Trip with Dad', 'The ocean', 'My band', "Mom's 70th", 'Our wedding?', 'Mountains'];
  labels.forEach((l, i) => { const x = 700 + (i % 3) * 360, y = 160 + Math.floor(i / 3) * 330, a = prog(t, 0.5 + i * 0.6, 1.0 + i * 0.6);
    ctx.save(); ctx.globalAlpha = a; rr(x, y, 300, 230, 6); fs('#5a3a22', 8); rr(x + 18, y + 18, 264, 194, 4); fs('#2a2220');
    ctx.setLineDash([12, 10]); rr(x + 40, y + 40, 220, 150, 6); fs(null, 3, 'rgba(255,255,255,0.25)'); ctx.setLineDash([]);
    textC(l, x + 150, y + 270, 26, '#d9c9a8', 'normal'); ctx.restore(); });
  oldF({ x: 380, y: 1000, s: 1.05, pose: 'stand', expr: 'sad', look: 0.9 });
  dust(t, 40, 'rgba(230,220,200,0.3)');
};
S.screen80 = (t, d) => {
  ctx.fillStyle = '#05060c'; ctx.fillRect(0, 0, W, H); glow(W / 2, H / 2, 700, 'rgba(110,150,255,0.35)');
  ctx.save(); ctx.translate(W / 2, H / 2 + 20); phone(0, 0, 2.0, '#0f1a2c');
  textC('Screen Time', 0, -330, 40, '#9fb4d6', 'normal'); textC('Lifetime total', 0, -270, 28, '#778', 'normal');
  const y = Math.min(21, prog(t, 0.3, 3.5) * 21); textC(Math.floor(y) + ' years', 0, -150, 100, '#ff6b5a');
  ['Videos', 'Games', 'Feeds', 'Chats'].forEach((n, i) => { const w = [300, 230, 200, 140][i] * prog(t, 0.5 + i * 0.3, 1.5 + i * 0.3); textC(n, -170, -20 + i * 80, 28, '#ccd', 'normal', 'left'); rr(-170, 10 + i * 80, w, 18, 9); fs(['#ff5a7a', '#6a8aff', '#ff4a3a', '#d070ff'][i]); });
  ctx.restore();
};

// ---------- Act 4 ----------
S.benchKid = (t, d) => {
  PEOPLE = []; RIM = 'rgba(255,190,120,1)'; streetDay(t, { sunset: 1 });
  rr(620, 850, 680, 26, 8); fs('#5a3a22', 6); line([660, 876, 660, 990], 12, '#3a2414'); line([1260, 876, 1260, 990], 12, '#3a2414');
  oldF({ x: 760, y: 1000, s: 1.05, pose: 'sit', expr: t > d * 0.6 ? 'calm' : 'sad', look: 0.7, cane: false });
  line([640, 1000, 610, 760], 10, '#5a3a22');
  const k = prog(t, 0.3, 3.5);
  figure({ x: lerp(1700, 1120, k), y: 1000, s: 0.85, kind: 'kid', top: '#5aa0e0', pose: k < 1 ? 'walk' : 'sit', phase: t * 0.9, dir: -1, expr: 'happy', look: -0.8, noBand: true });
  const bx = lerp(1780, 1250, k) + (k >= 1 ? Math.sin(t * 2) * 6 : 0); circle(bx, 970, 30); fs('#e05a3a', 5); line([bx - 28, 960, bx + 28, 980], 3, '#fff');
};
S.oldClose = (t, d) => {
  PEOPLE = []; RIM = 'rgba(255,190,120,1)'; streetDay(t, { sunset: 1 });
  ctx.fillStyle = 'rgba(20,10,10,0.25)'; ctx.fillRect(0, 0, W, H);
  person(Object.assign({}, OLD, { x: 900, y: 1320, s: 2.3, expr: 'cry', tear: prog(t, 0.5, 4), look: 0.4 }));
};
S.closeEyes = (t, d) => {
  ctx.fillStyle = '#fffaf0'; ctx.fillRect(0, 0, W, H);
  const r = rand(4); ctx.save(); for (let i = 0; i < 160; i++) { const a = r() * Math.PI * 2, rad = (1 - prog(t, 0, d)) * (300 + r() * 700); circle(W / 2 + Math.cos(a) * rad, H / 2 + Math.sin(a) * rad, 3 + r() * 4); fs(`rgba(255,${180 + r() * 60},120,${0.6})`); } ctx.restore();
  glow(W / 2, H / 2, 600, 'rgba(255,220,160,0.6)');
};

// ---------- Act 5 ----------
S.wakeYoung = (t, d) => {
  PEOPLE = []; RIM = 'rgba(255,220,170,1)'; livingRoom(t, { light: 0.8 });
  clockWall(780, 220, 70, 6, 2 + t);
  couch8(960, 980);
  const z = figure(Object.assign({}, YOUNG, { x: 960, y: 980, s: 1.05, pose: t < 2 ? 'slump' : t < 5 ? 'think' : 'armsUp', expr: t < 2 ? 'tired' : t < 5 ? 'shock' : 'happy', look: Math.sin(t * 1.5) * 0.5 }));
  ctx.save(); ctx.translate(1240, 900); ctx.rotate(0.4); phone(0, 0, 0.3, '#2a3d66'); ctx.restore(); textC('6:02', 1240, 900, 18, '#fff');
};
S.windowSun = (t, d) => {
  PEOPLE = []; RIM = 'rgba(255,220,170,1)';
  skyline(t, { y: 860, layers: 4, seed: 12, sky: ['#3a2a6a', '#e0805a', '#ffd090'], lit: 0.15, warm: true });
  circle(W / 2 + 200, 760, 170); fs('#fff1c0'); glow(W / 2 + 200, 760, 800, 'rgba(255,220,160,0.75)');
  ctx.save(); ctx.fillStyle = '#2a1e1e'; ctx.beginPath(); ctx.rect(0, 0, W, H); ctx.rect(240, 80, 1440, 880); ctx.fill('evenodd'); ctx.restore();
  rr(240, 80, 1440, 880, 6); fs(null, 18, '#3a2a24'); line([960, 80, 960, 960], 16, '#3a2a24');
  figure(Object.assign({}, YOUNG, { x: 700, y: 1120, s: 1.4, pose: t > 2 ? 'armsUp' : 'stand', expr: 'happy', look: 0.5 }));
};
S.callMomYoung = (t, d) => {
  PEOPLE = []; RIM = 'rgba(255,200,140,1)'; livingRoom(t, { light: 0.9 });
  const p = person(Object.assign({}, YOUNG, { x: 860, y: 1010, s: 1.4, expr: 'happy', look: 0.3, blush: true, bob: Math.abs(Math.sin(t * 3)) * -5 }));
  ctx.save(); ctx.translate(p.hx + p.R * 0.95, p.hy + 10); ctx.rotate(0.3); rr(-30, -70, 60, 140, 12); fs('#1c1c22', 6); ctx.restore();
  hand(p.hx + p.R * 1.15, p.hy + 80, 1.2, -1.2, C.skin);
  rr(1180, 600, 330, 100, 24); fs('rgba(0,0,0,0.6)'); textC('Mom ❤  00:' + String(Math.floor(t + 3)).padStart(2, '0'), 1345, 650, 34, '#9fe0b8');
};
S.runYoung = (t, d) => {
  PEOPLE = []; const sc = t * 420;
  ctx.fillStyle = vgrad(0, H, ['#3a2a5a', '#e0705a', '#ffb070']); ctx.fillRect(0, 0, W, H);
  circle(1500, 640, 130); fs('#ffe0a0'); glow(1500, 640, 600, 'rgba(255,200,120,0.7)');
  ctx.fillStyle = '#5a3a4a'; for (let i = 0; i < 6; i++) { const x = ((i * 520 - sc * 0.25) % 3120 + 3120) % 3120 - 400; ctx.beginPath(); ctx.ellipse(x, 820, 420, 200, 0, Math.PI, 0); ctx.fill(); }
  ctx.fillStyle = '#2a2230'; ctx.fillRect(0, 900, W, 180);
  for (let i = 0; i < 10; i++) { const x = ((i * 300 - sc) % 3000 + 3000) % 3000 - 100; ctx.fillStyle = '#d8c070'; ctx.fillRect(x, 975, 120, 12); }
  figure(Object.assign({}, YOUNG, { x: 800, y: 960, s: 1.05, expr: 'happy', look: 0.8, pose: 'run', phase: t * 0.9, dir: 1 }));
};
S.guitarYoung = (t, d) => {
  PEOPLE = []; RIM = 'rgba(255,210,150,1)'; livingRoom(t, { light: 0.9 });
  person(Object.assign({}, YOUNG, { x: 900, y: 1060, s: 1.5, expr: 'happy', bob: Math.sin(t * 4) * 4 }));
  ctx.save(); ctx.translate(960, 880); ctx.rotate(-1.2); ctx.scale(1.1, 1.1); rr(-14, -330, 28, 260, 6); fs('#4a2e1c', 5); ctx.beginPath(); ctx.ellipse(0, -40, 75, 70, 0, 0, 7); fs('#c4733a', 6); ctx.beginPath(); ctx.ellipse(0, 70, 100, 95, 0, 0, 7); fs('#c4733a', 6); circle(0, 15, 28); fs('#1a1a1a', 4); ctx.restore();
  hand(940, 860 + Math.sin(t * 10) * 18, 1.2, 0.3, C.skin); hand(1320, 680, 1.1, -1.2, C.skin);
  for (let i = 0; i < 5; i++) { const k = (t * 0.5 + i / 5) % 1; ctx.save(); ctx.globalAlpha = Math.sin(k * Math.PI); textC(i % 2 ? '♪' : '♫', 500 + i * 80 + Math.sin(k * 6) * 20, 760 - k * 500, 64, '#ffd08a'); ctx.restore(); }
};
S.benchMom = (t, d) => {
  PEOPLE = []; RIM = 'rgba(255,190,120,1)'; streetDay(t, { sunset: 1 });
  rr(620, 850, 680, 26, 8); fs('#5a3a22', 6); line([660, 876, 660, 990], 12, '#3a2414'); line([1260, 876, 1260, 990], 12, '#3a2414');
  figure(Object.assign({}, MOM8, { x: 820, y: 1000, s: 1.0, pose: 'sit', expr: 'happy', look: 0.6, blush: true }));
  figure(Object.assign({}, YOUNG, { x: 1110, y: 1000, s: 1.05, pose: 'sit', expr: t % 4 > 2 ? 'happy' : 'calm', look: -0.6 }));
  fireflies(t, 20, 400, 300, 1100, 500, 'rgba(255,220,150,', 3);
};
Object.assign(LOOK, { title8: { noVig: 1 } });
