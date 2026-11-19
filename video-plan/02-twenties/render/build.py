"""Video #2 "Don't Waste Your 20s." — text-only (~4:15): timeline + music + SFX.

Usage: python3 build.py <out_dir>
Then:  node ../../01-parents/render/render.js <out_dir> video 30 scenes20.js
"""
import json, os, sys, wave
import numpy as np

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
SR = 44100

STORY = [
    ("mirror", 11, [(1.5, 5.4, "Tomorrow you turn 30.", "Завтра тобі 30."),
                    (6.0, 10.4, "Where did ten years go?", "Куди поділися десять років?")]),
    ("title", 7, []),
    ("card", 5, [(0.8, 4.4, "Let's go back.", "Повернімося назад.")]),
    ("age20", 12, [(1.5, 5.6, "At 20, you had dreams.", "У 20 у тебе були мрії."),
                   (6.4, 11.4, "And all the time in the world.", "І весь час світу.")]),
    ("gaming", 8, [(1.5, 7.4, "\"I'll start tomorrow.\"", "«Почну завтра.»")]),
    ("alarm", 8, [(5.0, 7.6, "Snooze.", "Ще 5 хвилин.")]),
    ("scroll", 8, [(1.5, 7.4, "Just one more video.", "Ще одне відео.")]),
    ("typing", 9, [(7.2, 8.8, "Never sent.", "Так і не надіслав.")]),
    ("years", 14, [(1.5, 6.4, "Tomorrow became next week.", "Завтра стало наступним тижнем."),
                   (7.0, 13.2, "Next week became next year.", "Наступний тиждень — наступним роком.")]),
    ("feed", 10, [(1.0, 4.6, "Everyone moved forward.", "Всі рушили вперед."),
                  (5.4, 9.4, "You stayed the same.", "А ти залишився тим самим.")]),
    ("dustwall", 11, [(1.0, 5.2, "Your dreams didn't die.", "Твої мрії не померли."),
                      (5.8, 10.4, "You just stopped visiting them.", "Ти просто перестав до них приходити.")]),
    ("hourglass", 12, [(1.0, 5.2, "Every day you waited...", "Кожен день, який ти чекав..."),
                       (5.8, 11.4, "is a day you will never get back.", "це день, який ніколи не повернеш.")]),
    ("days", 14, [(6.0, 13.2, "How many did you really live?", "Скільки з них ти справді прожив?")]),
    ("cake30", 12, [(1.5, 5.6, "30 candles.", "30 свічок."),
                    (6.4, 11.4, "And a wish you've made ten times before.", "І бажання, яке ти загадував уже десять разів.")]),
    ("card", 4, []),
    ("wakeup", 11, [(3.0, 10.4, "What if you got one more chance?", "А якби в тебе був ще один шанс?")]),
    ("card", 6, [(0.8, 5.4, "You do. It's called today.", "Він є. Він називається «сьогодні».")]),
    ("drawer", 8, [(4.6, 7.6, "Day 1.", "День 1.")]),
    ("run", 9, [(1.5, 8.4, "It will hurt.", "Буде боляче.")]),
    ("gym", 9, [(1.5, 8.4, "You will want to quit.", "Тобі захочеться кинути.")]),
    ("read", 9, [(1.5, 8.4, "Do it anyway.", "Все одно роби.")]),
    ("guitar", 9, [(1.5, 8.4, "One day at a time.", "Один день за раз.")]),
    ("mom", 8, [(1.5, 7.4, "And call your mom.", "І подзвони мамі.")]),
    ("daysfill", 10, [(2.0, 9.2, "Make these days count.", "Зроби так, щоб ці дні мали значення.")]),
    ("summit", 13, [(3.0, 11.6, "Your 20s are not a waiting room.", "Твої 20 — це не зал очікування.")]),
    ("card", 6, [(0.8, 5.4, "You're not running out of time.", "У тебе не закінчується час.")]),
    ("card", 6, [(0.8, 5.4, "You're running out of excuses.", "У тебе закінчуються відмовки.")]),
    ("card", 7, [(1.0, 6.2, "Start today.", "Почни сьогодні.")]),
]
scenes, caps, t = [], [], 0.0
for sid, dur, lines in STORY:
    scenes.append({"id": sid, "start": round(t, 3), "end": round(t + dur, 3), "cut": sid in ("alarm", "scroll")})
    for a, b, en, uk in lines:
        caps.append({"start": t + a, "end": t + b, "en": en, "uk": uk, "scene": sid})
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
sad = [AM, F, C, G]; warm = [C, G, AM, F]; dark = [AM, Em, F, Dm]
ARP = [0, 1, 2, 4, 2, 1, 0, 2]
# 1) mirror: drone + lonely notes; title hit
put(drone(45, S0("title"), 0.05), 0)
for i, at in enumerate(np.arange(1.5, S0("title") - 1.5, 3.0)):
    put(piano([64, 62, 60, 59][i % 4], 4, 0.05), at)
