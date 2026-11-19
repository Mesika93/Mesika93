"""Build voice-over, music and timeline for video #1.

Usage: python3 build_audio.py <tts_model_dir> <out_dir>
Produces: out_dir/voice.wav, music.wav, mix.wav, timeline.json, subtitles_en.srt, subtitles_uk.srt
"""
import json, subprocess, sys, wave, os
import numpy as np

SR = 22050
MODEL_DIR, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
MALE = os.path.join(MODEL_DIR, "en_US-ryan-high.onnx")
FEMALE = os.path.join(MODEL_DIR, "en_US-amy-medium.onnx")

# scene id, lead silence, [(text_en, text_uk, voice, gap_after)], tail silence
SCENES = [
    ("phone", 1.2, [("You declined her call again.", "Ти знову скинув її дзвінок.", "m", 0.8)], 0.4),
    ("gaming", 0.3, [("\"I'll call her back later.\"", "«Передзвоню потім.»", "m", 0.6)], 0.6),
    ("shoulders", 0.6, [("Remember when they were your whole world?", "Пам'ятаєш, коли вони були всім твоїм світом?", "m", 0.4)], 1.4),
    ("bicycle", 0.4, [("She ran behind you... so you wouldn't fall.", "Вона бігла позаду... щоб ти не впав.", "m", 0.4)], 1.6),
    ("door", 0.4, [("Then you grew up.", "Потім ти виріс.", "m", 0.7),
                   ("And they became... annoying.", "І вони стали... набридливими.", "m", 0.4)], 1.6),
    ("kitchen", 0.6, [("She still cooks for two.", "Вона досі готує на двох.", "m", 0.7),
                      ("Just in case you visit.", "Раптом ти приїдеш.", "m", 0.4)], 1.8),
    ("stairs", 0.6, [("His hands shake now.", "У нього тепер тремтять руки.", "m", 0.6),
                     ("He won't tell you.", "Він тобі не скаже.", "m", 0.4)], 1.8),
    ("hourglass", 0.5, [("You think you have time.", "Ти думаєш, що в тебе є час.", "m", 0.8),
                        ("You see them maybe five times a year.", "Ти бачиш їх, може, п'ять разів на рік.", "m", 0.6)], 0.6),
    ("hundred", 0.4, [("If they live twenty more years...", "Якщо вони проживуть ще двадцять років...", "m", 0.8),
                      ("that's one hundred visits.", "це сто зустрічей.", "m", 0.8),
                      ("Left.", "Всього.", "m", 0.4)], 2.2),
    ("missed", 0.8, [("One day... the phone will stop ringing.", "Одного дня... цей телефон перестане дзвонити.", "m", 0.4)], 2.6),
    ("call", 0.3, [("So call her.", "Тож подзвони їй.", "m", 0.4)], 2.8),
    ("mom", 0.6, [("Hello? Sweetheart? Is everything okay?", "Алло? Синку? Все добре?", "f", 0.4)], 1.2),
    ("bus", 0.4, [("Not because you have to.", "Не тому що треба.", "m", 0.5)], 0.6),
    ("hug", 0.2, [("Because one day... you won't be able to.", "А тому що колись... не зможеш.", "m", 0.4)], 1.4),
    ("dinner", 0.4, [("They gave you their whole life.", "Вони віддали тобі все життя.", "m", 0.7),
                     ("Give them an hour.", "Дай їм годину.", "m", 0.4)], 1.4),
    ("bench", 0.6, [], 4.0),
    ("end", 0.6, [("Call them today.", "Подзвони їм сьогодні.", "m", 0.4)], 3.5),
]


def tts(text, voice, path):
    model = MALE if voice == "m" else FEMALE
    ls = "1.18" if voice == "m" else "1.08"
    subprocess.run([sys.executable, "-m", "piper", "-m", model, "--length-scale", ls,
                    "--sentence-silence", "0.35", "-f", path],
                   input=text.replace('"', "").encode(), check=True, capture_output=True)
    with wave.open(path) as w:
        sr = w.getframerate()
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    if sr != SR:
        a = np.interp(np.linspace(0, len(a), int(len(a) * SR / sr), endpoint=False), np.arange(len(a)), a)
    return a


voice = []
t = 0.0
timeline, caps = [], []
for i, (sid, lead, lines, tail) in enumerate(SCENES):
    start = t
    voice.append(np.zeros(int(lead * SR))); t += lead
    for j, (en, uk, v, gap) in enumerate(lines):
        a = tts(en, v, os.path.join(OUT, f"l_{i}_{j}.wav"))
        caps.append({"start": t, "end": t + len(a) / SR + 0.15, "en": en, "uk": uk, "scene": sid})
        voice.append(a); t += len(a) / SR
        voice.append(np.zeros(int(gap * SR))); t += gap
    voice.append(np.zeros(int(tail * SR))); t += tail
    timeline.append({"id": sid, "start": round(start, 3), "end": round(t, 3)})

