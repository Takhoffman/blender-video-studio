---
name: blender-video-video-review-delivery
description: "Inspect rendered videos and editable Blender projects for visual, editorial, audio, packaging, and playback problems before delivery. Use for final QA, export checks, or project handoff."
---
# Video Review & Delivery

Review against the user’s actual brief and intended viewing size. Separate source inspection, rendered-frame inspection, playback review and audio listening in the evidence record; each proves something different.

Inspect distributed frames plus boundaries around cuts, overlays, fades, retiming and the ending. Look for cropped subjects, HUD fragments, black gaps, unexpected freeze frames, unstable picture edges, unreadable captions and inconsistent colors. Contact sheets help coverage but do not replace playback. Review the full short video with synchronized sound when available; for long work review the complete export as feasible and state any sampling limitation.

Compare captions and quotes to the source. Check that edits preserve meaning and that instructional actions are reproducible. Verify the hook and ending for the chosen video type; do not enforce promotional pacing on a lesson. Fix observed problems, render the changed portions or full video as appropriate, and inspect the revised result.

Probe the actual final file with ffprobe for streams, codec, dimensions, frame rate, duration and audio layout. Decode both streams to catch corruption; check timing alignment where required. For H.264/yuv420p ensure even dimensions, including previews. Measure encoded audio rather than quoting a normalization setting. Use a fresh final file for checks after remuxes or revisions.

Open or reopen the editable project with the exact documented Blender binary. Check strips, source references, packed/unpacked fonts and audio, and 5.x workspace scene links. Verify preview plus layers in the actual window when GUI handoff is requested. Do not infer UI success from a shell exit code. Preserve unsaved work and avoid acting on a stale window.

Deliver the requested final MP4, editable .blend, build scripts and essential dependencies. Use relative asset paths where practical and name missing/unpacked sources. Record exact tested Blender version, rebuild command, decisions and material limitations. Do not promise old-version compatibility merely because a newer file saves successfully.

For Blender execution and UI setup use [Blender Video](../blender-video-tools/SKILL.md). For color discrepancies use [Color & Finishing](../blender-video-color-finishing/SKILL.md). For mixing problems use [Audio & Sound Design](../blender-video-audio-sound-design/SKILL.md). Never expand review into publishing or destructive cleanup without authorization.
