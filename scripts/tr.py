import sys,json,subprocess,numpy as np
from faster_whisper import WhisperModel
p,out,task=sys.argv[1],sys.argv[2],sys.argv[3]
a=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p,'-vn','-f','s16le','-ac','1','-ar','16000','-'],capture_output=True).stdout,np.int16).astype(np.float32)/32768
m=WhisperModel(sys.argv[4] if len(sys.argv)>4 else 'small',device='cpu',compute_type='int8',cpu_threads=2)
s,i=m.transcribe(a,beam_size=1,task=task,language='ml',vad_filter=True,condition_on_previous_text=False)
S=[(round(x.start,1),round(x.end,1),x.text.strip()) for x in s]
json.dump(S,open(out,'w'),ensure_ascii=False)
for x in S: print(f"{x[0]:7.1f} {x[2]}")
