// Video #6 "What If You Met Yourself From 10 Years Ago?"
// Load: scene.html, scenes20.js, scenes5.js, style2.js, assets/fx.js, scenes6.js
const KID = { kind: 'kid', top: '#ff8a3c', band: true };
const ADULT = { top: '#c9692e' };
const LAMP = 1000;

function kidP(o) { // 15-year-old Zero with a backpack
  const s = o.s || 1, x = o.x;
  rr(x - 95 * s, o.y - 150 * s, 190 * s, 120 * s, 30 * s); fs('#3d6fb0', 7 * s);
  const p = person(Object.assign({}, KID, o));
  line([x - 45 * s, o.y - 140 * s, x - 55 * s, o.y - 10 * s], 9 * s, '#2a4f80'); line([x + 45 * s, o.y - 140 * s, x + 55 * s, o.y - 10 * s], 9 * s, '#2a4f80');
  return p;
}
function adultP(o) { return person(Object.assign({}, ADULT, o)); }
// blurred skyline is expensive: render it once per dawn level into a cache (drawn at device scale, before camera transforms)
const SKY_CACHE = {};
function skyCached(dawn) {
  const key = Math.round(dawn * 20);
  if (!SKY_CACHE[key]) {
    const dd = key / 20, c = document.createElement('canvas'); c.width = W; c.height = 880;
    ctx.save(); ctx.setTransform(cv.width / W, 0, 0, cv.height / H, 0, 0); ctx.filter = 'blur(3px)';
    skyline(0, { y: 760, layers: 3, seed: 41, sky: [lerpCol('#070a1e', '#2a2a6a', dd), lerpCol('#1a1a44', '#c86a7a', dd), lerpCol('#3a2a5a', '#ffb070', dd)], lit: 0.45 });
    ctx.restore();
    c.getContext('2d').drawImage(cv, 0, 0, cv.width, cv.height * 880 / H, 0, 0, W, 880);
    SKY_CACHE[key] = c;
  }
  return SKY_CACHE[key];
}
function streetNight(t, o = {}) {
  const { lampX = LAMP, pan = 0, rainA = 1, dawn = 0, lampGlow = 1, magic = 0 } = o;
  ctx.drawImage(skyCached(dawn), -40 - pan * 0.5, 0, W + 80, 880);
  ctx.fillStyle = vgrad(760, H, ['#141428', '#0a0a16']); ctx.fillRect(0, 760, W, 320);
  const r = rand(5); for (let i = 0; i < 40; i++) { const x = r() * W; ctx.fillStyle = `rgba(255,200,120,${0.05 + r() * 0.07})`; ctx.fillRect(x, 800, 6 + r() * 10, 120 + r() * 160); }
  ctx.fillStyle = '#23233c'; ctx.fillRect(0, 900, W, 14);
  line([lampX, 1000, lampX, 330], 14, '#15142a'); line([lampX, 330, lampX + 95, 330], 12, '#15142a'); rr(lampX + 60, 318, 75, 28, 8); fs('#2a2840');
  const gc = magic > 0 ? `rgba(255,${200 + 30 * magic},${140 - 60 * magic},1)` : 'rgba(255,210,140,1)';
  glow(lampX + 97, 350, 340 + magic * 200, `rgba(255,210,140,${0.55 * lampGlow})`);
  lightBeam(lampX + 97, 345, 260 + magic * 80, 650, gc, 0.2 * lampGlow + magic * 0.15);
  ctx.save(); ctx.globalCompositeOperation = 'lighter'; ctx.globalAlpha = 0.35 * lampGlow; ctx.beginPath(); ctx.ellipse(lampX + 97, 985, 280, 40, 0, 0, 7); ctx.fillStyle = 'rgba(255,200,130,0.6)'; ctx.fill(); ctx.restore();
  if (rainA > 0) rain(t, 260, 0.45 * rainA);
}
function walkHands(p, t, s, sp = 7) { hand(p.hx - 120 * s, p.hy + 230 * s + Math.sin(t * sp) * 28 * s, 1.0 * s, 0.3, C.skin); hand(p.hx + 120 * s, p.hy + 230 * s - Math.sin(t * sp) * 28 * s, 1.0 * s, Math.PI - 0.3, C.skin); }
function notebook(x, y, s, mode, t) { // mode: 'closed' | 'cross' | 'tick' | 'open'
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  if (mode === 'closed') { rr(-120, -160, 240, 320, 12); fs('#2f5f9a', 8); rr(-80, -100, 160, 70, 6); fs('#f2ead8', 5); textC('MY DREAMS', 0, -66, 24, '#333'); ctx.restore(); return; }
  rr(-560, -330, 1120, 660, 18); fs('#2f5f9a', 10); rr(-540, -310, 530, 620, 8); fs('#f6efdf', 5); rr(10, -310, 530, 620, 8); fs('#f6efdf', 5);
  for (let i = 0; i < 12; i++) { line([-520, -230 + i * 46, -30, -230 + i * 46], 2, 'rgba(90,120,180,0.35)'); line([30, -230 + i * 46, 520, -230 + i * 46], 2, 'rgba(90,120,180,0.35)'); }
  ctx.font = '46px Lucky'; ctx.textAlign = 'center'; ctx.fillStyle = '#b8452e'; ctx.fillText('MY DREAMS', -275, -250);
  ctx.font = '26px Lucky'; ctx.fillStyle = '#555'; ctx.fillText('age 15', -275, -205);
  // doodles
  circle(300, -150, 60); fs('#ffd27a', 4); for (let i = 0; i < 8; i++) { const a = i * Math.PI / 4; line([300 + Math.cos(a) * 75, -150 + Math.sin(a) * 75, 300 + Math.cos(a) * 100, -150 + Math.sin(a) * 100], 4, '#e0a030'); }
  ctx.beginPath(); ctx.moveTo(60, 200); for (let i = 0; i <= 10; i++) ctx.lineTo(60 + i * 46, 200 - (i % 2 ? 90 : 30) - i * 4); fs(null, 4, '#3d6fb0');
  textC('♪', 140, -60, 80, '#555'); textC('✈', 430, 40, 70, '#555');
  const items = ['Learn guitar', 'Draw every day', 'See the ocean', 'Travel abroad', 'Make mom proud'];
  items.forEach((it, i) => {
    const yy = -130 + i * 92; ctx.font = '40px Lucky'; ctx.textAlign = 'left'; ctx.fillStyle = '#333'; ctx.fillText((i + 1) + '. ' + it, -500, yy);
    const w = ctx.measureText((i + 1) + '. ' + it).width;
    if (mode === 'cross') { const k = prog(t, 1.0 + i * 1.1, 1.6 + i * 1.1); if (k > 0) line([-505, yy - 12, -505 + (w + 10) * k, yy - 8], 7, 'rgba(200,40,40,0.9)'); }
    if (mode === 'tick') { const k = prog(t, 0.6 + i * 1.0, 1.1 + i * 1.0); if (k > 0) { ctx.save(); ctx.globalAlpha = k; ctx.translate(-500 + w + 50, yy - 14); ctx.scale(0.6 + 0.4 * k, 0.6 + 0.4 * k); line([-18, 0, -4, 16, 26, -22], 9, '#2fa05a'); ctx.restore(); if (k < 1) glow(-500 + w + 50, yy - 14, 70, 'rgba(120,255,160,0.6)'); } }
  });
  ctx.restore();
}

