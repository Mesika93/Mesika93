// Scenes for video #2 "Don't Waste Your 20s." — loaded on top of 01-parents/render/scene.html
const NOTES = ['LEARN GUITAR', 'TRAVEL', 'OWN BUSINESS', 'GET FIT', 'WRITE A BOOK', 'LEARN ENGLISH'];
function dreamWall(x0, y0, dusty, t) {
  NOTES.forEach((n, i) => {
    const x = x0 + (i % 3) * 210, y = y0 + Math.floor(i / 3) * 190, rot = ((i * 37) % 9 - 4) * 0.025;
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot + (dusty && i === 2 ? 0.5 : 0));
    rr(-85, -70, 170, 150, 4); fs(dusty ? '#8a8577' : ['#ffd76a', '#ff9f80', '#9fd6ff'][i % 3], 5);
    ctx.font = 'bold 22px "DejaVu Sans"'; const words = n.split(' ');
    words.forEach((w, k) => textC(w, 0, -10 + k * 30 - (words.length - 1) * 10, 22, dusty ? '#555' : '#333'));
    ctx.restore();
  });
  if (dusty) for (const [cx, cy] of [[x0 - 90, y0 - 75], [x0 + 510, y0 + 260]]) {
    for (let k = 0; k < 5; k++) line([cx, cy, cx + Math.cos(k * 0.35) * 120, cy + Math.sin(k * 0.35) * 120], 1.5, 'rgba(220,220,220,0.5)');
    for (let r = 30; r < 120; r += 25) { ctx.beginPath(); ctx.arc(cx, cy, r, 0, 1.4); fs(null, 1.5, 'rgba(220,220,220,0.4)'); }
  }
}
function guitarAt(x, y, s, dusty) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.rotate(-0.25);
  rr(-14, -330, 28, 260, 6); fs(dusty ? '#5a5048' : '#4a2e1c', 5);
  ctx.beginPath(); ctx.ellipse(0, -40, 75, 70, 0, 0, 7); fs(dusty ? '#8a7a66' : '#c4733a', 6);
  ctx.beginPath(); ctx.ellipse(0, 70, 100, 95, 0, 0, 7); fs(dusty ? '#8a7a66' : '#c4733a', 6);
  circle(0, 15, 28); fs('#1a1a1a', 4);
  ctx.restore();
}
function dust(t, n = 40, col = 'rgba(230,220,200,0.35)') {
  const r = rand(21);
  for (let i = 0; i < n; i++) { const x = (r() * W + t * 15 * (r() - 0.5)) % W, y = (r() * H + t * 10 * r()) % H; circle((x + W) % W, y, 2 + r() * 3); fs(col); }
}
function sweat(x, y, t) { for (let i = 0; i < 2; i++) { const k = (t * 1.3 + i * 0.5) % 1; ctx.globalAlpha = 1 - k; ctx.beginPath(); ctx.ellipse(x + i * 30, y + k * 60, 9, 14, 0, 0, 7); fs('#9fd0ff', 3); ctx.globalAlpha = 1; } }