voice = np.concatenate(voice)
N = len(voice)
total = N / SR

# ---------- music: soft piano + pad, silence before the call, warm lift after ----------
def tstart(sid):
    return next(s["start"] for s in timeline if s["id"] == sid)

def piano_note(freq, dur, amp):
    n = int(dur * SR); tt = np.arange(n) / SR
    env = np.exp(-tt * 2.2) * np.minimum(1, tt * 200)
    tone = sum(np.sin(2 * np.pi * freq * k * tt) / (k ** 1.6) for k in range(1, 6))
    return amp * env * tone

def pad(freqs, dur, amp):
    n = int(dur * SR); tt = np.arange(n) / SR
    env = np.minimum(1, tt / 1.5) * np.minimum(1, (dur - tt) / 1.5)
    s = sum(np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 1.003 * tt) for f in freqs)
    return amp * env * s / len(freqs)

def hz(m):
    return 440 * 2 ** ((m - 69) / 12)

music = np.zeros(N + SR * 4)
def add(sig, at):
    i = int(at * SR); j = min(len(music), i + len(sig)); music[i:j] += sig[: j - i]

# Am - F - C - G (sad), each chord 4 s, arpeggiated
sad = [[57, 60, 64], [53, 57, 60], [48, 55, 64], [55, 59, 62]]
silence_at, lift_at = tstart("missed") + 3.0, tstart("mom")
x, k = 3.0, 0
while x < silence_at - 4:
    ch = sad[k % 4]
    add(pad([hz(n - 12) for n in ch], 4.2, 0.05), x)
    for b, n in enumerate([ch[0], ch[1], ch[2], ch[1] + 12, ch[2], ch[1], ch[0] + 12, ch[2]]):
        add(piano_note(hz(n), 2.0, 0.07), x + b * 0.5)
    x += 4; k += 1
# lift: C - G - Am - F, brighter, louder, with bass
lift = [[60, 64, 67], [55, 59, 62], [57, 60, 64], [53, 57, 60]]
x, k = lift_at, 0
while x < total + 1:
    ch = lift[k % 4]
    add(pad([hz(n) for n in ch] + [hz(ch[0] - 12)], 4.2, 0.07 + min(0.05, k * 0.008)), x)
    add(piano_note(hz(ch[0] - 24), 3.5, 0.10), x)
    for b, n in enumerate([ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[1] + 12] * 2):
        add(piano_note(hz(n), 1.6, 0.06), x + b * 0.5)
    x += 4; k += 1
music = music[:N]
# fade-in / fade-out
fi = int(3 * SR); music[:fi] *= np.linspace(0, 1, fi)
fo = int(4 * SR); music[-fo:] *= np.linspace(1, 0, fo)

# SFX: phone vibration (scene phone + missed), dial tones (call)
def buzz(dur):
    tt = np.arange(int(dur * SR)) / SR
    return 0.18 * np.sign(np.sin(2 * np.pi * 160 * tt)) * (np.sin(2 * np.pi * 18 * tt) > 0) * (tt % 1.0 < 0.55)
add(buzz(2.4), 0.0)
cs = tstart("call")
for r in range(2):
    tt = np.arange(int(1.0 * SR)) / SR
    add(0.08 * (np.sin(2 * np.pi * 440 * tt) + np.sin(2 * np.pi * 480 * tt)), cs + 1.6 + r * 1.6)
# heartbeat on "100"
hs = tstart("hundred")
for b in range(6):
    for off, a in ((0, 0.5), (0.22, 0.35)):
        tt = np.arange(int(0.18 * SR)) / SR
        add(a * np.sin(2 * np.pi * 55 * tt) * np.exp(-tt * 25), hs + 4.0 + b * 0.9 + off)
music = music[:N]

def write(path, a):
    a = np.clip(a, -1, 1)
    with wave.open(path, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((a * 32767).astype(np.int16).tobytes())

write(os.path.join(OUT, "voice.wav"), voice)
write(os.path.join(OUT, "music.wav"), music)
mix = voice * 0.95 + music * 0.55
mix = mix / max(1e-6, np.abs(mix).max()) * 0.9
write(os.path.join(OUT, "mix.wav"), mix)

json.dump({"duration": total, "scenes": timeline, "captions": caps},
          open(os.path.join(OUT, "timeline.json"), "w"), ensure_ascii=False, indent=1)

def srt_time(s):
    ms = int(round(s * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); sec, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{sec:02},{ms:03}"
for lang in ("en", "uk"):
    with open(os.path.join(OUT, f"subtitles_{lang}.srt"), "w") as f:
        for n, c in enumerate(caps, 1):
            f.write(f"{n}\n{srt_time(c['start'])} --> {srt_time(c['end'])}\n{c[lang]}\n\n")
print(f"duration {total:.1f}s, scenes {len(timeline)}")
for s in timeline:
    print(s)
