# motion-graphics

Free video-editing skills for Claude Code. Each skill does one job.

<p>
  <img src="docs/demo-panel.gif" width="49%" alt="A transparent panel animating beside a picture-in-picture shot of the speaker">
  <img src="docs/demo-cutaway.gif" width="49%" alt="A full-frame cutaway: build notes turning into a master prompt that is dragged into a session">
</p>

<!-- SKOOL LINK HERE -->
> **Want my entire AI video editing process?** I teach it step by step, with the full set of skills, in my community: **[Bart's AI Workshop](https://www.skool.com/barts-ai-workshop-4507/about)**

## Install

```
npx skills add Barty-Bart/motion-graphics
```

Pick the skills you want. It works in Claude Code and other agents that read skills. Or copy a skill's folder from `skills/` into `.claude/skills/`.

## Skills

### motion-broll

<p align="center"><img src="docs/demo-cutaway.gif" width="80%" alt="A full-frame cutaway: build notes turning into a master prompt that is dragged into a session"></p>

Give it a video and a transcript and it makes motion-graphic B-roll timed to your words.

**[Full guide →](skills/motion-broll/README.md)**

### object-separation

<p align="center"><img src="docs/object-separation.gif" width="80%" alt="Before and after: talking-head footage, then the same footage with the speaker separated from the background"></p>

Separates a person, product or hand from the background in a video, on your own computer, and shows you exactly what it picked up.

**[Full guide →](skills/object-separation/README.md)**

### explainer-high-energy

<p align="center"><img src="docs/explainer-high-energy.gif" width="80%" alt="explainer-high-energy before and after: the brief, then a beat-locked hype promo"></p>

A 12–20 s hype promo for any product: beat-locked kinetic type, shapes that carry across every transition.

**[Full guide →](skills/explainer-high-energy/README.md)**

### explainer-default

<p align="center"><img src="docs/explainer-default.gif" width="80%" alt="explainer-default before and after: the brief, then a clean product demo"></p>

A clean 45–90 s product demo: your product's UI rebuilt and filmed up close while it's used.

**[Full guide →](skills/explainer-default/README.md)**

### explainer-engaging

<p align="center"><img src="docs/explainer-engaging.gif" width="80%" alt="explainer-engaging before and after: the brief, then a one-take story through the product"></p>

A 10–30 s one-take story: one element travels through your product's workflow while the camera follows it.

**[Full guide →](skills/explainer-engaging/README.md)**

### sound-effects

<p align="center"><img src="docs/sound-effects.gif" width="80%" alt="Before and after: a silent explainer clip, then the same clip after the sound pass with its audio level meter moving"></p>

Adds real sound effects and music to your motion graphics, timed to the beat and measured, so it doesn't sound like cheap beeps.

**[Full guide →](skills/sound-effects/README.md)**

More skills will be added to this repo.

## Licence

MIT. Geist fonts: SIL Open Font License. Icon paths adapted from Lucide (ISC). Sound effects in `skills/sound-effects/sfx/`: CC0 1.0 (see that skill's [`LICENSES.md`](skills/sound-effects/LICENSES.md)). Sound-pass method by Vox ([@Voxyz_ai](https://x.com/Voxyz_ai/status/2109358372873183564)); full credits are in each skill's README.
