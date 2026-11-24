"""Video #6 "What If You Met Yourself From 10 Years Ago?" — shot list (beat-synced at 80 BPM) + themed score.

Usage: python3 build.py <out_dir>
Then:  node ../../01-parents/render/render.js <out_dir> video 30 \
         ../../02-twenties/render/scenes20.js,../../05-days-left/render/scenes5.js,../../05-days-left/render/style2.js,../../assets/fx.js,../../assets/rig.js,scenes6.js
"""
import json, os, sys, wave
import numpy as np

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
SR = 44100
BEAT = 0.75          # 80 BPM; every shot length is a multiple of 2 beats so cuts land on the beat

def c(a, b, en, uk): return (a, b, en, uk)
WARM, BLUE, GOLD = 'rgba(255,170,90,1)', 'rgba(140,190,255,1)', 'rgba(255,215,140,1)'
# id, dur, captions, opts
STORY = [
    # ---- Act 1: the meeting (night, rain) ----
    ("rainCity", 7.5, [c(1.5, 6.6, "Another rainy night.", "Ще одна дощова ніч.")], dict(trans="fade", flashes=[2.2], grade="night", rim=BLUE, cam=[960, 540, 1.0, 960, 600, 1.12])),
    ("walkHome", 9, [c(1.0, 4.2, "Another ordinary day.", "Ще один звичайний день."), c(4.8, 8.4, "The same tired walk home.", "Та сама втомлена дорога додому.")], dict(grade="night", rim=BLUE, cam=[700, 600, 1.15, 760, 600, 1.05])),
    ("lampGlow", 9, [c(1.0, 4.8, "Then the streetlight did something *strange*.", "А потім ліхтар зробив щось дивне."), c(5.4, 8.6, "Someone was standing in the light.", "Хтось стояв у світлі.")], dict(grade="night", rim=GOLD, cam=[900, 600, 1.0, 1000, 620, 1.15])),
    ("reveal", 7.5, [c(1.0, 3.6, "It was *you*.", "Це був ти."), c(4.2, 7.0, "Fifteen years old.", "П'ятнадцятирічний.")], dict(trans="flash", shake=7, grade="night", rim=GOLD, leak='rgba(255,170,90,', cam=[1100, 640, 1.6, 1100, 620, 1.8])),
    ("title6", 7.5, [c(0.6, 6.8, "What if you met yourself from *10* *years* *ago?*", "А якби ти зустрів себе з минулого, на 10 років молодшого?")], dict(trans="fade")),
    # ---- Act 2: the questions ----
    ("meet", 9, [c(1.0, 4.0, "\"No way... is that *us*?\"", "«Не може бути... це ми?»"), c(4.6, 8.4, "He couldn't stop smiling.", "Він не міг перестати усміхатися.")], dict(grade="night", rim=GOLD, cam=[960, 640, 1.0, 960, 620, 1.06])),
    ("kidClose", 6, [c(0.6, 5.6, "\"Did we become a *musician*?\"", "«Ми стали музикантом?»")], dict(trans="whip", grade="night", rim=GOLD)),
    ("adultClose", 4.5, [c(1.0, 4.0, "\"...Not really.\"", "«...Не зовсім.»")], dict(grade="night", rim=BLUE, cam=[760, 600, 1.0, 760, 580, 1.08])),
    ("kidClose", 6, [c(0.6, 5.6, "\"Did we see the *ocean*?\"", "«Ми бачили океан?»")], dict(grade="night", rim=GOLD)),
    ("screenTime", 7.5, [c(2.8, 7.0, "\"I... watch videos about it.\"", "«Я... дивлюся про нього відео.»")], dict(trans="zoom", grade="night")),
    ("kidClose", 6, [c(0.6, 5.6, "\"Do we still *draw* every day?\"", "«А ми досі малюємо щодня?»")], dict(grade="night", rim=GOLD)),
    ("memoryDraw", 7.5, [c(1.0, 6.8, "You used to. *Every* single day.", "Колись — так. Щодня.")], dict(trans="fade", grade="memory", rim=WARM, cam=[960, 600, 1.0, 1000, 620, 1.1])),
    ("roomMess", 9, [c(1.0, 4.2, "He looked at your room.", "Він подивився на твою кімнату."), c(4.8, 8.4, "At your *life*.", "На твоє життя.")], dict(trans="whip", grade="cold", rim=BLUE, cam=[960, 560, 1.1, 900, 560, 1.0])),
    # ---- Act 3: the truth ----
    ("curb", 9, [c(1.2, 4.8, "\"What *happened* to us?\"", "«Що з нами сталося?»"), c(5.2, 8.4, "You didn't have an answer.", "У тебе не було відповіді.")], dict(grade="cold", rim=BLUE, cam=[960, 620, 1.0, 900, 640, 1.08])),
    ("dreamsCross", 9, [c(6.0, 8.8, "Every \"later\" crossed out a *dream*.", "Кожне «потім» закреслювало мрію.")], dict(trans="zoom", grade="cold", cam=[960, 540, 1.0, 960, 540, 1.06])),
    ("kidCloseSad", 6, [c(0.8, 5.6, "He wasn't angry.", "Він не злився.")], dict(grade="cold", rim=BLUE)),
    ("kidCloseCry", 6, [c(0.8, 5.6, "He was just... *disappointed*.", "Він був просто... розчарований.")], dict(grade="cold", rim=BLUE, cam=[1180, 760, 1.0, 1180, 720, 1.15])),
    ("card", 3, [], {}),
    # ---- Act 4: the gift ----
    ("giveBook", 9, [c(1.0, 4.0, "\"Here. Take it.\"", "«Ось. Тримай.»"), c(4.6, 8.4, "\"You still have *time*.\"", "«У тебе ще є час.»")], dict(trans="fade", grade="night", rim=GOLD, cam=[960, 640, 1.0, 960, 620, 1.08])),
    ("adultCloseCalm", 4.5, [c(1.0, 4.0, "\"And you?\"", "«А ти?»")], dict(grade="night", rim=GOLD)),
    ("fade", 10.5, [c(1.2, 4.6, "\"I'm just a memory.\"", "«Я — лише спогад.»"), c(5.2, 9.8, "\"*You're* the one who's real.\"", "«Справжній — це ти.»")], dict(grade="night", rim=GOLD, leak='rgba(255,190,110,', cam=[1150, 640, 1.2, 1150, 560, 1.35])),
    ("alone", 9, [c(1.0, 4.4, "\"Make me *proud*.\"", "«Зроби так, щоб я пишався.»"), c(5.0, 8.4, "The rain stopped.", "Дощ припинився.")], dict(grade="dawn", rim=WARM, cam=[960, 600, 1.15, 960, 560, 1.0])),
    # ---- Act 5: the rise ----
    ("desk6", 6, [c(0.8, 5.4, "*Day* *1.*", "День 1.")], dict(trans="flash", grade="warm", leak='rgba(255,180,100,', cam=[860, 600, 1.0, 840, 620, 1.1])),
    ("guitar6", 7.5, [c(0.6, 3.4, "Bad at first.", "Спершу погано."), c(4.2, 7.0, "Then a little *better*.", "Потім трохи краще.")], dict(trans="whip", grade="warm")),
    ("drawing6", 7.5, [c(0.8, 6.8, "Page after *page*.", "Сторінка за сторінкою.")], dict(trans="whip", grade="warm", cam=[1000, 560, 1.0, 1080, 560, 1.1])),
    ("run6", 6, [c(0.8, 5.4, "Every *morning*.", "Щоранку.")], dict(trans="whip", grade="dawn")),
    ("plane", 7.5, [c(0.8, 6.8, "The first *trip*.", "Перша подорож.")], dict(trans="whip", grade="warm", leak='rgba(255,200,130,')),
    ("oceanSee", 7.5, [c(0.8, 6.8, "The *ocean*. Finally.", "Океан. Нарешті.")], dict(trans="zoom", grade="warm", cam=[960, 640, 1.15, 960, 600, 1.0])),
    ("callMom6", 6, [c(0.8, 5.4, "And the call he kept *postponing*.", "І дзвінок, який він усе відкладав.")], dict(trans="whip", grade="warm")),
    ("checks", 9, [c(6.0, 8.8, "One dream at a *time*.", "Одна мрія за раз.")], dict(trans="flash", grade="warm", cam=[960, 540, 1.06, 960, 540, 1.0])),
    # ---- Act 6: ten years later ----
    ("tenYears", 13.5, [c(1.0, 6.2, "Ten years later, he came back to the same light.", "Через десять років він повернувся до того самого ліхтаря."),
                        c(6.8, 12.8, "This time, someone was waiting for *him*.", "Цього разу хтось чекав на нього.")], dict(trans="fade", grade="night", rim=GOLD, leak='rgba(255,190,110,', cam=[960, 620, 1.0, 1000, 600, 1.12])),
    ("card", 6, [c(0.8, 5.4, "Somewhere, 10 years from now...", "Десь, через 10 років...")], {}),
    ("card", 6, [c(0.8, 5.4, "...someone is counting on *you*.", "...хтось розраховує на тебе.")], {}),
    ("card", 7.5, [c(1.0, 6.6, "Make them *proud*.", "Зроби так, щоб вони пишалися.")], {}),
]

