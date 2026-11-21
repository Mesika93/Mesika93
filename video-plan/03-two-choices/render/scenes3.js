// Video #3 "Same Day. Two Choices." — split-screen scenes.
// Loaded after scene.html + 02-twenties/render/scenes20.js (reuses alarm, wakeup, run, read, mirror helpers).
const DULL = '#8a5a3e';   // A's hoodie slowly loses colour

// Draw a full-width scene into one half of the screen (shows the centre 960px of it).
function half(side, fn, t, d, f) {
  ctx.save();
  ctx.beginPath(); ctx.rect(side === 'L' ? 0 : W / 2, 0, W / 2, H); ctx.clip();
  ctx.translate(side === 'L' ? -W / 4 : W / 4, 0);
  fn(t, d, f);
  ctx.restore();
  ctx.save(); ctx.beginPath(); ctx.rect(side === 'L' ? 0 : W / 2, 0, W / 2, H); ctx.clip();
  if (side === 'L') { ctx.globalCompositeOperation = 'saturation'; ctx.globalAlpha = 0.45; ctx.fillStyle = '#808080'; ctx.fillRect(0, 0, W, H);
    ctx.globalCompositeOperation = 'multiply'; ctx.globalAlpha = 0.25; ctx.fillStyle = '#20263a'; ctx.fillRect(0, 0, W, H); }
  else { ctx.globalCompositeOperation = 'soft-light'; ctx.globalAlpha = 0.25; ctx.fillStyle = '#ffb060'; ctx.fillRect(0, 0, W, H); }
  ctx.restore();
}
function split(fa, fb, label) {
  return (t, d, f) => {
    half('L', fa, t, d, f); half('R', fb, t, d, f);
    line([W / 2, 0, W / 2, H], 8, '#000'); line([W / 2, 0, W / 2, H], 2, 'rgba(255,200,140,0.5)');
    if (label) { rr(W / 2 - 150, 36, 300, 74, 37); fs('rgba(0,0,0,0.75)', 4, 'rgba(255,200,140,0.6)'); textC(label, W / 2, 74, 40, '#f3e9da'); }
  };
}

// ---------- single-side scenes (full-width coordinates, subject at x = W/2) ----------
function room(dark) {
  ctx.fillStyle = dark ? vgrad(0, H, ['#14151b', '#0a0a0e']) : vgrad(0, H, ['#3a2e26', '#251c16']); ctx.fillRect(0, 0, W, H);
  ctx.fillStyle = dark ? '#0c0c10' : '#1d1510'; ctx.fillRect(0, 980, W, 100);
}
function couch(col = '#3a3f55') { rr(560, 760, 800, 260, 50); fs(col, 8); rr(520, 660, 880, 140, 50); fs(shade(col, 0.1), 8); }
function tvGlow(f) { glow(1500, 500, 700, `rgba(80,130,255,${0.35 + 0.08 * Math.sin(f * 0.8)})`); }
const A = (o = {}) => Object.assign({ x: W / 2, y: 1010, s: 1.4, top: DULL }, o);
const B = (o = {}) => Object.assign({ x: W / 2, y: 1010, s: 1.4 }, o);

