import ssl, json, sys, subprocess, os
orig=ssl.create_default_context
def ctx(*a,**k):
    c=orig(*a,**k); c.load_verify_locations("/root/.ccr/ca-bundle.crt"); return c
ssl.create_default_context=ctx
import edge_tts, asyncio
out=sys.argv[1]; os.makedirs(out,exist_ok=True)
N=("en-US-GuyNeural","+12%","+0Hz")
SEG=[
 (N,"He ordered his soldiers to stop marching in step, right in the middle of a bridge. You see, his regiment was the pride of the city, and every Sunday they crossed the new iron bridge in perfect rhythm. Left. Right. Left. The crowds loved it. So when the young officer shouts"),
 (("en-US-EricNeural","+5%","+4Hz"),"Break step!"),
 (N,"the general turns purple."),
 (("en-GB-RyanNeural","+0%","-12Hz"),"Are you trying to make us look like a mob?!"),
 (N,"The soldiers stumble across like drunk ducks, and the whole town laughs. The newspapers call them the Duck Brigade. Next Sunday, the general leads the march himself. Perfect rhythm. Chins up. And halfway across, the bridge starts to hum. Then bounce. Every step pushes it a little higher, like a kid on a swing. The crowd cheers, thinking it's part of the show. Then the bolts start popping like gunshots, and the whole bridge folds into the river. Every bridge has its own rhythm. Match it with a hundred boots, and it'll shake itself apart."),
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
