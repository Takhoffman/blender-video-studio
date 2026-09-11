---
name: blender-vse-asset-sourcing
description: Find and prepare footage, fonts, music, sound effects, graphics, and 3D assets for Blender video projects. Use when a production needs external assets, stock APIs, or generated media; covers selection, Blender compatibility, provenance, and portable project dependencies.
---
# Asset Sourcing

Inspect the existing project and brief first. Identify the missing role—an establishing shot, readable caption font, ambience, or a particular object—before searching. Reuse supplied brand assets. Choose a small coherent set, and skip asset categories that do not improve the edit.

## Find candidates

Use [provider references](references/providers.md) only for the asset category needed. Prefer official APIs for programmatic search when available; otherwise use supported downloads. Verify current documentation, authentication, terms, and formats at use time. This skill provides sourcing guidance, not installed service connectors.

Separate searching existing footage from generating new footage. For generation, use available tools and record the actual provider/model, prompt, and cost when reported. Respect the user's spending authorization; sourcing does not authorize subscriptions or purchases. Use authorized credentials without putting secrets in scripts, URLs saved to provenance, or logs. On authentication or quota failure, report the dependency or choose an available alternative; do not repeatedly retry.

Shortlist candidates against their intended shot: subject, action, available duration, crop room, lighting, and continuity. A relevant thumbnail is insufficient. Download a preview when useful, inspect the moving content, and acquire the selected usable resolution. Never deliver watermarked previews as final assets.

## Prepare for the installed Blender

Use [Blender Video](../blender-vse-video/SKILL.md) to detect the exact runtime and available importers. Support in one Blender version does not prove support in another; test a representative import/render before preparing a large asset set.

| Asset | Acceptance check |
| --- | --- |
| Footage | Probe actual streams, dimensions, duration, frame rate, and color metadata. Inspect useful action and crop at delivery aspect ratio. Preserve originals; make transcodes/proxies separately when needed. |
| Fonts | Acquire desktop TTF/OTF files rather than web CSS or assuming WOFF works. Prefer static weights when variable-font behavior is unverified. Render the actual captions, punctuation, and required language glyphs in Blender; inspect missing glyphs, wrapping, and small-screen readability. |
| Music and effects | Audition for tone, pacing, transitions, and a usable ending before fitting the whole edit. Waveforms and loudness meters do not establish musical fit. Route mixing to [Audio & Sound Design](../blender-vse-audio-sound-design/SKILL.md); disclose if listening is unavailable. |
| Graphics and overlays | Check alpha interpretation, resolution, color, and edge quality over the intended background. Preserve editable text/shapes when practical. Templates for other editors may require rebuilding; do not claim native Blender editability. |
| Models, textures, HDRIs | Check importer availability, texture dependencies, scale, orientation, material behavior, and render cost in the actual scene. Keep downloaded executable scripts disabled unless separately inspected and needed. |
| LUTs | Establish expected input/output color spaces before applying. Route to [Color & Finishing](../blender-vse-color-finishing/SKILL.md); avoid duplicate transforms and blind preset application. |

Check downloaded file contents, not just extensions or HTTP success: reject HTML error pages and incomplete files. Name local assets consistently and retain a stable relative project layout. Do not overwrite originals while normalizing media.

## Retain provenance and hand off

Keep a compact asset record alongside the edit plan: local path, intended role, provider and asset ID/title, creator when provided, canonical source URL, retrieval date, license URL or saved terms, required attribution, and modifications or generation details. Exclude signed download credentials. Derive any raw-footage statistics from the original files, not guesses or proxy lengths.

Check the selected asset's terms for both inclusion in the rendered video and redistribution of the raw file. Include allowed dependencies and attribution with the editable project; for restricted dependencies provide acquisition/relink instructions. Do not bundle third-party libraries into the plugin by default.

Hand selected assets and unresolved dependencies back to [Production Workflow](../blender-vse-production-workflow/SKILL.md). Verify their actual appearance or sound in a preview, then use [Video Review & Delivery](../blender-vse-video-review-delivery/SKILL.md) to check the reopened project. A successful download is not completion.
