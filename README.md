# Blender Video Studio

**Turn a video brief into an editable Blender project—with a script you can run again.**

![Blender Video Studio: separate footage, keyframe, and audio layers connected to a finished ocean composite](assets/blender-video-studio-cover.png)

Blender Video Studio is a Codex plugin for producing and troubleshooting video with Blender Python, the Video Sequence Editor, and FFmpeg. Give Codex your footage and a brief; the skills guide it through source inspection, editorial choices, project construction, rendering, and review.

The goal is a finished video **and** a usable project: separate footage, titles, graphics, and sound where appropriate, plus the scripts and dependencies needed to rebuild it.

> This is a collection of agent skills and a small Python compatibility layer. It is not a Blender add-on, a hosted rendering service, or a one-click editor. Blender and FFmpeg run on your machine.

## Start with a brief

After installing the plugin, open a new Codex task and try:

```text
Use $blender-video-highlights-montages to turn the clips in my footage folder
into a 25-second highlight reel. Keep the action readable, use sparse text,
and give me an MP4, an editable .blend, and the build script.
Render a preview, inspect it, and fix visible problems before delivery.
```

Or ask for a specific job:

- “Make a product demo that shows the result before explaining the steps.”
- “Cut this interview into a short clip while preserving the speaker's meaning.”
- “Add a rendered 3D object to this shot and keep the scene editable.”
- “My Blender file renders correctly, but its timeline looks empty. Diagnose it.”

These are workflows the agent can carry out using Blender, not prebuilt video templates. Asset quality, the brief, available tools, and review all affect the result.

## Thirteen focused skills

All skills use the `blender-video-` prefix so they stay distinct from general Blender modeling or animation skills.

| Skill | What it handles |
| --- | --- |
| [`blender-video-production-workflow`](skills/blender-video-production-workflow/SKILL.md) | Coordinates stages, evidence, unfinished work, and specialist skills. |
| [`blender-video-interchange`](skills/blender-video-interchange/SKILL.md) | Cuts-only OTIO import/export scripts and editor handoff checks. |
| [`blender-video-asset-sourcing`](skills/blender-video-asset-sourcing/SKILL.md) | Finds and prepares footage, fonts, sound, graphics, and 3D assets with provenance. |
| [`blender-video-color-finishing`](skills/blender-video-color-finishing/SKILL.md) | Exposure and white balance, shot matching, grading, and output color checks. |
| [`blender-video-tools`](skills/blender-video-tools/SKILL.md) | Python/VSE construction, tool selection, version checks, rendering, and editor troubleshooting. |
| [`blender-video-social-video-edit`](skills/blender-video-social-video-edit/SKILL.md) | Chooses the right editorial workflow when the video type is still unclear. |
| [`blender-video-highlights-montages`](skills/blender-video-highlights-montages/SKILL.md) | Gameplay, travel, sports, and event highlights shaped around meaningful moments. |
| [`blender-video-product-demos`](skills/blender-video-product-demos/SKILL.md) | Product demonstrations that make a benefit and its supporting steps clear. |
| [`blender-video-talking-head-clips`](skills/blender-video-talking-head-clips/SKILL.md) | Spoken clips with contextual cuts, readable captions, and intelligible dialogue. |
| [`blender-video-explainers-tutorials`](skills/blender-video-explainers-tutorials/SKILL.md) | Explanations and tutorials with an understandable progression. |
| [`blender-video-promos-trailers`](skills/blender-video-promos-trailers/SKILL.md) | Promos and trailers built around a clear reveal or offer. |
| [`blender-video-audio-sound-design`](skills/blender-video-audio-sound-design/SKILL.md) | Dialogue, music, ambience, transitions, and measured output levels. |
| [`blender-video-review-delivery`](skills/blender-video-review-delivery/SKILL.md) | Visual review, export checks, project dependencies, and handoff. |

For complete productions, use `blender-video-production-workflow` to coordinate stages. Asset sourcing provides provider references and selection guidance, not bundled APIs or asset libraries. Color finishing provides procedural guidance, not an automatic grading engine. Use one primary editorial skill. The technical, audio, and review skills support it; loading every format at once is unnecessary.

## How production works

**Inspect → plan → build → preview → review → revise → render**

1. Inspect the actual media: frames, duration, frame rate, dimensions, and audio streams.
2. Choose source ranges and an editorial structure appropriate to the brief.
3. Build a reproducible Blender timeline. Use scene animation or compositing when it helps the shot.
4. Render a preview and inspect it for framing, text, timing, and obvious defects.
5. Revise, render the final output, and check the encoded file and project dependencies.

Blender handles the editable timeline and 2D/3D work. FFmpeg and ffprobe handle media inspection, preprocessing, encoding, and audio measurements when they are the simpler tools. Playback and listening are part of review when available; the skills require disclosing when only frames or measurements were checked.

## Blender compatibility

Version support is based on runtime feature detection and recorded tests, not a blanket promise that every Blender API behaves identically.

