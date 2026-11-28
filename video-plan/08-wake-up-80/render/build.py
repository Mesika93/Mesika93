"""Video #8 "What If You Woke Up At 80?" — shot list (beat-synced, 80 BPM) + themed score.

Usage: python3 build.py <out_dir>
Then:  node ../../01-parents/render/render.js <out_dir> video 30 \
         ../../02-twenties/render/scenes20.js,../../05-days-left/render/scenes5.js,../../05-days-left/render/style2.js,../../assets/fx.js,../../assets/rig.js,../../07-hear-thoughts/render/scenes7.js,scenes8.js
"""
import json, os, sys, wave
import numpy as np

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
SR = 44100
BEAT = 0.75          # 80 BPM; every shot length is a multiple of 2 beats so cuts land on the beat

def c(a, b, en, uk): return (a, b, en, uk)
WARM, BLUE, GOLD = 'rgba(255,170,90,1)', 'rgba(140,190,255,1)', 'rgba(255,215,140,1)'
STORY = [
    # ---- Act 1: falling asleep, waking up old ----
    ("couchNight", 10.5, [c(1.0, 4.6, "\"Just five more minutes.\"", "«Ще п'ять хвилин.»"), c(6.0, 10.0, "You fell asleep with the phone in your hand.", "Ти заснув із телефоном у руці.")], dict(trans="fade", grade="night", cam=[960, 600, 1.0, 960, 560, 1.12])),
    ("timeWarp", 6, [c(1.0, 5.4, "And the minutes kept *going*.", "А хвилини все йшли.")], dict(trans="flash", shake=5)),
    ("wake80", 10.5, [c(1.0, 4.4, "You woke up.", "Ти прокинувся."), c(5.0, 10.0, "Something felt... *wrong*.", "Щось було... не так.")], dict(trans="flash", grade="warm", cam=[960, 600, 1.08, 960, 600, 1.0])),
    ("hands80", 6, [c(0.8, 5.4, "Your hands were *shaking*.", "Твої руки тремтіли.")], dict(trans="zoom", grade="warm")),
    ("mirror80", 10.5, [c(4.5, 10.0, "You were *80*.", "Тобі було 80.")], dict(trans="cut", grade="none", shake=0, cam=[960, 540, 1.0, 900, 520, 1.1])),
    ("title8", 7.5, [c(0.6, 6.8, "What if you woke up at *80*?", "А якби ти прокинувся у 80?")], dict(trans="fade")),
    # ---- Act 2: the future ----
    ("cal2081", 6, [c(1.8, 5.6, "*2081*.", "2081.")], dict(trans="whip", grade="warm")),
    ("futureStreet", 13.5, [c(1.0, 5.6, "The world had moved on.", "Світ рушив далі."), c(6.6, 13.0, "*Without* you.", "Без тебе.")], dict(trans="whip", grade="night", cam=[960, 600, 1.0, 1000, 600, 1.06])),
    ("futureLookUp", 7.5, [c(1.0, 7.0, "Everything you meant to see... you missed.", "Усе, що ти збирався побачити... ти пропустив.")], dict(trans="cut", grade="night")),
    ("friendsHouse", 9, [c(1.0, 8.4, "Your best friend's house had a new name on the door.", "На дверях дому твого найкращого друга було чуже прізвище.")], dict(trans="whip", grade="warm", cam=[1000, 600, 1.0, 1100, 580, 1.1])),
    # ---- Act 3: everything you postponed ----
    ("tryRun", 10.5, [c(1.0, 3.2, "You tried to run.", "Ти спробував побігти."), c(4.2, 10.0, "Like you always *planned* to.", "Як завжди планував.")], dict(trans="whip", grade="warm")),
    ("tryGuitar", 10.5, [c(1.0, 10.0, "You tried to play. Your fingers wouldn't *listen*.", "Ти спробував заграти. Пальці не слухались.")], dict(trans="whip", grade="warm", cam=[960, 600, 1.0, 960, 580, 1.08])),
    ("callMom80", 12, [c(7.0, 11.4, "You called Mom.", "Ти подзвонив мамі.")], dict(trans="zoom", grade="none")),
    ("card", 3, [], {}),
    ("photoWall", 10.5, [c(1.0, 10.0, "All the photos you never *took*.", "Усі фото, яких ти так і не зробив.")], dict(trans="fade", grade="warm", cam=[1000, 560, 1.0, 1050, 520, 1.08])),
    ("screen80", 7.5, [c(3.6, 7.0, "Twenty-one years. On a *screen*.", "Двадцять один рік. В екрані.")], dict(trans="zoom", grade="none")),
    # ---- Act 4: the question ----
    ("benchKid", 13.5, [c(1.0, 4.4, "A kid sat down next to you.", "Поруч сів хлопчик."), c(6.0, 13.0, "\"Mister... what's the best part of life?\"", "«Пане... а що в житті найкраще?»")], dict(trans="fade", grade="warm", leak='rgba(255,180,110,', cam=[960, 640, 1.0, 1000, 620, 1.08])),
    ("oldClose", 10.5, [c(1.5, 10.0, "\"Everything you keep *postponing*.\"", "«Усе, що ти постійно відкладаєш.»")], dict(trans="cut", grade="warm", leak='rgba(255,180,110,')),
    ("closeEyes", 6, [], dict(trans="flash")),
    # ---- Act 5: second chance ----
    ("wakeYoung", 10.5, [c(1.0, 4.4, "You woke up.", "Ти прокинувся."), c(5.4, 10.0, "*25*. It was 6 AM.", "25. Шоста ранку.")], dict(trans="flash", grade="warm", cam=[960, 600, 1.1, 960, 600, 1.0])),
    ("windowSun", 9, [c(1.0, 8.4, "It was just a dream. You still had *time*.", "Це був лише сон. У тебе ще був час.")], dict(trans="whip", grade="dawn", leak='rgba(255,200,130,')),
    ("callMomYoung", 9, [c(1.0, 8.4, "\"Mom? I'm coming this *Sunday*.\"", "«Мам? Я приїду цієї неділі.»")], dict(trans="whip", grade="warm")),
    ("runYoung", 6, [c(0.8, 5.4, "You ran. Because you *could*.", "Ти побіг. Бо міг.")], dict(trans="whip", grade="dawn")),
    ("guitarYoung", 6, [c(0.8, 5.4, "You played. Because you still *can*.", "Ти заграв. Бо ще можеш.")], dict(trans="whip", grade="warm")),
    ("benchMom", 10.5, [c(1.0, 9.4, "And you sat with her. Just *sat*.", "І ти посидів із нею. Просто посидів.")], dict(trans="fade", grade="warm", leak='rgba(255,190,110,', cam=[960, 620, 1.0, 960, 600, 1.1])),
    ("card", 6, [c(0.8, 5.4, "You won't wake up at 80 tomorrow.", "Завтра ти не прокинешся у 80.")], {}),
    ("card", 6, [c(0.8, 5.4, "But you will *someday*.", "Але колись — так.")], {}),
    ("card", 7.5, [c(1.0, 6.6, "Make it worth *remembering*.", "Зроби так, щоб було що згадати.")], {}),
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

def bleep(m, amp=0.04, dur=0.18):
    n = int(dur * SR); tt = np.arange(n) / SR
    return amp * np.sign(np.sin(2 * np.pi * hz(m) * tt)) * 0.5 * np.exp(-tt * 18)
def reverse_swell(dur, amp=0.12):
    n = int(dur * SR); tt = np.arange(n) / SR
    return amp * lp(rng.standard_normal(n), 4) * (tt / dur) ** 3 + strings([60, 64, 67, 72], dur, amp * 0.6, att=dur * 0.9, rel=0.05)

# --- Act 1: lullaby music box -> accelerating clock -> time-warp swell -> impact
put(drone(45, S0("timeWarp"), 0.04), 0)
x = 0.5
while x < S0("timeWarp") - 0.5:
    for i, m in enumerate([76, 72, 69, 72]): put(mbox(m, 0.035), x + i * BEAT * 1.5, 0.25 * (1 if i % 2 else -1))
    x += BAR * 1.5
x, gap = S0("couchNight") + 5, BEAT
while x < S0("timeWarp") + 5.5:
    put(tick(0.09), x, 0.3); gap = max(0.05, gap * (0.93 if x > S0("timeWarp") else 0.99)); x += gap
put(reverse_swell(5.5, 0.14), S0("timeWarp")); put(impact(0.7), S0("wake80"))
put(strings([45, 52, 57, 60], 10, 0.04, att=2), S0("wake80"))
for i, m in enumerate([69, 68, 64, 63]): put(piano(m, 4, 0.05), S0("hands80") + i * 1.4)
put(impact(0.6), S0("mirror80") + 4.5); put(strings([44, 51, 56, 59], 6, 0.06, att=0.2), S0("mirror80") + 4.5)
put(impact(0.8), S0("title8") + 0.4); put(strings([45, 52, 57, 64], 7.5, 0.07, att=0.3), S0("title8") + 0.4)

# --- Act 2: eerie future: pads + sci-fi arpeggio bleeps
f0, f1 = S0("cal2081"), S0("tryRun")
x, k = f0, 0
while x < f1 - 0.1:
    ch = [AM, Em, F, Dm][k % 4]
    put(strings([n - 12 for n in ch] + [ch[2] + 12], BAR + 1, 0.035, att=1.0, bright=0.6), x)
    for b in range(16): put(bleep(ch[b % 3] + 24 + (12 if b % 4 == 3 else 0), 0.025), x + b * BEAT / 4, 0.4 * np.sin(b))
    x += BAR; k += 1

# --- Act 3: sad piano + strings, silence after the call
s0, s1 = S0("tryRun"), S0("benchKid")
x, k = s0, 0
while x < s1 - 0.1:
    ch = [AM, F, C, G][k % 4]
    if not (S0("callMom80") + 4 <= x < S0("photoWall")):
        put(strings(ch, BAR + 1.5, 0.045, att=1.0), x)
        for b, m in enumerate([ch[0], ch[2], ch[1] + 12, ch[2]]): put(piano(m, 3, 0.055), x + b * BEAT)
    x += BAR; k += 1
for r_ in range(3):
    n = int(1.0 * SR); tt = np.arange(n) / SR
    put(0.05 * (np.sin(2 * np.pi * 440 * tt) + np.sin(2 * np.pi * 480 * tt)), S0("callMom80") + 0.6 + r_ * 1.4)
n = int(0.9 * SR); tt = np.arange(n) / SR
for i, fq in enumerate([950, 1400, 1800]): put(0.06 * np.sin(2 * np.pi * fq * tt[: int(0.3 * SR)]), S0("callMom80") + 4.2 + i * 0.32)

# --- Act 4: tender strings + kid music box, reverse swell into the flash
b0 = S0("benchKid")
x, k = b0, 0
while x < S0("closeEyes") - 0.1:
    ch = [F, C, G, AM][k % 4]; put(strings(ch + [ch[0] - 12], BAR + 1.5, 0.05, att=1.2), x); put(piano(ch[0] - 12, 3, 0.06), x)
    if k % 2 == 0:
        for i, m in enumerate([81, 79, 76, 79]): put(mbox(m, 0.03), x + i * BEAT)
    x += BAR; k += 1
put(reverse_swell(6, 0.15), S0("closeEyes"))

# --- Act 5: bright drums + piano build
w0, w1 = S0("wakeYoung"), S0("card", 1)
put(impact(0.6), w0)
x, k = w0, 0
while x < w1 - 0.1:
    ch = [C, G, AM, F][k % 4]; g = 1 + 0.4 * (x - w0) / (w1 - w0)
    if x >= S0("windowSun"):
        for b in range(4):
            if b in (0, 2): put(kick(0.42 * g), x + b * BEAT)
            if b in (1, 3): put(snare(0.15 * g), x + b * BEAT, 0.1)
        for b in range(8): put(hat(0.04 * g), x + b * BEAT / 2, 0.35)
        put(piano(ch[0] - 24, BAR, 0.10 * g), x)
    for b, idx in enumerate([0, 1, 2, 4, 2, 1, 0, 2]): put(piano(ch[idx % 3] + 12 * (idx // 3), 1.8, 0.05 * g), x + b * BEAT / 2, 0.2 * np.sin(b))
    put(strings(ch, BAR + 1, 0.035 * g, att=0.6), x)
    x += BAR; k += 1
e0 = S0("card", 1)
put(piano(48, 7, 0.10) + piano(60, 7, 0.07) + piano(64, 7, 0.06) + piano(67, 7, 0.05), e0 + 0.3)
put(strings([48, 55, 64, 72], 19, 0.05, att=1.0), e0)
put(piano(53, 7, 0.09) + piano(60, 7, 0.06) + piano(69, 7, 0.05), e0 + 6.3)
put(piano(48, 8, 0.11) + piano(55, 8, 0.07) + piano(64, 8, 0.06) + piano(72, 8, 0.05), e0 + 12.4)

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
acts = [("couchNight", "Five more minutes"), ("cal2081", "2081"), ("tryRun", "Everything you postponed"), ("benchKid", "The question"), ("wakeYoung", "Second chance")]
with open(os.path.join(OUT, "chapters.txt"), "w") as f:
    for sid, name in acts:
        s = 0 if sid == "couchNight" else S0(sid); f.write(f"{int(s // 60)}:{int(s % 60):02} {name}\n")
print(f"total {total:.1f}s = {int(total // 60)}:{int(total % 60):02}, scenes {len(scenes)}")