S.mirror = (t, d, f) => {
  ctx.fillStyle = vgrad(0, H, ['#1a1d22', '#0c0d10']); ctx.fillRect(0, 0, W, H);
  const fl = t % 3 > 2.85 ? 0.4 : 1;
  rr(1000, 140, 700, 760, 20); fs('#4a4f58', 12);
  ctx.save(); ctx.beginPath(); ctx.roundRect(1012, 152, 676, 736, 14); ctx.clip();
  ctx.fillStyle = '#1d232b'; ctx.fillRect(1000, 140, 700, 760);
  person({ x: 1350, y: 1060, s: 1.5, expr: t > d * 0.55 ? 'sad' : 'tired', look: -0.5 });
  ctx.fillStyle = 'rgba(160,190,220,0.08)'; ctx.fillRect(1000, 140, 700, 760);
  line([1100, 200, 1250, 140], 6, 'rgba(255,255,255,0.12)');
  ctx.restore();
  glow(1350, 120, 520, `rgba(255,220,170,${0.35 * fl})`);
  person({ x: 620, y: 1080, s: 1.65, expr: t > d * 0.55 ? 'sad' : 'tired', look: 0.6 });
  textC('23:59', 300, 200, 54, '#c84a3a'); rr(200, 150, 200, 100, 10); fs(null, 5, '#333');
};
S.title = (t, d) => {
  ctx.fillStyle = '#050403'; ctx.fillRect(0, 0, W, H);
  const a = prog(t, 0.4, 1.6) * (1 - prog(t, d - 1, d));
  glow(W / 2, H / 2, 700, 'rgba(255,140,50,0.35)', a);
  ctx.globalAlpha = a; textC("DON'T WASTE", W / 2, H / 2 - 70, 130, '#f3e9da'); textC('YOUR 20s.', W / 2, H / 2 + 70, 130, '#ff8a3c');
  ctx.globalAlpha = a * 0.6; textC('an animated short film', W / 2, H / 2 + 200, 36, '#d9a070', 'normal'); ctx.globalAlpha = 1;
};
S.age20 = (t, d) => {
  ctx.fillStyle = vgrad(0, H, ['#3b2f2a', '#2a201b']); ctx.fillRect(0, 0, W, H);
  glow(900, 300, 900, 'rgba(255,190,110,0.45)');
  dreamWall(1150, 300, false, t);
  guitarAt(380, 800, 1.0, false);
  person({ x: 820, y: 1060, s: 1.5, expr: 'happy', look: 0.6, bob: Math.abs(Math.sin(t * 2)) * -6 });
  ctx.fillStyle = '#1e1612'; ctx.fillRect(0, 1000, W, 80);
};
S.alarm = (t, d) => {
  ctx.fillStyle = vgrad(0, H, ['#1b2233', '#0d111a']); ctx.fillRect(0, 0, W, H);
  rr(1350, 120, 380, 330, 8); fs('#3a4a66', 10); glow(1540, 280, 300, 'rgba(160,190,230,0.25)');
  rr(150, 160, 260, 120, 6); fs('#ffd76a', 5); textC('GYM 6:30', 280, 220, 34, '#333');
  // bed & pillow
  ctx.beginPath(); ctx.ellipse(760, 640, 260, 90, -0.05, 0, 7); fs('#e8e4da', 7);
  const ring = t > 0.8 && t < 3.2, hit = t > 3.2;
  const p = person({ x: 820, y: 900, s: 1.3, expr: hit ? 'calm' : 'tired', look: 0.5, hood: false });
  ctx.beginPath(); ctx.moveTo(150, 760); ctx.quadraticCurveTo(900, 640, 1500, 760); ctx.lineTo(1500, 1080); ctx.lineTo(150, 1080); ctx.closePath(); fs('#3f4f7a', 8);
  rr(1500, 780, 300, 300, 10); fs('#4a3221', 7);
  const sx = ring ? Math.sin(t * 80) * 6 : 0;
  ctx.save(); ctx.translate(1650 + sx, 700); rr(-110, -70, 220, 140, 30); fs('#222', 7); textC(hit ? 'SNOOZE' : '6:00', 0, 0, hit ? 36 : 64, hit ? '#7fd' : '#ff5a4a'); ctx.restore();
  if (ring) for (const sd of [-1, 1]) { ctx.beginPath(); ctx.arc(1650, 700, 160, sd > 0 ? -0.5 : Math.PI - 0.5, sd > 0 ? 0.5 : Math.PI + 0.5); fs(null, 6, '#ff8a6a'); }
  const k = prog(t, 2.6, 3.2) * (1 - prog(t, 3.6, 4.4));
  hand(lerp(1200, 1630, k), lerp(820, 620, k), 1.5, -0.4, C.skin);
  if (hit) { ctx.globalAlpha = prog(t, 4.5, 5.2); textC('z', p.hx + 140, p.hy - 120, 50, '#9fb4d6'); textC('z', p.hx + 190, p.hy - 190, 64, '#9fb4d6'); textC('Z', p.hx + 250, p.hy - 270, 80, '#9fb4d6'); ctx.globalAlpha = 1; }
};
S.typing = (t, d) => {
  ctx.fillStyle = '#06070b'; ctx.fillRect(0, 0, W, H);
  glow(W / 2, H / 2, 650, 'rgba(100,140,255,0.3)');
  ctx.save(); ctx.translate(W / 2, H / 2 + 20); phone(0, 0, 2.0, '#0f1a2c');
  rr(-210, -420, 420, 90, 0); fs('#16243a'); circle(-150, -375, 30); fs('#d98aa6'); textC('Anna', -60, -375, 40, '#fff', 'bold', 'left');
  rr(-190, -250, 300, 80, 24); fs('#22324d'); textC('haha see you', -170, -210, 28, '#ccd', 'normal', 'left');
  const msg = 'I think I like you...'; const typed = t < 4.2 ? Math.floor(prog(t, 0.8, 4.0) * msg.length) : Math.floor((1 - prog(t, 5.0, 7.0)) * msg.length);
  rr(-200, 290, 400, 90, 30); fs('#1c2a42', 4, '#33476a');
  textC(msg.slice(0, typed) + ((t * 2 | 0) % 2 ? '|' : ''), -175, 335, 30, '#fff', 'normal', 'left');
  circle(160, 335, 34); fs(typed ? '#3c7cf0' : '#2a3550'); textC('➤', 162, 337, 30, '#fff');
  ctx.restore();
  hand(W / 2 + 120, H / 2 + 420, 1.8, -2.2, C.skin);
};
S.years = (t, d) => {
  const k = clamp(t / (d - 1.5)), age = 20 + Math.min(9, Math.floor(k * 10));
  ctx.fillStyle = vgrad(0, H, [lerpCol('#2f2620', '#141414', k), lerpCol('#1d1712', '#0a0a0a', k)]); ctx.fillRect(0, 0, W, H);
  glow(W / 2, 400, 800, `rgba(255,170,90,${0.4 * (1 - k)})`);
  person({ x: 1250, y: 1060, s: 1.6, expr: k < 0.3 ? 'calm' : k < 0.7 ? 'tired' : 'sad', look: -0.3 });
  const pulse = ((t / (d - 1.5)) * 10) % 1;
  ctx.save(); ctx.translate(560, 520); ctx.scale(1 + (1 - Math.min(1, pulse * 4)) * 0.08, 1 + (1 - Math.min(1, pulse * 4)) * 0.08);
  textC('AGE', 0, -190, 50, '#888'); textC(String(age), 0, 20, 300, age >= 28 ? '#ff6b4a' : '#f3e9da'); ctx.restore();
  dust(t, Math.floor(k * 50));
};
function lerpCol(a, b, k) {
  const pa = parseInt(a.slice(1), 16), pb = parseInt(b.slice(1), 16);
  const c = s => Math.round(lerp((pa >> s) & 255, (pb >> s) & 255, k));
  return `rgb(${c(16)},${c(8)},${c(0)})`;
}
S.feed = (t, d) => {
  ctx.fillStyle = '#07080c'; ctx.fillRect(0, 0, W, H);
  glow(700, 540, 600, 'rgba(110,150,255,0.35)');
  const posts = [['Got engaged! 💍', '#d98aa6'], ['First day at my new job!', '#7fbf7f'], ['We bought a house 🏡', '#e0b050'],
    ['Finished my first marathon', '#6fa8dc'], ['Launched my own business!', '#c9733a'], ['Graduated! 🎓', '#a07fd0'], ['Moving to Canada ✈️', '#5fc9c0']];
  ctx.save(); ctx.translate(700, 540); phone(0, 0, 2.0, '#0f1a2c');
  ctx.beginPath(); ctx.roundRect(-210, -420, 420, 840, 40); ctx.clip();
  const off = t * 70;
  posts.forEach(([txt, col], i) => {
    const y = -380 + i * 200 - off; if (y < -600 || y > 500) return;
    rr(-195, y, 390, 180, 18); fs('#16243a'); circle(-150, y + 45, 28); fs(col);
    textC('friend', -105, y + 45, 22, '#889', 'normal', 'left');
    ctx.font = 'bold 26px "DejaVu Sans"'; textC(txt, -175, y + 110, 26, '#fff', 'bold', 'left');
    textC('♥ ' + (40 + i * 23), -175, y + 155, 20, '#ff7a8a', 'normal', 'left');
  });
  ctx.restore();
  person({ x: 1420, y: 1080, s: 1.7, expr: t > 4 ? 'sad' : 'calm', look: -0.8 });
};
S.dustwall = (t, d) => {
  ctx.fillStyle = vgrad(0, H, ['#24221f', '#151412']); ctx.fillRect(0, 0, W, H);
  dreamWall(700, 330, true, t);
  guitarAt(350, 820, 1.0, true);
  glow(1000, 200, 700, 'rgba(200,190,170,0.15)');
  dust(t, 70);
};
S.days = (t, d) => {
  ctx.fillStyle = '#050505'; ctx.fillRect(0, 0, W, H);
  const cols = 100, n = 3650, sz = 11, gap = 14.5, x0 = (W - cols * gap) / 2, y0 = 300;
  const shown = Math.floor(prog(t, 0.5, 3.5) * n), r = rand(99), used = new Set();
  for (let i = 0; i < 110; i++) used.add(Math.floor(r() * n));
  const fill = typeof S.days.fill === 'number' ? S.days.fill : 0;
  const lit = t > 5.5;
  for (let i = 0; i < shown; i++) {
    const x = x0 + (i % cols) * gap, y = y0 + Math.floor(i / cols) * gap;
    ctx.fillStyle = (lit && used.has(i)) ? '#ff8a3c' : '#2e2e2e'; ctx.fillRect(x, y, sz, sz);
  }
  ctx.globalAlpha = prog(t, 0.3, 1.0); textC('3,650 days.', W / 2, 180, 90, '#f3e9da'); ctx.globalAlpha = 1;
};
S.daysfill = (t, d) => {
  ctx.fillStyle = '#050505'; ctx.fillRect(0, 0, W, H);
  const cols = 100, n = 3650, sz = 11, gap = 14.5, x0 = (W - cols * gap) / 2, y0 = 300;
  const filled = Math.floor(Math.pow(prog(t, 1.0, d - 1.5), 1.3) * n);
  for (let i = 0; i < n; i++) {
    const x = x0 + (i % cols) * gap, y = y0 + Math.floor(i / cols) * gap;
    ctx.fillStyle = i < filled ? '#ff8a3c' : '#2e2e2e'; ctx.fillRect(x, y, sz, sz);
  }
  glow(W / 2, 560, 700, `rgba(255,130,50,${0.3 * filled / n})`);
};
S.cake30 = (t, d, f) => {
  ctx.fillStyle = '#0a0706'; ctx.fillRect(0, 0, W, H);
  glow(W / 2, 640, 600, `rgba(255,170,70,${0.5 + Math.sin(f * 0.7) * 0.05})`);
  person({ x: W / 2 - 230, y: 760, s: 1.25, expr: 'sad', look: 0.7, hood: true });
  rr(300, 760, 1320, 36, 8); fs('#5a4231', 7);
  ctx.save(); ctx.translate(260, 0);
  rr(W / 2 - 130, 640, 260, 120, 14); fs('#f2e4d0', 7); rr(W / 2 - 130, 640, 260, 34, 14); fs('#c97a9a', 6);
  for (const [dx, ch] of [[-40, '3'], [40, '0']]) {
    textC(ch, W / 2 + dx, 580, 110, '#7ab6e8', 'bold', 'center', 10);
    ctx.beginPath(); ctx.ellipse(W / 2 + dx + Math.sin(f * 0.5 + dx) * 2, 495, 9, 17, 0, 0, 7); fs('#ffcf5a'); glow(W / 2 + dx, 495, 50, 'rgba(255,200,90,0.6)');
  }
  ctx.restore();
  for (const x of [520, 1400]) { rr(x - 15, 520, 30, 250, 8); fs('#3a2a1d', 6); }
};
S.wakeup = (t, d) => {
  ctx.fillStyle = vgrad(0, H, ['#ffd9a0', '#f4b77a']); ctx.fillRect(0, 0, W, H);
  rr(1300, 120, 460, 400, 8); fs('#fff4d6', 10); glow(1530, 320, 700, 'rgba(255,240,200,0.8)');
  for (let i = 0; i < 5; i++) { ctx.save(); ctx.globalAlpha = 0.12; ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.moveTo(1300 + i * 90, 520); ctx.lineTo(1340 + i * 90, 520); ctx.lineTo(700 + i * 130, 1080); ctx.lineTo(620 + i * 130, 1080); ctx.fill(); ctx.restore(); }
  const up = prog(t, 0.6, 1.4);
  person({ x: 820, y: lerp(1150, 1000, up), s: 1.45, expr: t < 2.8 ? 'shock' : 'happy', look: 0.4, hood: false });
  ctx.beginPath(); ctx.moveTo(250, 860); ctx.quadraticCurveTo(900, 800, 1500, 880); ctx.lineTo(1500, 1080); ctx.lineTo(250, 1080); ctx.closePath(); fs('#e0823f', 8);
  rr(150, 180, 280, 300, 10); fs('#fff', 7); rr(150, 180, 280, 70, 10); fs('#c84a3a', 7); textC('DAY', 290, 215, 40, '#fff'); textC('1', 290, 380, 160, '#222');
};
S.drawer = (t, d) => {
  ctx.fillStyle = vgrad(0, H, ['#2a231e', '#17120e']); ctx.fillRect(0, 0, W, H);
  glow(W / 2, 400, 700, 'rgba(255,180,100,0.35)');
  person({ x: W / 2, y: 720, s: 1.3, expr: 'determined' });
  rr(250, 700, 1420, 380, 10); fs('#5a4030', 8);
  const open = prog(t, 0.3, 1.0) * (1 - prog(t, 4.0, 4.8));
  rr(700, 820 + open * 60, 520, 170, 8); fs('#6d4e3a', 8); rr(900, 890 + open * 60, 120, 24, 10); fs('#c9a14a', 4);
  const pk = prog(t, 1.2, 3.4);
  if (t < 4.2) { ctx.save(); ctx.translate(lerp(W / 2 + 200, W / 2, pk), lerp(560, 880, pk)); ctx.scale(0.5, 0.5); ctx.globalAlpha = 1 - prog(t, 3.2, 3.6); phone(0, 0, 1, '#13223a'); ctx.restore(); }
  hand(lerp(W / 2 + 260, W / 2 + 60, pk), lerp(620, 900, pk) - (t > 3.6 ? (t - 3.6) * 200 : 0), 1.3, -0.5, C.skin);
};
S.run = (t, d) => {
  const sc = t * 420;
  ctx.fillStyle = vgrad(0, H, ['#3a2a5a', '#e0705a', '#ffb070']); ctx.fillRect(0, 0, W, H);
  circle(1500, 640, 130); fs('#ffe0a0'); glow(1500, 640, 600, 'rgba(255,200,120,0.7)');
  ctx.fillStyle = '#5a3a4a'; for (let i = 0; i < 6; i++) { const x = ((i * 520 - sc * 0.25) % 3120 + 3120) % 3120 - 400; ctx.beginPath(); ctx.ellipse(x, 820, 420, 200, 0, Math.PI, 0); ctx.fill(); }
  ctx.fillStyle = '#2a2230'; ctx.fillRect(0, 900, W, 180);
  for (let i = 0; i < 10; i++) { const x = ((i * 300 - sc) % 3000 + 3000) % 3000 - 100; ctx.fillStyle = '#d8c070'; ctx.fillRect(x, 975, 120, 12); }
  const b = Math.abs(Math.sin(t * 9)) * -24;
  person({ x: 800, y: 980, s: 1.35, expr: t > d / 2 ? 'determined' : 'angry', look: 0.8, bob: b, lean: 0.1 });
  hand(970, 820 + Math.sin(t * 9) * 40, 1.1, -0.3, C.skin); hand(640, 820 - Math.sin(t * 9) * 40, 1.1, 0.3, C.skin);
  sweat(700, 450 + b, t);
};
S.gym = (t, d) => {
  ctx.fillStyle = vgrad(0, H, ['#1b1d22', '#0c0d10']); ctx.fillRect(0, 0, W, H);
  glow(W / 2, 200, 800, 'rgba(255,170,90,0.3)');
  for (let i = 0; i < 4; i++) { rr(1400, 300 + i * 150, 380, 20, 6); fs('#444', 5); circle(1430, 290 + i * 150, 40); fs('#2a2a2a', 6); circle(1750, 290 + i * 150, 40); fs('#2a2a2a', 6); }
  const rep = Math.sin(t * 2.2), y = 850 + rep * 70;
  const p = person({ x: 820, y: 1040, s: 1.5, expr: rep < -0.3 ? 'angry' : 'determined' });
  line([560, y, 1080, y], 14, '#555'); for (const x of [560, 1080]) { rr(x - 22, y - 90, 44, 180, 10); fs('#222', 6); }
  hand(700, y + 10, 1.2, 0, C.skin); hand(940, y + 10, 1.2, Math.PI, C.skin);
  sweat(p.hx - 120, p.hy - 40, t); sweat(p.hx + 110, p.hy - 20, t + 0.4);
};
S.read = (t, d) => {
  ctx.fillStyle = vgrad(0, H, ['#1a1612', '#0d0b09']); ctx.fillRect(0, 0, W, H);
  glow(1200, 520, 650, 'rgba(255,190,110,0.55)');
  line([1300, 750, 1350, 420, 1220, 330], 10, '#333'); ctx.beginPath(); ctx.moveTo(1150, 300); ctx.lineTo(1300, 300); ctx.lineTo(1260, 380); ctx.lineTo(1190, 380); ctx.closePath(); fs('#c58a3c', 7);
  person({ x: 860, y: 900, s: 1.4, expr: 'calm', look: 0.1 });
  rr(200, 880, 1520, 200, 0); fs('#3e2e22', 6);
  ctx.save(); ctx.translate(860, 860); ctx.beginPath(); ctx.moveTo(-220, -10); ctx.quadraticCurveTo(-110, -50, 0, -20); ctx.quadraticCurveTo(110, -50, 220, -10); ctx.lineTo(220, 40); ctx.quadraticCurveTo(110, 10, 0, 40); ctx.quadraticCurveTo(-110, 10, -220, 40); ctx.closePath(); fs('#f2ead8', 6);
  const flip = (t % 3) / 3; if (flip < 0.25) { ctx.beginPath(); ctx.moveTo(0, -20); ctx.quadraticCurveTo(lerp(110, -110, flip * 4), -80, lerp(220, -220, flip * 4), -10); fs(null, 5); }
  for (let i = 0; i < 4; i++) { line([-190, -10 + i * 12, -30, -10 + i * 12], 3, '#aaa'); line([30, -10 + i * 12, 190, -10 + i * 12], 3, '#aaa'); }
  ctx.restore();
  for (let i = 0; i < 4; i++) { rr(1500, 760 - i * 40, 160, 38, 4); fs(['#b8452e', '#3d6fb0', '#5a8a4a', '#d9a03a'][i], 4); }
};
S.guitar = (t, d) => {
  ctx.fillStyle = vgrad(0, H, ['#33261e', '#1d150f']); ctx.fillRect(0, 0, W, H);
  glow(W / 2, 450, 800, 'rgba(255,180,100,0.45)');
  const p = person({ x: W / 2, y: 1060, s: 1.5, expr: 'happy', bob: Math.sin(t * 4) * 4 });
  ctx.save(); ctx.translate(W / 2 + 60, 880); ctx.rotate(-1.2); ctx.scale(1.1, 1.1);
  rr(-14, -330, 28, 260, 6); fs('#4a2e1c', 5); ctx.beginPath(); ctx.ellipse(0, -40, 75, 70, 0, 0, 7); fs('#c4733a', 6); ctx.beginPath(); ctx.ellipse(0, 70, 100, 95, 0, 0, 7); fs('#c4733a', 6); circle(0, 15, 28); fs('#1a1a1a', 4);
  ctx.restore();
  hand(W / 2 + 40, 860 + Math.sin(t * 10) * 18, 1.2, 0.3, C.skin); hand(W / 2 + 420, 680, 1.1, -1.2, C.skin);
  for (let i = 0; i < 4; i++) { const k = (t * 0.4 + i / 4) % 1; ctx.globalAlpha = Math.sin(k * Math.PI); textC(i % 2 ? '♪' : '♫', W / 2 - 300 + i * 70 + Math.sin(k * 6) * 20, 700 - k * 500, 60, '#ffd08a'); ctx.globalAlpha = 1; }
};
S.summit = (t, d) => {
  const z = 1.15 - prog(t, 0, d) * 0.15;
  ctx.save(); ctx.translate(W / 2, H / 2); ctx.scale(z, z); ctx.translate(-W / 2, -H / 2);
  ctx.fillStyle = vgrad(0, H, ['#2a2a5a', '#c85a5a', '#ffa64d', '#ffd690']); ctx.fillRect(0, 0, W, H);
  const sy = 640 - prog(t, 0, d) * 120;
  circle(W / 2, sy, 230); fs('#ffe1a0'); glow(W / 2, sy, 900, 'rgba(255,200,120,0.8)');
  ctx.fillStyle = '#3a2440'; ctx.beginPath(); ctx.moveTo(0, 1080); ctx.lineTo(0, 900); ctx.lineTo(W / 2, 780); ctx.lineTo(W, 900); ctx.lineTo(W, 1080); ctx.fill();
  person({ x: W / 2, y: 800, s: 1.1, expr: 'determined' });
  ctx.restore();
};

