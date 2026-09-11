# Commands and current scope

Run `blender_bridge.py` inside Blender. Run `otio_bridge.py` in an isolated ordinary Python environment with `opentimelineio==0.18.1`. Python 3.11 with the official macOS arm64 wheel was tested; a local Python 3.14 source build failed at OTIO manifest loading. Do not install dependencies into Blender's Python to fix that mismatch.

Set `bridge` to this skill's absolute `scripts` directory. Use fresh output paths; existing plans, OTIO files, and `.blend` outputs are not overwritten. `ffprobe` must be on PATH, or pass its absolute path with `--ffprobe` to the Blender script.

```sh
# Blender -> OTIO
blender --background source.blend --python-exit-code 1 \
  --python "$bridge/blender_bridge.py" -- export edit-plan.json
python "$bridge/otio_bridge.py" encode edit-plan.json edit.otio

# Resolve/other editor -> Blender: first export the timeline as OTIO in that editor
python "$bridge/otio_bridge.py" decode received.otio received-plan.json --fps 24
blender --background --factory-startup --python-exit-code 1 \
  --python "$bridge/blender_bridge.py" -- import received-plan.json --output received.blend
```

Use the actual timeline rate, such as `23.976023976`, not a guessed integer. Omit `--fps` when the OTIO global start time carries the correct rate. The receiving Blender scene begins at frame 1; original start timecode is recorded as a scene custom property. Relative media URLs resolve against the OTIO file's folder. Exported URLs are absolute `file:` URLs; relink when moving machines.

## Boundaries

- Only single local movie/audio files on flat Video/Audio tracks. No image sequences, remote URLs, compound clips, nested tracks, or transitions.
- Video must be constant-rate media matching the timeline rate. Metadata rate checks are a preflight, not a complete VFR detector; normalize known VFR inputs first.
- Frame-aligned timing only; subframe audio edits are rejected.
- Known strip transformations, cropping, gain/pan, modifiers, retiming, mute states, markers, and scene animation block export. OTIO effects/markers and trimmed parent tracks block import.
- Application-specific metadata (including grades, sizing, and Fusion information) is not interpreted. It may also be absent from the source application's OTIO export. The bridge transfers edit decisions, not the final look or mix.
- Audio and video are separate tracks; clip linking and exact original Blender channel numbers are not retained. Relative video stacking and clip placement are retained.
- Resolution uses our metadata when present, otherwise defaults to 1920x1080. Adjust it to the source brief before rendering.
- Reports are adjacent JSON files. A `converted` status means a file was converted, not that it passed review in Resolve.

## Reproducible checks

`python "$bridge/test_otio_bridge.py"` checks gaps, source offsets, fractional rates, timecode origins, missing media, overlapping clips, unsupported effects, and subframe rejection.

For Blender integration, create a fresh test directory with a 4-second, 24fps, 320x180 movie named `picture.mp4` and a 4-second WAV named `sound.wav` (FFmpeg lavfi test sources are suitable). Run:

```sh
blender -b --factory-startup --python-exit-code 1 \
  --python "$bridge/build_test_fixture.py" -- /absolute/test-directory
```

This creates a three-video-strip/one-audio-strip project with source trims, layer overlap, and gaps, renders six reference frames, and asserts that a title is rejected. Encode `original.json`, decode the resulting OTIO, import it into a new `.blend`, then compare strip ranges and rendered frames at 7, 19, 30, 42, 43, and 72. Full Resolve verification additionally requires importing and exporting the OTIO in Resolve itself.

## Sources

- [OTIO specification](https://opentimelineio.readthedocs.io/en/latest/tutorials/otio-file-format-specification.html): use the library rather than a hand-written OTIO parser.
- [Blender Studio interchange experiment](https://studio.blender.org/blog/opentimelineio-in-blender/).
- [Resolve 18.5 feature guide](https://documents.blackmagicdesign.com/ca/SupportNotes/DaVinci_Resolve_18.5_New_Features_Guide.pdf?_v=1681801210000): OTIO timeline exchange. Verify menus and codecs against the installed release.

See [exact test evidence](tested-versions.json) for tested versions and unresolved checks.
