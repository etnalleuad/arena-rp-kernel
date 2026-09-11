import re,sys
name=sys.argv[1]; start=int(sys.argv[2]) if len(sys.argv)>2 else 0; end=int(sys.argv[3]) if len(sys.argv)>3 else 10**9
lines=[l for l in open(f"research4/{name}.txt",encoding='utf-8').read().splitlines() if l.startswith("[")]
buf=[];cur=None;out=[]
for l in lines:
    m=re.match(r"\[(\d\d):(\d\d):(\d\d)\] (.*)",l)
    if not m: continue
    mm=int(m.group(1))*60+int(m.group(2))
    if mm<start or mm>=end: continue
    key=mm//2
    if key!=cur:
        if buf: out.append(f"[{cur*2//60:02d}:{cur*2%60:02d}] "+" ".join(buf))
        buf=[];cur=key
    buf.append(m.group(4))
if buf: out.append(f"[{cur*2//60:02d}:{cur*2%60:02d}] "+" ".join(buf))
print("\n\n".join(out))
