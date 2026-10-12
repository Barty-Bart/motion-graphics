# sound-effects

<p align="center"><img src="../../docs/sound-effects.gif" width="80%" alt="Before and after: a silent explainer clip, then the same clip after the sound pass with its audio level meter moving"></p>

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

## What you get
The video with sound (`after.mp4`), a `report.html` where you can play every cue and swap sounds (or let the model decide), proof frames and waveforms for each cue, and 5 timestamps to check with headphones.

## The sounds
A 7-sound default kit plus 103 alternatives (whoosh, transition, pop, click, typing, riser, impact, ding, glitch, UI blips, ambience), all CC0 from Kenney and Freesound and bundled as small OGG files. The default typing sound and 40 optional extras come from Mixkit, which allows use in videos but not redistribution, so the skill downloads them into your project when needed and they're never stored in this repo. Every file's creator, source and licence is in [`LICENSES.md`](LICENSES.md).

## Use it
Run `npx skills add Barty-Bart/motion-graphics` and pick `sound-effects`, then ask Claude Code something like *"add sound effects to this video"*.

## How it measures
Claude can't hear, so this skill measures everything instead: it checks the music's beat grid against the kick drums, lands cuts on the beat, places one real sound effect per cue, and mixes to -16 LUFS measured on the exported MP4.

## Library
`sfx/` contains a 7-sound **default kit** (`sfx/kit/`, 6 CC0 files plus Mixkit typing fetched at runtime) and 103 CC0 alternatives, stored as small OGG Vorbis files (about 2.7 MB in total). Every bundled file is **CC0**, from Kenney and Freesound. `sfx/manifest.json` lists each file's category, duration, source URL and licence. There are also 40 optional Mixkit links that are downloaded at runtime and never stored in this repo. See `LICENSES.md`.

The bundled files are compressed OGG previews. If one sounds too rough, every entry in the manifest links to its original (Freesound or Kenney), and the skill can help you grab it. Ask for more sounds and it will search Freesound, Kenney, Mixkit and other free libraries and suggest options with their licences.

## Install
```
npx skills add Barty-Bart/motion-graphics
```
Then ask Claude Code: "add sound effects to this video".
Requirements: ffmpeg and Python 3.10+. The skill installs librosa and its dependencies into a local venv.

## Credits
- Default kit (short list): qubodup, adh.dreaming, ethernel0, BeaconStudio, peoplearehappy, Squirrel_404 and Mixkit; alternatives by Kenney and the Freesound creators listed in [`TOP-PICKS.md`](TOP-PICKS.md) and [`LICENSES.md`](LICENSES.md).

The top picks per category, with links, are in `TOP-PICKS.md`. Every file's source and licence is in `LICENSES.md`.

## Licence
Skill code: MIT. Sound effects in `sfx/`: CC0 1.0 (see [`LICENSES.md`](LICENSES.md)). Mixkit sounds are downloaded at runtime under the Mixkit Free License and never stored in this repo.
