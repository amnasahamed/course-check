#!/usr/bin/env python3
# usage: gup.py <local_root> <list_of_relpaths_file>   uploads into Drive ROOT keeping subfolders; resumable; state in gup_state.json
import sys,os,json,requests,time
S=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT=os.environ['DRIVE_FOLDER_ID']  # target Drive folder
API='https://www.googleapis.com/drive/v3/files'; UP='https://www.googleapis.com/upload/drive/v3/files'
V='/root/.ccr/ca-bundle.crt'; H={'Authorization':'Bearer proxy-injected'}
st_path=os.path.join(S,'gup_state.json')
st=json.load(open(st_path)) if os.path.exists(st_path) else {'folders':{},'files':{}}
def save(): json.dump(st,open(st_path,'w'),indent=1)
class Auth(Exception): pass
def chk(r):
    if r.status_code in (401,403): raise Auth(r.text[:300])
    r.raise_for_status(); return r
def folder(rel):
    if rel in ('','.'): return ROOT
    if rel in st['folders']: return st['folders'][rel]
    par=folder(os.path.dirname(rel)); name=os.path.basename(rel)
    q="name='%s' and '%s' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"%(name.replace("'","\\'"),par)
    r=chk(requests.get(API,params={'q':q,'fields':'files(id)','supportsAllDrives':'true','includeItemsFromAllDrives':'true'},headers=H,verify=V)).json()['files']
    fid=r[0]['id'] if r else chk(requests.post(API,params={'supportsAllDrives':'true'},json={'name':name,'mimeType':'application/vnd.google-apps.folder','parents':[par]},headers=H,verify=V)).json()['id']
    st['folders'][rel]=fid; save(); return fid
CH=32*1024*1024
def upload(root,rel):
    if rel in st['files']: print('SKIP',rel,flush=True); return
    p=os.path.join(root,rel); size=os.path.getsize(p); par=folder(os.path.dirname(rel))
    r=chk(requests.post(UP,params={'uploadType':'resumable','supportsAllDrives':'true'},json={'name':os.path.basename(rel),'parents':[par]},
        headers={**H,'X-Upload-Content-Type':'video/mp4','X-Upload-Content-Length':str(size)},verify=V))
    url=r.headers['Location']; off=0
    with open(p,'rb') as f:
        while off<size:
            f.seek(off); data=f.read(CH); end=off+len(data)-1
            for a in range(5):
                try:
                    r=requests.put(url,data=data,headers={**H,'Content-Range':'bytes %d-%d/%d'%(off,end,size)},verify=V,timeout=600); break
                except requests.RequestException as e: print('retry',e,flush=True); time.sleep(5*(a+1))
            if r.status_code in (200,201): off=size; st['files'][rel]=r.json()['id']; save(); break
            if r.status_code==308:
                rg=r.headers.get('Range'); off=int(rg.split('-')[1])+1 if rg else 0; continue
            chk(r)
    print('UPLOADED',rel,size,flush=True)
root=sys.argv[1]
try:
    for rel in [l.rstrip('\n') for l in open(sys.argv[2]) if l.strip()]: upload(root,rel)
    print('ALLDONE',flush=True)
except Auth as e: print('AUTHFAIL',e,flush=True)
