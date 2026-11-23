# review.py windows/<key>.json out.jpg : one tile per window at its middle, box drawn in red
import json,sys,subprocess,os,tempfile
d=json.load(open(sys.argv[1])); ws=d['windows']; T=tempfile.mkdtemp(dir='.')
tiles=[]
for i,w in enumerate(ws[:40]):
    t=(w['t0']+w['t1'])/2; x,y,bw,bh=w['box']; o=f'{T}/{i:03d}.png'
    subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{t:.2f}','-i',d['file'],'-frames:v','1','-vf',
      f"drawbox=x={max(0,x)}:y={max(0,y)}:w={bw}:h={bh}:color=red@0.9:t=8,scale=-2:600,drawtext=text='{i} {w['t0']:.0f}-{w['t1']:.0f} {w['cat'][:18]}':x=4:y=4:fontsize=18:fontcolor=yellow:box=1",o])
    tiles.append(o)
n=len(tiles); cols=min(n,8) if n else 1
subprocess.run(['ffmpeg','-v','error','-y','-pattern_type','glob','-i',f'{T}/*.png','-vf',f'tile={cols}x{(n+cols-1)//cols}',sys.argv[2]])
subprocess.run(['rm','-r',T])
print(n,len(ws))
