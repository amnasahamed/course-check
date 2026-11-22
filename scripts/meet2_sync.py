import subprocess,sys,os
V,A,OUT=sys.argv[1:4]; T='out/meet2_tmp'; os.makedirs(T,exist_ok=True)
S=[(0,25,130,152),(25,48,152,164),(48,66,230,238),(66,109,238,282),(109,120,282,290),(120,128,312,332),
(128,137,332,340),(164,185,340,362),(185,218,362,374),(218,231,374,382),(231,247,382,388),(247,272,388,396),
(272,281,396,404),(281,333,404,416),(333,345,416,420),(345,371,420,434),(371,383,434,440),(383,398,440,446),
(398,437,446,456),(437,451,456,463),(451,480,463,471),(480,524,471,479),(524,540,479,487),(540,572,487,500),
(572,584,500,505),(584,614,505,516),(614,631,516,534),(631,642,534,545.1),(642,745.3,518,None)]
L=[]
for i,(a0,a1,v0,v1) in enumerate(S):
    da=a1-a0; o=f'{T}/s{i:02d}.mp4'; L.append(o)
    if v1 is None: vin=['-ss',str(v0),'-t','0.5','-i',V]; vf=f"setpts=PTS-STARTPTS,fps=30,tpad=stop_mode=clone:stop_duration={da}"
    else: vin=['-ss',str(v0),'-t',str(v1-v0),'-i',V]; vf=f"setpts=(PTS-STARTPTS)*{da/(v1-v0):.5f},fps=30,tpad=stop_mode=clone:stop_duration=1"
    af=f"afade=t=in:d=0.03,afade=t=out:st={da-0.03:.3f}:d=0.03"
    subprocess.run(['ffmpeg','-v','error','-y',*vin,'-ss',str(a0),'-t',str(da),'-i',A,'-vf',vf+',setsar=1','-af',af,'-t',str(da),
      '-map','0:v','-map','1:a','-c:v','libx264','-preset','medium','-crf','22','-pix_fmt','yuv420p','-c:a','pcm_s16le','-ar','48000','-ac','1',o.replace('.mp4','.mov')],check=True)
open(f'{T}/list.txt','w').write(''.join(f"file '{os.path.abspath(x.replace('.mp4','.mov'))}'\n" for x in L))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',f'{T}/list.txt','-c:v','copy','-af','highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11',
  '-c:a','aac','-b:a','160k','-ar','48000','-movflags','+faststart',OUT],check=True)