// ---------------- Act 1: the meeting ----------------
S.rainCity = (t, d) => {
  skyline(t, { y: 820, layers: 4, seed: 12, pan: t * 18, sky: ['#05071a', '#141436', '#2a2050'], lit: 0.42 });
  ctx.fillStyle = '#0b0b18'; ctx.fillRect(0, 900, W, 180);
  const v = lightning(t, [2.2]); if (v) { ctx.save(); ctx.globalAlpha = v; line([1300, 0, 1260, 160, 1320, 260, 1240, 420], 5, '#e8ecff'); glow(1280, 200, 400, 'rgba(200,210,255,0.6)'); ctx.restore(); }
  rain(t, 320, 0.5);
};
S.walkHome = (t, d) => {
  PEOPLE = []; streetNight(t, { pan: t * 10 });
  const x = lerp(380, 820, t / d), s = 1.15;
  const p = adultP({ x, y: 1000, s, expr: 'tired', look: 0.6, bob: Math.abs(Math.sin(t * 6)) * -10 });
  walkHands(p, t, s, 6);
  rain(t, 120, 0.35);
};
S.lampGlow = (t, d) => {
  PEOPLE = []; const m = prog(t, 0.5, d);
  streetNight(t, { magic: m, rainA: 1 - m * 0.6 });
  fireflies(t, Math.floor(10 + 40 * m), LAMP - 150, 500, 500, 450, 'rgba(255,210,130,', 7);
  // silhouette forms
  ctx.save(); ctx.globalAlpha = prog(t, d * 0.45, d); ctx.fillStyle = '#0a0812';
  rr(LAMP + 97 - 70, 1000 - 125, 140, 125, 30); ctx.fill(); circle(LAMP + 97, 1000 - 125 - 60, 75); ctx.fill(); ctx.restore();
  adultP({ x: 420, y: 1000, s: 1.15, expr: t > d * 0.5 ? 'shock' : 'calm', look: 0.9 });
};
S.reveal = (t, d) => {
  PEOPLE = []; streetNight(t, { magic: 1, rainA: 0.4 });
  fireflies(t, 30, LAMP - 200, 450, 600, 500, 'rgba(255,215,140,', 9);
  const k = kidP({ x: LAMP + 97, y: 1000, s: 1.25, expr: 'happy', look: -0.6 });
  hand(k.hx - 160 + Math.sin(t * 8) * 25, k.hy - 40, 1.0, -0.4, C.skin);
};
S.title6 = (t, d) => {
  ctx.fillStyle = '#05040a'; ctx.fillRect(0, 0, W, H);
  fireflies(t, 40, 0, 0, W, H, 'rgba(255,210,130,', 4);
  glow(W / 2, H / 2, 700, 'rgba(255,170,80,0.2)');
};

