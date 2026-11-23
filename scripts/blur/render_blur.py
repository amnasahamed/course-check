# usage: render_blur.py in.mp4 windows.json out.mp4   windows: [{"t0":..,"t1":..,"box":[x,y,w,h],"cat":..}]
import sys,json,subprocess
src,wf,out=sys.argv[1:4]; W=json.load(open(wf)); W=W['windows'] if isinstance(W,dict) else W
pr=json.loads(subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height:format=duration','-of','json',src],capture_output=True,text=True).stdout)
w,h=pr['streams'][0]['width'],pr['streams'][0]['height']; dur=float(pr['format']['duration'])
boxes=[]
for x in W:
    bx,by,bw,bh=[int(v) for v in x['box']]; bx=max(0,bx);by=max(0,by);bw=min(bw,w-bx);bh=min(bh,h-by)
    boxes.append(f"drawbox=x={bx}:y={by}:w={bw}:h={bh}:color=white:t=fill:enable='between(t,{x['t0']:.2f},{x['t1']:.2f})'")
mask=f"color=black:s={w}x{h}:r=30:d={dur:.3f},format=gray,"+','.join(boxes)
fg=f"{mask}[m];[0:v]split=2[o][c];[c]scale={w//4}:{h//4},boxblur=12:3,scale={w}:{h},format=yuv420p[b];[b][m]alphamerge[ba];[o][ba]overlay=shortest=1:format=auto,format=yuv420p[v]"
open(out+'.filter','w').write(fg)
subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-i',src,'-filter_complex_script',out+'.filter','-map','[v]','-map','0:a','-c:a','copy','-c:v','libx264','-preset','superfast','-crf','20','-movflags','+faststart',out],check=True)
