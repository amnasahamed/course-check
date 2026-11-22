import json,subprocess,sys,re,os
def run(c): return subprocess.run(c,capture_output=True,text=True)
def probe(p):
    r=json.loads(run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',p]).stdout or '{}')
    out={'file':p,'size_mb':round(int(r.get('format',{}).get('size',0))/1e6,1),'dur':float(r.get('format',{}).get('duration',0))}
    for s in r.get('streams',[]):
        if s['codec_type']=='video' and 'v' not in out:
            out['v']=f"{s['codec_name']} {s.get('width')}x{s.get('height')} {s.get('avg_frame_rate')} rot={next((sd.get('rotation') for sd in s.get('side_data_list',[]) if 'rotation' in sd),0)}"
        if s['codec_type']=='audio' and 'a' not in out:
            out['a']=f"{s['codec_name']} {s.get('sample_rate')} ch={s.get('channels')}"
    if 'a' in out:
        e=run(['ffmpeg','-nostats','-i',p,'-vn','-af','ebur128=peak=true,astats=measure_perchannel=RMS_level:measure_overall=none','-f','null','-']).stderr
        m=re.search(r'Integrated loudness:\s+I:\s+(-?[\d.]+)',e); out['lufs']=float(m.group(1)) if m else None
        m=re.search(r'True peak:\s+Peak:\s+(-?[\d.inf]+)',e); out['tp']=m.group(1) if m else None
        out['ch_rms']=re.findall(r'RMS level dB: (-?[\d.inf]+)',e)
        s=run(['ffmpeg','-nostats','-i',p,'-vn','-af','silencedetect=n=-45dB:d=4','-f','null','-']).stderr
        st=[float(x) for x in re.findall(r'silence_start: (-?[\d.]+)',s)]; en=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',s)]
        out['silences']=[(round(a,1),round(en[i],1) if i<len(en) else round(out['dur'],1)) for i,a in enumerate(st)]
    if 'v' in out:
        b=run(['ffmpeg','-nostats','-i',p,'-an','-vf','fps=2,blackdetect=d=1:pix_th=0.1,freezedetect=n=0.003:d=20','-f','null','-']).stderr
        out['black']=[(round(float(a),1),round(float(c),1)) for a,c in re.findall(r'black_start:([\d.]+) black_end:([\d.]+)',b)]
        fs=[float(x) for x in re.findall(r'freeze_start: ([\d.]+)',b)]; fe=[float(x) for x in re.findall(r'freeze_end: ([\d.]+)',b)]
        out['freeze']=[(round(a,1),round(fe[i],1) if i<len(fe) else round(out['dur'],1)) for i,a in enumerate(fs)]
    return out
print(json.dumps(probe(sys.argv[1])))