scenes, caps, t, seen = [], [], 0.0, {}
for sid, dur, lines, opt in STORY:
    base = sid.replace("Sad", "").replace("Cry", "").replace("Calm", "")
    t0 = seen.get(base, 0) if sid != "card" else 0
    seen[base] = t0 + dur
    sc = {"id": sid, "start": round(t, 3), "end": round(t + dur, 3), "t0": t0}
    sc.update(opt); scenes.append(sc)
    for a, b, en, uk in lines:
        caps.append({"start": t + a, "end": t + b, "en": en, "uk": uk.replace("*", ""), "scene": sid})
    t += dur
total = t
starts = {}
for s in scenes: starts.setdefault(s["id"], []).append(s["start"])
S0 = lambda sid, i=0: starts[sid][i]
END = lambda sid, i=0: [s["end"] for s in scenes if s["id"] == sid][i]

# ================= themed score =================
N = int((total + 3) * SR); L = np.zeros(N); R = np.zeros(N)
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
rng = np.random.default_rng(6)
def put(sig, at, pan=0.0, gain=1.0):
    i = int(at * SR); j = min(N, i + len(sig))
    if j <= i or i < 0: return
    L[i:j] += sig[:j - i] * gain * (1 - pan); R[i:j] += sig[:j - i] * gain * (1 + pan)