// ---------------- Act 2: questions ----------------
S.meet = (t, d) => {
  PEOPLE = []; streetNight(t, { magic: 0.4, rainA: 0.3 });
  fireflies(t, 14, 400, 450, 1100, 400, 'rgba(255,215,140,', 2);
  adultP({ x: 700, y: 1000, s: 1.2, expr: 'shock', look: 0.8 });
  const k = kidP({ x: 1250, y: 1000, s: 1.0, expr: 'happy', look: -0.8, bob: Math.abs(Math.sin(t * 5)) * -16 });
};
S.kidClose = (t, d) => {
  PEOPLE = []; streetNight(t, { magic: 0.4, rainA: 0.3 });
  const ex = S.kidClose.expr || 'happy';
  kidP({ x: 1180, y: 1060, s: 2.0, expr: ex, look: -0.6, tear: 0.6 });
  fireflies(t, 10, 700, 200, 900, 500, 'rgba(255,215,140,', 5);
};
S.kidCloseSad = (t, d) => { S.kidClose.expr = 'sad'; S.kidClose(t, d); S.kidClose.expr = 'happy'; };
S.kidCloseCry = (t, d) => { S.kidClose.expr = 'cry'; S.kidClose(t, d); S.kidClose.expr = 'happy'; };
S.adultClose = (t, d) => {
  PEOPLE = []; streetNight(t, { magic: 0.3, rainA: 0.35 });
  adultP({ x: 760, y: 1280, s: 2.0, expr: S.adultClose.expr || 'sad', look: t > d * 0.5 ? -0.5 : 0.5 });
};
S.adultCloseCalm = (t, d) => { S.adultClose.expr = 'calm'; S.adultClose(t, d); S.adultClose.expr = 'sad'; };
S.screenTime = (t, d) => {
  ctx.fillStyle = '#05060c'; ctx.fillRect(0, 0, W, H); glow(W / 2, H / 2, 700, 'rgba(110,150,255,0.35)');
  ctx.save(); ctx.translate(W / 2, H / 2 + 20); phone(0, 0, 2.0, '#0f1a2c');
  textC('Screen Time', 0, -330, 40, '#9fb4d6', 'normal'); textC('Daily average', 0, -270, 28, '#778', 'normal');
  const h = Math.min(7.7, prog(t, 0.3, 2.5) * 7.7); textC(Math.floor(h) + 'h ' + Math.floor((h % 1) * 60) + 'm', 0, -170, 96, '#ff6b5a');
  ['TikTok', 'YouTube', 'Games', 'Instagram'].forEach((n, i) => { const w = [300, 240, 170, 110][i] * prog(t, 0.5 + i * 0.3, 1.5 + i * 0.3); textC(n, -170, -40 + i * 80, 28, '#ccd', 'normal', 'left'); rr(-170, -10 + i * 80, w, 18, 9); fs(['#ff5a7a', '#ff4a3a', '#6a8aff', '#d070ff'][i]); });
  ctx.restore();
};
S.memoryDraw = (t, d) => {
  PEOPLE = [];
  ctx.fillStyle = vgrad(0, H, ['#3a2a1e', '#20160e']); ctx.fillRect(0, 0, W, H);
  glow(1250, 380, 700, 'rgba(255,190,110,0.55)'); lightBeam(1250, 250, 400, 800, 'rgba(255,210,150,1)', 0.14);
  kidP({ x: 820, y: 900, s: 1.25, expr: 'happy', look: 0.5 });
  rr(300, 880, 1320, 200, 0); fs('#5a4030', 7);
  rr(900, 820, 380, 70, 4); fs('#f6efdf', 5);
  const k = prog(t, 0.5, d - 0.5); ctx.save(); ctx.beginPath(); ctx.rect(905, 790, 370 * k, 100); ctx.clip(); circle(1000, 850, 22); fs('#ffd27a', 3); line([1040, 870, 1100, 830, 1160, 865, 1230, 820], 4, '#3d6fb0'); ctx.restore();
  hand(905 + 370 * k, 840, 0.9, -0.4, C.skin);
  fireflies(t, 25, 600, 300, 900, 500, 'rgba(255,215,140,', 11);
};
S.roomMess = (t, d) => {
  PEOPLE = [];
  ctx.fillStyle = vgrad(0, H, ['#11131c', '#08090e']); ctx.fillRect(0, 0, W, H);
  windowCity(1350, 140, 420, 340, t, true);
  ctx.fillStyle = '#0c0c12'; ctx.fillRect(0, 960, W, 120);
  for (const [x, r] of [[300, 0.2], [380, -0.4], [1500, 0.1], [1580, 0.6], [700, -0.2]]) { ctx.save(); ctx.translate(x, 990); ctx.rotate(r); rr(-25, -60, 50, 80, 8); fs('#2b9b5a', 5); ctx.restore(); }
  for (let i = 0; i < 4; i++) { rr(1100 - i * 6, 980 - i * 26, 230, 26, 3); fs('#c9a06a', 4); }
  glow(1560, 520, 700, 'rgba(90,120,255,0.35)'); glow(760, 500, 500, 'rgba(255,190,120,0.25)');
  dust(t, 30, 'rgba(160,160,180,0.3)');
  kidP({ x: 760, y: 1000, s: 1.15, expr: t > 2 ? 'shock' : 'calm', look: Math.sin(t * 0.8) });
};

