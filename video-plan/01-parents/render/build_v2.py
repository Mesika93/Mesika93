"""Long text-only version (~5 min): story timeline + music + SFX, no voice-over.

Usage: python3 build_v2.py <out_dir>
Produces: timeline.json, mix.wav, subtitles_en.srt, subtitles_uk.srt
"""
import json, os, sys, wave
import numpy as np

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
SR = 44100

# (scene, duration, [(start, end, EN, UA)], cut_into_next)
STORY = [
    ("phone", 8, [(3.6, 7.4, "You declined her call again.", "Ти знову скинув її дзвінок.")]),
    ("gaming", 7, [(1.2, 6.4, "\"I'll call her back later.\"", "«Передзвоню їй пізніше.»")]),
    ("scroll", 8, [(5.2, 7.6, "Later.", "Пізніше.")]),
    ("work", 8, [(3.0, 7.4, "Always later.", "Завжди пізніше.")]),
    ("calendar", 10, [(5.0, 9.4, "Days became weeks.", "Дні ставали тижнями.")]),
    ("title", 7, []),
    ("card", 5, [(0.8, 4.4, "Remember?", "Пам'ятаєш?")]),
    ("shoulders", 10, [(2.0, 9.0, "When they were your whole world.", "Коли вони були всім твоїм світом.")]),
    ("bicycle", 10, [(2.0, 9.0, "She ran behind you... so you wouldn't fall.", "Вона бігла позаду... щоб ти не впав.")]),
    ("knee", 12, [(1.0, 5.2, "And when you did fall...", "А коли ти таки падав..."),
                  (6.6, 11.4, "she was always there.", "вона завжди була поруч.")]),
    ("school", 10, [(1.5, 8.8, "He held your hand on your first day.", "Він тримав тебе за руку в перший день.")]),
    ("card", 5, [(0.8, 4.4, "Then you grew up.", "Потім ти виріс.")]),
    ("door", 9, [(2.0, 8.4, "And they became... annoying.", "І вони стали... набридливими.")]),
    ("train", 12, [(1.0, 5.6, "You left to build your life.", "Ти поїхав будувати своє життя."),
                   (6.4, 11.4, "They stayed. And waited.", "Вони лишились. І чекали.")]),
    ("kitchen", 11, [(1.5, 5.6, "She still cooks for two.", "Вона досі готує на двох."),
                     (6.2, 10.4, "Just in case you visit.", "Раптом ти приїдеш.")]),
    ("waiting", 10, [(1.5, 9.2, "She keeps her phone close. Just in case.", "Вона тримає телефон поруч. Про всяк випадок.")]),
    ("stairs", 10, [(1.5, 5.2, "His hands shake now.", "У нього тепер тремтять руки."),
                    (5.8, 9.4, "He won't tell you.", "Він тобі не скаже.")]),
    ("birthday", 12, [(1.5, 5.4, "Another birthday.", "Ще один день народження."),
                      (6.4, 11.4, "Another empty chair.", "Ще один порожній стілець.")]),
    ("hourglass", 11, [(1.0, 5.0, "You think you have time.", "Ти думаєш, що в тебе є час."),
                       (5.6, 10.4, "You see them maybe five times a year.", "Ти бачиш їх, може, п'ять разів на рік.")]),
    ("hundred", 12, []),
    ("missed", 10, [(2.0, 9.2, "One day... the phone will stop ringing.", "Одного дня... цей телефон перестане дзвонити.")]),
    ("card", 4, []),
    ("call", 8, [(2.4, 7.4, "So call her.", "Тож подзвони їй.")]),
    ("mom", 9, [(2.0, 8.4, "\"Sweetheart? Is everything okay?\"", "«Синку? Все добре?»")]),
    ("bus", 9, [(1.5, 8.4, "Not because you have to.", "Не тому що треба.")]),
    ("hug", 10, [(1.5, 9.2, "Because one day... you won't be able to.", "А тому що колись... не зможеш.")]),
    ("dinner", 10, [(1.5, 9.0, "Sit at her table.", "Сядь за її стіл.")]),
    ("walk", 10, [(1.5, 9.0, "Listen to his old stories.", "Послухай його старі історії.")]),
    ("album", 10, [(1.5, 9.0, "Ask about their life.", "Розпитай про їхнє життя.")]),
    ("bench", 13, [(3.0, 11.6, "They gave you their whole life.", "Вони віддали тобі все життя.")]),
    ("card", 6, [(0.8, 5.4, "Give them an hour.", "Дай їм годину.")]),
    ("card", 8, [(1.0, 7.0, "Call them today.", "Подзвони їм сьогодні.")]),
]

scenes, caps, t = [], [], 0.0
for sid, dur, lines in STORY:
    scenes.append({"id": sid, "start": round(t, 3), "end": round(t + dur, 3), "cut": sid in ("gaming", "call")})
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
sad = [AM, F, C, G]
warm = [C, G, AM, F]
ARP = [0, 1, 2, 4, 2, 1, 0, 2]