def env(n, a, r):
    e = np.ones(n); ai = max(1, int(a * SR)); ri = max(1, int(r * SR))
    e[:ai] = np.linspace(0, 1, ai)[:n]; e[-ri:] *= np.linspace(1, 0, ri)[-n:] if ri <= n else 1
    return e
def lp(x, k=8): return np.convolve(x, np.ones(k) / k, mode="same")
def piano(m, dur, amp):
    n = int(dur * SR); tt = np.arange(n) / SR; f = hz(m)
    e = np.exp(-tt * (1.6 + f / 900)) * np.minimum(1, tt * 300)
    return amp * e * sum(np.sin(2 * np.pi * f * k * tt * (1 + 0.0004 * k)) * np.exp(-tt * k * 0.6) / k ** 1.4 for k in range(1, 7))
def strings(ms, dur, amp, att=1.4, rel=1.6, bright=1.0):
    n = int(dur * SR); tt = np.arange(n) / SR; s = np.zeros(n)
    vib = 0.004 * np.sin(2 * np.pi * 5.2 * tt) * np.minimum(1, tt / 1.5)
    for m in ms:
        for det in (0.996, 1.0, 1.004):
            f = hz(m) * det
            ph = 2 * np.pi * f * (tt + np.cumsum(vib) / SR * 0)
            s += sum(np.sin(ph * k + vib * k * 40) / k * np.exp(-k * 0.35 / bright) for k in range(1, 9))
    return amp * s / (len(ms) * 3) * env(n, att, rel)
