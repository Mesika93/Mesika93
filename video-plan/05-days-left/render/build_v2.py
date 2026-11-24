"""Video #5 "What If You Could See How Many Days You Have Left?" — v2: Ifverse-like visuals, shot list with camera moves.

Usage: python3 build.py <out_dir>
Then:  node ../../01-parents/render/render.js <out_dir> video 30 ../../02-twenties/render/scenes20.js,scenes5.js,style2.js
"""
import json, os, sys, wave
import numpy as np

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
SR = 44100

def LR(l_en, l_uk, r_en, r_uk, d=12):
    return [(1.5, d - 0.6, l_en, l_uk, "L"), (4.0, d - 0.6, r_en, r_uk, "R")]

def c(a, b, en, uk): return (a, b, en, uk, None)
# (scene, duration, captions, camera [cx0, cy0, zoom0, cx1, cy1, zoom1] or None)
WIDE = None
STORY = [
    ("title5", 7, [], None),
    ("cityOpen", 8, [], [960, 540, 1.0, 960, 600, 1.12]),
    ("wake5", 8, [], [900, 560, 1.0, 860, 580, 1.08]),
    ("wake5", 5, [c(0.3, 4.6, "One morning, you see a number above your head.", "Одного ранку ти бачиш число над своєю головою.")], [820, 500, 1.6, 820, 470, 1.9]),
    ("mirror5", 8, [c(1.5, 7.4, "17,412. Days left.", "17 412. Днів залишилось.")], [1000, 520, 1.05, 1180, 460, 1.35]),
    ("street", 10, [c(1.5, 8.4, "Everyone has one.", "Воно є в кожного.")], [960, 600, 1.0, 960, 560, 1.06]),
    ("street", 4, [c(0.3, 3.6, "Some are big.", "У когось велике.")], [960, 640, 2.0, 960, 620, 2.2]),
    ("street", 5, [c(0.6, 4.6, "Some are not.", "У когось — ні.")], [1290, 660, 2.1, 1290, 640, 2.5]),
    ("gaming5", 8, [c(1.5, 7.4, "\"17,000 days. Plenty of time.\"", "«17 000 днів. Ще купа часу.»")], [960, 560, 1.0, 960, 500, 1.15]),
    ("scroll5", 8, [c(1.5, 7.4, "So you spend them like you always did.", "Тож ти витрачаєш їх, як завжди.")], [960, 540, 1.0, 960, 600, 1.12]),
    ("phone5", 7, [c(3.4, 6.6, "Mom calls. \"Later.\"", "Дзвонить мама. «Потім.»")], [960, 540, 1.0, 960, 540, 1.1]),
    ("bus5", 7, [c(1.0, 6.6, "Then one Sunday, you finally went home.", "А потім однієї неділі ти нарешті поїхав додому.")], [700, 600, 1.0, 680, 620, 1.1]),
    ("doorMom", 7, [c(0.8, 6.4, "She was so happy to see you.", "Вона так тобі зраділа.")], [960, 560, 1.0, 1000, 560, 1.05]),
    ("doorMom", 6, [c(0.8, 5.6, "And then you saw her number.", "А потім ти побачив її число.")], [1250, 560, 1.6, 1250, 500, 2.1]),
    ("card", 4, [c(0.6, 3.6, "214.", "214.")], None),
    ("grid214", 14, [c(4.0, 8.6, "That's 30 Sundays.", "Це 30 неділь."), c(9.2, 13.4, "30 Sunday dinners. If you come.", "30 недільних обідів. Якщо ти приїдеш.")], None),
    ("cry5", 8, [c(1.5, 7.4, "You had thousands of days.", "У тебе були тисячі днів.")], [960, 600, 1.0, 960, 640, 1.15]),
    ("card", 5, [c(0.8, 4.4, "She had 214.", "У неї — 214.")], None),
    ("card", 4, [c(0.6, 3.6, "So you changed everything.", "Тож ти змінив усе.")], None),
    ("dinner5", 8, [c(1.0, 7.4, "Every Sunday at her table.", "Щонеділі за її столом.")], [960, 560, 1.0, 900, 560, 1.12]),
    ("cook", 8, [c(1.0, 7.4, "She taught you her recipes.", "Вона навчила тебе своїх рецептів.")], [1040, 640, 1.15, 1000, 600, 1.0]),
    ("album5", 8, [c(1.0, 7.4, "You asked about her life.", "Ти розпитував про її життя.")], [960, 700, 1.25, 960, 640, 1.05]),
    ("mom5", 7, [c(1.0, 6.4, "On the days you couldn't come, you called.", "У дні, коли не міг приїхати, — дзвонив.")], [860, 560, 1.0, 860, 520, 1.2]),
    ("walkMom", 8, [c(1.0, 7.4, "You stopped counting your days.", "Ти перестав рахувати свої дні.")], [960, 600, 1.08, 960, 560, 1.0]),
    ("stars", 8, [c(1.0, 7.4, "You started making them count.", "Ти почав робити так, щоб вони щось важили.")], [960, 400, 1.2, 960, 560, 1.0]),
    ("bench5", 13, [c(2.0, 12.4, "And when her number reached zero...", "А коли її число дійшло до нуля...")], None),
    ("card", 3, [], None),
    ("emptyChair", 10, [c(1.5, 9.4, "...you had no regrets.", "...ти ні про що не шкодував.")], [900, 600, 1.0, 860, 600, 1.1]),
    ("emptyChair", 6, [c(0.6, 5.6, "Only memories.", "Лише спогади.")], [1020, 640, 2.0, 1020, 640, 2.4]),
    ("closeup5", 12, [c(1.5, 5.6, "You can't see your number.", "Ти не бачиш свого числа."), c(6.6, 11.4, "But it's counting.", "Але воно рахує.")], [960, 560, 1.0, 960, 520, 1.12]),
    ("card", 6, [c(0.8, 5.4, "Everyone you love has a number.", "У кожного, кого ти любиш, є своє число.")], None),
    ("card", 6, [c(0.8, 5.4, "Don't wait to see it.", "Не чекай, поки побачиш його.")], None),
    ("card", 7, [c(1.0, 6.2, "Call them today.", "Подзвони їм сьогодні.")], None),
]

