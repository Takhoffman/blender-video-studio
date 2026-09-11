# Blender 5.1

Status: documented branch; not yet runtime-tested by this plugin. Run the bundled smoke test with the actual 5.1 executable before claiming compatibility. Keep the 5.0 workspace scene link.

## Timing names

5.1 introduces clearer strip timing names while retaining deprecated aliases. Prefer new names when present and inspect RNA when adapting older scripts:

| Older name | New name |
| --- | --- |
| frame_final_duration | duration |
| frame_final_start | left_handle |
| frame_final_end | right_handle |
| frame_offset_start | left_handle_offset |
| frame_offset_end | right_handle_offset |
| frame_duration | content_duration |
| frame_start | content_start |
| animation_offset_start | content_trim_start |
| animation_offset_end | content_trim_end |

`content_end` is read-only. Content placement and visible handles are different: trimming a handle does not mean moving the entire source. The release notes schedule old names for removal in 6.0; do not code future support around their indefinite existence.

## Retiming

Negative Multiply speed is supported for reversal in 5.1, and the `keep_retiming` operator option was removed. Inspect the relevant operator parameters rather than passing a remembered keyword. Validate a short retimed sample, its duration and audio alignment. Ripple-cut UI behavior can move downstream material; verify resulting ranges instead of assuming an isolated trim.

Source: https://developer.blender.org/docs/release_notes/5.1/sequencer/

Use capability checks for effect creation, collection names and text. Documentation coverage is not a successful test run, and a patch version can contain behavior fixes.