def pluck(m, amp, dur=1.2):
    n = int(dur * SR); tt = np.arange(n) / SR; f = hz(m)
    return amp * sum(np.sin(2 * np.pi * f * k * tt) / k ** 1.2 * np.exp(-tt * (5 + k * 3)) for k in range(1, 7)) * np.minimum(1, tt * 800)
def mbox(m, amp, dur=2.5):
    n = int(dur * SR); tt = np.arange(n) / SR; f = hz(m)
    return amp * (np.sin(2 * np.pi * f * tt) * np.exp(-tt * 2.2) + 0.35 * np.sin(2 * np.pi * f * 2.76 * tt) * np.exp(-tt * 5) + 0.15 * np.sin(2 * np.pi * f * 5.4 * tt) * np.exp(-tt * 9))
def drone(m, dur, amp):
    n = int(dur * SR); tt = np.arange(n) / SR
    return amp * env(n, 3, 3) * (np.sin(2 * np.pi * hz(m) * tt) + 0.5 * np.sin(2 * np.pi * hz(m) * 1.5 * tt) * (0.5 + 0.5 * np.sin(tt * 0.4)))
def kick(amp=0.5):
    n = int(0.35 * SR); tt = np.arange(n) / SR
    return amp * np.sin(2 * np.pi * (48 + 90 * np.exp(-tt * 28)) * tt) * np.exp(-tt * 7)
def snare(amp=0.25):
    n = int(0.25 * SR); tt = np.arange(n) / SR
    return amp * (rng.standard_normal(n) * np.exp(-tt * 18) * 0.7 + np.sin(2 * np.pi * 190 * tt) * np.exp(-tt * 25))
def hat(amp=0.06):
    n = int(0.06 * SR); x = rng.standard_normal(n); x = x - lp(x, 4)
    return amp * x * np.exp(-np.arange(n) / SR * 60)
def tick(amp=0.08):
    n = int(0.03 * SR); tt = np.arange(n) / SR
    return amp * np.sin(2 * np.pi * 2800 * tt) * np.exp(-tt * 300)
def riser(dur, amp=0.12):
    n = int(dur * SR); tt = np.arange(n) / SR; x = rng.standard_normal(n)
    sweep = np.sin(2 * np.pi * (200 * tt + 900 * tt ** 2 / dur))
    return amp * (lp(x, 6) * 0.6 + sweep * 0.25) * (tt / dur) ** 2
def impact(amp=0.6):
    n = int(2.5 * SR); tt = np.arange(n) / SR
    return amp * (np.sin(2 * np.pi * 38 * tt) * np.exp(-tt * 2.2) + lp(rng.standard_normal(n), 3) * 0.3 * np.exp(-tt * 9))
def thunder(amp=0.4):
    n = int(4 * SR); tt = np.arange(n) / SR
    return amp * lp(rng.standard_normal(n), 60) * 6 * np.exp(-tt * 1.1) * np.minimum(1, tt * 20)
def heartbeat(at, count, amp=0.45):
    for b in range(count):
        for off, a in ((0, amp), (0.22, amp * 0.7)):
            n = int(0.2 * SR); tt = np.arange(n) / SR
            put(a * np.sin(2 * np.pi * 52 * tt) * np.exp(-tt * 22), at + b * 0.9 + off)

AM, F, C, G, Em, Dm, E = [57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62], [52, 55, 59], [50, 53, 57], [52, 56, 59]
BAR = 4 * BEAT

