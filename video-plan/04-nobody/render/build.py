"""Video #4 "Nobody Is Coming To Save You." — text-only (~4:15).

Usage: python3 build.py <out_dir>
Then:  node ../../01-parents/render/render.js <out_dir> video 30 ../../02-twenties/render/scenes20.js,scenes4.js
"""
import json, os, sys, wave
import numpy as np

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
SR = 44100

def LR(l_en, l_uk, r_en, r_uk, d=12):
    return [(1.5, d - 0.6, l_en, l_uk, "L"), (4.0, d - 0.6, r_en, r_uk, "R")]

def c(a, b, en, uk): return (a, b, en, uk, None)
STORY = [
    ("floor", 13, [c(1.5, 6.0, "Everything is falling apart.", "Все розвалюється."), c(7.0, 12.4, "And you're waiting.", "А ти чекаєш.")]),
    ("doorWait", 13, [c(1.5, 6.0, "Waiting for someone to come.", "Чекаєш, що хтось прийде."), c(7.0, 12.4, "Someone to fix it all.", "Хтось, хто все виправить.")]),
    ("title4", 7, []),
    ("hopeFriend", 9, [c(6.2, 8.6, "Not your friends.", "Не друзі.")]),
    ("hopeGirl", 9, [c(4.0, 8.6, "Not her.", "Не вона.")]),
    ("hopeLuck", 9, [c(7.0, 8.8, "Not luck.", "Не удача.")]),
    ("hopeMoment", 9, [c(4.0, 8.6, "Not the \"perfect moment\".", "Не «ідеальний момент».")]),
    ("excuses", 16, [c(1.5, 5.4, "\"If only I had money...\"", "«Якби в мене були гроші...»"),
                     c(6.0, 9.6, "\"If only I had time...\"", "«Якби в мене був час...»"),
                     c(10.4, 15.4, "Every excuse became a brick.", "Кожна відмовка ставала цеглиною.")]),
    ("walled", 12, [c(2.0, 11.4, "Until you built your own prison.", "Поки ти не збудував собі в'язницю.")]),
    ("daysPass", 14, [c(1.5, 6.4, "Days passed.", "Минали дні."), c(7.4, 13.4, "The door never opened.", "Двері так і не відчинилися.")]),
    ("card", 5, [c(0.8, 4.4, "Nobody is coming.", "Ніхто не прийде.")]),
    ("card", 4, []),
    ("mirror4", 12, [c(1.5, 5.8, "But there was one person...", "Але була одна людина..."), c(6.6, 11.4, "...who could change everything.", "...яка могла все змінити.")]),
    ("card", 4, [c(0.6, 3.6, "You.", "Ти.")]),
    ("brickBreak", 11, [c(3.6, 10.4, "It starts with one brick.", "Все починається з однієї цеглини.")]),
    ("fall", 10, [c(5.0, 9.4, "You will fall.", "Ти падатимеш.")]),
    ("bandage", 10, [c(1.5, 4.6, "Nobody will patch you up.", "Ніхто тебе не залатає."), c(6.0, 9.4, "So you do it yourself.", "Тож ти робиш це сам.")]),
    ("help", 10, [c(1.0, 4.4, "People can help.", "Люди можуть допомогти."), c(5.0, 9.4, "But nobody can stand up for you.", "Але ніхто не встане замість тебе.")]),
    ("climb", 10, [c(2.0, 9.4, "Get back up. Again. And again.", "Вставай. Знову. І знову.")]),
    ("gym", 9, [c(1.5, 8.4, "Nobody will do the work for you.", "Ніхто не зробить роботу за тебе.")]),
    ("read", 9, [c(1.5, 8.4, "Nobody will learn for you.", "Ніхто не вчитиметься за тебе.")]),
    ("run", 9, [c(1.5, 8.4, "Nobody will run your race.", "Ніхто не пробіжить твою дистанцію.")]),
    ("doorOpen", 14, [c(1.0, 4.6, "No one opened the door.", "Ніхто не відчинив двері."), c(8.0, 13.4, "So you opened it yourself.", "Тож ти відчинив їх сам.")]),
    ("summit", 13, [c(3.0, 11.6, "Nobody is coming to save you.", "Ніхто не прийде тебе рятувати.")]),
    ("card", 6, [c(0.8, 5.4, "So save yourself.", "Тож врятуй себе сам.")]),
    ("card", 7, [c(1.0, 6.2, "Start today.", "Почни сьогодні.")]),
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
sad = [AM, F, C, G]; warm = [C, G, AM, F]; dark = [AM, Em, F, Dm]
ARP = [0, 1, 2, 4, 2, 1, 0, 2]
def kick(at, amp=0.3):
    n = int(0.25 * SR); tt = np.arange(n) / SR
    put(amp * np.sin(2 * np.pi * (45 + 60 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 9), at)
# opening: drone + lonely piano
put(drone(45, S0("title4"), 0.05), 0)
for i, at in enumerate(np.arange(1.5, S0("title4") - 1.5, 3.2)):
    put(piano([64, 62, 60, 59, 57][i % 5], 4, 0.05), at)
put(piano(45, 6, 0.16) + piano(57, 6, 0.10) + piano(64, 6, 0.08), S0("title4") + 0.4)
# hopes: sparse sad
section(S0("hopeFriend"), S0("excuses"), sad, 0.6, [0, None, 2, None, 4, None, 2, None], 0.055, 0.04)
# excuses / walled / days: dark, growing, with slow pulse
section(S0("excuses"), S0("card", 0), dark, 0.55, ARP, 0.05, 0.05, bass=0.07, grow=0.8)
x = S0("excuses")
while x < S0("card", 0) - 1: kick(x, 0.18); x += 1.1
# "Nobody is coming." single note, then silence card, mirror: lone notes
put(piano(57, 5, 0.07), S0("card", 0) + 0.6)
for i, n in enumerate([60, 64, 67, 72]): put(piano(n, 4, 0.06), S0("mirror4") + 1 + i * 2.6)
put(piano(48, 5, 0.12) + piano(60, 5, 0.08) + piano(67, 5, 0.06), S0("card", 2) + 0.4)
# rise: building, kick, climax at door
r0, r1 = S0("brickBreak"), S0("card", 3)
section(r0, r1, warm, 0.5, ARP, 0.06, 0.05, bass=0.08, grow=1.4,
        mel=lambda k: [(0, [76, 74, 72, 72][k % 4], 1.5), (3, [79, 79, 76, 77][k % 4], 1.0), (4, [77, 74, 76, 72][k % 4], 2.5)] if k >= 3 else [])
x = S0("climb")
while x < r1 - 1: kick(x, 0.26); x += 1.0
end0 = S0("card", 3)
put(piano(48, 7, 0.10) + piano(60, 7, 0.07) + piano(64, 7, 0.06) + piano(67, 7, 0.05), end0 + 0.3)
put(piano(53, 8, 0.09) + piano(60, 8, 0.06) + piano(69, 8, 0.05), end0 + 6.3)
# SFX: brick thuds while the wall grows, crack when the first brick falls, door creak
ex = S0("excuses")
for i in range(44):
    at = ex + 1.0 + i * (16 - 2.0) / 44
    n = int(0.12 * SR); tt = np.arange(n) / SR
    put(0.10 * np.sin(2 * np.pi * 80 * tt) * np.exp(-tt * 40) + 0.04 * rng.standard_normal(n) * np.exp(-tt * 60), at)
n = int(0.6 * SR); tt = np.arange(n) / SR
put(0.35 * rng.standard_normal(n) * np.exp(-tt * 12), S0("brickBreak") + 2.6)
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
