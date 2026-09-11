# Provider starting points

These are discovery routes, not bundled integrations or guarantees of current availability. Read the relevant official documentation and selected asset's terms before use. Avoid hardcoding changing endpoints, model lists, prices, or rate limits.

| Need | Starting point | Routing notes |
| --- | --- | --- |
| Stock footage and photos | [Pexels API](https://www.pexels.com/api/documentation/), [Pixabay API](https://pixabay.com/api/docs/) | Search existing media, inspect candidates, then download a suitable variant. Follow provider attribution and API requirements. |
| Fonts | [Google Fonts Developer API](https://developers.google.com/fonts/docs/developer_api), [font repository](https://github.com/google/fonts) | The API requires a key and supplies family metadata and file references. The repository offers direct font files; retain the selected family's license. Choose desktop font files and test in Blender. |
| Models, materials, lighting | [Poly Haven](https://polyhaven.com/), [asset license](https://polyhaven.com/license) | Assets are CC0; distinguish asset terms from website/API terms. Select the needed format, textures, and resolution, then test materials in the target render engine. |
| Music, effects, stock, templates | [Motion Array](https://motionarray.com/browse/), [software compatibility](https://help.motionarray.com/hc/en-us/articles/9240968772637-Do-These-Assets-Work-With-My-Software) | Inspect available downloads and account entitlements. Do not assume a public API or that editor-specific templates import into Blender. |
| Generated video or audio | [OpenRouter video generation](https://openrouter.ai/docs/guides/overview/multimodal/video-generation), [audio](https://openrouter.ai/docs/guides/overview/multimodal/audio) | Discover current models and supported outputs. Stock search, speech generation, and music generation are different capabilities. Confirm the chosen model supports the requested one and inspect the returned file format. |

Use the user's preferred provider when specified. If it lacks the necessary access or formats, explain the concrete limitation and use an authorized alternative. Do not acquire more services simply to fill every category in this table.
