// Video #4 "Nobody Is Coming To Save You." — loaded after scene.html + 02-twenties/render/scenes20.js
const BRICK = '#7a3a2a';
function darkRoom(bulb = true, f = 0) {
  ctx.fillStyle = vgrad(0, H, ['#121014', '#08070a']); ctx.fillRect(0, 0, W, H);
  ctx.fillStyle = '#0d0b0c'; ctx.fillRect(0, 960, W, 120);
  if (bulb) { const fl = (f % 97) > 92 ? 0.3 : 1; line([W / 2 - 200, 0, W / 2 - 200, 200], 4, '#222'); circle(W / 2 - 200, 220, 26); fs(`rgba(255,220,150,${fl})`, 5); glow(W / 2 - 200, 260, 700, `rgba(255,190,110,${0.35 * fl})`); }
}
// seated on the floor, hugging knees
function seated(o) {
  const p = person(Object.assign({ y: 1000, s: 1.3, expr: 'sad', noBand: true }, o));
  const s = o.s || 1.3, x = o.x;
  for (const sd of [-1, 1]) { rr(x + sd * 70 * s - 55 * s, 1000 - 150 * s, 110 * s, 160 * s, 50 * s); fs('#3a3d48', 7 * s); }
  hand(x - 40 * s, 1000 - 130 * s, s * 0.9, 0.3, C.skin); hand(x + 40 * s, 1000 - 130 * s, s * 0.9, -0.3 + Math.PI, C.skin);
  return p;
}
function bills() {
  for (const [x, y, r] of [[560, 1010, 0.2], [700, 1035, -0.3], [1320, 1020, 0.1], [1450, 1040, -0.15]]) {
    ctx.save(); ctx.translate(x, y); ctx.rotate(r); rr(-70, -40, 140, 80, 4); fs('#e8e2d6', 4);
    ctx.save(); ctx.rotate(-0.2); rr(-55, -16, 110, 32, 4); fs(null, 4, '#c0392b'); textC('PAST DUE', 0, 0, 18, '#c0392b'); ctx.restore(); ctx.restore();
  }
}
function door(x, open = 0, light = 0.6) {
  const w = 320, h = 640, y = 960 - h;
  glow(x + w / 2, 960, 260, `rgba(255,220,160,${light})`);
  ctx.fillStyle = `rgba(255,225,170,${0.6 * light + 0.4 * open})`; ctx.fillRect(x, 950, w, 10);
  rr(x - 14, y - 14, w + 28, h + 14, 4); fs('#1a1412', 8);
  if (open > 0) { ctx.fillStyle = '#fff1d0'; ctx.fillRect(x, y, w, h); glow(x + w / 2, y + h / 2, 400 + open * 1200, 'rgba(255,235,190,0.9)', open); }
  const dw = w * (1 - open * 0.85);
  ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + dw, y + open * 40); ctx.lineTo(x + dw, y + h - open * 40); ctx.lineTo(x, y + h); ctx.closePath(); fs('#4a3226', 8);
  circle(x + dw - 40, y + h / 2, 14); fs('#c9a14a', 4);
}
function chat(name, avatarCol, msgs, t) {
  ctx.fillStyle = '#06070b'; ctx.fillRect(0, 0, W, H);
  glow(W / 2, H / 2, 650, 'rgba(100,140,255,0.3)');
  ctx.save(); ctx.translate(W / 2, H / 2 + 20); phone(0, 0, 2.0, '#0f1a2c');
  rr(-210, -420, 420, 90, 0); fs('#16243a'); circle(-150, -375, 30); fs(avatarCol); textC(name, -100, -375, 38, '#fff', 'bold', 'left');
  msgs.forEach(([who, txt, at, extra], i) => {
    if (t < at) return; const y = -270 + i * 120, me = who === 'me';
    ctx.font = 'normal 24px "DejaVu Sans"'; const w = Math.min(390, ctx.measureText(txt).width + 50);
    rr(me ? 190 - w : -190, y, w, 76, 24); fs(me ? '#3c7cf0' : '#22324d');
    textC(txt, me ? 190 - w + 25 : -165, y + 38, 24, '#fff', 'normal', 'left');
    if (extra && t > at + 1.5) textC(extra, me ? 180 : -180, y + 100, 20, '#8899aa', 'normal', me ? 'right' : 'left');
  });
  ctx.restore();
}
function brick(x, y, w, h, word, col = BRICK) {
  rr(x, y, w, h, 4); fs(col, 5, '#2a120c');
  if (word) textC(word, x + w / 2, y + h / 2 + 2, Math.min(26, w / word.length * 1.5), '#f3e1c8');
}

