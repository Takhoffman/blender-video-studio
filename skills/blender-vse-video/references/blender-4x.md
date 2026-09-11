# Blender 4.x

Status: 4.5.13 LTS synthetic smoke test passed on macOS arm64; earlier 4.x branches remain documentation-guided. See `tested-versions.json` for actual test evidence. Resolve the minor release before adapting a script.

## 4.0–4.3

Use runtime detection for older `sequences` collections and `Sequence` type names. Do not blindly reference the 5.x workspace scene property. Check text anchoring, effect-constructor arguments and render settings from that installation. This is a legacy adaptation path, not a certification of every 4.x feature.

## 4.4 transition

The official Python notes document the rename from Sequence-related types to Strip-related types, new `strips` collections, and text anchor names replacing `align_x`/`align_y`. Adopt modern names when present; do not confuse paragraph alignment with anchoring. Actions gained slots: prefer property `keyframe_insert` for ordinary animation. If manually assigning or editing actions, inspect the slot/channel-bag API rather than assuming a flat `action.fcurves` collection.

Source: https://developer.blender.org/docs/release_notes/4.4/python_api/

## 4.5 LTS

Carries the newer strip API. Its release notes describe preview/HDR, slip-edit and keymap changes; don't treat an old shortcut as a reliable UI action. Over Drop was removed; use Alpha Over for that legacy case. Strip insertion into a blank edit may change frame rate or view transform: set and verify intended delivery settings after importing media.

Source: https://developer.blender.org/docs/release_notes/4.5/sequencer/

## Before delivery

Run the synthetic test with the exact binary and explicit font, then build a representative real-media sample including audio and timing. Inspect both render and reopened timeline. Feature-detected code does not prove complete compatibility. Do not install or downgrade a release solely to avoid investigating a failure.