S.foodA = (t, d, f) => {
  room(true); tvGlow(f); couch();
  person(A({ y: 900, expr: 'tired', look: 0.8 }));
  ctx.save(); ctx.translate(1080, 760 + Math.sin(t * 2) * 30); ctx.rotate(-0.4);
  ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(90, -40); ctx.lineTo(90, 40); ctx.closePath(); fs('#f0b84a', 6); circle(55, -8, 9); fs('#c0392b'); circle(70, 15, 8); fs('#c0392b'); ctx.restore();
  hand(1060, 780 + Math.sin(t * 2) * 30, 1.1, 0, C.skin);
  rr(700, 930, 260, 40, 6); fs('#c9a06a', 6); textC('PIZZA', 830, 950, 24, '#7a3a1a');
  for (const x of [1150, 1210]) { rr(x, 900, 40, 70, 8); fs('#b83a3a', 5); }
};
S.foodB = (t, d, f) => {
  room(false); glow(W / 2, 400, 800, 'rgba(255,200,120,0.4)');
  rr(1150, 120, 420, 300, 8); fs('#ffe8b5', 10);
  person(B({ y: 880, expr: 'calm', look: 0.5 }));
  rr(400, 860, 1120, 220, 0); fs('#6a4a30', 7);
  rr(1060, 800, 220, 40, 10); fs('#333', 6); line([1280, 820, 1400, 800], 14, '#222');
  for (let i = 0; i < 3; i++) { const y = 780 - ((t * 45 + i * 40) % 120); ctx.globalAlpha = 0.5; line([1110 + i * 50, y, 1120 + i * 50 + Math.sin(t * 3 + i) * 10, y - 40], 6, '#eee'); ctx.globalAlpha = 1; }
  ctx.beginPath(); ctx.ellipse(700, 830, 110, 40, 0, 0, Math.PI); fs('#f2ede2', 6);
  for (const [x, c] of [[650, '#5aa83c'], [700, '#e0503a'], [745, '#7cc04a'], [680, '#f0c040']]) { circle(x, 815, 22); fs(c, 4); }
  hand(1150, 790, 1.1, -0.4, C.skin);
};
S.moneyA = (t, d, f) => {
  room(true); glow(W / 2, 600, 600, 'rgba(110,150,255,0.35)');
  person(A({ expr: t > d * 0.7 ? 'shock' : 'calm' }));
  ctx.save(); ctx.translate(W / 2, 860); phone(0, 0, 0.7, '#13223a'); rr(-60, -60, 120, 50, 10); fs('#f0a030'); textC('BUY NOW', 0, -35, 20, '#222'); ctx.restore();
  const n = Math.floor(prog(t, 0.5, d - 1) * 7);
  for (let i = 0; i < n; i++) { const x = 640 + (i % 4) * 75 + (i > 3 ? 560 : 0), y = 950 - Math.floor(i / 4) * 60 - (i > 3 ? 0 : 0); rr(x - 35, y - 30, 70, 60, 4); fs('#b98a55', 5); line([x - 35, y, x + 35, y], 3, '#8a6035'); }
  textC('-$' + (39 * n + (n ? 20 : 0)), 1250, 260, 80, '#ff5a4a');
};
S.moneyB = (t, d, f) => {
  room(false); glow(W / 2, 450, 700, 'rgba(255,200,120,0.4)');
  rr(1130, 170, 300, 220, 8); fs('#f2ead8', 6); line([1160, 360, 1220, 320, 1280, 330, 1340, 260, 1400, 200], 8, '#3aa05a');
  person(B({ expr: 'happy', look: 0.3 }));
  const k = prog(t, 0.5, d - 1);
  ctx.save(); ctx.translate(1180, 900);
  ctx.beginPath(); ctx.moveTo(-80, -160); ctx.lineTo(80, -160); ctx.lineTo(95, 60); ctx.quadraticCurveTo(0, 90, -95, 60); ctx.closePath(); fs('rgba(200,230,255,0.25)', 6);
  ctx.save(); ctx.beginPath(); ctx.moveTo(-80, -160); ctx.lineTo(80, -160); ctx.lineTo(95, 60); ctx.quadraticCurveTo(0, 90, -95, 60); ctx.closePath(); ctx.clip();
  ctx.fillStyle = '#e8b830'; ctx.fillRect(-100, 70 - k * 200, 200, 300); ctx.restore();
  const cy = ((t * 1.4) % 1) * 240 - 300; circle(0, cy, 24); fs('#f5cf4a', 5);
  ctx.restore();
  hand(1180, 620, 1.1, -0.2, C.skin);
  textC('+$' + Math.round(k * 300), 760, 260, 80, '#5ad07a');
};
S.socialA = (t, d, f) => {
  room(true); tvGlow(f); couch();
  person(A({ y: 900, expr: 'tired', look: -0.8 }));
  const buzz = t < 6 && Math.sin(t * 5) > 0;
  ctx.save(); ctx.translate(1150 + (buzz ? Math.sin(t * 90) * 4 : 0), 940); ctx.rotate(-0.1);
  if (t < 5) { rr(-60, -100, 120, 200, 16); fs('#1c1c22', 6); rr(-50, -88, 100, 176, 10); fs('#13223a'); textC('Mom ❤', 0, -30, 22, '#fff'); circle(-25, 50, 16); fs('#e04848'); circle(25, 50, 16); fs('#38c66a'); }
  else { rr(-60, -100, 120, 200, 16); fs('#111', 6); }
  ctx.restore();
};
S.socialB = (t, d, f) => {
  room(false); glow(W / 2, 450, 700, 'rgba(255,190,110,0.45)');
  const p = person(B({ expr: 'happy', look: 0.3, blush: true, bob: Math.abs(Math.sin(t * 3)) * -5 }));
  ctx.save(); ctx.translate(p.hx + p.R * 0.95, p.hy + 10); ctx.rotate(0.3); rr(-30, -70, 60, 140, 12); fs('#1c1c22', 6); ctx.restore();
  hand(p.hx + p.R * 1.15, p.hy + 80, 1.2, -1.2, C.skin);
  rr(1100, 180, 260, 90, 20); fs('rgba(0,0,0,0.6)'); textC('Mom ❤  ' + Math.floor(t / 60 + 12) + ':' + String(Math.floor(t + 4) % 60).padStart(2, '0'), 1230, 225, 30, '#9fe0b8');
};
S.excuseA = (t, d, f) => {
  room(true); couch('#33384a');
  rr(1150, 250, 220, 150, 4); fs('#8a8577', 5); textC('GYM', 1260, 325, 44, '#555');
  person(A({ y: 900, expr: 'tired', look: 0.2 }));
  const a = prog(t, 0.8, 1.6);
  ctx.globalAlpha = a; for (const [x, y, r] of [[1110, 520, 14], [1150, 470, 22]]) { circle(x, y, r); fs('#fff', 4); }
  ctx.beginPath(); ctx.ellipse(1300, 380, 190, 100, 0, 0, 7); fs('#fff', 6); textC('MONDAY.', 1300, 382, 52, '#333'); ctx.globalAlpha = 1;
};
S.excuseB = (t, d, f) => {
  room(false); glow(W / 2, 400, 700, 'rgba(255,190,110,0.4)');
  person(B({ y: 900, expr: 'determined', look: 0.6 }));
  rr(400, 880, 1120, 200, 0); fs('#6a4a30', 7);
  rr(1060, 180, 380, 420, 10); fs('#f2ead8', 7); textC('TODAY', 1250, 235, 42, '#333');
  ['Workout', 'Read 10 pages', 'Work on project'].forEach((s, i) => {
    const y = 320 + i * 95; rr(1090, y - 25, 50, 50, 8); fs('#fff', 5);
    textC(s, 1160, y, 30, '#333', 'normal', 'left');
    if (t > 2 + i * 2) { line([1095, y, 1112, y + 18, 1150, y - 30], 9, '#3aa05a'); line([1160, y, 1160 + 30 * s.length * 0.55 * prog(t, 2.2 + i * 2, 2.8 + i * 2), y], 4, '#555'); }
  });
  hand(1050, 700, 1.1, -0.6, C.skin);
};
S.nightA = (t, d, f) => { S.scroll(t, d, f); rr(560, 140, 230, 90, 12); fs('rgba(0,0,0,0.7)'); textC('3:12 AM', 675, 185, 46, '#ff5a4a'); };
S.nightB = (t, d, f) => {
  bedroom();
  ctx.beginPath(); ctx.ellipse(W / 2, 700, 260, 80, 0, 0, 7); fs('#e8e4da', 7);
  const p = person({ x: W / 2, y: 960, s: 1.3, expr: 'calm', hood: false });
  ctx.beginPath(); ctx.moveTo(400, 820); ctx.quadraticCurveTo(W / 2, 760, 1520, 820); ctx.lineTo(1520, 1080); ctx.lineTo(400, 1080); ctx.closePath(); fs('#e0823f', 8);
  for (let i = 0; i < 3; i++) { const k = (t * 0.4 + i / 3) % 1; ctx.globalAlpha = Math.sin(k * Math.PI); textC('z', p.hx + 120 + k * 120, p.hy - 100 - k * 200, 40 + i * 14, '#9fb4d6'); ctx.globalAlpha = 1; }
  rr(1130, 140, 230, 90, 12); fs('rgba(0,0,0,0.7)'); textC('11:00 PM', 1245, 185, 44, '#9fe0b8');
};
function mirrorScene(expr, dark) {
  return (t, d) => {
    ctx.fillStyle = dark ? vgrad(0, H, ['#16181d', '#0b0c0f']) : vgrad(0, H, ['#2e2a26', '#1a1714']); ctx.fillRect(0, 0, W, H);
    rr(700, 120, 520, 700, 20); fs('#4a4f58', 12);
    ctx.save(); ctx.beginPath(); ctx.roundRect(712, 132, 496, 676, 14); ctx.clip(); ctx.fillStyle = dark ? '#1a1f26' : '#2c2a2a'; ctx.fillRect(700, 120, 520, 700);
    person({ x: W / 2, y: 1000, s: 1.3, expr, top: dark ? DULL : C.hoodie }); ctx.restore();
    glow(W / 2, 100, 500, dark ? 'rgba(180,200,255,0.25)' : 'rgba(255,210,150,0.45)');
  };
}
S.mirrorA = mirrorScene('sad', true);
S.mirrorB = mirrorScene('determined', false);
S.weekendA = (t, d, f) => {
  room(true); tvGlow(f); couch();
  rr(500, 100, 300, 500, 6); fs('#2a1f2a', 6); rr(800, 100, 300, 500, 6); fs('#2a1f2a', 6);
  person(A({ y: 900, expr: 'calm', look: 0.8 }));
  for (const [x, r] of [[700, 0.2], [760, -0.3], [1180, 0.1]]) { ctx.save(); ctx.translate(x, 950); ctx.rotate(r); rr(-25, -50, 50, 70, 8); fs('#b83a3a', 5); ctx.restore(); }
};
S.weekendB = (t, d) => {
  ctx.fillStyle = vgrad(0, H, ['#8ec6ff', '#ffe0a8']); ctx.fillRect(0, 0, W, H);
  glow(1300, 200, 500, 'rgba(255,240,200,0.9)');
  ctx.fillStyle = '#7a9a6a'; ctx.beginPath(); ctx.moveTo(300, 1080); ctx.lineTo(900, 380); ctx.lineTo(1500, 1080); ctx.fill();
  ctx.fillStyle = '#5a7a4a'; ctx.beginPath(); ctx.moveTo(800, 1080); ctx.lineTo(1300, 560); ctx.lineTo(1800, 1080); ctx.fill();
  const b = i => Math.abs(Math.sin(t * 3 + i)) * -8;
  person({ x: 700, y: 1060, s: 1.0, top: '#3d8bd0', expr: 'happy', look: 0.5, bob: b(0) });
  person({ x: W / 2, y: 1080, s: 1.15, expr: 'happy', bob: b(1) });
  person({ x: 1220, y: 1060, s: 1.0, top: '#5a9a4a', expr: 'happy', look: -0.5, bob: b(2) });
  hand(W / 2 + 150, 720 + Math.sin(t * 4) * 20, 1, -0.5, C.skin);
};

