# Showing an editable project

1. Verify the file/window title. A second OS open request can leave the user in an older or unsaved window.
2. Confirm that the expected scene's sequence editor has strips.
3. On Blender 5.0+, set the intended workspace's `sequencer_scene` to that scene. A **New** selector and blank editor can mean this link is unset even though rendering works.
4. Use `SEQUENCE_EDITOR` and `SEQUENCER_PREVIEW`; enable channel names. The ordinary animation Timeline with yellow diamonds is not the strip timeline.
5. Frame strips with `bpy.ops.sequencer.view_all()` in a valid `WINDOW` region of that editor. A background context may not yet expose the correct region after changing editor types. Save/reopen or defer in the live UI; check poll instead of assuming success.
6. Check the preview and strips in a fresh targeted window observation. Then explain layers using the actual strip names. To edit a selected text strip, show its strip properties/sidebar rather than general scene settings.

If a helper opens or changes a workspace, preserve unsaved user content. Do not send keys after the user switches windows without a new observation. Correct the smallest faulty setting; repeated app opens or blind keyboard shortcuts are not verification.
