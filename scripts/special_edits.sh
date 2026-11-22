#!/bin/bash
# Special edits (run from a folder containing dl/ = original Drive download, tools in scripts/)
set -e
M="dl/Section 1: SECTION 1 — GET READY TO TEACH ONLINE/Module 1 — Google Meet"
P="dl/SECTION 7 — BUILD YOUR PROFESSIONAL IDENTITY/Module 17 — AI-Powered CV _ Resume Building"
L="dl/SECTION 7 — BUILD YOUR PROFESSIONAL IDENTITY/Module 18 — LinkedIn Profile Creation & Optimisation"
# 1) Module 1 mobile: sync separate voice onto silent 2nd-part video (29 anchor segments, see meet2_sync.py)
python3 scripts/meet2_sync.py "$M/Meet Mobile 2nd Part.mp4" "$M/Google Meet 2nd Part Voice.m4a" out/meet2_raw.mp4
#    then: part 1 [0 - 12:31.0] (video freezes after this; Android stops screen recording during Meet screen share)
#    + synced part 2  -> "Google Meet Mobile (complete).mp4" (concat of re-encoded segments, then norm.sh)
# 2) Module 17: insert pickup "Missing Slide 6" -> main [0-645.0] + pickup [10.85-130.38] + main [646.6-end]
# 3) LinkedIn Mobile: blur saved-password emails (67.3-72.2s) and Google account chooser (88.8-95.3s)
VF="split=3[m][x][y];[x]crop=1000:520:40:1390,boxblur=25:3[bx];[y]crop=1000:1700:40:540,boxblur=25:3[by];[m][bx]overlay=40:1390:enable='between(t,67.3,72.2)'[t1];[t1][by]overlay=40:540:enable='between(t,88.8,95.3)'" \
  scripts/norm.sh "$L/LinkedIn Mobile.mp4" "edited/LinkedIn Mobile.mp4" "pan=mono|c0=c1"
# 4) Dead air trims
SS=8.4 scripts/norm.sh "$L/Linkedin Computer Use.mp4" "edited/Linkedin Computer Use.mp4" "pan=mono|c0=c0"
SS=5.0 scripts/norm.sh "dl/Section 2 - BECOME AN AI-POWERED TEACHER/Module 8 — ChatGPT for Teachers/ChatGPT for Teachers.mp4" "edited/ChatGPT for Teachers.mp4" "pan=mono|c0=c0"
