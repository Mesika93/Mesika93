import ssl, json, sys, subprocess, os
orig=ssl.create_default_context
def ctx(*a,**k):
    c=orig(*a,**k); c.load_verify_locations("/root/.ccr/ca-bundle.crt"); return c
ssl.create_default_context=ctx
import edge_tts, asyncio
out=sys.argv[1]; os.makedirs(out,exist_ok=True)
N=("en-US-GuyNeural","+12%","+0Hz")
SEG=[
 (N,"He climbed onto a platform high above a crowd, and ordered a man to cut the only rope holding it. You see, it's 1854, New York. Buildings stop at five or six floors, because nobody trusts a lifting machine. Ropes snap. Platforms fall. Workers die. Elisha Otis, a quiet mechanic, says he's built one that can't fall. Nobody believes him."),
 (("en-US-ChristopherNeural","+5%","-8Hz"),"A rope is a rope, Otis. When it breaks, you die."),
 (N,"So at the Crystal Palace fair, he builds a tower, steps onto the platform, and rises above the crowd. Then he hands an axe to his assistant. Cut it. The crowd screams. The rope snaps. The platform drops, a few inches. And stops."),
 (("en-GB-RyanNeural","+0%","+0Hz"),"All safe, gentlemen. All safe."),
 (N,"Above that platform, a wagon spring snapped open the moment the rope went slack, and jammed iron teeth into the rails. That's why the elevator you ride can't just fall. And that's why cities grew up, instead of out."),
]
async def gen(i,v,t):
    c=edge_tts.Communicate(t,v[0],rate=v[1],pitch=v[2],boundary="WordBoundary")
    words=[]
    with open(f"{out}/s{i}.mp3","wb") as f:
        async for ch in c.stream():
            if ch["type"]=="audio": f.write(ch["data"])
            elif ch["type"]=="WordBoundary": words.append((ch["offset"]/1e7,(ch["offset"]+ch["duration"])/1e7,ch["text"]))
    return words
async def main():
    allw=[];t0=0.0;files=[]
    for i,(v,t) in enumerate(SEG):
        w=await gen(i,v,t)
        subprocess.run(["ffmpeg","-v","error","-y","-i",f"{out}/s{i}.mp3","-ar","44100","-ac","1",f"{out}/s{i}.wav"],check=True)
        d=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"{out}/s{i}.wav"]))
        for a,b,x in w: allw.append({"s":round(a+t0,3),"e":round(b+t0,3),"w":x,"seg":i})
        files.append((f"{out}/s{i}.wav",t0)); t0+=d+0.12
    json.dump({"words":allw,"dur":t0,"files":files},open(f"{out}/words.json","w"),indent=0)
    print("total",round(t0,2),"words",len(allw))
asyncio.run(main())
