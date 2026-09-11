---
name: blender-vt-audio-sound-design
description: "Edit and mix video audio: dialogue cleanup, music ducking, game or location sound, synchronized effects, transitions, and final loudness verification."
---
# Audio & Sound Design

Inspect available audio streams and listen when a playback tool is available. Determine which source sounds carry meaning before muting or replacing them. Record sample rates, channel layouts and timing offsets. Silence in the source is a fact to plan around, not a defect to conceal.

For speech, first establish intelligibility with appropriate clip gain and gentle cleanup. Avoid unnecessary compression, aggressive gates or denoising that damages speech. Use short fades/room tone around edits, then add music and effects beneath the important signal. Duck music with deliberate envelopes around speech; do not merely set every asset to the same peak.

Use effects to reinforce real actions and scene changes. Align perceptual transients, not just file starts. Preserve useful game or location sound. Choose music with an arc and ending that fit the edit. Avoid smothering every cut with a whoosh or representing a repetitive generated loop as a fully arranged score.

Check mono compatibility when relevant and avoid silently summing multichannel material. Retiming can alter pitch or synchronization; inspect the actual encoded result. Use FFmpeg for extraction, resampling, loudness analysis and normalization, and VSE strips/envelopes for editable placement.

Set levels for the brief and delivery. Around −14 LUFS integrated can be a social starting point, not a universal specification. Measure integrated loudness, range and true peak after final encoding. AAC can overshoot pre-encode peaks; leave appropriate headroom. A loudnorm target is not proof of achieved loudness. If a target is missed, adjust and remeasure.

Disclose whether audio was actually auditioned. Waveform and meter checks cannot prove pleasant sound. Do not claim listening from a screenshot. For silent footage, add sourced or original generated audio only when the requested scope supports it; identify synthesized music accurately.

Handoff: final mix, editable sound strips/envelopes, source/created-audio notes, and measured final levels. Supply stems only when requested or useful to the next editor.
