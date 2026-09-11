"""Transcribe N chunks of one video (resumable). usage: one.py NAME [N]"""
import sys, os, glob, time, numpy as np
from faster_whisper import WhisperModel
name=sys.argv[1]; N=int(sys.argv[2]) if len(sys.argv)>2 else 1
out=f"/home/user/research4/{name}.txt"
done=set()
if os.path.exists(out):
    for line in open(out,encoding="utf-8"):
        if line.startswith("##CHUNK "): done.add(int(line.split()[1]))
files=[f for f in sorted(glob.glob(f"/home/user/.cache/asr/{name}.c*.raw")) if int(f.split(".c")[-1].split(".")[0]) not in done]
if not files:
    open(f"/home/user/research4/{name}.done","w").write("ok"); print("DONE",name); sys.exit(0)
m=WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=2)
t=time.time()
with open(out,"a",encoding="utf-8") as f:
    for fn in files[:N]:
        ci=int(fn.split(".c")[-1].split(".")[0]); a=np.fromfile(fn,dtype=np.float32); off=ci*300
        segs,_=m.transcribe(a, language="ru", beam_size=1, vad_filter=True, condition_on_previous_text=False)
        for s in segs:
            tt=int(s.start+off); f.write(f"[{tt//3600:02d}:{(tt%3600)//60:02d}:{tt%60:02d}] {s.text.strip()}\n")
        f.write(f"##CHUNK {ci}\n"); f.flush(); os.remove(fn)
        print(name, f"chunk {ci} ok", round(time.time()-t), "left", len(files)-files.index(fn)-1, flush=True)