S.floor = (t, d, f) => { darkRoom(true, f); bills(); seated({ x: W / 2, expr: t > d / 2 ? 'cry' : 'sad', tear: prog(t, d / 2, d) }); };
S.doorWait = (t, d, f) => {
  darkRoom(false, f); door(1300, 0, 0.5 + 0.1 * Math.sin(t));
  rr(300, 220, 160, 160, 80); fs('#1a1a1e', 6); line([380, 300, 380, 245], 6, '#bbb'); line([380, 300, 380 + Math.cos(t) * 50, 300 + Math.sin(t) * 50], 5, '#bbb');
  seated({ x: 760, expr: 'calm', look: 0.9 });
};
S.title4 = (t, d) => {
  ctx.fillStyle = '#050403'; ctx.fillRect(0, 0, W, H);
  const a = prog(t, 0.4, 1.6) * (1 - prog(t, d - 1, d));
  glow(W / 2, H / 2, 700, 'rgba(255,140,50,0.3)', a);
  ctx.globalAlpha = a; textC('NOBODY IS COMING', W / 2, H / 2 - 70, 120, '#f3e9da'); textC('TO SAVE YOU.', W / 2, H / 2 + 70, 120, '#ff8a3c');
  ctx.globalAlpha = a * 0.6; textC('an animated short film', W / 2, H / 2 + 200, 36, '#d9a070', 'normal'); ctx.globalAlpha = 1;
};
S.hopeFriend = (t) => chat('Max', '#5a9a4a', [['me', 'bro, I need help', 0.8], ['them', 'sorry man, busy today', 3.5], ['them', 'maybe next week', 5.0]], t);
S.hopeGirl = (t) => chat('Anna', '#d98aa6', [['me', 'can we talk?', 0.8, 'Seen 2:14 AM']], t);
S.hopeLuck = (t, d) => {
  ctx.fillStyle = '#0a0806'; ctx.fillRect(0, 0, W, H); glow(W / 2, H / 2, 600, 'rgba(255,190,90,0.35)');
  ctx.save(); ctx.translate(W / 2, H / 2); ctx.rotate(-0.04);
  rr(-420, -230, 840, 460, 20); fs('#f0d36a', 8); textC('LUCKY 7', 0, -160, 60, '#b8452e');
  for (let i = 0; i < 3; i++) {
    const x = -260 + i * 260; rr(x - 110, -70, 220, 220, 14); fs('#fff6dc', 6);
    textC(i === 2 ? '✕' : '7', x, 40, 140, i === 2 ? '#888' : '#b8452e');
    const k = prog(t, 1 + i * 1.6, 2.2 + i * 1.6); rr(x - 110, -70, 220, 220 * (1 - k), 14); fs('#a9a9a9', 0);
  }
  if (t > 6.2) { ctx.globalAlpha = prog(t, 6.2, 6.8); textC('TRY AGAIN', 0, 195, 50, '#333'); ctx.globalAlpha = 1; }
  ctx.restore();
  const i = Math.min(2, Math.floor(Math.max(0, t - 1) / 1.6)); hand(W / 2 - 260 + i * 260 + Math.sin(t * 20) * 40, H / 2 + 60, 1.5, -0.4, C.skin);
};
S.hopeMoment = (t, d) => {
  ctx.fillStyle = vgrad(0, H, ['#1c1a18', '#0e0d0c']); ctx.fillRect(0, 0, W, H); glow(W / 2, 450, 600, 'rgba(255,170,90,0.2)');
  const i = Math.floor(t / 0.7), k = (t / 0.7) % 1;
  rr(W / 2 - 300, 180, 600, 640, 16); fs('#efe7da', 8); rr(W / 2 - 300, 180, 600, 130, 16); fs('#b8452e', 8);
  textC(['JANUARY', 'MARCH', 'MAY', 'JULY', 'SEPTEMBER', 'NOVEMBER'][Math.floor(i / 2) % 6], W / 2, 245, 50, '#fff');
  textC('MONDAY', W / 2, 460, 80, '#555'); textC(['"I\'ll start"', '"Next one"', '"For real"', '"This time"'][i % 4], W / 2, 640, 56, '#b8452e');
  if (k < 0.3) { ctx.save(); ctx.globalAlpha = 1 - k / 0.3; ctx.translate(W / 2, 310); ctx.scale(1, 1 - k / 0.3); rr(-300, 0, 600, 510, 10); fs('#f7f1e6', 6); ctx.restore(); }
};
const EXCUSES = ['NO MONEY', 'NO TIME', 'BAD LUCK', 'MY PARENTS', 'TOO LATE', 'NOT TALENTED', 'TOO TIRED', 'NO HELP', 'TOO HARD', 'MAYBE LATER'];
function brickWall(n, x0, y0, cols, bw, bh) {
  for (let i = 0; i < n; i++) {
    const row = Math.floor(i / cols), col = i % cols, off = row % 2 ? bw / 2 : 0;
    brick(x0 + col * bw + off - (row % 2 ? bw / 2 : 0), y0 - row * bh, bw - 6, bh - 6, (i * 7) % 3 === 0 ? EXCUSES[(i * 3) % EXCUSES.length] : '');
  }
}
S.excuses = (t, d, f) => {
  darkRoom(true, f);
  seated({ x: W / 2, y: 1000, expr: 'tired', look: 0 });
  const n = Math.floor(prog(t, 1.0, d - 1.0) * 44);
  brickWall(n, 420, 900, 8, 135, 70);
};
S.walled = (t, d) => {
  ctx.fillStyle = '#060506'; ctx.fillRect(0, 0, W, H);
  for (let r = 0; r < 16; r++) for (let c = -1; c < 16; c++) { const x = c * 135 + (r % 2 ? 67 : 0), y = H - (r + 1) * 70; if (x > 620 && x < 1180 && y > 120) continue; brick(x, y, 129, 64, (r * 5 + c * 3) % 11 === 0 ? EXCUSES[(r + c + 20) % EXCUSES.length] : '', '#4a2219'); }
  ctx.save(); ctx.globalAlpha = 0.18; ctx.fillStyle = '#ffe8c0'; ctx.beginPath(); ctx.moveTo(760, 0); ctx.lineTo(1060, 0); ctx.lineTo(1160, H); ctx.lineTo(680, H); ctx.fill(); ctx.restore();
  seated({ x: W / 2, y: 1000, s: 1.0, expr: 'sad', look: -0.2 });
};
S.daysPass = (t, d, f) => {
  darkRoom(false, f); door(1300, 0, 0.45);
  const i = Math.floor(t / 1.0);
  rr(260, 200, 260, 290, 10); fs('#efe7da', 6); rr(260, 200, 260, 70, 10); fs('#b8452e', 6); textC('DAY', 390, 235, 36, '#fff'); textC(String(1 + i * 3), 390, 380, 120, '#222');
  seated({ x: 760, expr: t > d / 2 ? 'sad' : 'tired', look: t > d / 2 ? 0 : 0.9 });
  dust(t, Math.floor(prog(t, 0, d) * 40));
};
S.mirror4 = (t, d) => {
  ctx.fillStyle = vgrad(0, H, ['#1a1d22', '#0c0d10']); ctx.fillRect(0, 0, W, H);
  rr(1000, 140, 700, 760, 20); fs('#4a4f58', 12);
  ctx.save(); ctx.beginPath(); ctx.roundRect(1012, 152, 676, 736, 14); ctx.clip(); ctx.fillStyle = '#2a2622'; ctx.fillRect(1000, 140, 700, 760);
  glow(1350, 400, 500, 'rgba(255,180,100,0.35)', prog(t, 2, 5));
  person({ x: 1350, y: 1060, s: 1.5, expr: t > 3 ? 'determined' : 'sad', look: -0.5, noBand: true }); ctx.restore();
  glow(1350, 120, 520, 'rgba(255,220,170,0.3)');
  person({ x: 620, y: 1080, s: 1.65, expr: t > 8 ? 'determined' : t > 4 ? 'shock' : 'sad', look: 0.6, noBand: true });
};
S.brickBreak = (t, d) => {
  ctx.fillStyle = '#060506'; ctx.fillRect(0, 0, W, H);
  const out = prog(t, 2.5, 3.2), more = prog(t, 5, d - 1);
  for (let r = 0; r < 16; r++) for (let c = -1; c < 16; c++) {
    const x = c * 135 + (r % 2 ? 67 : 0), y = H - (r + 1) * 70, dc = Math.hypot(x + 65 - 1000, y + 32 - 470);
    if (dc < 60 && out > 0) continue; if (dc < 60 + more * 380) continue;
    brick(x, y, 129, 64, '', '#4a2219');
  }
  if (out > 0) { const rad = 70 + more * 380; glow(1000, 470, rad * 3, 'rgba(255,230,180,0.9)', out); ctx.save(); ctx.globalAlpha = 0.2 * out; ctx.fillStyle = '#ffe8c0'; ctx.beginPath(); ctx.moveTo(1000 - rad * 0.6, 470); ctx.lineTo(1000 + rad * 0.6, 470); ctx.lineTo(1500, H); ctx.lineTo(300, H); ctx.fill(); ctx.restore(); }
  const p = person({ x: 760, y: 1080, s: 1.5, expr: out > 0 ? 'determined' : 'angry', look: 0.7, lean: 0.15, noBand: true });
  hand(lerp(880, 960, prog(t, 1.5, 2.6)), 520, 1.4, -0.2, C.skin);
};
S.fall = (t, d) => {
  ctx.fillStyle = vgrad(0, H, ['#3a3040', '#6a4a40']); ctx.fillRect(0, 0, W, H);
  ctx.fillStyle = '#2a2026'; ctx.fillRect(0, 940, W, 140);
  rr(1100, 920, 60, 30, 6); fs('#555', 5);
  const trip = t > 3.4, k = prog(t, 3.4, 4.0), walk = t < 3.4 ? t * 120 : 3.4 * 120;
  ctx.save(); ctx.translate(700 + walk + k * 120, 960); ctx.rotate(k * 1.35);
  person({ x: 0, y: 0, s: 1.3, expr: trip ? (t > 5 ? 'cry' : 'shock') : 'determined', look: 0.8, bob: trip ? 0 : Math.abs(Math.sin(t * 7)) * -12, tear: prog(t, 5, 8), noBand: true });
  ctx.restore();
};
S.bandage = (t, d) => {
  ctx.fillStyle = vgrad(0, H, ['#2a2220', '#141010']); ctx.fillRect(0, 0, W, H);
  glow(W / 2, 450, 700, 'rgba(255,180,100,0.35)', prog(t, 3, 7));
  const on = t > 5.2;
  const p = person({ x: W / 2, y: 1150, s: 2.1, expr: on ? 'determined' : 'sad', noBand: !on, tear: 0.5 });
  const k = prog(t, 2.0, 5.0), tx = p.hx + p.R * 0.5, ty = p.hy + p.R * 0.22;
  if (!on) {
    const bx = lerp(W / 2 + 350, tx, k), by = lerp(1000, ty, k);
    ctx.save(); ctx.translate(bx, by); ctx.rotate(-0.45); rr(-p.R * 0.17, -p.R * 0.065, p.R * 0.34, p.R * 0.13, p.R * 0.05); fs('#e6c9a0', 6); ctx.restore();
    hand(bx + 30, by + 40, 1.6, -0.8, C.skin);
  } else hand(lerp(tx + 30, W / 2 + 500, prog(t, 5.6, 6.6)), lerp(ty + 40, 1100, prog(t, 5.6, 6.6)), 1.6, -0.8, C.skin);
};
S.climb = (t, d) => {
  ctx.fillStyle = vgrad(0, H, ['#3a2a3a', '#a0584a', '#e0905a']); ctx.fillRect(0, 0, W, H);
  glow(1750, 80, 700, 'rgba(255,220,160,0.8)');
  for (let i = 0; i < 9; i++) for (let j = 0; j <= i; j++) brick(200 + i * 190, 1000 - j * 80, 184, 74, '', '#7a3a2a');
  const k = prog(t, 0.3, d - 0.5) * 6, step = Math.floor(k), sub = k - step;
  const x = 292 + (step + ease(clamp(sub * 1.5))) * 190, y = 1000 - (step + ease(clamp(sub * 1.5))) * 80;
  person({ x, y, s: 1.0, expr: 'determined', look: 0.8 });
};
S.help = (t, d) => {
  ctx.fillStyle = vgrad(0, H, ['#2a2622', '#16130f']); ctx.fillRect(0, 0, W, H);
  glow(W / 2, 400, 700, 'rgba(255,180,100,0.35)');
  ctx.fillStyle = '#100c0a'; ctx.fillRect(0, 980, W, 100);
  person({ x: 1280, y: 1010, s: 1.4, top: '#3d8bd0', expr: 'calm', look: -0.8 });
  const up = prog(t, 4.0, 7.0);
  if (up < 0.01) seated({ x: 700, expr: 'sad', look: 0.8, s: 1.3 }); else person({ x: 700, y: lerp(1150, 1010, up), s: 1.4, expr: 'determined', look: 0.8 });
  hand(lerp(1120, 1070, prog(t, 0.5, 2)), 760, 1.2, 0.3, C.skin);
};
S.doorOpen = (t, d, f) => {
  darkRoom(false, f);
  const open = prog(t, 4.0, 7.5);
  door(1050, open, 0.6);
  const walk = prog(t, 0.5, 3.5);
  person({ x: lerp(500, 880, walk), y: 1000, s: 1.4, expr: 'determined', look: 0.9, bob: walk > 0 && walk < 1 ? Math.abs(Math.sin(t * 7)) * -10 : 0 });
  if (t > 3.2 && t < 5) hand(1010, 640, 1.2, -0.2, C.skin);
  if (open > 0.6) { ctx.fillStyle = `rgba(255,240,210,${(open - 0.6) * 1.2})`; ctx.fillRect(0, 0, W, H); }
};

Object.assign(LOOK, { hopeFriend: { noVig: 0 } });
Object.assign(ZOOM, { floor: [1.0, 1.08], doorWait: [1.0, 1.06], hopeFriend: [1.0, 1.05], hopeGirl: [1.0, 1.08], hopeLuck: [1.0, 1.05],
  excuses: [1.0, 1.05], walled: [1.12, 1.0], daysPass: [1.0, 1.06], mirror4: [1.0, 1.08], brickBreak: [1.0, 1.06], bandage: [1.0, 1.06],
  help: [1.0, 1.04], doorOpen: [1.0, 1.06] });