// ---------- status after N days: k = 0..1 how far each version has gone ----------
function statusSide(good, k, day) {
  return (t, d, f) => {
    if (good) { ctx.fillStyle = vgrad(0, H, ['#3a2e26', '#2a2019']); ctx.fillRect(0, 0, W, H); glow(W / 2, 450, 800, `rgba(255,190,110,${0.25 + 0.35 * k})`); }
    else { ctx.fillStyle = vgrad(0, H, ['#16171d', '#0b0b0f']); ctx.fillRect(0, 0, W, H); glow(W / 2, 500, 600, `rgba(80,120,255,${0.25})`); }
    ctx.fillStyle = good ? '#1d1510' : '#0c0c10'; ctx.fillRect(0, 980, W, 100);
    const r = rand(good ? 3 : 4);
    if (good) {
      const shelf = Math.floor(k * 8);
      rr(600, 420, 220, 12, 3); fs('#4a3221', 4);
      for (let i = 0; i < shelf; i++) { rr(610 + i * 25, 340, 20, 80, 3); fs(['#b8452e', '#3d6fb0', '#5a8a4a', '#d9a03a'][i % 4], 3); }
      for (let i = 0; i < Math.floor(k * 3); i++) { rr(1230 + i * 60, 900, 40, 80, 8); fs('#8a5a3a', 4); circle(1250 + i * 60, 870, 30 + k * 10); fs('#5aa83c', 5); }
      if (k > 0.6) { circle(1300, 380, 40); fs('#f5c542', 6); line([1280, 320, 1300, 345, 1320, 320], 8, '#c0392b'); }
      if (k > 0.3) { rr(560, 940, 120, 30, 10); fs('#444', 4); circle(560, 955, 26); fs('#222', 4); circle(680, 955, 26); fs('#222', 4); }
    } else {
      for (let i = 0; i < Math.floor(k * 9); i++) { const x = 560 + r() * 800, rot = r() - 0.5; ctx.save(); ctx.translate(x, 960); ctx.rotate(rot); rr(-20, -55, 40, 70, 8); fs(r() > 0.5 ? '#b83a3a' : '#2b9b5a', 4); ctx.restore(); }
      for (let i = 0; i < Math.floor(k * 4); i++) { rr(1150 - i * 6, 950 - i * 22, 200, 22, 3); fs('#c9a06a', 4); }
      dust(t, Math.floor(k * 30), 'rgba(160,160,170,0.3)');
    }
    const expr = good ? (k > 0.5 ? 'happy' : k > 0.1 ? 'determined' : 'calm') : (k > 0.5 ? 'sad' : k > 0.1 ? 'tired' : 'calm');
    const p = person({ x: W / 2, y: 1010 + (good ? 0 : k * 25), s: 1.45 + (good ? k * 0.12 : -k * 0.05), expr, top: good ? C.hoodie : DULL, lean: good ? 0 : k * 0.12 });
    if (!good && k > 0.3) for (const sd of [-1, 1]) { ctx.beginPath(); ctx.ellipse(p.hx + sd * p.R * 0.32, p.hy + p.R * 0.14, p.R * 0.13, p.R * 0.05, 0, 0, 7); fs('rgba(60,40,80,0.45)'); }
    // stat bars
    const stats = [['ENERGY', good ? 0.35 + 0.6 * k : 0.35 - 0.25 * k], ['SKILLS', good ? 0.2 + 0.75 * k : 0.2], ['MONEY', good ? 0.25 + 0.6 * k : 0.25 - 0.2 * k], ['CONFIDENCE', good ? 0.3 + 0.65 * k : 0.3 - 0.22 * k]];
    rr(540, 150, 360, 250, 16); fs('rgba(0,0,0,0.55)');
    stats.forEach(([n, v], i) => {
      const y = 190 + i * 55, a = prog(t, 0.5, 2.0);
      textC(n, 560, y, 22, '#ccc', 'bold', 'left');
      rr(720, y - 12, 160, 24, 12); fs('#333'); rr(720, y - 12, Math.max(14, 160 * v * a), 24, 12); fs(good ? '#ff8a3c' : '#6a7080');
    });
  };
}
function statusScene(day, kA, kB) { return split(statusSide(false, kA, day), statusSide(true, kB, day), 'DAY ' + day); }

