# build blur windows from scan2/*.json -> windows/<key>.json (no OCR text stored)
import json,glob,re,os,sys
EM=re.compile(r'[A-Za-z0-9._%+-]{3,}@(gmail|gma|gm\b|yahoo|hotmail|outlook|icloud|rediff|[A-Za-z0-9-]+\.(com|in|org|net|co|edu|gov))',re.I)
PH=re.compile(r'(\+91[\s-]?)?(?<![\d])[6-9]\d{4}[\s-]?\d{5}(?!\d)')
LIST=re.compile(r'^\W{0,3}(add participants|suggestions|choose an account|choose a saved password|search contacts|frequently contacted|new broadcast|contacts on whatsapp|ask meta a[il1]|search for someone in this call|select contact|send to|recent chats|in call\b|people\b.*information)',re.I)
PAD=1.3
os.makedirs('windows',exist_ok=True)
def merge(ws):
    ws=sorted(ws,key=lambda w:w['t0']); out=[]
    for w in ws:
        for o in out:
            ox,oy,ow,oh=o['box'];x,y,bw,bh=w['box']
            if w['t0']<=o['t1']+0.5 and o['cat']==w['cat'] and not (x>ox+ow or ox>x+bw or y>oy+oh or oy>y+bh):
                nx,ny=min(ox,x),min(oy,y); o['box']=[nx,ny,max(ox+ow,x+bw)-nx,max(oy+oh,y+bh)-ny]; o['t1']=max(o['t1'],w['t1']); break
        else: out.append(dict(w))
    return out
STOP=re.compile(r'new contact|invite|link|qr code|search|contacts on|frequently|suggestions|add |create|schedule|group call|share|dismiss|cancel|select|chats|updates|communities|calls|message|whatsapp|google|meet|^you$|photo|voice|today|yesterday|\d{1,2}[:.]\d{2}|@|am$|pm$',re.I)
NAMES={'hdfc bank ltd','lalu cousin','amazon pay','bindu chechi edapt','premium subscriptions by karan'}
for f in sorted(glob.glob('scan2/*.json')):
    d=json.load(open(f))
    for r in d['res']:
        L=[h for h in r['hits'] if h[0]=='line']
        hdr=[h for h in L if LIST.search(h[1].strip())]
        for h in hdr:
            for k,txt,x,y,bw,bh in L:
                t=re.sub(r'[^\w ]','',txt).strip().lower()
                if y>h[3]+h[5] and 4<=len(t)<=40 and not STOP.search(t) and not re.fullmatch(r'[\d ]+',t): NAMES.add(t)
json.dump(sorted(NAMES),open('names_found.json','w'),ensure_ascii=False)
if os.path.exists('names_curated.json'): NAMES=set(json.load(open('names_curated.json')))  # plus a few extra private seed names (kept out of the repo)
summary={}
def load(f):
    d=json.load(open(f)); g=f.replace('scan2/','scan3/')
    if os.path.exists(g):
        e={r['t']:r['hits'] for r in json.load(open(g))['res']}
        for r in d['res']: r['hits']=r['hits']+e.pop(r['t'],[])
        d['res']+= [{'t':t,'hits':h} for t,h in e.items()]
    return d
for f in sorted(glob.glob('scan2/*.json')):
    d=load(f); W,H=d['w'],d['h']; mob=W<1300; ws=[]; tracks={}
    V=int(0.08*H) if mob else 60
    for r in d['res']:
        t=r['t']
        lines=[h for h in r['hits'] if h[0]=='line']
        for k,txt,x,y,bw,bh in r['hits']:
            if (k=='email' and EM.search(txt) and not re.match(r'(abc|example|name|youremail|email)@',txt.lower())) or (k=='phone' and PH.search(txt) and len(set(re.sub(r'\D','',PH.search(txt).group(0))[-10:]))>3 and not re.search(r'/|http|\.com|docs\.',txt)):
                bh=max(bh,20)
                if mob: box=[0,y-int(1.9*bh)-8,W,int(3.4*bh)+16]
                else: box=[x-90,y-int(1.6*bh)-6,bw+130,int(3.1*bh)+12]
                key=(k,re.sub(r'[^a-z0-9]','',txt.lower())[:12])
                tracks.setdefault(key,[]).append((t,box))
        nm=[l for l in lines if re.sub(r'[^\w ]','',l[1]).strip().lower() in NAMES]
        if len(nm)>=2:
            y0=min(l[3] for l in nm);y1=max(l[3]+l[5] for l in nm)
            if mob: box=[0,y0-120,W,y1-y0+240]
            else:
                x0=min(l[2] for l in nm);x1=max(l[2]+l[4] for l in nm); box=[x0-110,y0-60,x1-x0+260,y1-y0+120]
            ws.append({'t0':max(0,t-0.5-PAD),'t1':t+0.5+PAD,'box':box,'cat':'names'})
        for k,txt,x,y,bw,bh in lines:
            m=LIST.search(txt.strip())
            if m and mob:
                below=[l for l in lines if l[3]>y+bh]
                yb=max([l[3]+l[5] for l in below],default=y+bh)
                if yb-(y+bh)>80:
                    ws.append({'t0':max(0,t-0.5-PAD),'t1':t+0.5+PAD,'box':[0,max(0,y+bh+4-V),W,min(H-60,yb+40+V)-(y+bh+4-V)],'cat':'list'})
    def U(a,b): x,y=min(a[0],b[0]),min(a[1],b[1]); return [x,y,max(a[0]+a[2],b[0]+b[2])-x,max(a[1]+a[3],b[1]+b[3])-y]
    def grow(b): return [b[0],b[1]-V,b[2],b[3]+2*V]
    for (k,_),D in tracks.items():
        D.sort(); chains=[[D[0]]]
        for p in D[1:]:
            (chains[-1].append(p) if p[0]-chains[-1][-1][0]<=3 else chains.append([p]))
        for c in chains:
            ws.append({'t0':max(0,c[0][0]-0.5-PAD),'t1':c[0][0]+0.5,'box':grow(c[0][1]),'cat':k})
            ws.append({'t0':c[-1][0]-0.5,'t1':c[-1][0]+0.5+PAD,'box':grow(c[-1][1]),'cat':k})
            for a,b in zip(c,c[1:]): ws.append({'t0':a[0]-0.5,'t1':b[0]+0.5,'box':U(a[1],b[1]),'cat':k})
    ws+= [dict(w) for w in json.load(open('manual.json')).get(d['file'],[])] if os.path.exists('manual.json') else []
    ws=merge(merge(ws))
    key=os.path.basename(f)[:-5]
    json.dump({'file':d['file'],'windows':ws},open(f'windows/{key}.json','w'))
    summary[d['file']]=(len(ws),round(sum(w['t1']-w['t0'] for w in ws)))
for k,v in summary.items(): print(v,k[-70:])
