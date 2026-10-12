---
name: sound-effects
description: Add a measured sound pass to a motion-graphics video made with Claude Code (HyperFrames, Remotion, GSAP, Claude Motion or the motion-broll skill). Builds a cue list, checks the music's beat grid against the kick drums, lands cuts on the beat, places one real sound effect per cue from a bundled CC0 library, mixes to -16 LUFS with true peaks below -4 dBFS measured on the exported MP4, and proves it with frames, waveforms and 5 timestamps for a human to check. Use when someone wants sound effects, sound design or music added to a motion-graphics video, or says their AI video sounds like cheap beeps.
---

# Sound effects

Claude can't hear. So this skill never judges sound by feel: it measures every step, and it hands the user 5 timestamps to check with headphones. It never says "it sounds good".

The approach is Vox's sound-pass prompt (@Voxyz_ai, https://x.com/Voxyz_ai/status/2109358372873183564, 11 Oct 2026). Keep that credit.

## Default kit (use this first)
`sfx/manifest.json` → `default_kit`: one sound per core category, picked by ear by Bart (12 Oct 2026). Use it unless the user asks for something else.

| Category | Sound | Where it comes from |
|---|---|---|
| whoosh | "Whoosh" by qubodup | bundled `sfx/kit/whoosh.ogg` (CC0) |
| click | "Classic Click" by adh.dreaming | bundled `sfx/kit/click.ogg` (CC0) |
| pop | "POP SFX Neutral" by ethernel0 | bundled `sfx/kit/pop.ogg` (CC0) |
| riser | "Cinematic Riser #3 subtle" | bundled `sfx/kit/riser.ogg` (CC0) |
| impact | "soft_impact3" by peoplearehappy | bundled `sfx/kit/impact.ogg` (CC0) |
| tick | "Click / Tick" by Squirrel_404 | bundled `sfx/kit/tick.ogg` (CC0) |
| typing | Mixkit "Fast laptop keyboard typing" (#1392) | **downloaded at runtime** into `<out>/sound-effects-cache/` (Mixkit licence: never commit it) |

Everything else in the manifest is an alternative (`alt_categories` lists which categories can stand in for each other). See `TOP-PICKS.md` for credits.

## Rules
- **Never synthesize music or sound effects in code** (no oscillator or sine beeps). Use real recorded files.
- **Sound effects: use the bundled library first.** `sfx/manifest.json` lists every file with its category, duration, source and licence. All bundled files are CC0.
- If the bundled library has nothing that fits, use the `runtime` entries in the manifest (Mixkit). Download them into the user's project, never into this skill folder, and never commit them. Mixkit allows use in videos but not standalone redistribution.
- **Music:** a track the user gives you, or one with a licence that allows monetised YouTube use (Mixkit Stock Music Free License, CC0). Write the source and licence into `SOUND.md`. If neither exists, ask the user.
- Measure the **exported MP4**, never the intermediate WAV.

## 1. Set up
Needs ffmpeg and Python 3.10+. Install into a folder you can delete:
```
python3 -m venv .sound-effects
.sound-effects/bin/pip install librosa soundfile numpy scipy matplotlib
```

## 2. Build the cue list
Read the video's duration and fps with `ffprobe`. List every moment that needs a sound. Take them from the composition source when you can (HyperFrames/Remotion timeline, GSAP labels, motion-broll `plan.json`). Otherwise detect scene cuts with `ffmpeg -i in.mp4 -vf "select='gt(scene,0.3)',showinfo" -f null -`.
Write `cues.json` as `[{"t": 2.0, "type": "scene_cut", "desc": "cut to card"}, {"t": 4.2, "type": "typing", "dur": 1.3, "desc": "..."}]`.

The cue types map to library categories (`category_map` in the manifest):

| Cue type | Category | Notes |
|---|---|---|
| movement (slide, camera move) | whoosh | starts 2 frames early; pick length to match the move |
| scene_cut | whoosh | short whoosh, 2 frames early (`transition` sounds are alternatives) |
| appear | pop | on the frame |
| click | click | on the frame |
| typing | typing | looped/trimmed to `dur`, quiet |
| build_up | riser | **ends** on the next hit |
| reveal | impact | the loudest SFX |
| success | pop | (`ding` sounds are alternatives) |
| error_or_tech | glitch | |
| hover_or_small_ui | tick | very quiet (`ui-blip` and `click` are alternatives) |
| bed | ambience | under everything, optional |

Use one sound per cue. Vary takes within a category so repeats don't sound robotic.

## 3. Beat grid, and check it
Run `librosa.beat.beat_track`. **librosa sometimes locks onto the off-beat.** Low-pass the music below 120 Hz, plot it against the beat lines for the first 4 bars, and compare where the kicks land. If the kicks don't sit on the lines, shift the whole grid by the median offset and plot again. Show the user `beatgrid.png`.

## 4. Put the big moves on the beat
Hard cuts and reveals should land on a beat. If you can change the animation timings, change them. If you can't, move where the music starts (search offsets and pick the one with the smallest cut-to-beat error). Report the error per cut in ms.

## 5. Place SFX and mix
Priority: **voiceover > SFX > music.** The music bed sits around -12 dB under the SFX and ducks under any voiceover by 8–12 dB.
Target **about -16 LUFS integrated** with **true peak below -4 dBFS**, so nothing clips after AAC compression or on a phone speaker. Export, measure, adjust gain or add a limiter, then export and measure again:
```
ffmpeg -nostats -i after.mp4 -af ebur128=peak=true -f null - 2>&1 | tail -12
ffmpeg -nostats -i after.mp4 -ac 1 -af ebur128=peak=true -f null - 2>&1 | tail -12   # mono check
```

## 6. Prove it
For every cue, grab one frame just before and just after it from the exported MP4, and plot the waveform around it (`checks/cue-XX.png`). Then pick the **5 riskiest timestamps** (largest beat error, long sounds such as typing and risers, the reveal) and give them to the user to check with headphones.

## Original-quality files
The bundled sounds are compressed OGG Vorbis previews (trimmed, normalised, often mono), which is fine for most videos. If a sound is too low quality for the job (audible artefacts, a close-up hero sound, a final master), fetch the original:
- Look up the entry's `source_url` in `sfx/manifest.json`. Every bundled and `default_kit` entry has one.
- **Freesound** (`freesound.org/people/<user>/sounds/<id>/`): the original is the Download button on that page. It needs a free Freesound account, so ask the user to download it (or use their API key if they give you one).
- **Kenney** (`kenney.nl/assets/<pack>`): download the pack zip from that page. Each Kenney entry's `original_file` in the manifest names the exact file, e.g. `kenney_interface-sounds.zip → Audio/click_001.ogg`. The rule: drop the prefix (`kenney-interface-` → interface-sounds, `kenney-ui-` → ui-audio, `kenney-digital-` → digital-audio, `kenney-impact-` → impact-sounds, `kenney-sci-` → sci-fi-sounds), then match the rest inside `Audio/` ignoring case, with `-` read as `_` (`kenney-digital-phaserup1` → `Audio/phaserUp1.ogg`, `kenney-impact-impactpunch-heavy-000` → `Audio/impactPunch_heavy_000.ogg`). Kenney's originals are OGG too, but unprocessed.
- Save originals into the user's project (for example `sound-effects-cache/originals/`), never into this skill folder, and pass the file to the script via `--swaps` or by editing a copy of the manifest. Apply the same trim and level as the bundled file.

## Find more sounds
When the user wants more or different sounds, search these sources, suggest 3–5 candidates with a link, creator and licence for each, and let the user pick. Only use or redistribute a sound as its licence allows.

| Source | Search | Licence notes |
|---|---|---|
| Freesound | `https://freesound.org/search/?q=<words>&f=license:"Creative Commons 0"` | Use the CC0 filter. CC0 can be bundled and needs no credit (credit anyway). CC-BY needs credit in the video description; never bundle CC-BY-NC or use it commercially. |
| Kenney | `https://kenney.nl/assets/category:Audio` | All CC0. Free to use and bundle. |
| Mixkit | `https://mixkit.co/free-sound-effects/<category>/` (e.g. `whoosh`, `typing`) | Mixkit SFX Free License: fine in videos, including monetised ones, but **no redistribution**. Download only into the user's project at runtime; never commit or bundle it. |
| Pixabay | `https://pixabay.com/sound-effects/search/<words>/` | Free in videos, no credit needed, but no standalone redistribution. The user downloads it in a browser; never bundle it. |
| Sonniss GDC bundles | `https://sonniss.com/gameaudiogdc/` | Royalty-free in videos; no raw redistribution or AI training. Local use only. |
| YouTube Audio Library | YouTube Studio → Audio Library | For YouTube videos only; available only inside Studio. Never bundle it. |

Only CC0 sounds may be added to this repo's `sfx/` folder, each with a manifest entry (file, category, duration, source_url, licence, attribution) and a row in `LICENSES.md`.

## Script
`scripts/sound_pass.py` runs steps 3–6 end to end:
```
.sound-effects/bin/python scripts/sound_pass.py --video silent.mp4 --cues cues.json \
  --music track.mp3 --manifest sfx/manifest.json --out out/
```
It outputs `after.mp4`, `report.html`, `SOUND.md` (log, cue → file table, LUFS and peak numbers, the 5 timestamps), `beatgrid.png` and `checks/`. Read its log and fix anything over target. If you changed the animation timings, re-render first.

## 7. Swap report
`sound_pass.py` also writes `report.html`. It lists every cue with its timestamp, category, the sound used (with a play button), the source page, licence and credit, plus the alternatives in that category, each with a play button and a "let model decide" option. Open it for the user. They choose, click **Download swaps.json**, and you re-run with `--swaps swaps.json`. `"auto"` means pick another sound from the alternatives. Keep cue indices stable between runs.

## Report to the user
Report the music source and licence, the beat-grid result (shifted or not, and by how much), the cut-to-beat errors, final LUFS and true peak (stereo and mono), and the 5 timestamps. Don't tell them it sounds good.
