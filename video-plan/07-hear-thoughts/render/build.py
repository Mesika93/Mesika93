"""Video #7 "What If You Could Hear What People Really Think?" — shot list (beat-synced, 80 BPM) + themed score.

Usage: python3 build.py <out_dir>
Then:  node ../../01-parents/render/render.js <out_dir> video 30 \
         ../../02-twenties/render/scenes20.js,../../05-days-left/render/scenes5.js,../../05-days-left/render/style2.js,../../assets/fx.js,../../assets/rig.js,scenes7.js
"""
import json, os, sys, wave
import numpy as np

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
SR = 44100
BEAT = 0.75          # 80 BPM; every shot length is a multiple of 2 beats so cuts land on the beat

def c(a, b, en, uk): return (a, b, en, uk)
WARM, BLUE, GOLD = 'rgba(255,170,90,1)', 'rgba(140,190,255,1)', 'rgba(255,215,140,1)'
STORY = [
    # ---- Act 1: the gift ----
    ("cityOpen", 6, [], dict(trans="fade", grade="dawn", cam=[960, 540, 1.0, 960, 600, 1.1])),
    ("wake7", 10.5, [c(1.0, 4.4, "One morning, the world got *loud*.", "Одного ранку світ став гучним."), c(5.0, 8.4, "Whispers. Everywhere.", "Шепіт. Звідусіль.")], dict(grade="night", cam=[900, 560, 1.0, 860, 560, 1.1])),
    ("streetMorning", 10.5, [c(1.0, 4.4, "Then you realized...", "А потім ти зрозумів..."), c(5.0, 8.4, "...you could hear what people were *thinking*.", "...що чуєш, про що думають люди.")], dict(trans="whip", grade="warm")),
    ("title7", 7.5, [c(0.6, 6.8, "What if you could hear what people *really* think?", "А якби ти чув, що люди насправді думають?")], dict(trans="fade")),
    # ---- Act 2: the fear ----
    ("metroFear", 12, [c(1.0, 4.8, "On the train, everyone was thinking...", "У метро всі про щось думали..."), c(5.6, 10.0, "...about *you*. Or so it felt.", "...про тебе. Принаймні так здавалося.")], dict(trans="cut", grade="cold", cam=[960, 600, 1.0, 900, 600, 1.08])),
    ("fearClose", 6, [c(0.6, 5.6, "\"They think I'm *weird*.\"", "«Вони думають, що я дивний.»")], dict(trans="zoom", grade="cold", shake=4)),
    ("officeFear", 10.5, [c(1.0, 8.4, "At work, you kept your head *down*.", "На роботі ти не піднімав голови.")], dict(trans="whip", grade="cold", cam=[960, 560, 1.06, 960, 600, 1.0])),
    ("mirror7", 10.5, [c(4.0, 8.4, "You rehearsed every *word*.", "Ти репетирував кожне слово.")], dict(trans="cut", grade="cold", cam=[960, 540, 1.0, 900, 520, 1.08])),
    ("postDraft", 7.5, [c(5.0, 7.2, "You deleted every *post*.", "Ти видаляв кожен допис.")], dict(trans="zoom", grade="cold")),
    ("cafeFear", 10.5, [c(1.0, 4.2, "You wanted to say hi.", "Ти хотів привітатися."), c(5.0, 8.4, "You *didn't*.", "Але не привітався.")], dict(trans="whip", grade="cold", cam=[960, 600, 1.0, 1000, 600, 1.08])),
    ("imagine", 7.5, [c(4.0, 7.2, "Because you *knew* what she'd think.", "Бо ти «знав», що вона подумає.")], dict(trans="flash", shake=6, grade="cold")),
    ("smaller", 10.5, [c(1.5, 8.4, "Every day, you made yourself *smaller*.", "Щодня ти робив себе меншим.")], dict(trans="fade", grade="night", cam=[900, 640, 1.0, 900, 620, 1.12])),
    # ---- Act 3: the truth ----
    ("card", 4.5, [c(0.6, 4.0, "Then one day, you finally *listened*.", "А потім одного дня ти нарешті прислухався.")], {}),
    ("metroTruth", 13.5, [c(7.0, 11.4, "Nobody was thinking about *you*.", "Ніхто не думав про тебе.")], dict(trans="flash", grade="none", cam=[960, 560, 1.06, 960, 560, 1.0])),
    ("officeTruth", 10.5, [c(4.0, 8.4, "They were scared of the *same* thing.", "Вони боялися того самого.")], dict(trans="whip", grade="none")),
    ("cafeTruth", 10.5, [c(4.5, 8.4, "Even *her*.", "Навіть вона.")], dict(trans="whip", grade="warm", cam=[1100, 600, 1.0, 1250, 560, 1.25])),
    ("strangers", 12, [c(5.6, 10.0, "Everyone was fighting a battle you couldn't *see*.", "Кожен вів свою битву, якої ти не бачив.")], dict(trans="cut", grade="warm")),
    ("laugh", 7.5, [c(1.0, 7.0, "Everyone was too busy worrying about *themselves*.", "Всі були надто зайняті тривогами про себе.")], dict(trans="zoom", grade="warm", leak='rgba(255,200,120,')),
    ("card", 6, [c(0.8, 5.4, "Nobody is watching you as closely as you *think*.", "Ніхто не стежить за тобою так пильно, як тобі здається.")], {}),
    # ---- Act 4: freedom ----
    ("freeWalk", 9, [c(0.8, 6.8, "So you stopped *hiding*.", "Тож ти перестав ховатися.")], dict(trans="flash", grade="warm", leak='rgba(255,190,110,')),
    ("parkDraw", 10.5, [c(1.0, 8.4, "You drew in the park. In *public*.", "Ти малював у парку. Прилюдно.")], dict(trans="whip", grade="warm", cam=[960, 640, 1.12, 960, 600, 1.0])),
    ("openMic", 10.5, [c(1.0, 4.6, "You sang at an open mic.", "Ти заспівав на відкритому мікрофоні."), c(5.2, 10.0, "*Badly*. And nobody cared.", "Погано. І всім було байдуже.")], dict(trans="whip", grade="warm", cam=[960, 620, 1.1, 960, 600, 1.0])),
    ("sayHi", 12, [c(1.0, 4.4, "You said *hi*.", "Ти привітався."), c(5.0, 10.0, "She'd been waiting for someone to.", "Вона якраз на це чекала.")], dict(trans="whip", grade="warm", leak='rgba(255,180,120,')),
    ("finalCrowd", 13.5, [c(1.0, 3.8, "Everyone still has their thoughts.", "У кожного й далі свої думки."), c(6.0, 11.4, "Yours just got *quieter*.", "Просто твої стали тихішими.")], dict(trans="fade", grade="warm", leak='rgba(255,190,110,', cam=[960, 600, 1.0, 960, 560, 1.1])),
    ("card", 6, [c(0.8, 5.4, "They're not thinking about you.", "Вони не думають про тебе.")], {}),
    ("card", 7.5, [c(1.0, 6.6, "So live like nobody's *listening*.", "Тож живи так, ніби ніхто не слухає.")], {}),
]

