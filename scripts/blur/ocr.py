import sys,re,pytesseract
from PIL import Image,ImageOps,ImageStat
EM=re.compile(r'\S+@[A-Za-z]{2,}|\S+\.(gmail|yahoo)|gmail\.com|yahoo\.com|hotmail|outlook\.com',re.I)
PH=re.compile(r'(\+91[\s-]?)?(?<!\d)[6-9]\d{4}[\s-]?\d{5}(?!\d)')
KW=re.compile(r'add participants|suggestions|choose an account|password manager|search contacts|add people|in-call messages|message yourself|switch account|manage your google account|share to|sharing text|contacts',re.I)
def _ocr(v,S):
    hits=[];lines={}
    d=pytesseract.image_to_data(v,config='--psm 11',output_type=pytesseract.Output.DICT)
    for i,w in enumerate(d['text']):
        w=w.strip()
        if not w: continue
        b=(int(d['left'][i]/S),int(d['top'][i]/S),int(d['width'][i]/S),int(d['height'][i]/S))
        if EM.search(w): hits.append(('email',w,*b))
        lines.setdefault((d['block_num'][i],d['par_num'][i],d['line_num'][i]),[]).append((w,b))
    for ws in lines.values():
        t=' '.join(w for w,_ in ws)
        x0=min(b[0] for _,b in ws);y0=min(b[1] for _,b in ws);x1=max(b[0]+b[2] for _,b in ws);y1=max(b[1]+b[3] for _,b in ws)
        if PH.search(t): hits.append(('phone',t,x0,y0,x1-x0,y1-y0))
        m=KW.search(t)
        if m: hits.append(('kw',m.group(0).lower(),x0,y0,x1-x0,y1-y0))
        hits.append(('line',t,x0,y0,x1-x0,y1-y0))
    return hits
def scan(img,mode='both'):
    g=ImageOps.grayscale(img); S=1
    dark=ImageStat.Stat(g).mean[0]<110
    if not dark: return _ocr(g,S) if mode!='thr' else []
    h=[]
    if mode in ('both','inv'): h+=_ocr(ImageOps.invert(g),S)
    if mode in ('both','thr'): h+=_ocr(ImageOps.invert(g.point(lambda p:255 if p>150 else 0)),S)
    return h
if __name__=='__main__':
    for p in sys.argv[1:]:
        h=scan(Image.open(p)); print(p,len(h)); [print('  ',x) for x in h]
