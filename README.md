# motion-graphics

Free video-editing skills for Claude Code. Each skill does one job.

> **Want my entire AI video editing process?** I teach it step by step, with the full set of skills, in my community: **[Bart's AI Workshop](https://www.skool.com/barts-ai-workshop-4507/about)**

| Skill | What it does |
|---|---|
| [`motion-broll`](#motion-broll) | Give it a video and a transcript and it makes motion-graphic B-roll timed to your words. |
| [`object-separation`](#object-separation) | Separates a person, product or hand from the background in a video, on your own computer, and shows you exactly what it picked up. |

More skills will be added to this repo.

## motion-broll

**Motion-graphic B-roll for your videos, made by Claude Code.** Give it a video and a transcript and it plans, animates and renders clips timed to your words. Each clip is one continuous shape that keeps morphing (pill → card → terminal → chart) and never cuts, with a cursor driving every change.

<p>
  <img src="docs/demo-panel.gif" width="49%" alt="A transparent panel animating beside a picture-in-picture shot of the speaker">
  <img src="docs/demo-cutaway.gif" width="49%" alt="A full-frame cutaway: build notes turning into a master prompt that is dragged into a session">
</p>

### What you get

You run `/motion-broll`, answer a few questions, approve a plan, and get back:

- **The clips**, named by where they go on your timeline (`04-master-prompt_0m32s40.mp4`). Full-frame cutaways are MP4. Panels that sit in empty space next to you are transparent ProRes 4444 `.mov`.
- **A preview render** of your video with the clips cut in.
- **`compare.html`**: original vs. with motion graphics, synced, as side by side, stacked or wipe.
- **`viewer.html`**: step through the clips one by one.
- **`TIMING.md`**: every clip with its in/out point and the line it covers.

The preview is for review. For your final cut, drop the clips into your own editor.

### Install

```
npx skills add Barty-Bart/motion-graphics
```

That installs the skills from this repo (pick `motion-broll`, `object-separation`, or both). It works in Claude Code and other agents that read skills.

Or copy a skill's folder from `skills/` into your project's `.claude/skills/` (or `~/.claude/skills/` to use it everywhere).

**Requirements for motion-broll:** Node 18+, Python 3, and ffmpeg (with the ProRes encoder, standard in Homebrew builds). On first run the skill installs Playwright and Chromium into a local `motion/` folder.

### Use it

```
/motion-broll
```

Then point it at your video and transcript (an SRT from your editor, Descript or YouTube works). It will:

1. **Inspect the footage.** It reads resolution, frame rate and layout, including picture-in-picture sections and whether the box changes size.
2. **Estimate word timings** from your transcript.
3. **Plan the clips** in a table and wait for your OK. For each clip it chooses a full-frame cutaway, a transparent panel in empty space, or nothing, and tells you why.
4. **Build each clip**, check stills on the key words, and fix what's off.
5. **Render** with motion blur at your video's frame rate, then make the preview and the comparison pages.

It never invents numbers or results. Bars show relative size and text uses skeleton lines until you give it the real figures.

### How it works

- Every frame is a pure function of time. Springs are closed-form step responses, and a value that changes target many times is the sum of one spring per change. There are no CSS transitions or timers, so any frame can be rendered on its own.
- Clips are small HTML files on a shared engine (`skills/motion-broll/engine/motion.js`). Headless Chromium captures 4 sub-frames per frame across a 180° shutter, and ffmpeg blends them into motion blur.
- The worked example in `skills/motion-broll/examples/opus-aoe2/` is the six clips from the demo above.

## object-separation

**Separate anything from the background in a video, on your own computer.** Point it at a video and tell it what to separate (you, a product, a hand). It uses SAM 2.1 (Segment Anything, from Meta), which is free and runs locally, so nothing gets uploaded.

The whole skill is one file, `skills/object-separation/SKILL.md`. Run it in Claude Code, which works directly on your computer and can use your graphics chip.

**What it does**

1. **Scans your computer** and picks the right model size, then downloads it:

   | Your machine | Model | Download |
   |---|---|---|
   | NVIDIA GPU with 12 GB+ | large | 898 MB |
   | Smaller NVIDIA GPU, or Apple Silicon | base-plus | 323 MB |
   | No GPU (CPU only) | tiny | 156 MB |

2. **Picks the subject** with a couple of click points on the first frame.
3. **Separates it** in every frame, trying a short test range first and then the full clip.
4. **Gives you back your video with the subject highlighted in green**, with the original audio, so you can see exactly what it picked up. It also saves a mask for every frame.

Once you have the masks, your video is effectively two layers, so you can ask Claude for whatever you want to do with the subject next without running the separation again.

**Install:** `npx skills add Barty-Bart/motion-graphics` and pick `object-separation`, or copy `skills/object-separation` into `.claude/skills/`.

**Use it:** in Claude Code, ask something like *"use object-separation to separate me from the background in clip.mp4"*.

**Requirements:** any 64-bit Windows, Mac or Linux computer with 8 GB RAM, Python 3.10+ and ffmpeg. No GPU needed: on a plain CPU it works but is slow (about 5 seconds per frame). Apple Silicon or an NVIDIA GPU makes it much faster. Everything installs into one `.object-separation` folder in your project, and the skill tells you how to delete it and the model when you're done.

## Want the full process?

These skills are a starting point. My complete AI video editing process, with the full set of skills, is in **[Bart's AI Workshop](https://www.skool.com/barts-ai-workshop-4507/about)**.

## Licence

MIT. Geist fonts: SIL Open Font License. Icon paths adapted from Lucide (ISC).
