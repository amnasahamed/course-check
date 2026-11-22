#!/bin/bash
# usage: sheet.sh <video> <outdir> ; one tile per N seconds so ~40 tiles
f="$1"; o="$2"; d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f"); n=$(python3 -c "print(max(10,int($d/40)))")
name=$(echo "${f#dl/}" | sed 's|[/: ]|_|g; s|—|-|g' | cut -c1-120)
ffmpeg -v error -y -skip_frame nokey -i "$f" -an -vf "fps=1/$n,scale=320:320:force_original_aspect_ratio=decrease,pad=320:320:(ow-iw)/2:(oh-ih)/2,drawtext=text='%{pts\:hms}':x=4:y=4:fontsize=18:fontcolor=yellow:box=1:boxcolor=black,tile=8x5" -frames:v 1 "$o/$name.jpg"
echo "$n s/tile $o/$name.jpg"
