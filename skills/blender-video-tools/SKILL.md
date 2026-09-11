---
name: blender-video-tools
description: Create, edit, render, and troubleshoot videos with Blender Python, the Video Sequence Editor, compositing, animation, tracking, and FFmpeg. Use for programmable Blender media production and editable timeline delivery, including version compatibility and missing-strip UI problems.
---
# Blender Video Studio

Treat Blender as a programmable media-production environment. The rendered media is the output; the `.blend`, scripts, and source dependencies are editable deliverables. This technical skill does not impose social pacing, a visual style, duration, or aspect ratio.

## Choose the right tool

Prefer `bpy` and background Blender for repeatable project construction. Use the VSE for sequencing, trims, overlays, text, transforms, speed changes, transitions, sound, and final assembly. Use scene animation for cameras, lights, geometry, 2D/3D titles and procedural motion; compositor nodes for masks, color, alpha, blur and layered effects; tracking for stabilization or motion-attached inserts. Use FFmpeg/ffprobe for metadata, proxies, transcodes, frame extraction, remuxing, mechanical trims and audio measurement. Do not force a simple conversion through Blender. Use targeted GUI interaction when the outcome is an editor view or playback review.

## Detect before building

- Resolve the exact executable and read `bpy.app.version_string`; record it in the output notes. Respect a requested version and do not silently select another installed Blender.
- Read [references/versions.md](references/versions.md) and its matching branch note for the detected version. Run `scripts/probe_version.py` inside that Blender for a read-only JSON capability report. Feature-detect RNA parameters rather than assuming that examples for another release apply. For unknown versions inspect local RNA and official versioned documentation.
- Run `blender --background --factory-startup --python-exit-code 1 --python scripts/smoke_test.py -- --out /absolute/temp/path --font /absolute/font.ttf` when validating a newly installed version or changed compatibility code. The helper creates only a synthetic project in its explicit output directory. Require a fresh report.json with the expected version and successful checks; process success alone is insufficient.
- Probe supplied media for dimensions, fps/timebase, duration, rotation, colorspace, and audio streams. Inspect distributed frames and important actions; a filename is not content inspection. Inspect variable-frame-rate timestamps when synchronization matters.

For end-to-end coordination use [Production Workflow](../blender-video-production-workflow/SKILL.md). For exposure correction, shot matching, grading, and mixed footage/3D color pipelines use [Color & Finishing](../blender-video-color-finishing/SKILL.md).

## Build and review

For a produced edit, follow source inspection → edit plan → scripted timeline → preview render → visual inspection → revision → final render. Scale the plan to the brief. Preserve source files. Make deterministic source offsets and timeline ranges explicit; keep text, gameplay, graphics and audio on separately named channels. Use the compatibility helpers in `scripts/vse_compat.py` for strips, effect construction and workspace links.

Inspect previews at delivery size for readable text, safe margins, cropped subjects, HUD fragments, black gaps, unintentional freeze frames and awkward action timing. Review playback with sound when available: contact sheets cannot prove temporal flow or audio quality. If playback/listening is unavailable, disclose that specific limit instead of claiming to have watched or heard the result. Fix observed problems and inspect the revised output. Do not call a render professional merely because it has typography and music.

For frame-sequence export use an even-sized encode, e.g. `-vf 'pad=ceil(iw/2)*2:ceil(ih/2)*2' -c:v libx264 -pix_fmt yuv420p -movflags +faststart`; half-resolution previews can have odd heights even when the final size is even. Explicitly map soundtrack and duration when muxing. Measure the encoded audio, not just the pre-encode WAV; normalization targets are not measured results. Silence in a supplied source is not a processing failure. Add or synthesize sound only when the brief supports it, and identify it accurately.

## Make the project usable in the app

Rendering successfully does not prove the editor is showing the edit. In Blender 5.0+, link each intended editing workspace with `workspace.sequencer_scene = scene`. Merely setting the window scene or changing an area to `SEQUENCE_EDITOR` is insufficient. Set `view_type='SEQUENCER_PREVIEW'`, show the channel region, and frame the strips with a valid editor/region context. In a live UI, defer region-dependent operations through a short `bpy.app.timers` callback after changing editor type. Avoid blind retries if an operator's poll fails.

When asked to show the edit, inspect the exact live Blender window and verify preview plus strips after opening. A successful OS open command is not proof. If UI state changes unexpectedly or the user is editing simultaneously, observe again; do not type into a stale target or discard unsaved work. A separate instance is useful when preserving an existing document. See [references/editor-view.md](references/editor-view.md).

Save to a new output path when modifying an existing project unless replacing it is requested. Keep source paths portable where practical and enumerate unpacked dependencies: packing does not guarantee movies are embedded. Reopening in an older version is not a safe migration strategy; rebuild a separate project from compatible scripts and inspect it.

Deliver the MP4, `.blend`, scripts and necessary dependencies, plus brief editorial decisions, exact tested Blender version, rebuild command, and material review limitations. Do not install, upgrade, or remove Blender solely because this skill is invoked.
