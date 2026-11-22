# START TEACHING ONLINE — Video Review & Edits

Source: Google Drive folder "START TEACHING ONLINE" (69 files: 59 videos, 1 voice file, 9 PDFs; 14.6 hours, 17 GB, Malayalam narration).
All files downloaded and checked. Every video was checked for loudness, channel balance, silence, black frames and frozen picture. Contact sheets were used for a visual pass. Speech was transcribed where an edit depended on it.

## Summary

| # | Issue | Videos affected | Fixed? |
|---|-------|-----------------|--------|
| 1 | **Voice only in the RIGHT channel** (left is silent). With headphones, students hear the teacher in one ear only. | All 27 mobile recordings | ✅ Voice now in both ears |
| 2 | **Audio far too quiet**: -27 to -34 LUFS (online video standard is about -16) | All 29 computer and slide recordings | ✅ Raised to -16 LUFS |
| 3 | **Google Meet Mobile: picture frozen for the last 13.6 min** (27:11 total, frozen after about 13:30). Android stops screen recording when Meet screen-sharing starts. | Module 1 | ✅ Cut at 12:31 and joined to the reshot part 2 (below) |
| 4 | **Meet Mobile 2nd Part has no audio**. Its narration was a separate file (`Google Meet 2nd Part Voice.m4a`, recorded 3 days later). It is 3 minutes longer than the video and in a different order. | Module 1 | ✅ Voice synced to the picture (29 timed segments). Unnarrated fumbling (WhatsApp, home screen, Play Store) and a 27 s silence removed |
| 5 | **Slide 6 missing**. "Understanding a Good Teacher CV" skips slide 6 ("How Do You Describe Teaching Experience?"). It was recorded separately as `Missing Slide 6.mp4`. | Module 17 | ✅ Pickup inserted between slides 5 and 7, with no repeated lines |
| 6 | **Personal email addresses on screen**: Google Password Manager (3 accounts) and the Google account chooser (10 accounts) | LinkedIn Mobile, 1:07–1:12 and 1:29–1:35 | ✅ Blurred |
| 7 | Dead air at the start | LinkedIn Computer Use (9 s), ChatGPT for Teachers (6 s) | ✅ Trimmed |
| 8 | Filename typos | `(Mobile) ntelligent CV`, `AI InterviewPreparation`, `Section 3 .mp4`, `Docs + Sheet .mp4`, `Get Your First Students (1)` | ✅ Renamed |

All edited videos were checked afterwards: 58/58 measure -16.3 to -17.4 LUFS, with the voice in both ears.
Where only the audio was fixed, the **picture is copied untouched** (no re-encode, no quality loss).

## New / replaced files

| Folder | Edited file | Replaces |
|--------|-------------|----------|
| Module 1 — Google Meet | `Google Meet Mobile (complete).mp4` (24:29) | `Google Meet Mobile.mp4` + `Meet Mobile 2nd Part.mp4` + `Google Meet 2nd Part Voice.m4a` |
| Module 1 — Google Meet | `Meet Mobile 2nd Part (with voice).mp4` (11:58) | (part 2 on its own, if you prefer two videos) |
| Module 17 — CV | `Understanding a Good Teacher CV (with slide 6).mp4` (18:00) | `Understanding a Good Teacher CV.mp4` + `Missing Slide 6.mp4` |

All other videos keep their names (apart from the typo fixes) and have the audio fixes.

## Still needs your attention (could not be fixed by editing)

1. **Lost content in Google Meet Mobile.** The frozen part of the original covered **pinning participants / layouts** (about 15:25–19:30) and **joining a meeting from a link with a second account** (about 24:05–26:10). The reshot part 2 doesn't cover these, so they are no longer in the module. Re-record them if they matter.
2. **Black screens during sign-in / secure screens.** Android blacks out secure screens while recording, so the narration plays over black:
   LinkedIn Mobile 1:11–1:30 (19 s, LinkedIn sign-in), Canva Mobile 1:41–1:56 and 2:03–2:11, Productivity 8:04–8:12, WhatsApp Mobile 12:58–13:04, plus short 1–4 s blips in about 10 other mobile videos. Consider a text overlay ("Sign-in screen hidden for privacy").
3. **Other personal data on screen** (not blurred; worth reviewing before publishing):
   - Google Meet videos, "Add participants" / suggestions: contacts' names, emails and a phone number (e.g. Meet Mobile 2nd Part around 1:05; Google Meet Mobile around 6:40).
   - Meet Mobile 2nd Part around 3:00: a WhatsApp chat with bill amounts and names is briefly visible.
   - Other mobile screen recordings likely show similar account lists; I only checked the frames in the contact sheets.
4. **Some mobile recordings are clipped** (original true peak above 0 dB, e.g. AI Audio Mobile, NotebookLM Mobile). Loudness is fixed, but distortion already in the recording can't be removed.
5. **Course structure gaps** (for your information):
   - Slide videos / PDFs exist only for Modules 1, 2, 4, 5, 6, 17, 22, 23, 24. Modules 3, 7–16, 18–21 and 25 have demo videos only.
   - Some modules have only a computer *or* only a mobile version (e.g. 12 computer only; 14, 15, 19–21, 25 mobile only).
   - `Tutor Profile (Personal website Part 1/2)` and the Module 25 video have no `.mp4` extension on Drive. They are MP4s, and the edited copies are saved as `.mp4`.
   - `Computer Using.mp4` (Module 1) has 48 s of frozen picture at the end (narration continues, so it was left in).

## How it was done (reproducible)

- `scripts/probe.py`: technical check (loudness, per-channel level, silence, black, freeze). Raw results are in `data/probe_results.jsonl`.
- `scripts/norm.sh`: two-pass EBU R128 loudness normalisation to -16 LUFS / -1.5 dBTP, 80 Hz high-pass, mono output, video stream copied.
- `scripts/batch_audio_fix.sh`: the 52 audio-only fixes.
- `scripts/meet2_sync.py`: voice-to-video sync map for Meet part 2 (English translation of the voice is in `data/meet2_voice_transcript_en.json`).
- `scripts/special_edits.sh`: the Module 1 join, the Module 17 slide-6 splice, the LinkedIn blur and the dead-air trims.
