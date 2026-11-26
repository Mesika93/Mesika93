// Usage: node thumbs.js <out_dir>   -> renders YouTube thumbnails (1280x720 jpg) in the channel style
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const out = process.argv[2]; fs.mkdirSync(out, { recursive: true });
const font = fs.readFileSync(path.join(__dirname, 'LuckiestGuy.ttf')).toString('base64');

const THUMBS = `
function head3d(p, light = 'rgba(255,140,60,1)', side = 1) {
  const { hx, hy, R } = p;
  ctx.save(); circle(hx, hy, R - 3); ctx.clip();
  let g = ctx.createRadialGradient(hx - R * 0.35, hy - R * 0.45, R * 0.1, hx, hy, R * 1.1);
  g.addColorStop(0, 'rgba(255,255,255,0.35)'); g.addColorStop(0.55, 'rgba(255,255,255,0)'); g.addColorStop(1, 'rgba(0,0,30,0.45)');
  ctx.fillStyle = g; ctx.fillRect(hx - R, hy - R, 2 * R, 2 * R);
  g = ctx.createRadialGradient(hx + side * R * 1.1, hy, R * 0.6, hx + side * R * 1.1, hy, R * 1.0);
  g.addColorStop(0, light); g.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.globalCompositeOperation = 'lighter'; ctx.globalAlpha = 0.38; ctx.fillStyle = g; ctx.fillRect(hx - R, hy - R, 2 * R, 2 * R);
  ctx.restore();
}
function bigText(lines, x, y, size, rot = -0.04, col = '#fff') {
  ctx.save(); ctx.translate(x, y); ctx.rotate(rot);
  ctx.font = size + 'px Lucky'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.lineJoin = 'round';
  lines.forEach((l, i) => {
    const yy = (i - (lines.length - 1) / 2) * size * 0.95;
    ctx.fillStyle = 'rgba(0,0,0,0.7)'; ctx.fillText(l, 10, yy + 14);
    ctx.lineWidth = size * 0.16; ctx.strokeStyle = '#000'; ctx.strokeText(l, 0, yy);
    ctx.fillStyle = col; ctx.fillText(l, 0, yy);
  });
  ctx.restore();
}
function bg(c1, c2, x, y) {
  ctx.fillStyle = '#060504'; ctx.fillRect(0, 0, W, H);
  glow(x, y, 900, c1); glow(x, y, 450, c2);
}
function tears(p) {
  for (const sd of [-1, 1]) {
    const x = p.hx + sd * p.R * 0.32, y = p.hy + p.R * 0.08;
    ctx.beginPath(); ctx.moveTo(x - 10, y); ctx.quadraticCurveTo(x + sd * 14, y + p.R * 0.5, x + sd * 4, y + p.R * 0.8); ctx.lineTo(x + sd * 22, y + p.R * 0.8); ctx.quadraticCurveTo(x + sd * 28, y + p.R * 0.4, x + 12, y); ctx.closePath();
    fs('rgba(140,200,255,0.85)', 3, 'rgba(60,120,200,0.9)');
    circle(x + sd * 13, y + p.R * 0.85, 13); fs('rgba(160,215,255,0.95)', 3, 'rgba(60,120,200,0.9)');
  }
}
const T = {};
T.lastcall = () => {
  bg('rgba(220,60,30,0.55)', 'rgba(255,150,60,0.5)', 1250, 700);
  const p = person({ x: 1250, y: 1500, s: 3.0, expr: 'cry' }); head3d(p); tears(p);
  ctx.save(); ctx.translate(1250, 1000); ctx.rotate(-0.08); phone(0, 0, 1.15, '#13223a');
  glow(0, -60, 260, 'rgba(120,170,255,0.5)');
  textC('Mom ❤', 0, -130, 54, '#fff'); textC('7 missed calls', 0, -60, 36, '#ff6b6b'); ctx.restore();
  hand(1080, 1060, 2.0, 0.4, C.skin); hand(1420, 1060, 2.0, -0.4 + Math.PI, C.skin);
  vignette(0.5);
  bigText(['LAST', 'CALL.'], 520, 470, 250);
};
T.hundred = () => {
  bg('rgba(255,110,30,0.5)', 'rgba(255,200,120,0.45)', 1300, 620);
  const p = person({ x: 1300, y: 1420, s: 2.7, kind: 'mom', old: true, skin: C.momSkin, top: '#d8c3a0', expr: 'sad', look: -0.4 }); head3d(p, 'rgba(255,170,80,1)', -1);
  vignette(0.5);
  bigText(['100', 'LEFT.'], 520, 470, 260, -0.05);
};
T.wasted = () => {
  bg('rgba(90,120,255,0.45)', 'rgba(150,180,255,0.4)', 1250, 650);
  const p = person({ x: 1250, y: 1480, s: 2.9, expr: 'tired' }); head3d(p, 'rgba(110,150,255,1)');
  for (const sd of [-1, 1]) { ctx.beginPath(); ctx.ellipse(p.hx + sd * p.R * 0.32, p.hy + p.R * 0.14, p.R * 0.14, p.R * 0.06, 0, 0, 7); fs('rgba(60,40,80,0.45)'); }
  ctx.save(); ctx.translate(1250, 1000); ctx.rotate(0.05); phone(0, 0, 1.1, '#2a3d66'); glow(0, -80, 300, 'rgba(140,180,255,0.6)'); ctx.restore();
  hand(1090, 1060, 1.9, 0.4, C.skin); hand(1410, 1060, 1.9, -0.4 + Math.PI, C.skin);
  textC('3:47 AM', 1700, 160, 60, '#ff5a4a'); 
  vignette(0.5);
  bigText(['WASTED'], 540, 330, 230, -0.05);
  bigText(['20S.'], 520, 610, 260, -0.03, '#ff8a3c');
};
T.thirty = () => {
  bg('rgba(255,120,40,0.55)', 'rgba(255,190,90,0.5)', 1350, 760);
  const p = person({ x: 1400, y: 1460, s: 2.6, expr: 'sad', look: -0.5 }); head3d(p, 'rgba(255,170,70,1)', -1);
  ctx.save(); ctx.translate(820, 930); ctx.scale(0.8, 0.8);
  rr(-260, -60, 520, 220, 20); fs('#f2e4d0', 9); rr(-260, -60, 520, 60, 20); fs('#c97a9a', 8);
  for (const [dx, ch] of [[-75, '3'], [75, '0']]) { ctx.font = '190px Lucky'; ctx.textAlign = 'center'; ctx.lineWidth = 16; ctx.strokeStyle = '#000'; ctx.strokeText(ch, dx, -110); ctx.fillStyle = '#7ab6e8'; ctx.fillText(ch, dx, -110);
    ctx.beginPath(); ctx.ellipse(dx, -290, 18, 32, 0, 0, 7); fs('#ffcf5a'); glow(dx, -290, 120, 'rgba(255,200,90,0.8)'); }
  ctx.restore();
  vignette(0.5);
  bigText(['ALONE', 'AT 30.'], 480, 330, 200, -0.05);
};
T.sameday = () => {
  ctx.fillStyle = '#060504'; ctx.fillRect(0, 0, W, H);
  ctx.save(); ctx.beginPath(); ctx.rect(0, 0, W / 2, H); ctx.clip();
  ctx.fillStyle = '#0a0c16'; ctx.fillRect(0, 0, W, H); glow(480, 760, 700, 'rgba(80,120,255,0.55)');
  const a = person({ x: 480, y: 1480, s: 2.4, expr: 'tired', top: '#8a5a3e' }); head3d(a, 'rgba(110,150,255,1)', 1);
  for (const sd of [-1, 1]) { ctx.beginPath(); ctx.ellipse(a.hx + sd * a.R * 0.32, a.hy + a.R * 0.14, a.R * 0.13, a.R * 0.05, 0, 0, 7); fs('rgba(60,40,80,0.5)'); }
  ctx.save(); ctx.translate(480, 1130); phone(0, 0, 0.9, '#2a3d66'); glow(0, -80, 260, 'rgba(140,180,255,0.6)'); ctx.restore();
  hand(350, 1150, 1.6, 0.4, C.skin); hand(610, 1150, 1.6, -0.4 + Math.PI, C.skin);
  ctx.globalCompositeOperation = 'saturation'; ctx.globalAlpha = 0.4; ctx.fillStyle = '#808080'; ctx.fillRect(0, 0, W, H);
  ctx.restore();
  ctx.save(); ctx.beginPath(); ctx.rect(W / 2, 0, W / 2, H); ctx.clip();
  ctx.fillStyle = vgrad(0, H, ['#3a2a5a', '#e0705a', '#ffb070']); ctx.fillRect(0, 0, W, H);
  circle(1440, 820, 260); fs('#ffe0a0'); glow(1440, 820, 800, 'rgba(255,200,120,0.8)');
  const b = person({ x: 1440, y: 1480, s: 2.4, expr: 'determined' }); head3d(b, 'rgba(255,170,70,1)', -1);
  ctx.restore();
  line([W / 2, 0, W / 2, H], 16, '#000');
  vignette(0.45);
  bigText(['SAME DAY.'], W / 2, 190, 230, -0.03);
};
T.nobody = () => {
  ctx.fillStyle = '#050405'; ctx.fillRect(0, 0, W, H);
  // door with light under it on the right
  const dx = 1380, w = 360, h = 760, y = 1000 - h;
  glow(dx + w / 2, 1000, 420, 'rgba(255,220,160,0.75)');
  ctx.fillStyle = '#ffe2b0'; ctx.fillRect(dx, 990, w, 14);
  rr(dx - 16, y - 16, w + 32, h + 16, 4); fs('#1a1412', 10); rr(dx, y, w, h, 2); fs('#3a281e', 8); circle(dx + w - 50, y + h / 2, 18); fs('#c9a14a', 5);
  ctx.fillStyle = 'rgba(255,220,160,0.12)'; ctx.beginPath(); ctx.moveTo(dx, 1004); ctx.lineTo(dx + w, 1004); ctx.lineTo(dx + w + 300, H); ctx.lineTo(dx - 500, H); ctx.fill();
  const p = person({ x: 720, y: 1350, s: 2.6, expr: 'cry', look: 0.6, noBand: true }); head3d(p, 'rgba(255,190,110,1)', 1); tears(p);
  hand(1130, 720, 2.0, -0.2, C.skin);
  vignette(0.5);
  bigText(['NOBODY.'], 600, 190, 230, -0.04);
};
T.daysleft = () => {
  bg('rgba(255,90,40,0.45)', 'rgba(255,170,90,0.4)', 1350, 650);
  const m = person({ x: 1420, y: 1330, s: 2.2, kind: 'mom', old: true, skin: C.momSkin, top: '#d8c3a0', expr: 'happy', look: -0.5, blush: true }); head3d(m, 'rgba(255,170,80,1)', -1);
  const z = person({ x: 560, y: 1420, s: 2.3, expr: 'shock', look: 0.8 }); head3d(z, 'rgba(255,140,60,1)', 1);
  // red counter above mom
  const ty = m.hy - m.R - 200;
  glow(m.hx, ty, 300, 'rgba(255,60,40,0.7)');
  rr(m.hx - 180, ty - 85, 360, 170, 85); fs('rgba(10,5,5,0.85)', 8, '#ff4a3a');
  ctx.font = '150px Lucky'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillStyle = '#ff4a3a'; ctx.fillText('214', m.hx, ty + 8);
  vignette(0.45);
  bigText(['DAYS', 'LEFT.'], 520, 300, 200, -0.05);
};
T.daysleft_ext = () => {
  PEOPLE = [];
  skyline(0, { y: 780, layers: 4, seed: 9, sky: ['#0a0e2a', '#25205a', '#6a3a7a'], lit: 0.5 });
  ctx.fillStyle = '#16142a'; ctx.fillRect(0, 860, W, 220);
  glow(1420, 520, 650, 'rgba(255,80,60,0.35)');
  const m = person({ x: 1420, y: 1330, s: 2.2, kind: 'mom', old: true, skin: C.momSkin, top: '#d8c3a0', expr: 'happy', look: -0.5, blush: true });
  RIM = 'rgba(120,200,255,1)'; RIM_SIDE = -1;
  const z = person({ x: 560, y: 1420, s: 2.3, expr: 'shock', look: 0.8 });
  RIM_SIDE = 1;
  const ty = m.hy - m.R - 200;
  glow(m.hx, ty, 320, 'rgba(255,60,40,0.8)');
  rr(m.hx - 180, ty - 85, 360, 170, 85); fs('rgba(10,5,5,0.85)', 8, '#ff4a3a');
  ctx.font = '150px Lucky'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillStyle = '#ff4a3a'; ctx.fillText('214', m.hx, ty + 8);
  vignette(0.4);
  bigText(['DAYS'], 470, 200, 220, -0.04); bigText(['LEFT.'], 470, 420, 220, -0.04, '#ffd23a');
};
T.younger_ext = () => {
  PEOPLE = [];
  skyline(0, { y: 780, layers: 4, seed: 41, sky: ['#070a22', '#1e1a52', '#4a2a6a'], lit: 0.5 });
  ctx.fillStyle = '#12122a'; ctx.fillRect(0, 860, W, 220);
  // streetlight beam on the kid
  glow(1380, 300, 500, 'rgba(255,210,140,0.6)'); lightBeam(1380, 260, 420, 900, 'rgba(255,215,150,1)', 0.25);
  const r = rand(4); ctx.save(); ctx.globalCompositeOperation = 'lighter'; for (let i = 0; i < 40; i++) { const x = 1100 + r() * 560, y = 250 + r() * 700; glow(x, y, 18, 'rgba(255,215,140,0.5)'); } ctx.restore();
  RIM = 'rgba(140,190,255,1)'; RIM_SIDE = 1;
  const a = person({ x: 520, y: 1450, s: 2.4, expr: 'shock', look: 0.8, top: '#c9692e' });
  RIM = 'rgba(255,210,140,1)'; RIM_SIDE = -1;
  rr(1380 - 95 * 1.8, 1180 - 150 * 1.8, 190 * 1.8, 120 * 1.8, 50); fs('#3d6fb0', 10);
  const k = person({ x: 1380, y: 1180, s: 1.8, kind: 'kid', top: '#ff8a3c', band: true, expr: 'happy', look: -0.7 });
  vignette(0.4);
  bigText(['ME?'], 960, 170, 230, -0.04, '#ffd23a');
};
T.thoughts_ext = () => {
  if (typeof thought === 'undefined') return;
  PEOPLE = []; TIME = 0;
  metro(0.3);
  ctx.fillStyle = 'rgba(10,12,24,0.35)'; ctx.fillRect(0, 0, W, H);
  const ps = [[220, '#3d8bd0'], [1450, '#5a9a4a'], [1760, '#a07fd0']].map(([x, c], i) => figure({ x, y: 1060, s: 1.05, top: c, pose: i === 0 ? 'sit' : 'stand', expr: 'calm', look: x < 960 ? 0.5 : -0.5, noBand: true }));
  thought(330, 300, 'LOSER', 1, 0, { mode: 'red', size: 56 });
  thought(1500, 300, 'WEIRD', 1, 0, { mode: 'red', size: 56 });
  RIM = 'rgba(255,120,120,1)';
  const z = person({ x: 900, y: 1400, s: 2.5, expr: 'shock', look: 0.3, top: '#d9692a' }); head3d(z, 'rgba(255,100,100,1)', 1);
  vignette(0.45);
  bigText(['THEY', 'KNOW?'], 960, 250, 190, -0.04, '#fff');
};
`;

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  page.on('pageerror', e => console.error('PAGE ERROR', e.message));
  await page.goto('file://' + path.join(__dirname, '../01-parents/render/scene.html'));
  await page.evaluate(async b64 => {
    const f = new FontFace('Lucky', Uint8Array.from(atob(b64), c => c.charCodeAt(0)).buffer); await f.load(); document.fonts.add(f);
  }, font);
  for (const x of (process.env.EXTRA || '').split(',').filter(Boolean)) await page.addScriptTag({ path: path.resolve(x) });
  await page.addScriptTag({ content: THUMBS + ';window.T = T;' });
  for (const name of await page.evaluate(() => Object.keys(window.T).filter(k => !k.endsWith('_ext') || typeof skyline !== 'undefined'))) {
    const b64 = await page.evaluate(n => { ctx.setTransform(1, 0, 0, 1, 0, 0); window.T[n](); applyGrain(1, 0.05);
      const c = document.createElement('canvas'); c.width = 1280; c.height = 720; c.getContext('2d').drawImage(document.getElementById('c'), 0, 0, 1280, 720);
      return c.toDataURL('image/jpeg', 0.92).split(',')[1]; }, name);
    fs.writeFileSync(path.join(out, name + '.jpg'), Buffer.from(b64, 'base64'));
  }
  await browser.close();
})();
