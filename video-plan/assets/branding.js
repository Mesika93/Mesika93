// Usage: node branding.js <out_dir>  -> avatar.png (800x800) and banner.png (2560x1440, YouTube safe area respected)
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const out = process.argv[2]; fs.mkdirSync(out, { recursive: true });
const font = fs.readFileSync(path.join(__dirname, 'LuckiestGuy.ttf')).toString('base64');
const NAME = process.env.CHANNEL || 'ZYNEX';

const DRAW = `
function head3d(p, light, side) {
  const { hx, hy, R } = p; ctx.save(); circle(hx, hy, R - 3); ctx.clip();
  let g = ctx.createRadialGradient(hx - R * 0.35, hy - R * 0.45, R * 0.1, hx, hy, R * 1.1);
  g.addColorStop(0, 'rgba(255,255,255,0.35)'); g.addColorStop(0.55, 'rgba(255,255,255,0)'); g.addColorStop(1, 'rgba(0,0,30,0.4)');
  ctx.fillStyle = g; ctx.fillRect(hx - R, hy - R, 2 * R, 2 * R);
  g = ctx.createRadialGradient(hx + side * R * 1.1, hy, R * 0.6, hx + side * R * 1.1, hy, R);
  g.addColorStop(0, light); g.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.globalCompositeOperation = 'lighter'; ctx.globalAlpha = 0.35; ctx.fillStyle = g; ctx.fillRect(hx - R, hy - R, 2 * R, 2 * R); ctx.restore();
}
function lucky(str, x, y, size, col = '#fff', stroke = 0.14, rot = 0) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.font = size + 'px Lucky'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.lineJoin = 'round';
  ctx.fillStyle = 'rgba(0,0,0,0.6)'; ctx.fillText(str, size * 0.04, size * 0.06);
  ctx.lineWidth = size * stroke; ctx.strokeStyle = '#000'; ctx.strokeText(str, 0, 0); ctx.fillStyle = col; ctx.fillText(str, 0, 0); ctx.restore();
}
function sparkle(x, y, s, a = 1) {
  ctx.save(); ctx.globalAlpha = a; ctx.translate(x, y); ctx.beginPath();
  for (let i = 0; i < 4; i++) { ctx.rotate(Math.PI / 2); ctx.moveTo(0, 0); ctx.quadraticCurveTo(s * 0.15, s * 0.15, 0, s); ctx.quadraticCurveTo(-s * 0.15, s * 0.15, 0, 0); }
  ctx.fillStyle = '#ffd27a'; ctx.fill(); ctx.restore(); glow(x, y, s * 2, 'rgba(255,200,100,0.6)', a);
}
window.avatar = () => {
  const cx = W / 2, cy = H / 2;
  ctx.fillStyle = vgrad(0, H, ['#120c14', '#2a1410', '#3a1a0c']); ctx.fillRect(0, 0, W, H);
  const R = 95 * 2.3, hy = cy - 20;
  glow(cx, hy, 700, 'rgba(255,120,40,0.6)');
  circle(cx, hy, R * 1.75); fs('#ff8a30'); circle(cx, hy, R * 1.55); fs('#ffb860');
  glow(cx, hy, R * 2.2, 'rgba(255,220,150,0.55)');
  for (let i = 0; i < 16; i++) { const a = i / 16 * Math.PI * 2; line([cx + Math.cos(a) * R * 1.85, hy + Math.sin(a) * R * 1.85, cx + Math.cos(a) * R * 2.15, hy + Math.sin(a) * R * 2.15], 10, 'rgba(255,190,100,0.7)'); }
  const p = person({ x: cx, y: hy + R * 0.72 + 210 * 2.3, s: 2.3, expr: 'determined' }); head3d(p, 'rgba(255,170,70,1)', 1);
  for (const [x, y, s] of [[cx - 400, cy - 330, 44], [cx + 410, cy - 280, 32], [cx + 380, cy + 200, 22], [cx - 420, cy + 150, 24]]) sparkle(x, y, s);
};
window.banner = () => {
  ctx.fillStyle = vgrad(0, H, ['#0a0809', '#1a0f0c', '#0a0809']); ctx.fillRect(0, 0, W, H);
  // safe area (all devices): x 380..1540, y 381..698
  glow(W / 2, 540, 900, 'rgba(255,120,40,0.35)');
  circle(470, 530, 230); fs('#ff9a40'); circle(470, 530, 205); fs('#ffc070'); glow(470, 530, 450, 'rgba(255,200,120,0.55)');
  const p = person({ x: 470, y: 975, s: 1.6, expr: 'determined', look: 0.3 }); head3d(p, 'rgba(255,170,70,1)', 1);
  glow(1450, 540, 380, 'rgba(90,120,220,0.35)');
  const q = person({ x: 1450, y: 975, s: 1.6, expr: 'tired', top: '#8a5a3e', look: -0.4 }); head3d(q, 'rgba(110,150,255,1)', -1);
  ctx.fillStyle = vgrad(800, H, ['rgba(10,8,9,0)', 'rgba(10,8,9,1)']); ctx.fillRect(0, 800, W, 280);
  lucky('${NAME}', W / 2, 495, 160, '#fff', 0.13, -0.02);
  ctx.save(); ctx.shadowColor = 'rgba(0,0,0,0.9)'; ctx.shadowBlur = 16;
  ctx.font = 'bold 30px "DejaVu Sans"'; ctx.textAlign = 'center'; ctx.fillStyle = '#f3e9da';
  ctx.fillText('Animated short films about life,', W / 2, 610); ctx.fillText('discipline & becoming better.', W / 2, 652); ctx.restore();
  for (const [x, y, s] of [[700, 420, 20], [1230, 410, 16]]) sparkle(x, y, s, 0.9);
};
`;
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  page.on('pageerror', e => console.error('PAGE ERROR', e.message));
  await page.goto('file://' + path.join(__dirname, '../01-parents/render/scene.html'));
  await page.evaluate(async b64 => { const f = new FontFace('Lucky', Uint8Array.from(atob(b64), c => c.charCodeAt(0)).buffer); await f.load(); document.fonts.add(f); }, font);
  await page.addScriptTag({ content: DRAW });
  const shot = (fn, sx, sy, sw, sh, ow, oh) => page.evaluate(([fn, sx, sy, sw, sh, ow, oh]) => {
    const cv = document.getElementById('c'); cv.width = 3840; cv.height = 2160; ctx.setTransform(2, 0, 0, 2, 0, 0);
    window[fn](); applyGrain(1, 0.04);
    const o = document.createElement('canvas'); o.width = ow; o.height = oh; const g = o.getContext('2d'); g.imageSmoothingQuality = 'high';
    g.drawImage(cv, sx * 2, sy * 2, sw * 2, sh * 2, 0, 0, ow, oh); return o.toDataURL('image/png').split(',')[1];
  }, [fn, sx, sy, sw, sh, ow, oh]);
  fs.writeFileSync(path.join(out, 'avatar.png'), Buffer.from(await shot('avatar', 420, 0, 1080, 1080, 800, 800), 'base64'));
  fs.writeFileSync(path.join(out, 'banner.png'), Buffer.from(await shot('banner', 0, 0, 1920, 1080, 2560, 1440), 'base64'));
  await browser.close();
})();