| Version | Evidence in this repository |
| --- | --- |
| **4.5.13 LTS** | Synthetic smoke test passed on macOS Apple Silicon. |
| **5.0.1** | Synthetic smoke test passed on macOS Apple Silicon. |
| **5.2.1 LTS** | Synthetic smoke test passed on macOS Apple Silicon. |
| 4.0–4.4 and 5.1 | Branch guidance only; not runtime-certified. |
| Other versions | Inspect the installed API and validate before relying on it. |

The tests cover saving and reopening, visible rendered text, opacity evaluated at two frames, workspace binding when available, and construction of a two-input transition. They do **not** establish full API coverage, transition pixel correctness, or complete real-media playback compatibility.

See the [version guide](skills/blender-video-tools/references/versions.md) and [exact test records](skills/blender-video-tools/references/tested-versions.json).

A practical example: Blender 5.x can contain a valid edit while a workspace displays an empty sequencer. The toolkit documents the workspace-to-scene binding that resolves that particular problem, rather than treating every empty timeline as missing footage.

## What is included—and what is not

The executable helpers include a small compatibility layer and a cuts-only OTIO bridge. The bridge uses a separate Python environment and requires receiving-editor verification; it is not a lossless project converter.

The Blender compatibility helpers are:

- [`probe_version.py`](skills/blender-video-tools/scripts/probe_version.py) reports the installed Blender version and relevant API capabilities.
- [`vse_compat.py`](skills/blender-video-tools/scripts/vse_compat.py) adapts strip collections, effect timing and inputs, and editor workspace setup.
- [`smoke_test.py`](skills/blender-video-tools/scripts/smoke_test.py) builds, saves, reopens, and renders a synthetic test project.

Automatic transcription, word alignment, a reusable motion-template library, proxy management, and resumable rendering are **not shipped implementations**. Some skills guide related work, but the agent must implement or connect the necessary tooling for the task. This repository does not include stock footage, licensed music libraries, Blender, or a rendering backend.

## Install

You need Codex with plugin support. To produce videos, install Blender and FFmpeg/ffprobe separately; this plugin does not bundle them. Python helpers that import `bpy` run inside Blender. Fonts and other project assets must also be available or packaged.

### Codex desktop app

1. Open the plugin marketplace controls and choose **Add plugin marketplace**.
2. Fill in the dialog:

   | Field | Value |
   | --- | --- |
   | Source | `Takhoffman/blender-video-studio` |
   | Git ref | `main` |
   | Sparse paths | Leave blank |

3. Click **Add marketplace**.
4. Choose the **Blender Video Studio** marketplace, open **Blender Video Studio**, and install it.
5. Start a new Codex task to pick up the skills. If the marketplace does not appear, restart the app and check the plugin directory again.

### Codex CLI

With a Codex CLI that exposes `codex plugin`:

```sh
codex plugin marketplace add Takhoffman/blender-video-studio --ref main
codex plugin add blender-video-studio@blender-video-studio
codex plugin list --marketplace blender-video-studio --json
```

The selector is `plugin-name@marketplace-name`; both names are `blender-video-studio` in this repository. The older `@local-workspace` command referred to the author's private local setup and is not needed for this public marketplace.

### Verify and try it

The CLI listing should identify `blender-video-studio` as installed. In a new task, try:

```text
Use $blender-video-tools to inspect my installed Blender version and check
whether Blender, FFmpeg, and ffprobe are available. Report what is available
before creating a video.
```

Then use a brief from [Start with a brief](#start-with-a-brief). Installing the plugin does not establish that your Blender executable or media tools are configured correctly.

### Sources and verification scope

The marketplace format and Git-source registration follow [OpenAI's plugin packaging documentation](https://developers.openai.com/plugins/build/plugins#add-a-marketplace-from-the-cli). The catalog is [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json); it points to the plugin at the repository root. Leave sparse paths blank so the skills and assets are fetched together.

The CLI syntax was checked against `codex-cli 0.150.1` (`codex plugin marketplace add --help`, `codex plugin add --help`, and `codex plugin list --help`). The desktop field labels match the Add plugin marketplace dialog; the complete desktop click-through has not been tested. Blender runtime test coverage is recorded separately in [Blender compatibility](#blender-compatibility).

## Develop locally

From the repository root, a manual smoke test looks like:

```sh
blender --background --factory-startup --python-exit-code 1 \
  --python skills/blender-video-tools/scripts/smoke_test.py -- \
  --out /absolute/path/to/a-new-test-directory \
  --font /absolute/path/to/a-font.ttf
```

Use a fresh output directory. Check the generated `report.json` and inspect `preview.png`; a successful exit code alone is not visual verification. Substitute the exact Blender executable you intend to use.

```text
.agents/plugins/marketplace.json  Public marketplace catalog
.codex-plugin/plugin.json   Plugin manifest and UI metadata
skills/                    Thirteen skills, supporting references, and helpers
assets/                    Plugin icon and README artwork
```

The source belongs in version control; generated renders, local environments, and test output do not. Git tracks the plugin's history but is not required for Codex to load a local plugin.

---

Cover artwork generated with ChatGPT image generation. It is a product illustration, not a screenshot of Blender or a rendered example produced by this plugin. Blender is a separate application; this project is not an official Blender Foundation product.
