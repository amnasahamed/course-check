#!/bin/bash
# start renders (2 parallel) only while under the time budget; resumable
cd /tmp/claude-0/-home-user-course-check/b80c2a07-50f3-5e1b-b922-6276d5722a16/scratchpad
export START=$(date +%s) BUDGET=${BUDGET:-4800}
job(){ [ $(( $(date +%s) - START )) -gt $BUDGET ] && exit 0; tools/render_one.sh "$1" "$2"; }
export -f job
tr '\t' '\0' < render_jobs.txt | tr '\n' '\0' | xargs -0 -n2 -P2 bash -c 'job "$0" "$1"'
left=0; while IFS=$'\t' read -r w src; do [ -s "blurred/${src#edited/}" ] || left=$((left+1)); done < render_jobs.txt
echo "CHUNKDONE left=$left"
