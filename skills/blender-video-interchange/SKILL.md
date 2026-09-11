---
name: blender-video-interchange
description: Transfer cuts-only video and audio timelines between Blender and OTIO-capable editors such as DaVinci Resolve. Use for editable timeline handoffs or imports; includes strict export/import scripts, compatibility reports, and verification guidance, not lossless full-project conversion.
---
# Timeline Interchange

Use OpenTimelineIO for edit decisions and preserve the originating project separately. Read [commands and limitations](references/workflow.md) before running the scripts. Detect the installed applications and versions; a valid OTIO file does not prove that Resolve interpreted it correctly.

## Choose what remains editable

The shipped scripts transfer flat tracks of local video/audio files, source trims, hard cuts, gaps, and timeline frame rate. They reject known unsupported elements rather than drop them. They do not implement automatic effect translation or baking. Scene color management and application-specific metadata are not transferred; an OTIO exporter may omit effects without indicating that they existed. Always compare with a reference render.

For unsupported titles, 3D, transitions, grades, or retiming, prepare an exchange duplicate and render the affected composition to media using [Blender Video Tools](../blender-video-tools/SKILL.md), or the source editor's render tools. Keep the original editable project. A render of the whole movie is visually faithful but loses internal editability; use per-shot renders when continued trimming matters. Include handles only when actual source frames exist, and record their offsets. Do not delete effects from the original to make export pass.

## Exchange and check

1. Inspect the source timeline and create a reference render. Establish timeline rate, start timecode, output dimensions, and local media paths. Normalize mixed-rate/VFR footage before the cuts-only bridge; preserve source files.
2. Export a plan from Blender and encode it to OTIO, or decode another editor's OTIO and import into a new Blender scene/file. Read the generated reports. Import validates file presence and source ranges before creating a scene.
3. In Resolve, use timeline import/export for OTIO when the installed edition exposes it. The manual file workflow does not require external Python scripting access. Do not assume Free and Studio have identical scripting access or codec support.
4. Inspect the receiving timeline at every cut and gap, verify source frames and video layer order, and listen for audio alignment. Compare against the reference; preserve the evidence and actual app versions. For a round trip, export back from the receiving editor and compare again.

Report separately: OTIO library validation, Blender import/reopen/render checks, and actual Resolve round-trip verification. Do not mark the latter complete without Resolve. Use [Review & Delivery](../blender-video-review-delivery/SKILL.md) for media dependencies and final handoff. Keep large installers, proxies, cache, and test media on the user's chosen volume; check the installer's supported destination before attempting a low-space installation.