scenes, caps, t, seen = [], [], 0.0, {}
for sid, dur, lines, opt in STORY:
    base = sid
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

def whisper(dur, amp=0.05):
    n = int(dur * SR); x = rng.standard_normal(n); x = x - lp(x, 3); x = lp(x, 2)
    tt = np.arange(n) / SR; trem = 0.5 + 0.5 * np.sin(2 * np.pi * (5 + rng.random() * 4) * tt)
    return amp * x * trem * env(n, 0.2, 0.3)
def pop(amp=0.08):
    n = int(0.12 * SR); tt = np.arange(n) / SR
    return amp * np.sin(2 * np.pi * (500 + 900 * tt / 0.12) * tt) * np.exp(-tt * 30)
def clap(amp=0.12):
    n = int(0.15 * SR); return amp * rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 35)
Db = [49, 52, 56]

# --- Act 1: curious music box + whispers
put(piano(52, 5, 0.06) + piano(64, 5, 0.04), 0.3)
x = S0("wake7")
while x < S0("title7"):
    for i, m in enumerate([76, 79, 83, 79]): put(mbox(m, 0.035), x + i * BEAT, 0.3 * (1 if i % 2 else -1))
    x += BAR
for i in range(10): put(whisper(0.8 + rng.random(), 0.05), S0("wake7") + 2.5 + i * 0.6, rng.uniform(-0.8, 0.8))
for i in range(12): put(whisper(0.6, 0.035), S0("streetMorning") + 1 + i * 0.6, rng.uniform(-0.8, 0.8))
put(riser(2.5, 0.1), S0("title7") - 2.5); put(impact(0.6), S0("title7") + 0.4); put(strings([45, 52, 57, 64], 7.5, 0.06, att=0.3), S0("title7") + 0.4)

# --- Act 2: anxious pulse (8ths), dissonant strings, heartbeat, growing whispers
a0, a1 = S0("metroFear"), S0("card")
x, k = a0, 0
while x < a1 - 0.1:
    ch = [AM, F, Dm, E][k % 4]
    for b in range(8):
        n = int(0.18 * SR); tt = np.arange(n) / SR
        put(0.07 * np.sin(2 * np.pi * hz(ch[0] - 24) * tt) * np.exp(-tt * 14), x + b * BEAT / 2)
    put(strings(ch + [ch[0] + 1], BAR + 1, 0.035, att=0.8), x)
    if k % 2 == 0: put(piano(ch[2] + 12, 3, 0.04), x)
    x += BAR; k += 1
heartbeat(S0("fearClose") + 0.3, 6, 0.4); heartbeat(S0("imagine") + 0.3, 8, 0.45)
for sid in ("metroFear", "fearClose", "officeFear", "cafeFear", "imagine"):
    for i in range(8 if sid != "imagine" else 14): put(whisper(0.7, 0.045), S0(sid) + 0.5 + i * 0.55, rng.uniform(-0.9, 0.9))
