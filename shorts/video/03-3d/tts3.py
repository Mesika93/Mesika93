import ssl, json, sys, subprocess, os
orig=ssl.create_default_context
def ctx(*a,**k):
    c=orig(*a,**k); c.load_verify_locations("/root/.ccr/ca-bundle.crt"); return c
ssl.create_default_context=ctx
import edge_tts, asyncio
out=sys.argv[1]; os.makedirs(out,exist_ok=True)
N=("en-US-GuyNeural","+12%","+0Hz")
SEG=[
 (N,"He told the military to put armor exactly where the bombers had no bullet holes. You see, it's 1943, and American bombers are getting shot out of the sky over Europe. Armor is heavy, so you can only add a little. The officers have a plan: count the bullet holes on every bomber that comes home. Wings, full of holes. Tail, full of holes. Body, like Swiss cheese. Engines? Almost clean. So when a quiet mathematician named Abraham Wald says, armor the engines, the colonel laughs."),
 (("en-GB-RyanNeural","+0%","-10Hz"),"Are you blind? That's the one place they never get hit!"),
 (N,"But Wald asks one question. Where are the planes that didn't come back? Silence. Bombers hit in the wings limped home. Bombers hit in the engines never made it home at all. The holes weren't showing where planes get shot. They showed where a plane can get shot, and still survive. The missing holes were the real map. It's called survivorship bias, and it hides in every success story."),
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
