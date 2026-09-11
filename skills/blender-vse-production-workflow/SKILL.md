---
name: blender-vse-production-workflow
description: Coordinate complete Blender video productions from source inspection through editing, graphics, color, sound, review, and delivery. Use for end-to-end requests or resuming unfinished productions; use a specialist directly for a single correction or conversion.
---
# Production Workflow

Consider every production stage, but apply only those serving the brief. A video does not automatically need narration, captions, music, 3D, or a creative grade. Preserve the user's format, style, assets, and scope. For a targeted revision, revisit affected stages rather than restarting production.

## Establish the work

Inspect existing project notes and outputs before rebuilding. Resolve deliverables, destination, duration, aspect ratio, and reference look from the brief and assets. Ask only for missing choices that materially affect the work. Use [Blender Video](../blender-vse-video/SKILL.md) for installed-version detection, source inspection, scripted construction, and editor setup.

Keep a compact production record alongside the build script or existing edit plan. Record each relevant stage as `pending`, `done`, `skipped` with a reason, or `blocked` with the missing dependency. Link evidence such as source ranges, previews, measurements, and inspection notes. Small jobs need only a few lines of notes; do not build a tracking system. Unchecked work is not done.

## Route the stages

| Stage | Decision and evidence |
| --- | --- |
| Inspect and prepare | Inspect actual source frames and sound, metadata, and asset availability. Use [Asset Sourcing](../blender-vse-asset-sourcing/SKILL.md) for missing footage, fonts, sound, graphics, or 3D assets and their usage terms. Create proxies or transcodes when needed and preserve originals. |
| Plan and edit | Choose one primary format through [Social Video Edit](../blender-vse-social-video-edit/SKILL.md) when unclear. Record source ranges and their purpose, then construct the editable timeline. |
| Graphics and 3D | Add elements serving the brief. Keep text and graphics editable and verify composition, timing, and readability in context. Use the technical skill for scenes, compositor, and tracking. |
| Color and finishing | Use [Color & Finishing](../blender-vse-color-finishing/SKILL.md) for shot matching and output color checks. Already consistent footage may need no additional grade. |
| Sound | Use [Audio & Sound Design](../blender-vse-audio-sound-design/SKILL.md) for dialogue, music, effects, and mixing. Record listening separately from measurements. |
| Review and delivery | Use [Video Review & Delivery](../blender-vse-video-review-delivery/SKILL.md) for final media checks, project reopening, dependencies, and handoff. |

Stages can overlap. Establish the color pipeline before expensive 3D rendering; settle major cuts before detailed shot matching and caption timing. Preview a representative difficult shot early to catch unsupported features or compositing problems.

## Close the loop

Follow inspection → plan → scripted timeline → preview → inspection → revision → final render. After revisions inspect changed shots and neighboring cuts. Timing changes invalidate affected captions, voice cues, effects, and transitions; a remux invalidates previous final-file audio checks. Reuse verified unchanged work.

Distinguish rendered-frame inspection, synchronized playback, audio listening, export measurements, and project reopening in the record. If a review mode is unavailable, finish other authorized work and disclose the remaining limitation. Rendering successfully or reaching a loudness target does not prove the edit works.

Deliver the requested media and editable artifacts with rebuild instructions, decisions, and unresolved limitations. Do not describe skipped or blocked checks as completed or expand delivery into publishing or asset purchases without authorization.
