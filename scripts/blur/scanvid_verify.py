import sys,os,json,subprocess,tempfile,hashlib,glob
sys.path.insert(0,os.path.dirname(__file__))
from ocr import scan
from PIL import Image,ImageChops,ImageStat
v=sys.argv[1]; key=hashlib.md5(v.encode()).hexdigest()[:10]; out=f'scanv/{key}.json'
if os.path.exists(out): sys.exit()
with tempfile.TemporaryDirectory(dir='scanv') as T:
    subprocess.run(['ffmpeg','-v','error','-i',v,'-vf','fps=1','-q:v','3',f'{T}/%06d.jpg'],check=True)
    F=sorted(glob.glob(f'{T}/*.jpg')); res=[]; prev=None; ph=[]; n=0
    for i,f in enumerate(F):
        im=Image.open(f).convert('RGB'); sm=im.resize((96,96)).convert('L')
        if prev is not None and ImageStat.Stat(ImageChops.difference(sm,prev)).mean[0]<1.5: h=ph
        else: h=scan(im); n+=1; prev=sm; ph=h
        if h: res.append({'t':i+0.5,'hits':h})   # fps=1 frame i covers [i,i+1)
    json.dump({'file':v,'w':im.width,'h':im.height,'frames':len(F),'ocr':n,'res':res},open(out,'w'),ensure_ascii=False)
print(v,len(F),n,len(res),flush=True)
