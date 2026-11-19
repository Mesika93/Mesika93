// Usage:
//   node render.js <out_dir> stills          -> one PNG per scene (middle frame) for checking
//   node render.js <out_dir> video [fps] [extra_scenes.js] -> out_dir/video.mp4 with audio mix
// extra_scenes.js (optional) adds/overrides scenes on top of scene.html (shared character library)
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs'), path = require('path');

(async () => {
  const [out, mode = 'stills', fpsArg = '30', extra] = process.argv.slice(2);
  const fps = +fpsArg;
  const tl = JSON.parse(fs.readFileSync(path.join(out, 'timeline.json'), 'utf8'));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  page.on('pageerror', e => console.error('PAGE ERROR', e.message));
  await page.goto('file://' + path.join(__dirname, 'scene.html'));
  if (extra) await page.addScriptTag({ path: path.resolve(extra) });
  await page.evaluate(t => window.setTimeline(t), tl);
  const grab = async frame => {
    const b64 = await page.evaluate(([f, fps]) => { window.drawFrame(f, fps); return document.getElementById('c').toDataURL('image/jpeg', 0.93).split(',')[1]; }, [frame, fps]);
    return Buffer.from(b64, 'base64');
  };
  if (mode === 'stills') {
    fs.mkdirSync(path.join(out, 'stills'), { recursive: true });
    for (const [i, s] of tl.scenes.entries()) {
      const f = Math.round(((s.start + s.end) / 2) * fps);
      fs.writeFileSync(path.join(out, "stills", `${String(i).padStart(2, "0")}_${s.id}.jpg`), await grab(f));
    }
  } else {
    const total = Math.ceil(tl.duration * fps);
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
      '-i', path.join(out, 'mix.wav'), '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p',
      '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', path.join(out, 'video.mp4')], { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let f = 0; f < total; f++) {
      const buf = await grab(f);
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (f % 300 === 0) console.log(`frame ${f}/${total}`);
    }
    ff.stdin.end();
    await new Promise(r => ff.on('close', r));
  }
  await browser.close();
})();