scenes, caps, t = [], [], 0.0
seen = {}
for sid, dur, lines, cam in STORY:
    t0 = seen.get(sid, 0) if sid not in ("card",) else 0   # repeated shot of the same scene continues its action
    seen[sid] = t0 + dur
    scenes.append({"id": sid, "start": round(t, 3), "end": round(t + dur, 3), "cut": sid not in ("card", "title5", "grid214"), "cam": cam, "t0": t0})
    for a_, b_, en, uk, side in lines:
        caps.append({"start": t + a_, "end": t + b_, "en": en, "uk": uk, "scene": sid, "side": side})
    t += dur
total = t
starts = {}
for s in scenes:
    starts.setdefault(s["id"], []).append(s["start"])
S0 = lambda sid, i=0: starts[sid][i]

# ---------------- music ----------------
N = int((total + 2) * SR)
L = np.zeros(N); Rr = np.zeros(N)
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
rng = np.random.default_rng(1)

def put(sig, at, pan=0.0):
    i = int(at * SR); j = min(N, i + len(sig))
    if j <= i: return
    L[i:j] += sig[: j - i] * (1 - pan) ; Rr[i:j] += sig[: j - i] * (1 + pan)

def piano(m, dur, amp):
    n = int(dur * SR); tt = np.arange(n) / SR; f = hz(m)
    env = np.exp(-tt * (1.6 + f / 900)) * np.minimum(1, tt * 300)
    s = sum(np.sin(2 * np.pi * f * k * tt * (1 + 0.0004 * k)) * np.exp(-tt * k * 0.6) / k ** 1.4 for k in range(1, 7))
    return amp * env * s

