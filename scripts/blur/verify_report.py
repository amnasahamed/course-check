import json,glob,re,collections
src=open('tools/build_windows.py').read(); exec(src[src.index('EM='):src.index('PAD=')])
def ok_phone(txt):
    m=PH.search(txt); return m and len(set(re.sub(r'\D','',m.group(0))[-10:]))>3 and not re.search(r'/|http|\.com|docs\.',txt)
tot=0
for f in sorted(glob.glob('scanv/*.json')):
    d=json.load(open(f)); left=[]
    for r in d['res']:
        for k,txt,*b in r['hits']:
            if k=='email' and EM.search(txt) and not re.match(r'(abc|example|name|youremail|email)@',txt.lower()): left.append((r['t'],'email',b))
            if k=='phone' and ok_phone(txt): left.append((r['t'],'phone',b))
    tot+=len(left)
    print(len(left), d['file'][-60:], [(t,k,bb[:2]) for t,k,bb in left[:6]])
print('TOTAL remaining detections',tot)
