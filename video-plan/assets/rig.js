// Full-body character rig: legs (hip-knee-foot + shoes), arms (shoulder-elbow-hand) on top of the existing
// head/torso drawing. Poses: stand, walk, run, sit, wave, point, armsUp, hold, think, pockets, reach, hug.
// Load after fx.js. Usage: figure({ x, y: groundY, s, pose: 'walk', phase: t, dir: 1, ...person options })

const PANTS = '#3a3d4a', SHOE = '#1d1d24';
function limb(x, y, a1, l1, a2, l2, w, col, lw) {
  const kx = x + Math.sin(a1) * l1, ky = y + Math.cos(a1) * l1;
  const b = a1 + a2, fx = kx + Math.sin(b) * l2, fy = ky + Math.cos(b) * l2;
  ctx.lineCap = 'round'; ctx.lineJoin = 'round';
  ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(kx, ky); ctx.lineTo(fx, fy);
  ctx.lineWidth = w + lw * 2; ctx.strokeStyle = C.ink; ctx.stroke();
  ctx.lineWidth = w; ctx.strokeStyle = col; ctx.stroke();
  return { kx, ky, fx, fy, end: b };
}
// pose → { legs: [[hip, knee], [hip, knee]] (left, right), arms: [[shoulder, elbow], ...], lift, sit }
// angles in radians, 0 = straight down, positive = toward +x on screen
function poseAngles(o) {
  const ph = o.phase || 0, d = o.dir === undefined ? 1 : o.dir, P = o.pose || 'stand';
  const sway = Math.sin(TIME * 1.7 + (o.x || 0) * 0.01) * 0.03;
  switch (P) {
    case 'walk': { const k = Math.sin(ph * 6);
      return { legs: [[d * 0.42 * k, -d * 0.55 * Math.max(0, -k)], [-d * 0.42 * k, -d * 0.55 * Math.max(0, k)]],
               arms: [[-0.28 - d * 0.35 * k, 0.25], [0.28 + d * 0.35 * k, -0.25]], lift: Math.abs(Math.cos(ph * 6)) * 10 }; }
    case 'run': { const k = Math.sin(ph * 9);
      return { legs: [[d * 0.75 * k, -d * 1.1 * Math.max(0, -k) - 0.2 * d], [-d * 0.75 * k, -d * 1.1 * Math.max(0, k) - 0.2 * d]],
               arms: [[-0.35 - d * 0.7 * k, d * 1.5], [0.35 + d * 0.7 * k, d * 1.5]], lift: Math.abs(Math.cos(ph * 9)) * 26, lean: 0.08 * d }; }
    case 'sit': return { legs: [[-0.25, 0.25], [0.25, -0.25]], arms: [[-0.15, 0.9], [0.15, -0.9]], sit: true };
    case 'wave': { const w = Math.sin(TIME * 9) * 0.35;
      return { legs: [[-0.1, 0.05], [0.1, -0.05]], arms: [[-0.12 + sway, 0.1], [2.5, 0.6 + w]] }; }
    case 'point': return { legs: [[-0.1, 0.05], [0.1, -0.05]], arms: [[-0.12 + sway, 0.1], [d * 1.45, d * 0.05]] };
    case 'armsUp': { const w = Math.sin(TIME * 5) * 0.12; return { legs: [[-0.18, 0.05], [0.18, -0.05]], arms: [[-2.6 - w, -0.3], [2.6 + w, 0.3]], lift: Math.abs(Math.sin(TIME * 5)) * 14 }; }
    case 'hold': return { legs: [[-0.1, 0.05], [0.1, -0.05]], arms: [[-0.35, 1.5], [0.35, -1.5]] };
    case 'reach': return { legs: [[-0.12, 0.05], [0.12, -0.05]], arms: [[-0.12 + sway, 0.1], [d * 1.25, d * 0.15]] };
    case 'think': return { legs: [[-0.1, 0.05], [0.1, -0.05]], arms: [[-0.3, 1.6], [0.25, -2.3]] };
    case 'pockets': return { legs: [[-0.1, 0.05], [0.1, -0.05]], arms: [[-0.12, 0.45], [0.12, -0.45]], hidden: true };
    case 'hug': return { legs: [[-0.12, 0.05], [0.12, -0.05]], arms: [[-0.6, 1.9], [0.6, -1.9]] };
    case 'slump': return { legs: [[-0.1, 0.05], [0.1, -0.05]], arms: [[-0.05, 0.05], [0.05, -0.05]], slump: 1 };
    default: return { legs: [[-0.1 + sway, 0.05], [0.1 + sway, -0.05]], arms: [[-0.18 + sway, 0.12], [0.18 + sway, -0.12]] };
  }
}
function figure(o) {
  const s = o.s || 1, kid = o.kind === 'kid', A = poseAngles(o);
  const thigh = (kid ? 62 : 80) * s, shin = (kid ? 58 : 76) * s, legW = (kid ? 40 : 50) * s, lw = 6 * s;
  const bodyW = (kid ? 150 : 230) * s, bodyH = (kid ? 140 : 210) * s;
  const legLen = A.sit ? (thigh + shin) * 0.45 : (thigh + shin) * 0.97;
  const hipY = o.y - legLen - (A.lift || 0) * s, x = o.x;
  const pants = o.pants || PANTS;
  // legs (behind torso)
  const feet = [];
  [-1, 1].forEach((sd, i) => {
    const [a1, a2] = A.legs[i];
    if (A.sit) { // knees toward the viewer: short thighs, shins straight down, big knee caps
      const hx = x + sd * bodyW * 0.22, kx = x + sd * bodyW * 0.33, ky = hipY + thigh * 0.35;
      rr(kx - legW * 0.8, ky - legW * 0.9, legW * 1.6, legW * 1.6, legW * 0.8); fs(pants, lw);
      const l = limb(kx, ky, 0, shin * 0.6, 0, 1, legW, pants, lw); feet.push([l.fx, o.y - 8 * s, 0]);
    } else { const spread = (o.pose === 'walk' || o.pose === 'run') ? 0.05 : 0.2;
      const l = limb(x + sd * bodyW * spread, hipY, a1, thigh, a2, shin, legW, pants, lw); feet.push([l.fx, l.fy, l.end]); }
  });
  const dir = o.dir === undefined ? 0 : o.dir;
  feet.forEach(([fx, fy], i) => { const sd = i ? 1 : -1, f = dir || sd * 0.6;
    ctx.save(); ctx.translate(fx + f * 14 * s, fy + 6 * s); ctx.beginPath(); ctx.ellipse(0, 0, 34 * s, 17 * s, 0, 0, 7); fs(o.shoe || SHOE, lw * 0.8); ctx.restore(); });
  // torso + head (existing drawing; y is the torso bottom)
  const p = person(Object.assign({}, o, { y: hipY + 10 * s, lean: (o.lean || 0) + (A.lean || 0), bob: (o.bob || 0) + (A.slump ? 10 * s : 0) }));
  // arms (in front)
  const shY = hipY + 10 * s - bodyH + 42 * s, armW = (kid ? 36 : 46) * s;
  const up = (kid ? 62 : 78) * s, fore = (kid ? 58 : 72) * s;
  const top = o.top || C.hoodie, hands = [];
  if (!A.hidden) [-1, 1].forEach((sd, i) => {
    const [a1, a2] = A.arms[i];
    const l = limb(x + sd * bodyW * 0.38 + (o.lean || 0) * p.R * 0.3, shY, a1, up, a2, fore, armW, top, lw);
    hand(l.fx + Math.sin(l.end) * 10 * s, l.fy + Math.cos(l.end) * 10 * s, (kid ? 0.8 : 0.95) * s, -l.end + Math.PI / 2 * (sd > 0 ? 1 : -1) * 0, o.skin || C.skin);
    hands.push([l.fx, l.fy]);
  });
  else { for (const sd of [-1, 1]) line([x + sd * bodyW * 0.3, hipY - 30 * s, x + sd * bodyW * 0.18, hipY - 30 * s], 5 * s, shade(top, -0.3)); }
  return Object.assign(p, { hands, hipY, feet });
}