# 1) cold open: low drone, sparse notes
put(drone(45, S0("title"), 0.05), 0)
for i, at in enumerate(np.arange(2.0, S0("title") - 2, 4.0)):
    put(piano([69, 67, 64, 62][i % 4], 4, 0.05), at)
# title hit
put(piano(45, 6, 0.16) + piano(57, 6, 0.10) + piano(64, 6, 0.08), S0("title") + 0.4)
# 2) flashback: warm, music-box high register
fb0, fb1 = S0("card", 0), S0("card", 1)
section(fb0 + 1.0, fb1 + 2, warm, 0.5, ARP, 0.05, 0.035, oct_=12,
        mel=lambda k: [(0, [67, 67, 69, 65][k % 4], 1.5), (4, [64, 62, 64, 60][k % 4], 1.5)])
# 3) growing apart + their side: sad, slowly growing
sd0, sd1 = fb1 + 2, S0("hundred")
section(sd0, sd1, sad, 0.55, ARP, 0.055, 0.045, bass=0.06, grow=0.6,
        mel=lambda k: [(0, [76, 77, 79, 74][k % 4], 2.0), (4, [72, 72, 74, 71][k % 4], 2.0)] if k >= 4 else [])
# 4) 100: pad + heartbeat
h0 = S0("hundred")
put(pad([45, 52, 57], 12, 0.05, bright=0.1), h0)
for b in range(9):
    for off, a in ((0, 0.5), (0.22, 0.32)):
        n = int(0.2 * SR); tt = np.arange(n) / SR
        put(a * np.sin(2 * np.pi * 52 * tt) * np.exp(-tt * 22), h0 + 4.6 + b * 0.9 + off)
# 5) missed: lone piano, then total silence (card)
m0 = S0("missed")
for i, n in enumerate([64, 62, 60, 57]):
    put(piano(n, 4, 0.06), m0 + 1 + i * 2.2)
# 6) call -> end: lift, building to climax at bench
c0 = S0("call")
for r in range(2):
    n = int(1.0 * SR); tt = np.arange(n) / SR
    put(0.06 * (np.sin(2 * np.pi * 440 * tt) + np.sin(2 * np.pi * 480 * tt)), c0 + 2.0 + r * 2.0)
lift0, end0 = S0("mom"), S0("card", 3)
section(lift0, end0, warm, 0.5, ARP, 0.06, 0.05, bass=0.08, grow=1.2,
        mel=lambda k: [(0, [76, 74, 72, 72][k % 4], 1.5), (3, [79, 79, 76, 77][k % 4], 1.0),
                       (4, [77, 74, 76, 72][k % 4], 2.5)])
# final cards: single chords fading
put(piano(48, 7, 0.10) + piano(60, 7, 0.07) + piano(64, 7, 0.06) + piano(67, 7, 0.05), end0 + 0.3)
put(piano(53, 8, 0.08) + piano(60, 8, 0.06) + piano(69, 8, 0.05), end0 + 6.5)

# SFX: phone vibration in opening, phone buzz in "work", rain under kitchen/waiting, slam
def buzz(dur, amp=0.15):
    tt = np.arange(int(dur * SR)) / SR
    return amp * np.sign(np.sin(2 * np.pi * 150 * tt)) * (tt % 1.0 < 0.55) * 0.6
put(buzz(3.4), 0.2); put(buzz(3.0, 0.08), S0("work") + 2.6)
for sid in ("kitchen", "waiting"):
    n = int(11 * SR); r = rng.standard_normal(n) * 0.012
    r = np.convolve(r, np.ones(8) / 8, mode="same"); env = np.minimum(1, np.arange(n) / SR / 1.5) * np.minimum(1, (n / SR - np.arange(n) / SR) / 1.5)
    put(r * env, S0(sid))
n = int(0.5 * SR); tt = np.arange(n) / SR
put(0.5 * rng.standard_normal(n) * np.exp(-tt * 18) + 0.4 * np.sin(2 * np.pi * 70 * tt) * np.exp(-tt * 10), S0("door") + 1.15)

# reverb (FFT convolution with decaying noise)
def reverb(x, secs=2.6, wet=0.28):
    n = int(secs * SR); ir = rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 3.0); ir[0] = 0
    ir /= np.sqrt((ir ** 2).sum())
    size = 1 << int(np.ceil(np.log2(len(x) + n)))
    y = np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(ir, size), size)[: len(x)]
    return x * (1 - wet) + y * wet * 1.3
L, Rr = reverb(L), reverb(Rr)
# silence the dramatic gap exactly
g0, g1 = int(S0("card", 2) * SR), int((S0("card", 2) + 3.6) * SR)
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
