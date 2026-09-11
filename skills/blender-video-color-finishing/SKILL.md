---
name: blender-video-color-finishing
description: Correct exposure and white balance, match shots, and grade footage or mixed footage/3D edits in Blender with a reproducible color pipeline. Use for inconsistent shots, requested looks, or color finishing before export.
---
# Color & Finishing

Separate correction (exposure, neutral balance, and continuity) from grading (the requested look). Match the edit before imposing a look. Preserve intentional lighting differences and approved brand colors; do not automatically brighten night scenes, neutralize sunsets, or apply a cinematic preset.

## Establish the pipeline

Use [Blender Video](../blender-video-tools/SKILL.md) to resolve the exact binary and version guidance. Inspect available color-management settings, strip modifiers, and node properties through that Blender's RNA before scripting. Feature availability and enum names can differ; record chosen settings rather than assuming a 4.5 or 5.x example applies. Existing version smoke tests do not certify color accuracy.

Probe source color primaries, transfer, matrix, range, and bit depth. Tags may be missing or wrong: compare decoded images and known source information before assigning a space. Do not identify log footage solely because it looks flat. If the source transform is unknown, avoid guessing a camera LUT; disclose uncertainty and use a conservative correction or request source details when necessary.

Choose the intended delivery space and record source interpretation, working space, view/output transform, and export metadata. Preserve an established pipeline unless it causes an observed problem. HDR-to-SDR requires an intentional tone map; changing tags alone does not convert pixels. A LUT needs known input and output spaces and should not duplicate another transform.

For footage mixed with rendered 3D, distinguish scene-linear render data from display-referred media. Establish the compositing transform path before rendering assets. Avoid applying a view transform twice to an already baked render. Verify a representative composite through the final encode rather than choosing a transform based only on its name.

## Correct and match

1. Select representative reference shots and compare neighboring cuts at the same display size. Include faces, neutrals, highlights, and saturated objects when present. Use waveform, histogram, or vectorscope views when available; scopes support image inspection and do not determine creative intent.
2. Adjust exposure and white balance, then contrast and saturation. Preserve useful highlight and shadow detail; do not promise recovery from clipped source pixels. Match comparable subjects and lighting, not every shot's histogram.
3. Apply the requested look after matching. Inspect skin, gradients, brand colors, and dark regions for unwanted shifts, clipping, or banding. Selective corrections require masks that hold over the shot; one good frame is insufficient.
4. Check beginnings, middles, ends, and adjacent cuts. If lighting changes within a shot, keyframe or split corrections deliberately and inspect for pumping or abrupt changes.

Keep source corrections and the creative look separately named and reversible with VSE modifiers or compositor nodes where supported. Do not unintentionally grade captions or brand graphics; decide whether they belong before or after the look. For baked intermediates, retain originals, the transformation script, and settings, and identify what cannot be edited inside Blender.

## Validate the finish

Render a representative preview through the intended output pipeline. Compare before and after at identical frames and settings, then inspect the decoded export as well as Blender's preview. Verify color tags against the actual transformation; tags alone do not prove correct appearance. Do not claim calibrated color accuracy from screenshots or an uncalibrated display.

Check frame edges after stabilization/reframing and inspect noise or sharpening artifacts at delivery size. Do not add denoising, sharpening, grain, or upscaling by default. Revise observed defects and repeat affected comparisons. Use [Video Review & Delivery](../blender-video-video-review-delivery/SKILL.md) for final codec, audio, playback, and project checks. Record correction decisions, transform settings, exact Blender version, and material inspection limitations.