// ---------------- Act 3: the truth ----------------
S.curb = (t, d) => {
  PEOPLE = []; streetNight(t, { magic: 0.2, rainA: 0.7 });
  // adult sitting on the curb, hugging knees
  const p = adultP({ x: 760, y: 1010, s: 1.2, expr: 'sad', look: 0.2 });
  for (const sd of [-1, 1]) { rr(760 + sd * 84 - 66, 1010 - 180, 132, 190, 60); fs('#3a3d48', 8); }
  hand(712, 860, 1.1, 0.3, C.skin); hand(808, 860, 1.1, Math.PI - 0.3, C.skin);
  kidP({ x: 1250, y: 1000, s: 1.0, expr: 'sad', look: -0.8 });
};
S.dreamsCross = (t, d) => { ctx.fillStyle = '#0a0a10'; ctx.fillRect(0, 0, W, H); glow(W / 2, H / 2, 800, 'rgba(160,180,255,0.2)'); notebook(W / 2, H / 2 - 30, 1.15, 'cross', t); rain(t, 120, 0.25); };

// ---------------- Act 4: the gift ----------------
S.giveBook = (t, d) => {
  PEOPLE = []; streetNight(t, { magic: 0.6, rainA: 0.4 });
  fireflies(t, 20, 600, 450, 900, 400, 'rgba(255,215,140,', 6);
  adultP({ x: 700, y: 1000, s: 1.2, expr: t > d * 0.6 ? 'shock' : 'sad', look: 0.8 });
  const k = kidP({ x: 1200, y: 1000, s: 1.0, expr: 'calm', look: -0.8 });
  const m = prog(t, 1.0, d * 0.7), bx = lerp(1080, 880, m), by = lerp(820, 760, m);
  notebook(bx, by, 0.32, 'closed', t); hand(bx + 40, by + 40, 1.0, -0.3, C.skin); if (m > 0.8) hand(bx - 50, by + 30, 1.1, 0.3, C.skin);
};
S.fade = (t, d) => {
  PEOPLE = []; streetNight(t, { magic: 1 - prog(t, d * 0.5, d), rainA: 0.25 });
  const k = prog(t, 2.0, d - 1);
  ctx.save(); ctx.globalAlpha = 1 - k; kidP({ x: 1180, y: 1000, s: 1.3, expr: 'happy', look: -0.6 }); ctx.restore();
  sparksRise(t, 1060, 520, 240, 480, 160, k);
  glow(1180, 700, 380, `rgba(255,215,140,${0.4 * (1 - k)})`);
};
S.alone = (t, d) => {
  PEOPLE = []; const dawn = prog(t, 0, d) * 0.6;
  streetNight(t, { dawn, rainA: Math.max(0, 0.4 - t * 0.1), lampGlow: 1 - dawn });
  sparksRise(t + 6, 900, 400, 300, 300, 30, 0.7 + t * 0.05);
  adultP({ x: 900, y: 1000, s: 1.3, expr: t > d * 0.5 ? 'determined' : 'sad', look: 0.3 });
  notebook(980, 860, 0.3, 'closed', t); hand(1010, 900, 1.1, -0.3, C.skin);
};

