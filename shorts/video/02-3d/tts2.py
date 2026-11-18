import ssl, json, sys, subprocess, os
orig=ssl.create_default_context
def ctx(*a,**k):
    c=orig(*a,**k); c.load_verify_locations("/root/.ccr/ca-bundle.crt"); return c
ssl.create_default_context=ctx
import edge_tts, asyncio
out=sys.argv[1]; os.makedirs(out,exist_ok=True)
N=("en-US-GuyNeural","+12%","+0Hz")
SEG=[
 (N,"He spent the whole day poking at anthills, while millionaires were buying a diamond field. You see, two scruffy prospectors walked into a San Francisco bank with a sack of raw diamonds. Tiffany's in New York checked the stones. Real. A famous mining expert visited the field. Diamonds everywhere. Bankers poured in ten million dollars. So when a young government geologist asks to see the site, the banker laughs."),
 (("en-GB-RyanNeural","+0%","-10Hz"),"Son, the experts have already spoken."),
 (N,"But Clarence King goes anyway. And he finds diamonds, in all the wrong places. Pushed into anthills, with a stick hole right beside them. Rubies, sapphires and emeralds, lying in the same patch of dirt. Nature never mixes them like that. Then he picks up a diamond with marks from a jeweler's cutting wheel. The field was salted. King sends one telegram, and ten million dollars turn to dust overnight. Real gems hide deep in the rock. Fake ones lie exactly where you want to find them."),
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
