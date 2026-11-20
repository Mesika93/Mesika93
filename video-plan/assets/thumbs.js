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
`;

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  page.on('pageerror', e => console.error('PAGE ERROR', e.message));
  await page.goto('file://' + path.join(__dirname, '../01-parents/render/scene.html'));
  await page.evaluate(async b64 => {
    const f = new FontFace('Lucky', Uint8Array.from(atob(b64), c => c.charCodeAt(0)).buffer); await f.load(); document.fonts.add(f);
  }, font);
  await page.addScriptTag({ content: THUMBS + ';window.T = T;' });
  for (const name of await page.evaluate(() => Object.keys(window.T))) {
    const b64 = await page.evaluate(n => { ctx.setTransform(1, 0, 0, 1, 0, 0); window.T[n](); applyGrain(1, 0.05);
      const c = document.createElement('canvas'); c.width = 1280; c.height = 720; c.getContext('2d').drawImage(document.getElementById('c'), 0, 0, 1280, 720);
      return c.toDataURL('image/jpeg', 0.92).split(',')[1]; }, name);
    fs.writeFileSync(path.join(out, name + '.jpg'), Buffer.from(b64, 'base64'));
  }
  await browser.close();
})();