# --- rain ambience through acts 1-4
r_end = END("alone")
n = int(r_end * SR); rn = lp(rng.standard_normal(n), 3) * 0.035
lvl = np.ones(n); lvl[-int(9 * SR):] = np.linspace(1, 0, int(9 * SR))
put(rn * lvl, 0, -0.2); put(lp(rng.standard_normal(n), 3) * 0.03 * lvl, 0, 0.2)

# --- Act 1: mystery (clock ticks + drone + minor music box), thunder, riser -> impact on reveal
a1, rv = 0, S0("reveal")
put(drone(45, S0("title6") + 3, 0.05), 0)
x = 0.0
while x < S0("lampGlow"): put(tick(), x, 0.3); x += BEAT
put(thunder(0.45), 2.3)
for i, m in enumerate([76, 72, 69, 71, 72, 69, 64, 68]):
    put(mbox(m, 0.05), S0("lampGlow") + i * BEAT * 1.5, 0.2 * (i % 2 * 2 - 1))
put(riser(4.0, 0.14), rv - 4.0)
put(impact(0.7), rv); put(strings([57, 64, 69], 7.5, 0.05), rv)
put(impact(0.8), S0("title6") + 0.4); put(strings([45, 52, 57, 64], 7.5, 0.07, att=0.3), S0("title6") + 0.4)
for i, m in enumerate([69, 72, 76, 81]): put(mbox(m, 0.05), S0("title6") + 1.5 + i * BEAT)

# --- Act 2: playful plucks + shaker, music-box melody; darker on roomMess
p0, p1 = S0("meet"), S0("roomMess")
chords, k = [C, G, AM, F], 0
x = p0
while x < p1 - 0.1:
    ch = chords[k % 4]
    put(strings([n - 12 for n in ch], BAR + 1, 0.025), x)
    for b, idx in enumerate([0, 2, 1, 2, 0, 2, 1, 2]):
        put(pluck(ch[idx] + 12, 0.07), x + b * BEAT / 2, 0.25 * (1 if b % 2 else -1))
    for b in range(8): put(hat(0.03 if b % 2 else 0.05), x + b * BEAT / 2, 0.4)
    if k % 2 == 0:
        for i, m in enumerate([79, 76, 74, 76]): put(mbox(m, 0.035), x + i * BEAT, -0.2)
    x += BAR; k += 1
put(strings([45, 52, 60], END("roomMess") - p1 + 1, 0.05), p1)
for i in range(6): put(piano([64, 60, 57][i % 3], 3, 0.05), p1 + i * 1.5)

# --- Act 3: piano + strings, minor, slow; silence on the card
s0, s1 = S0("curb"), S0("card")
x, k = s0, 0
while x < s1 - 0.1:
    ch = [AM, F, C, G][k % 4]
    put(strings(ch, BAR + 1.5, 0.05, att=1.0), x)
    for b, m in enumerate([ch[0], ch[2], ch[1] + 12, ch[2]]): put(piano(m, 3, 0.06), x + b * BEAT)
    x += BAR; k += 1
put(piano(57, 4, 0.08), S0("dreamsCross") + 6.0)

# --- Act 4: heartbeat -> swelling strings, chimes on the dissolve
g0 = S0("giveBook")
heartbeat(g0 + 0.5, 9, 0.35)
x, k = g0, 0
while x < END("alone") - 0.1:
    ch = [C, G, AM, F][k % 4]
    put(strings([n for n in ch] + [ch[0] - 12], BAR + 1.5, 0.045 + 0.01 * k, att=1.2), x)
    put(piano(ch[0] - 12, 3, 0.07), x)
    x += BAR; k += 1
f0 = S0("fade")
for i in range(16): put(mbox([84, 88, 91, 86][i % 4], 0.03), f0 + 2 + i * 0.4, 0.4 * np.sin(i))
put(riser(3.0, 0.13), S0("desk6") - 3.0)

