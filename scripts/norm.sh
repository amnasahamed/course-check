#!/bin/bash
# two-pass loudnorm -16 LUFS, mono. usage: norm.sh in out "pre-filter" ; env VF / SS for video re-encode/trim
in="$1"; out="$2"; pre="$3"; mkdir -p "$(dirname "$out")"
AF="${pre:+$pre,}highpass=f=70"
m=$(ffmpeg -nostats ${SS:+-ss $SS} -i "$in" -vn -af "$AF,loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json" -f null - 2>&1 | sed -n '/^{/,/^}/p')
g(){ echo "$m" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
if [ -n "$VF$SS" ]; then V=(-vf "${VF:-null}" -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p); else V=(-c:v copy); fi
ffmpeg -v error -y ${SS:+-ss $SS} -i "$in" -map 0:v:0 -map 0:a:0 "${V[@]}" -af "$AF,loudnorm=I=-16:TP=-1.5:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true" -ac 1 -c:a aac -b:a 128k -ar 48000 -movflags +faststart "$out"
