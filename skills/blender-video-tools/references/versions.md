# Version-aware VSE work

Use the installed executable as the source of truth. Version labels route investigation; runtime feature checks decide which API calls are valid. The helper is smoke-tested on the exact versions recorded in `tested-versions.json`; do not represent other branches as tested.

| Branch | Guidance | Evidence |
| --- | --- | --- |
| 4.0–4.3 | [Legacy collection and UI adaptation](blender-4x.md) | Documentation/runtime discovery only |
| 4.4 | [Strip names, text anchors, action slots](blender-4x.md) | Documentation only |
| 4.5 LTS | [Preview, slip editing, API continuity](blender-4x.md) | Smoke-tested 4.5.13 |
| 5.0 | [Workspace binding and explicit fonts](blender-50.md) | Smoke-tested 5.0.1 |
| 5.1 | [Timing aliases and retiming changes](blender-51.md) | Documentation only; run local test |
| 5.2 LTS | [Current construction and compositor additions](blender-52.md) | Smoke-tested 5.2.1 |
| 3.x or other older versions | Inspect official versioned APIs and adapt a separate project | No support claim |
| Newer/unknown versions | Capability probe, matching release notes, then a representative render | No support claim |

Read only the relevant branch note. Shared creative skills are version-independent; all Blender execution routes through this table. No extra version needs installing just to use these instructions.

The compatibility helper checks `new_effect` RNA parameters directly, selects `strips` or `sequences`, and sets workspace bindings only when exposed. It does not abstract all of Blender or make old/new `.blend` files interchangeable.

## Font behavior observed during testing

On the tested macOS 5.0.1 build, a synthetic background render using the implicit default text font produced a blank title even though its text and opacity were correct. Explicitly loading and packing a TTF resolved it. Use an explicit font for reproducible text rendering and inspect the pixels; this observation is not a claim that every 5.0 installation has the same behavior. The smoke test requires `--font` and checks for visible text after save/reopen.

## Diagnosing the empty editor

A 5.x file can render all its strips while the UI shows an empty grid and a **New** scene selector. Check `context.workspace.sequencer_scene` before blaming zoom or missing media. The installed `scripts/startup/bl_ui/space_sequencer.py` header uses this workspace property. In the GUI select the existing scene in the Sequencer header; do not create another empty scene.

## Installation/version switching

When installation is requested, obtain the platform/architecture-specific build from Blender's official download archive, verify the published checksum, and install under an explicit versioned path. Preserve other versions by default. Test that exact binary with `--background` and record its reported version. Do not remove Gatekeeper protections to resolve an uninvestigated error. For a project created with a newer release, rebuild into a separate output with the requested version; keep the original intact.

Official references (consult the appropriate page; installed API probes supplement docs):
- https://developer.blender.org/docs/release_notes/5.0/sequencer/ — workspace-specific Sequencer Scene introduction.
- https://developer.blender.org/docs/release_notes/5.1/sequencer/ — timing and API changes.
- https://developer.blender.org/docs/release_notes/5.2/sequencer/ — compositor, text and API additions.
- https://download.blender.org/release/ — official archived builds and checksums.
