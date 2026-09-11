# Blender 5.2

Runtime-tested: 5.2.1 LTS on macOS arm64 for the scope recorded in `tested-versions.json`. Retains 5.0's workspace scene binding and 5.1's newer timing names.

The tested `new_effect` takes `length`; use the helper's RNA detection. Explicitly set and pack fonts, render settings and timing. After changing an editor area type, allow UI initialization before operating on its regions. Verify the actual open window, not merely the save/render exit status.

## Optional capabilities

The 5.2 notes document compositor effects within the VSE, GPU-capable compositor modifiers/effects, text style presets, and optional stream selection for movie/sound creation. These can help a requested composite or multi-stream import, but are not reasons to add effects to a simple edit. Inspect exact node/strip properties locally before building with them.

Compatibility changes include semitransparent sequencer color transforms and removal of movie timecode files. Inspect alpha edges after migration and do not expect an old proxy/timecode-building routine to work unchanged.

Source: https://developer.blender.org/docs/release_notes/5.2/sequencer/

When targeting 5.0 or 5.1, avoid unconditionally using 5.2-only features. Rebuild in that release, render a sample, and preserve the newer project as a separate file.