// ---------------- Act 5: the rise ----------------
function sunRoom(t) {
  ctx.fillStyle = vgrad(0, H, ['#5a3a3a', '#2a1a1a']); ctx.fillRect(0, 0, W, H);
  windowCity(1250, 120, 520, 420, t, false); lightBeam(1510, 520, 600, 900, 'rgba(255,220,170,1)', 0.18, 0.55);
  ctx.save(); ctx.globalCompositeOperation = 'lighter'; const r = rand(31); for (let i = 0; i < 40; i++) { const x = 900 + r() * 700 + Math.sin(t + i) * 20, y = 400 + r() * 500 - (t * 15 % 60); circle(x, y, 2 + r() * 2); fs(`rgba(255,230,180,${0.3 + 0.3 * Math.sin(t * 2 + i)})`); } ctx.restore();
}
S.desk6 = (t, d) => {
  PEOPLE = []; sunRoom(t);
  adultP({ x: 820, y: 900, s: 1.35, expr: 'determined', look: 0.2 });
  rr(250, 880, 1420, 200, 0); fs('#6a4a30', 7);
  notebook(820, 850, 0.18 + prog(t, 0.5, 2) * 0, 'closed', t);
};
S.guitar6 = (t, d) => {
  PEOPLE = []; sunRoom(t);
  const bad = t < d * 0.55;
  const p = adultP({ x: 900, y: 1060, s: 1.5, expr: bad ? 'angry' : 'happy', bob: Math.sin(t * 4) * 4 });
  ctx.save(); ctx.translate(960, 880); ctx.rotate(-1.2); ctx.scale(1.1, 1.1);
  rr(-14, -330, 28, 260, 6); fs('#4a2e1c', 5); ctx.beginPath(); ctx.ellipse(0, -40, 75, 70, 0, 0, 7); fs('#c4733a', 6); ctx.beginPath(); ctx.ellipse(0, 70, 100, 95, 0, 0, 7); fs('#c4733a', 6); circle(0, 15, 28); fs('#1a1a1a', 4); ctx.restore();
  hand(940, 860 + Math.sin(t * 10) * 18, 1.2, 0.3, C.skin); hand(1320, 680, 1.1, -1.2, C.skin);
  for (let i = 0; i < 5; i++) { const k = (t * 0.5 + i / 5) % 1; ctx.save(); ctx.globalAlpha = Math.sin(k * Math.PI); const jit = bad ? Math.sin(t * 30 + i) * 12 : 0;
    textC(bad ? (i % 2 ? '?' : '♪') : (i % 2 ? '♪' : '♫'), 500 + i * 80 + Math.sin(k * 6) * 20 + jit, 760 - k * 500, 64, bad ? '#9aa' : '#ffd08a'); ctx.restore(); }
  if (bad) sweat(p.hx + 110, p.hy - 30, t);
};
S.drawing6 = (t, d) => {
  PEOPLE = []; sunRoom(t);
  adultP({ x: 700, y: 900, s: 1.3, expr: t > d * 0.6 ? 'happy' : 'determined', look: 0.7 });
  rr(200, 880, 1520, 200, 0); fs('#6a4a30', 7);
  ctx.save(); ctx.translate(1180, 600); ctx.rotate(-0.04); rr(-280, -230, 560, 400, 6); fs('#5a3a22', 8); rr(-260, -210, 520, 360, 4); fs('#f6efdf');
  const k = prog(t, 0.3, d - 0.5);
  ctx.beginPath(); ctx.rect(-260, -210, 520 * k, 360); ctx.clip();
  ctx.fillStyle = vgrad(-210, 150, ['#ffb27a', '#ffd6a0']); ctx.fillRect(-260, -210, 520, 360);
  circle(80, -40, 60); fs('#fff1c0'); ctx.fillStyle = '#5a3a6a'; for (let i = 0; i < 8; i++) ctx.fillRect(-250 + i * 66, 40 - (i * 37 % 90), 56, 120 + (i * 37 % 90));
  ctx.fillStyle = '#3a6aa0'; ctx.fillRect(-260, 110, 520, 40); ctx.restore();
  hand(920 + 520 * k * 0.9, 640, 1.0, -0.4, C.skin);
};
S.plane = (t, d) => {
  PEOPLE = [];
  ctx.fillStyle = vgrad(0, H, ['#b8ae9e', '#8a8070']); ctx.fillRect(0, 0, W, H);
  ctx.save(); ctx.beginPath(); ctx.ellipse(1250, 470, 300, 390, 0, 0, 7); ctx.clip();
  ctx.fillStyle = vgrad(80, 860, ['#ff9a6a', '#ffc890', '#ffe6b8']); ctx.fillRect(900, 60, 700, 820);
  glow(1300, 380, 400, 'rgba(255,240,200,0.9)');
  const r = rand(14); for (let i = 0; i < 12; i++) { const sp = 160 + r() * 260, x = 900 + ((r() * 1100 - t * sp) % 1100 + 1100) % 1100 - 200, y = 150 + r() * 650, sc = 0.5 + r() * 0.8; ctx.fillStyle = 'rgba(255,255,255,0.9)'; for (let j = 0; j < 4; j++) { circle(x + j * 50 * sc, y + Math.sin(j) * 10, 42 * sc); ctx.fill(); } }
  ctx.restore();
  ctx.beginPath(); ctx.ellipse(1250, 470, 300, 390, 0, 0, 7); fs(null, 30, '#d8d0c2'); ctx.beginPath(); ctx.ellipse(1250, 470, 330, 420, 0, 0, 7); fs(null, 6, '#6a6458');
  lightBeam(1250, 470, 300, 900, 'rgba(255,210,150,1)', 0.14, 0.9);
  for (let i = 0; i < 3; i++) { rr(80 + i * 230, 120, 180, 40, 10); fs('#9a9080', 4); }
  adultP({ x: 640, y: 1100, s: 1.5, expr: 'happy', look: 0.9 });
};
S.oceanSee = (t, d) => {
  PEOPLE = [];
  ctx.fillStyle = vgrad(0, 640, ['#ffb27a', '#ffd6a0']); ctx.fillRect(0, 0, W, 640);
  circle(W / 2, 600, 160); fs('#fff1c0'); glow(W / 2, 600, 700, 'rgba(255,220,160,0.7)');
  ctx.fillStyle = vgrad(600, 900, ['#3a7ab0', '#1a4a7a']); ctx.fillRect(0, 600, W, 300);
  for (let i = 0; i < 14; i++) { const y = 620 + i * 20, x = ((i * 173 + t * 60 * (1 + i * 0.1)) % (W + 200)) - 100; ctx.fillStyle = 'rgba(255,230,190,0.5)'; ctx.fillRect(x, y, 120 + i * 8, 3); }
  ctx.fillStyle = '#e8c890'; ctx.fillRect(0, 880, W, 200);
  const k = prog(t, 0, d);
  person({ x: 760, y: 1080, s: 1.3, top: ADULT.top, expr: 'happy', look: 0.4 });
  lightLeak(t, 'rgba(255,200,120,', 0.25);
};
S.checks = (t, d) => { ctx.fillStyle = '#1a120c'; ctx.fillRect(0, 0, W, H); glow(W / 2, H / 2, 900, 'rgba(255,190,110,0.35)'); notebook(W / 2, H / 2 - 30, 1.15, 'tick', t); fireflies(t, 20, 200, 100, 1500, 800, 'rgba(255,220,150,', 8); };
S.callMom6 = (t, d, f) => {
  PEOPLE = []; sunRoom(t);
  const p = adultP({ x: 860, y: 1010, s: 1.4, expr: 'happy', look: 0.3, blush: true, bob: Math.abs(Math.sin(t * 3)) * -5 });
  ctx.save(); ctx.translate(p.hx + p.R * 0.95, p.hy + 10); ctx.rotate(0.3); rr(-30, -70, 60, 140, 12); fs('#1c1c22', 6); ctx.restore();
  hand(p.hx + p.R * 1.15, p.hy + 80, 1.2, -1.2, C.skin);
  rr(1180, 220, 330, 100, 24); fs('rgba(0,0,0,0.6)'); textC('Mom ❤  ' + String(Math.floor(t / 60 + 24)).padStart(2, '0') + ':' + String(Math.floor(t + 10) % 60).padStart(2, '0'), 1345, 270, 34, '#9fe0b8');
};

