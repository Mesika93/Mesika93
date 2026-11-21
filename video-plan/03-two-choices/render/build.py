"""Video #3 "Same Day. Two Choices." — split-screen, text-only (~4:15).

Usage: python3 build.py <out_dir>
Then:  node ../../01-parents/render/render.js <out_dir> video 30 ../../02-twenties/render/scenes20.js,scenes3.js
"""
import json, os, sys, wave
import numpy as np

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
SR = 44100

def LR(l_en, l_uk, r_en, r_uk, d=12):
    return [(1.5, d - 0.6, l_en, l_uk, "L"), (4.0, d - 0.6, r_en, r_uk, "R")]

STORY = [
    ("title3", 7, []),
    ("card", 6, [(0.8, 5.4, "Same person. Same 24 hours.", "Та сама людина. Ті самі 24 години.", None)]),
    ("sAlarm", 12, LR("Snooze.", "Ще 5 хвилин.", "Get up.", "Встає.")),
    ("sPhone", 12, LR("Scroll.", "Гортає стрічку.", "Move.", "Рухається.")),
    ("sFood", 12, LR("Easy.", "Як простіше.", "Better.", "Як краще.")),
    ("sWork", 12, LR("\"Later.\"", "«Потім.»", "Now.", "Зараз.")),
    ("sMoney", 12, LR("Spends.", "Витрачає.", "Saves.", "Відкладає.")),
    ("sSocial", 12, LR("Ignores her call.", "Ігнорує її дзвінок.", "Calls Mom.", "Дзвонить мамі.")),
    ("sExcuse", 12, LR("\"I'll start Monday.\"", "«Почну з понеділка.»", "Starts today.", "Починає сьогодні.")),
    ("sNight", 12, LR("3 AM. Again.", "3 ночі. Знову.", "Sleeps on time.", "Спить вчасно.")),
    ("card", 5, [(0.8, 4.4, "One day doesn't matter.", "Один день нічого не вирішує.", None)]),
    ("card", 4, [(0.6, 3.6, "Or does it?", "Чи все-таки вирішує?", None)]),
    ("day1", 10, [(4.0, 9.4, "Day 1. No difference.", "День 1. Різниці немає.", None)]),
    ("day30", 11, [(3.0, 10.4, "Day 30. Small changes.", "День 30. Маленькі зміни.", None)]),
    ("sWeekend", 12, LR("Alone again.", "Знову сам.", "New friends.", "Нові друзі.")),
    ("day100", 11, [(3.0, 10.4, "Day 100. You can see it now.", "День 100. Тепер це видно.", None)]),
    ("sMirror", 12, LR("\"What happened to me?\"", "«Що зі мною сталося?»", "\"I'm proud of you.\"", "«Я тобою пишаюсь.»")),
    ("day180", 11, [(3.0, 10.4, "Day 180. Two different people.", "День 180. Дві різні людини.", None)]),
    ("day365", 13, [(3.0, 12.2, "Day 365. Same start. Different life.", "День 365. Той самий старт. Різне життя.", None)]),
    ("card", 5, [(0.8, 4.4, "One year later, they met.", "Через рік вони зустрілися.", None)]),
    ("meet", 22, [(2.0, 6.4, "\"Who are you?\"", "«Хто ти?»", None),
                  (7.0, 12.4, "\"I'm who you could have been.\"", "«Я той, ким ти міг стати.»", None),
                  (13.0, 17.6, "\"Is it too late?\"", "«Вже запізно?»", None),
                  (18.0, 21.4, "\"Not if you start tomorrow.\"", "«Ні, якщо почнеш завтра.»", None)]),
    ("card", 6, [(0.8, 5.4, "Same 24 hours.", "Ті самі 24 години.", None)]),
    ("card", 6, [(0.8, 5.4, "Different choices.", "Різний вибір.", None)]),
    ("finalwake", 11, [(5.0, 10.4, "Tomorrow, 6:00 AM.", "Завтра, 6:00.", None)]),
    ("card", 8, [(1.0, 7.0, "Which one will you be?", "Яким будеш ти?", None)]),
]

scenes, caps, t = [], [], 0.0
for sid, dur, lines in STORY:
    scenes.append({"id": sid, "start": round(t, 3), "end": round(t + dur, 3), "cut": False})
    for a, b, en, uk, side in lines:
        caps.append({"start": t + a, "end": t + b, "en": en, "uk": uk, "scene": sid, "side": side})
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
sad = [AM, F, C, G]; warm = [C, G, AM, F]; drive = [AM, F, C, G]
ARP = [0, 1, 2, 4, 2, 1, 0, 2]
def kick(at, amp=0.35):
    n = int(0.25 * SR); tt = np.arange(n) / SR
    put(amp * np.sin(2 * np.pi * (45 + 60 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 9), at)
# title: two-note hit (dark + bright)
put(piano(45, 6, 0.14) + piano(57, 6, 0.08), S0("title3") + 0.4); put(piano(64, 6, 0.08) + piano(72, 6, 0.06), S0("title3") + 1.6)
# routine montage: steady pulse, arpeggio, grows
r0, r1 = S0("sAlarm"), S0("card", 1)
section(r0, r1, drive, 0.5, ARP, 0.05, 0.04, bass=0.07, grow=0.8,
        mel=lambda k: [(0, [76, 77, 79, 74][k % 4], 1.5), (4, [72, 72, 74, 71][k % 4], 1.5)] if k >= 4 else [])
x = r0
while x < r1 - 1:
    kick(x, 0.22); x += 1.0
# question cards: almost silence, single notes
put(piano(64, 4, 0.06), S0("card", 1) + 0.5); put(piano(62, 4, 0.06), S0("card", 2) + 0.4)
# days 1..365: building, brighter as it goes
d0, d1 = S0("day1"), S0("card", 3)
section(d0, d1, warm, 0.5, ARP, 0.05, 0.045, bass=0.07, grow=1.3,
        mel=lambda k: [(0, [76, 74, 72, 72][k % 4], 1.5), (3, [79, 79, 76, 77][k % 4], 1.0), (4, [77, 74, 76, 72][k % 4], 2.5)] if k >= 6 else [])
x = S0("day100")
while x < d1 - 1:
    kick(x, 0.25); x += 1.0
# meet: emotional, sparse then lifting
m0 = S0("meet")
section(m0 + 0.5, m0 + 12, sad, 0.6, [0, None, 2, None, 4, None, 2, None], 0.06, 0.05)
section(m0 + 12, S0("finalwake"), warm, 0.5, ARP, 0.06, 0.05, bass=0.08, grow=0.8)
# final: alarm then bright chords
fw = S0("finalwake")
for i in range(4):
    n = int(0.12 * SR); tt = np.arange(n) / SR
    for j in range(2): put(0.12 * np.sign(np.sin(2 * np.pi * 1800 * tt)) * 0.5, fw + 0.5 + i * 0.5 + j * 0.16)
put(piano(48, 7, 0.10) + piano(60, 7, 0.07) + piano(64, 7, 0.06) + piano(67, 7, 0.05), fw + 4.0)
section(fw + 4.5, total, warm, 0.5, ARP, 0.05, 0.04, oct_=12)
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