S.sAlarm = split(S.alarm, (t, d, f) => S.wakeup(t + 3, d, f), '6:00 AM');
S.sPhone = split(S.scroll, S.run, '7:00 AM');
S.sFood = split(S.foodA, S.foodB, '1:00 PM');
S.sWork = split(S.gaming, S.read, '4:00 PM');
S.sMoney = split(S.moneyA, S.moneyB, '6:00 PM');
S.sSocial = split(S.socialA, S.socialB, '8:00 PM');
S.sExcuse = split(S.excuseA, S.excuseB, '9:00 PM');
S.sNight = split(S.nightA, S.nightB, 'NIGHT');
S.sMirror = split(S.mirrorA, S.mirrorB, '');
S.sWeekend = split(S.weekendA, S.weekendB, 'SATURDAY');
S.day1 = statusScene(1, 0.0, 0.0);
S.day30 = statusScene(30, 0.25, 0.3);
S.day100 = statusScene(100, 0.5, 0.55);
S.day180 = statusScene(180, 0.75, 0.8);
S.day365 = statusScene(365, 1.0, 1.0);

S.meet = (t, d, f) => {
  ctx.fillStyle = '#08070a'; ctx.fillRect(0, 0, W, H);
  glow(1300, 520, 700, 'rgba(255,170,80,0.55)'); glow(600, 560, 500, 'rgba(90,110,160,0.3)');
  ctx.fillStyle = '#100c0a'; ctx.fillRect(0, 980, W, 100);
  const lift = prog(t, d - 6, d - 2);
  person({ x: 620, y: 1020, s: 1.5, top: DULL, expr: t < 4 ? 'shock' : lift > 0.5 ? 'determined' : 'sad', look: 0.8, lean: 0.12 * (1 - lift) });
  person({ x: 1300, y: 1020, s: 1.6, expr: lift > 0.5 ? 'happy' : 'calm', look: -0.8 });
  const reach = prog(t, d - 9, d - 6);
  hand(lerp(1150, 1000, reach), lerp(800, 700, reach), 1.3, 0.2, C.skin);
  if (lift > 0) hand(lerp(760, 900, lift), lerp(820, 710, lift), 1.3, Math.PI - 0.2, C.skin);
};
S.finalwake = (t, d) => {
  const light = prog(t, 4, 8);
  ctx.fillStyle = vgrad(0, H, [lerpCol('#1b2233', '#f4c38a', light), lerpCol('#0d111a', '#c88a5a', light)]); ctx.fillRect(0, 0, W, H);
  rr(1350, 120, 380, 330, 8); fs(light > 0.3 ? '#fff4d6' : '#3a4a66', 10); glow(1540, 280, 700, `rgba(255,230,180,${light * 0.8})`);
  ctx.beginPath(); ctx.ellipse(760, 640, 260, 90, -0.05, 0, 7); fs('#e8e4da', 7);
  const up = prog(t, 3.2, 4.2);
  person({ x: 820, y: lerp(900, 830, up), s: 1.3, expr: up > 0.5 ? 'determined' : 'tired', look: 0.5, hood: false });
  ctx.beginPath(); ctx.moveTo(150, 760); ctx.quadraticCurveTo(900, 640, 1500, 760); ctx.lineTo(1500, 1080); ctx.lineTo(150, 1080); ctx.closePath(); fs('#3f4f7a', 8);
  rr(1500, 780, 300, 300, 10); fs('#4a3221', 7);
  const ring = t > 0.5 && t < 2.6, off = t >= 2.6;
  ctx.save(); ctx.translate(1650 + (ring ? Math.sin(t * 80) * 6 : 0), 700); rr(-110, -70, 220, 140, 30); fs('#222', 7); textC(off ? 'OFF' : '6:00', 0, 0, off ? 50 : 64, off ? '#9fe0b8' : '#ff5a4a'); ctx.restore();
  const k = prog(t, 2.0, 2.6) * (1 - prog(t, 3.0, 3.8));
  hand(lerp(1200, 1630, k), lerp(820, 620, k), 1.5, -0.4, C.skin);
};
S.title3 = (t, d) => {
  ctx.fillStyle = '#050403'; ctx.fillRect(0, 0, W, H);
  const a = prog(t, 0.4, 1.6) * (1 - prog(t, d - 1, d));
  glow(W * 0.25, H / 2, 600, 'rgba(90,120,200,0.3)', a); glow(W * 0.75, H / 2, 600, 'rgba(255,140,50,0.35)', a);
  ctx.globalAlpha = a; textC('SAME DAY.', W / 2, H / 2 - 70, 130, '#f3e9da'); textC('TWO CHOICES.', W / 2, H / 2 + 70, 130, '#ff8a3c');
  ctx.globalAlpha = a * 0.6; textC('an animated short film', W / 2, H / 2 + 200, 36, '#d9a070', 'normal'); ctx.globalAlpha = 1;
};

