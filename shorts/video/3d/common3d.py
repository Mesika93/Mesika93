"""Shared timeline + bridge physics for the Blender render and the 2D compositor."""
import json, math, re, os

HERE = os.path.dirname(os.path.abspath(__file__))
R1 = os.path.join(HERE, "r1")
data = json.load(open(os.path.join(R1, "words.json")))
WORDS = data["words"]; DUR = data["dur"] + 0.6
norm = lambda s: re.sub(r"[^a-z0-9']", "", s.lower())
NW = [norm(w["w"]) for w in WORDS]

def find(phrase, after=0):
    p = [norm(x) for x in phrase.split()]
    for i in range(after, len(NW)):
        if NW[i:i + len(p)] == p: return i
    raise SystemExit("not found: " + phrase)

def wt(phrase, after=0): return WORDS[find(phrase, after)]["s"]

T = {"ordered": 0.0}
T["middle"] = wt("right in the middle"); T["yousee"] = wt("you see")
T["left1"] = wt("left"); T["right"] = wt("right", find("left")); T["left2"] = wt("left", find("left") + 1)
T["crowds"] = wt("the crowds loved"); T["sowhen"] = wt("so when the young"); T["break"] = wt("break step")
T["general"] = wt("the general turns"); T["mob"] = wt("are you trying"); T["stumble"] = wt("the soldiers stumble")
T["ducks"] = wt("ducks"); T["news"] = wt("the newspapers call"); T["next"] = wt("next sunday")
T["halfway"] = wt("and halfway across"); T["hum"] = wt("hum"); T["bounce"] = wt("then bounce")
T["every"] = wt("every step pushes"); T["cheers"] = wt("the crowd cheers"); T["bolts"] = wt("then the bolts")
T["popping"] = wt("popping"); T["folds"] = wt("and the whole bridge folds"); T["rhythm"] = wt("every bridge has")
T["match"] = wt("match it with"); T["apart"] = WORDS[-1]["s"]

SCENES = [("ordered", "s_order"), ("middle", "s_wide"), ("yousee", "s_parade"), ("left1", "s_boots"),
          ("crowds", "s_crowd"), ("sowhen", "s_officer"), ("general", "s_purple"), ("mob", "s_nose"),
          ("stumble", "s_ducks"), ("news", "s_news"), ("next", "s_proud"), ("halfway", "s_hum"),
          ("every", "s_swing"), ("cheers", "s_crowd2"), ("bolts", "s_bolts"), ("folds", "s_collapse"),
          ("rhythm", "s_diagram")]
STARTS = [T[k] for k, _ in SCENES] + [DUR]
def scene_range(name):
    i = [n for _, n in SCENES].index(name); return STARTS[i], STARTS[i + 1]

# ---- bridge geometry (metres) ----
SPAN = 22.0          # towers at x = +-SPAN
DECK_Z = 6.5
TOWER_TOP = 16.0
CHAIN_LOW = DECK_Z + 2.9
POP_TIMES = [T["popping"] + i * 0.35 for i in range(3)]

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(t): t = clamp(t); return t * t * (3 - 2 * t)

def bridge_state(now):
    """returns amp (m), freq (Hz), collapse progress 0..1"""
    amp, f, c = 0.0, 1.6, 0.0
    if now >= T["hum"]: amp, f = 0.04 + 0.06 * clamp((now - T["hum"]) / 1.0), 7.0
    if now >= T["bounce"]: amp, f = 0.35, 1.6
    if now >= T["every"]: amp = 0.35 + 1.25 * clamp((now - T["every"]) / max(0.1, T["cheers"] - T["every"]))
    if now >= T["cheers"]: amp = 1.6 + 0.5 * clamp((now - T["cheers"]) / 3)
    if now >= T["folds"]: c = ease((now - T["folds"] - 0.15) / 1.8)
    return amp, f, c

def deck_dy(x, now):
    amp, f, _ = bridge_state(now)
    u = clamp((x + SPAN) / (2 * SPAN))
    return amp * math.sin(math.pi * u) * math.sin(2 * math.pi * f * now)

def deck_z(x, now): return DECK_Z + deck_dy(x, now)

def chain_z(x, now):
    u = (x + SPAN) / (2 * SPAN)
    base = TOWER_TOP - (TOWER_TOP - CHAIN_LOW) * (1 - (2 * u - 1) ** 2)
    return base + 0.5 * deck_dy(x, now)