# --- Act 5: drums + bass + piano 8ths + strings, building
d0, d1 = S0("desk6"), S0("tenYears")
put(impact(0.6), d0)
x, k = d0, 0
while x < d1 - 0.1:
    ch = [C, G, AM, F][k % 4]; g = 1 + 0.4 * (x - d0) / (d1 - d0)
    for b in range(4):
        if b in (0, 2): put(kick(0.45 * g), x + b * BEAT)
        if b in (1, 3): put(snare(0.18 * g), x + b * BEAT, 0.1)
    for b in range(8): put(hat(0.04 * g), x + b * BEAT / 2, 0.35)
    put(piano(ch[0] - 24, BAR, 0.10 * g), x)
    for b, idx in enumerate([0, 1, 2, 4, 2, 1, 0, 2]):
        m = ch[idx % 3] + 12 * (idx // 3)
        put(piano(m, 1.8, 0.05 * g), x + b * BEAT / 2, 0.2 * np.sin(b))
    put(strings(ch, BAR + 1, 0.035 * g, att=0.6), x)
    x += BAR; k += 1
put(impact(0.5), S0("checks"))

# --- Act 6: full strings + melody, warm resolve on the cards
e0 = S0("tenYears"); x, k = e0, 0
while x < total - 0.1:
    ch = [F, C, G, AM, F, C, G, C][k % 8]
    put(strings(ch + [ch[0] - 12], BAR + 2, 0.06, att=1.0), x)
    put(piano(ch[0] - 12, 3.5, 0.08), x)
    mel = [[72, 76], [79, 76], [74, 79], [76, 72], [77, 81], [79, 76], [74, 71], [72, 72]][k % 8]
    put(piano(mel[0], 2.5, 0.07), x); put(piano(mel[1], 2.5, 0.06), x + 2 * BEAT)
    x += BAR; k += 1

# ---- reverb, master
def reverb(x, secs=2.8, wet=0.3):
    n = int(secs * SR); ir = rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 2.8); ir[0] = 0; ir /= np.sqrt((ir ** 2).sum())
    size = 1 << int(np.ceil(np.log2(len(x) + n)))
    y = np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(ir, size), size)[: len(x)]
    return x * (1 - wet) + y * wet * 1.3
L, R = reverb(L), reverb(R)
cs = S0("card"); g0_, g1_ = int(cs * SR), int((cs + 3.0) * SR)
for ch in (L, R):
    ch[g0_ - int(0.6 * SR):g0_] *= np.linspace(1, 0, int(0.6 * SR)); ch[g0_:g1_] = 0
mx = max(np.abs(L).max(), np.abs(R).max()); L, R = L / mx * 0.89, R / mx * 0.89
fo = int(3 * SR); tot = int(total * SR)
st = np.stack([L, R], 1)[:tot]; st[-fo:] *= np.linspace(1, 0, fo)[:, None]
with wave.open(os.path.join(OUT, "mix.wav"), "w") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(st, -1, 1) * 32767).astype(np.int16).tobytes())
json.dump({"duration": total, "scenes": scenes, "captions": caps}, open(os.path.join(OUT, "timeline.json"), "w"), ensure_ascii=False, indent=1)
def ts(s):
    ms = int(round(s * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); sec, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{sec:02},{ms:03}"
for lang in ("en", "uk"):
    with open(os.path.join(OUT, f"subtitles_{lang}.srt"), "w") as f:
        for i, cc in enumerate(caps, 1):
            f.write(f"{i}\n{ts(cc['start'])} --> {ts(cc['end'])}\n{cc[lang].replace('*', '')}\n\n")
# chapters for the description
acts = [("rainCity", "The meeting"), ("meet", "The questions"), ("curb", "The truth"), ("giveBook", "The gift"), ("desk6", "Day 1"), ("tenYears", "Ten years later")]
with open(os.path.join(OUT, "chapters.txt"), "w") as f:
    for sid, name in acts:
        s = 0 if sid == "rainCity" else S0(sid); f.write(f"{int(s // 60)}:{int(s % 60):02} {name}\n")
print(f"total {total:.1f}s = {int(total // 60)}:{int(total % 60):02}, scenes {len(scenes)}")