put(piano(45, 6, 0.16) + piano(57, 6, 0.10) + piano(64, 6, 0.08), S0("title") + 0.4)
# 2) age 20: hopeful music box
section(S0("card", 0) + 1.0, S0("gaming"), warm, 0.5, ARP, 0.05, 0.035, oct_=12,
        mel=lambda k: [(0, [67, 67, 69, 65][k % 4], 1.5), (4, [64, 62, 64, 60][k % 4], 1.5)])
# 3) procrastination -> decay: dark, slowly growing
section(S0("gaming"), S0("days"), dark, 0.55, ARP, 0.05, 0.045, bass=0.06, grow=0.7,
        mel=lambda k: [(0, [76, 76, 77, 74][k % 4], 2.0), (4, [72, 71, 72, 69][k % 4], 2.0)] if k >= 3 else [])
# 4) days: pad + heartbeat
h0 = S0("days")
put(pad([45, 52, 57], 14, 0.05, bright=0.1), h0)
for bt in range(10):
    for off, a in ((0, 0.5), (0.22, 0.32)):
        n = int(0.2 * SR); tt = np.arange(n) / SR
        put(a * np.sin(2 * np.pi * 52 * tt) * np.exp(-tt * 22), h0 + 5.0 + bt * 0.9 + off)
# 5) cake: lone piano, then silence card
for i, n in enumerate([64, 62, 60, 57, 55]):
    put(piano(n, 4, 0.06), S0("cake30") + 1 + i * 2.2)
# 6) wakeup: bright chord + music box, then lift to the end
put(piano(60, 6, 0.10) + piano(64, 6, 0.08) + piano(67, 6, 0.07) + piano(72, 6, 0.06), S0("wakeup") + 0.6)
section(S0("wakeup") + 3.5, S0("drawer"), warm, 0.5, ARP, 0.04, 0.03, oct_=12)
lift0, end0 = S0("drawer"), S0("card", 3)
section(lift0, end0, warm, 0.5, ARP, 0.06, 0.05, bass=0.08, grow=1.3,
        mel=lambda k: [(0, [76, 74, 72, 72][k % 4], 1.5), (3, [79, 79, 76, 77][k % 4], 1.0), (4, [77, 74, 76, 72][k % 4], 2.5)] if k >= 2 else [])
put(piano(48, 7, 0.10) + piano(60, 7, 0.07) + piano(64, 7, 0.06) + piano(67, 7, 0.05), end0 + 0.3)
put(piano(53, 7, 0.09) + piano(60, 7, 0.06) + piano(69, 7, 0.05), end0 + 6.3)
put(piano(48, 8, 0.11) + piano(55, 8, 0.07) + piano(64, 8, 0.06) + piano(72, 8, 0.05), end0 + 12.4)

# SFX: alarm beeps, typing clicks, pen of phone drawer
a0 = S0("alarm")
for i in range(5):
    n = int(0.12 * SR); tt = np.arange(n) / SR
    for j in range(2): put(0.12 * np.sign(np.sin(2 * np.pi * 1800 * tt)) * 0.5, a0 + 0.8 + i * 0.5 + j * 0.16)
t0 = S0("typing")
for i in range(20):
    n = int(0.03 * SR); put(0.08 * rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 200), t0 + 0.8 + i * 0.16 + rng.random() * 0.05)
for i in range(16):
    n = int(0.03 * SR); put(0.06 * rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 200), t0 + 5.0 + i * 0.125)
n = int(0.4 * SR); tt = np.arange(n) / SR
put(0.4 * rng.standard_normal(n) * np.exp(-tt * 20) + 0.3 * np.sin(2 * np.pi * 90 * tt) * np.exp(-tt * 12), S0("drawer") + 4.6)
# reverb (FFT convolution with decaying noise)
def reverb(x, secs=2.6, wet=0.28):
    n = int(secs * SR); ir = rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 3.0); ir[0] = 0
    ir /= np.sqrt((ir ** 2).sum())
    size = 1 << int(np.ceil(np.log2(len(x) + n)))
    y = np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(ir, size), size)[: len(x)]
    return x * (1 - wet) + y * wet * 1.3
L, Rr = reverb(L), reverb(Rr)
# silence the dramatic gap exactly
g0, g1 = int(S0("card", 1) * SR), int((S0("card", 1) + 3.6) * SR)
fade = np.linspace(1, 0, int(0.8 * SR))
for ch in (L, Rr):
    ch[g0 - len(fade):g0] *= fade; ch[g0:g1] = 0
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