for i in range(5): put(impact(0.18), S0("imagine") + 0.4 + i * 0.7)

# --- Act 3: silence -> single notes -> playful pizzicato as thoughts pop -> warm
t3 = S0("metroTruth")
for i, m in enumerate([72, 76, 79]): put(piano(m, 3, 0.06), t3 + 0.3 + i * 0.6)
x, k = t3 + 2 * BEAT, 0
while x < S0("laugh") - 0.1:
    ch = [C, F, G, C][k % 4]
    for b, idx in enumerate([0, 2, 1, 2, 0, 2, 1, 2]): put(pluck(ch[idx] + 12, 0.07), x + b * BEAT / 2, 0.25 * (1 if b % 2 else -1))
    put(strings([n - 12 for n in ch], BAR + 1, 0.025), x)
    x += BAR; k += 1
for sid, cnt in (("metroTruth", 4), ("officeTruth", 2), ("cafeTruth", 1), ("strangers", 4)):
    starts_ = [0.8 + i * 1.3 for i in range(cnt)] if sid == "metroTruth" else [0.6 + i * 1.2 for i in range(cnt)]
    for s in starts_: put(pop(0.09), S0(sid) + s, rng.uniform(-0.5, 0.5))
l0 = S0("laugh")
x, k = l0, 0
while x < S0("freeWalk") - 0.1:
    ch = [C, G, AM, F][k % 4]; put(strings(ch + [ch[0] - 12], BAR + 1.5, 0.05, att=0.8), x); put(piano(ch[0] - 12, 3, 0.07), x); x += BAR; k += 1

# --- Act 4: freedom groove: kick/snare/claps/hats, bass, bright piano, build to the end
f0, f1 = S0("freeWalk"), S0("card", 2)
put(impact(0.6), f0)
x, k = f0, 0
while x < f1 - 0.1:
    ch = [C, G, AM, F][k % 4]; g = 1 + 0.4 * (x - f0) / (f1 - f0)
    for b in range(4):
        if b in (0, 2): put(kick(0.45 * g), x + b * BEAT)
        if b in (1, 3): put(snare(0.14 * g), x + b * BEAT, 0.1); put(clap(0.1 * g), x + b * BEAT, -0.2)
    for b in range(8): put(hat(0.04 * g), x + b * BEAT / 2, 0.35)
    put(piano(ch[0] - 24, BAR, 0.10 * g), x)
    for b, idx in enumerate([0, 1, 2, 4, 2, 4, 1, 2]): put(pluck(ch[idx % 3] + 12 * (1 + idx // 3), 0.06 * g), x + b * BEAT / 2, 0.2 * np.sin(b))
    put(strings(ch, BAR + 1, 0.03 * g, att=0.6), x)
    if k % 2 == 1:
        mel = [[79, 76], [81, 79], [77, 76], [76, 72]][(k // 2) % 4]
        put(piano(mel[0], 2, 0.06 * g), x); put(piano(mel[1], 2, 0.05 * g), x + 2 * BEAT)
    x += BAR; k += 1
for i in range(12): put(clap(0.08), S0("openMic") + 6.5 + i * 0.25, rng.uniform(-0.6, 0.6))
# --- final cards: warm resolve
e0 = S0("card", 2)
put(piano(48, 7, 0.10) + piano(60, 7, 0.07) + piano(64, 7, 0.06) + piano(67, 7, 0.05), e0 + 0.3)
put(strings([48, 55, 64, 72], 13, 0.05, att=1.0), e0)
put(piano(53, 8, 0.09) + piano(60, 8, 0.06) + piano(69, 8, 0.05) + piano(72, 8, 0.05), e0 + 6.3)

# ---- reverb, master
def reverb(x, secs=2.8, wet=0.3):
    n = int(secs * SR); ir = rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 2.8); ir[0] = 0; ir /= np.sqrt((ir ** 2).sum())
    size = 1 << int(np.ceil(np.log2(len(x) + n)))
    y = np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(ir, size), size)[: len(x)]
    return x * (1 - wet) + y * wet * 1.3
L, R = reverb(L), reverb(R)
cs = S0("card"); g0_, g1_ = int(cs * SR), int((cs + 0.6) * SR)
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
acts = [("cityOpen", "The whispers"), ("metroFear", "The fear"), ("metroTruth", "What they really think"), ("freeWalk", "Freedom"), ("finalCrowd", "Quieter")]
with open(os.path.join(OUT, "chapters.txt"), "w") as f:
    for sid, name in acts:
        s = 0 if sid == "cityOpen" else S0(sid); f.write(f"{int(s // 60)}:{int(s % 60):02} {name}\n")
print(f"total {total:.1f}s = {int(total // 60)}:{int(total % 60):02}, scenes {len(scenes)}")