// ---------------- Act 6: ten years later ----------------
S.tenYears = (t, d) => {
  PEOPLE = []; streetNight(t, { magic: prog(t, d * 0.3, d), rainA: 0 });
  fireflies(t, 20 + Math.floor(prog(t, d * 0.3, d) * 30), LAMP - 200, 450, 600, 450, 'rgba(255,215,140,', 12);
  // present Zero (now the one with a calm, proud face) and the older self appears in the light
  adultP({ x: 640, y: 1000, s: 1.2, expr: t > d * 0.6 ? 'happy' : 'calm', look: 0.8 });
  const a = prog(t, d * 0.35, d * 0.7);
  ctx.save(); ctx.globalAlpha = a;
  const o = person({ x: LAMP + 97, y: 1000, s: 1.25, top: '#b85a26', expr: 'happy', look: -0.7 });
  for (const sd of [-1, 1]) { ctx.beginPath(); ctx.ellipse(o.hx + sd * o.R * 0.93, o.hy - o.R * 0.05, o.R * 0.17, o.R * 0.3, 0, 0, 7); fs('#c4c4c4', 6); }
  ctx.restore();
  if (a > 0.9) hand(LAMP - 40, 820 + Math.sin(t * 3) * 6, 1.1, -0.3, C.skin);
};

Object.assign(LOOK, { title6: { noVig: 1 } });
