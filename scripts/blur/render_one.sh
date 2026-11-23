#!/bin/bash
cd /tmp/claude-0/-home-user-course-check/b80c2a07-50f3-5e1b-b922-6276d5722a16/scratchpad
w="$1"; src="$2"; out="blurred/${src#edited/}"; [ -s "$out" ] && exit 0
mkdir -p "$(dirname "$out")"
python3 tools/render_blur.py "$src" "$w" "$out.tmp.mp4" </dev/null && mv "$out.tmp.mp4" "$out" && echo "RENDERED $out" || echo "RENDERFAIL $src"