Object.assign(LOOK, { age20: { warm: 1 }, wakeup: { warm: 1 }, days: { noVig: 1 }, daysfill: { noVig: 1 } });
Object.assign(ZOOM, { mirror: [1.0, 1.08], age20: [1.0, 1.05], alarm: [1.0, 1.05], typing: [1.0, 1.08], years: [1.0, 1.06],
  feed: [1.0, 1.05], dustwall: [1.0, 1.1], cake30: [1.0, 1.1], wakeup: [1.0, 1.04], drawer: [1.0, 1.04], gym: [1.0, 1.04],
  read: [1.0, 1.05], guitar: [1.0, 1.05], days: [1.0, 1.03] });
S.thumb20 = (t, d) => {
  ctx.fillStyle = '#070605'; ctx.fillRect(0, 0, W, H);
  // hourglass behind
  const cx = 1330, top = 120, bot = 1000, mid = 560;
  glow(cx, mid, 700, 'rgba(255,120,40,0.7)');
  ctx.beginPath(); ctx.moveTo(cx - 330, top); ctx.lineTo(cx + 330, top); ctx.quadraticCurveTo(cx + 330, mid - 80, cx + 24, mid); ctx.quadraticCurveTo(cx + 330, mid + 80, cx + 330, bot); ctx.lineTo(cx - 330, bot); ctx.quadraticCurveTo(cx - 330, mid + 80, cx - 24, mid); ctx.quadraticCurveTo(cx - 330, mid - 80, cx - 330, top); ctx.closePath();
  fs('rgba(255,200,140,0.10)', 10, '#d8c8b0');
  textC('20', cx, 260, 110, 'rgba(255,220,180,0.5)'); textC('30', cx, 880, 110, '#ff8a3c');
  person({ x: cx, y: 1250, s: 2.3, expr: 'tired' });
  ctx.save(); ctx.translate(cx, 900); phone(0, 0, 0.8, '#13223a'); ctx.restore();
  hand(cx - 130, 950, 1.5, 0.4, C.skin); hand(cx + 130, 950, 1.5, -0.4 + Math.PI, C.skin);
  vignette(0.6);
  ctx.save(); ctx.translate(480, 520); ctx.rotate(-0.05); textC('20s.', 0, 0, 330, '#fff', 'bold', 'center', 30); ctx.restore();
};
LOOK.thumb20 = { noVig: 1 };
