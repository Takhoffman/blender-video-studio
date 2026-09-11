# Blender 5.0

Runtime-tested: 5.0.1 on macOS arm64 for the narrow scope in `tested-versions.json`.

## Critical editor binding

Starting in 5.0, the Sequencer uses a workspace-specific scene instead of simply following the window scene. In a newly created editing workspace set:

```python
workspace.sequencer_scene = scene
```

A scene can contain valid strips and render successfully while an unlinked workspace shows an empty editor and a New selector. In the GUI select the existing scene, not a new blank one. When switching workspaces verify the binding there too.

Source: https://developer.blender.org/docs/release_notes/5.0/sequencer/

## Script construction

Use `strips` and runtime-inspected effect parameters; the tested 5.0.1 constructor takes `length`. Prefer property-level keyframe insertion. Older deprecated action/sequence APIs should not be assumed available. Keep source offsets and visible timeline handles distinct; the later 5.1 names are not a reason to assume they already exist here.

## Observed font issue

Our headless 5.0.1 test produced missing title pixels with the implicit font. Loading and packing an explicit TTF fixed that test. This is a local observation, not a blanket claim about every 5.0 installation. The smoke test checks rendered text, not just file existence.

Keep an explicit versioned executable path when 5.2 is installed alongside 5.0. Rebuild a separate project when moving from a newer release; do not overwrite the only newer `.blend` in an older application.