// split scenes get their own grade inside half(); no global tint for them
for (const k of ['sAlarm', 'sPhone', 'sFood', 'sWork', 'sMoney', 'sSocial', 'sExcuse', 'sNight', 'sMirror', 'sWeekend', 'day1', 'day30', 'day100', 'day180', 'day365'])
  LOOK[k] = { noVig: 1 };
Object.assign(ZOOM, { meet: [1.0, 1.08], finalwake: [1.0, 1.05] });

// captions: allow left/right captions at the same time
function caption(time, sc) {
  const list = TL.captions.filter(c => time >= c.start && time < c.end);
  for (const c of list) {
    const a = Math.min(clamp((time - c.start) / 0.5), clamp((c.end - time) / 0.5));
    const center = c.scene === 'card', side = c.side;
    const size = center ? 92 : side ? 56 : 62;
    const lines = wrap(c.en, size, center ? 1500 : side ? 820 : 1600);
    const x = side === 'L' ? W / 4 : side === 'R' ? W * 0.75 : W / 2;
    ctx.save(); ctx.globalAlpha = a; ctx.shadowColor = 'rgba(0,0,0,0.9)'; ctx.shadowBlur = 24;
    const lh = size * 1.25, y0 = center ? H / 2 - (lines.length - 1) * lh / 2 : H - 120 - (lines.length - 1) * lh;
    lines.forEach((l, i) => textC(l, x, y0 + i * lh, size, center ? '#f3e9da' : '#fff', 'bold', 'center', center ? 0 : 9));
    ctx.restore();
  }
}
