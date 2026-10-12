# sound-effects

**Makes Claude's motion graphics sound like a real editor scored them, not cheap electronic beeps.** It's a measured sound pass with a free CC0 sound library built in.

Based on the sound-pass prompt by **Vox ([@Voxyz_ai](https://x.com/Voxyz_ai/status/2109358372873183564))**.

## What it does
1. Builds a cue list from your animation: cuts, pops, clicks, typing and reveals.
2. Finds the music's beats with librosa, then **checks the grid against the kick drums below 120 Hz** and shifts it if librosa locked onto the off-beat.
3. Lands cuts on the beat, by retiming the animation or moving where the music starts.
4. Places one real sound effect per cue from the bundled library: whoosh, transition, pop, click, typing, riser, impact, ding, glitch, UI blips and ambience.
5. Mixes to **-16 LUFS with true peaks below -4 dBFS, measured on the exported MP4**, and checks the mono downmix too.
6. Writes `report.html`, where you can hear each cue, swap sounds or let the model decide.
7. Proves it with frames and waveforms for each cue, plus 5 timestamps for you to check with headphones.

## Library
`sfx/` contains a 7-sound **default kit** (`sfx/kit/`, 6 CC0 files plus Mixkit typing fetched at runtime) and 103 CC0 alternatives, stored as small OGG Vorbis files (about 2.7 MB in total). Every bundled file is **CC0**, from Kenney and Freesound. `sfx/manifest.json` lists each file's category, duration, source URL and licence. There are also 40 optional Mixkit links that are downloaded at runtime and never stored in this repo. See `LICENSES.md`.

## Install
```
npx skills add Barty-Bart/motion-graphics
```
Then ask Claude Code: "add sound effects to this video".
Requirements: ffmpeg and Python 3.10+. The skill installs librosa and its dependencies into a local venv.

## Credits
- Sound-pass method: **Vox ([@Voxyz_ai](https://x.com/Voxyz_ai/status/2109358372873183564))**.
- Default kit: "Whoosh" by qubodup, "Classic Click" by adh.dreaming, "POP SFX Neutral" by ethernel0, "Cinematic Riser #3 subtle" by BeaconStudio, "soft_impact3" by peoplearehappy, "Click / Tick" by Squirrel_404 (all CC0, Freesound), and "Fast laptop keyboard typing" by Mixkit (Mixkit Free License, downloaded at runtime).
- Alternatives: Kenney (kenney.nl), Narjara, syntheffects, DeVern, Jummit, malle99 and every other Freesound creator listed in `LICENSES.md`.

The top picks per category, with links, are in `TOP-PICKS.md`. Every file's source and licence is in `LICENSES.md`.