def pad(ms, dur, amp, bright=0.3):
    n = int(dur * SR); tt = np.arange(n) / SR
    env = np.minimum(1, tt / 2.0) * np.minimum(1, (dur - tt) / 2.0)
    s = np.zeros(n)
    for m in ms:
        f = hz(m)
        for det in (0.997, 1.0, 1.003):
            s += np.sin(2 * np.pi * f * det * tt) + bright * np.sin(4 * np.pi * f * det * tt) / 2
    return amp * env * s / (len(ms) * 3)

def drone(m, dur, amp):
    n = int(dur * SR); tt = np.arange(n) / SR
    env = np.minimum(1, tt / 3) * np.minimum(1, (dur - tt) / 3)
    return amp * env * (np.sin(2 * np.pi * hz(m) * tt) + 0.5 * np.sin(2 * np.pi * hz(m) * 1.5 * tt) * (0.5 + 0.5 * np.sin(tt * 0.4)))

def section(t0, t1, chords, beat, pattern, amp_p, amp_pad, mel=None, bass=0.0, oct_=0, grow=0.0):
    x, k = t0, 0
    while x < t1 - 0.5:
        ch = chords[k % len(chords)]; g = 1 + grow * (x - t0) / max(1, t1 - t0)
        bar = beat * len(pattern)
        put(pad([n + oct_ - 12 for n in ch], min(bar + 1.5, t1 - x + 1.5), amp_pad * g), x)
        if bass: put(piano(ch[0] - 24, bar, bass * g), x)
        for b, idx in enumerate(pattern):
            if idx is None: continue
            n = ch[idx % 3] + 12 * (idx // 3) + oct_
            put(piano(n, 2.5, amp_p * g * (0.85 + 0.3 * rng.random())), x + b * beat, pan=0.3 * np.sin(b))
        if mel:
            for (off, n, d) in mel(k):
                put(piano(n + oct_ + 12, d + 1.5, amp_p * 1.25 * g), x + off * beat)
        x += bar; k += 1

AM, F, C, G, Em, Dm = [57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62], [52, 55, 59], [50, 53, 57]
sad = [AM, F, C, G]; warm = [C, G, AM, F]; myst = [AM, Em, F, G]
ARP = [0, 1, 2, 4, 2, 1, 0, 2]
def kick(at, amp=0.3):
    n = int(0.25 * SR); tt = np.arange(n) / SR
    put(amp * np.sin(2 * np.pi * (45 + 60 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 9), at)
def chime(m, at, amp=0.06):
    n = int(3 * SR); tt = np.arange(n) / SR
    put(amp * np.sin(2 * np.pi * hz(m) * tt) * np.exp(-tt * 1.5) + amp * 0.4 * np.sin(2 * np.pi * hz(m) * 2.76 * tt) * np.exp(-tt * 3), at)
put(piano(45, 6, 0.14) + piano(57, 6, 0.08) + piano(64, 6, 0.07), 0.4)
# mystery: music box over drone (wake, mirror, street)
w0, w1 = S0("cityOpen"), S0("gaming5")
put(drone(45, w1 - w0, 0.04), w0)
section(w0 + 1, w1, myst, 0.5, ARP, 0.045, 0.03, oct_=12)
for s in [S0("wake5") + 3.2, S0("wake5", 1) + 0.2, S0("mirror5") + 0.3]: chime(88, s, 0.07)
# wasting: dull pulse
g0, g1 = S0("gaming5"), S0("doorMom")
section(g0, g1, sad, 0.55, ARP, 0.045, 0.04, bass=0.05)
# home + reveal: warm, then hit + silence on 214
h0 = S0("doorMom", 1)
section(S0("doorMom"), h0 + 1.5, warm, 0.5, ARP, 0.05, 0.04)
put(piano(41, 6, 0.18) + piano(53, 6, 0.10) + piano(60, 6, 0.08), h0 + 2.0)
for b in range(8):
    for off, a in ((0, 0.45), (0.22, 0.3)):
        n = int(0.2 * SR); tt = np.arange(n) / SR
        put(a * np.sin(2 * np.pi * 52 * tt) * np.exp(-tt * 22), h0 + 2.6 + b * 0.9 + off)
# grid / cry: sad piano
section(S0("grid214"), S0("card", 2), sad, 0.6, [0, None, 2, None, 4, None, 2, None], 0.06, 0.045)
# change: warm, growing
c0, c1 = S0("card", 2), S0("bench5")
section(c0 + 1, c1, warm, 0.5, ARP, 0.055, 0.045, bass=0.07, grow=1.0,
        mel=lambda k: [(0, [76, 74, 72, 72][k % 4], 1.5), (3, [79, 79, 76, 77][k % 4], 1.0), (4, [77, 74, 76, 72][k % 4], 2.5)] if k >= 2 else [])
# bench: emotional peak, then silence, empty chair lone piano
section(c1, S0("card", 3), sad, 0.6, ARP, 0.06, 0.06, bass=0.07)
e0 = S0("emptyChair")
for i, n in enumerate([64, 62, 60, 57, 60, 64]): put(piano(n, 4, 0.06), e0 + 1 + i * 2.2)
# closeup & end: warm resolve
section(S0("closeup5"), S0("card", 4), warm, 0.5, ARP, 0.045, 0.04, oct_=12)
end0 = S0("card", 4)
put(piano(48, 7, 0.10) + piano(60, 7, 0.07) + piano(64, 7, 0.06) + piano(67, 7, 0.05), end0 + 0.3)
put(piano(53, 7, 0.09) + piano(60, 7, 0.06) + piano(69, 7, 0.05), end0 + 6.3)
put(piano(48, 8, 0.11) + piano(55, 8, 0.07) + piano(64, 8, 0.06) + piano(72, 8, 0.05), end0 + 12.4)
def buzz(dur, amp=0.15):
    tt = np.arange(int(dur * SR)) / SR
    return amp * np.sign(np.sin(2 * np.pi * 150 * tt)) * (tt % 1.0 < 0.55) * 0.6
put(buzz(2.4), S0("phone5"))
# silence the beat right after the reveal and before the empty chair
# reverb (FFT convolution with decaying noise)
def reverb(x, secs=2.6, wet=0.28):
    n = int(secs * SR); ir = rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 3.0); ir[0] = 0
    ir /= np.sqrt((ir ** 2).sum())
    size = 1 << int(np.ceil(np.log2(len(x) + n)))
    y = np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(ir, size), size)[: len(x)]
    return x * (1 - wet) + y * wet * 1.3
L, Rr = reverb(L), reverb(Rr)
mx = max(np.abs(L).max(), np.abs(Rr).max()); L, Rr = L / mx * 0.89, Rr / mx * 0.89
fo = int(3 * SR); L[-fo:] *= np.linspace(1, 0, fo); Rr[-fo:] *= np.linspace(1, 0, fo)
st = np.stack([L, Rr], 1)[: int(total * SR)]
with wave.open(os.path.join(OUT, "mix.wav"), "w") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(st, -1, 1) * 32767).astype(np.int16).tobytes())

json.dump({"duration": total, "scenes": scenes, "captions": caps}, open(os.path.join(OUT, "timeline.json"), "w"), ensure_ascii=False, indent=1)
def ts(s):
    ms = int(round(s * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); sec, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{sec:02},{ms:03}"
for lang in ("en", "uk"):
    with open(os.path.join(OUT, f"subtitles_{lang}.srt"), "w") as f:
        for i, c in enumerate(caps, 1):
            f.write(f"{i}\n{ts(c['start'])} --> {ts(c['end'])}\n{c[lang]}\n\n")
print(f"total {total:.0f}s = {int(total // 60)}:{int(total % 60):02}, scenes {len(scenes)}")
