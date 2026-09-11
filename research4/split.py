import sys, av, numpy as np, os, glob
path=sys.argv[1]; name=sys.argv[2]; SR=16000; CH=5*60*SR
os.makedirs("/home/user/.cache/asr",exist_ok=True)
have=sorted(glob.glob(f"/home/user/.cache/asr/{name}.c*.raw"))
# resume: skip already-written full chunks
start_idx=0
for f in have:
    if os.path.getsize(f)==CH*4: start_idx+=1
    else: os.remove(f)
c=av.open(path); st=c.streams.audio[0]
res=av.AudioResampler(format="s16", layout="mono", rate=SR)
buf=np.zeros(0,dtype=np.float32); idx=0; skip=start_idx*CH
for fr in c.decode(st):
    for f2 in res.resample(fr):
        a=f2.to_ndarray().reshape(-1).astype(np.float32)/32768.0
        if skip>0:
            if len(a)<=skip: skip-=len(a); continue
            a=a[skip:]; skip=0
        buf=np.concatenate([buf,a]) if len(buf) else a
    while len(buf)>=CH:
        buf[:CH].tofile(f"/home/user/.cache/asr/{name}.c{start_idx+idx:03d}.raw"); idx+=1
        buf=buf[CH:].copy()
if len(buf)>SR:
    buf.tofile(f"/home/user/.cache/asr/{name}.c{start_idx+idx:03d}.raw"); idx+=1
c.close(); print("chunks total",start_idx+idx)
