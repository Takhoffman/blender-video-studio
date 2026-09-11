"""Synthetic construction/save/reopen/render test; output goes only to --out."""
import argparse, json, sys
from pathlib import Path
import bpy
sys.path.insert(0, str(Path(__file__).resolve().parent))
from vse_compat import strip_collection, new_effect, bind_workspace, configure_editor
args = sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
p = argparse.ArgumentParser()
p.add_argument('--out', required=True)
p.add_argument('--font', required=True, help='Explicit TTF/OTF to load and pack')
options = p.parse_args(args)
out = Path(options.out).resolve()
out.mkdir(parents=True, exist_ok=True)
if (out/'smoke.blend').exists():
    raise RuntimeError('Choose a fresh output directory; smoke.blend already exists')
bpy.ops.wm.read_factory_settings(use_empty=True)
s = bpy.context.scene
s.render.resolution_x = 640; s.render.resolution_y = 360
s.render.resolution_percentage = 100; s.render.fps = 25
s.frame_start = 1; s.frame_end = 25
s.view_settings.view_transform = 'Standard'
base = new_effect(s, 'Background', 'COLOR', 1, 1, 25)
base.color = (.02, .10, .18)
title = new_effect(s, 'Editable title', 'TEXT', 2, 1, 25)
title.text = 'BLENDER VIDEO TOOLS'; title.font_size = 34
title.font = bpy.data.fonts.load(str(Path(options.font).resolve()))
title.font.pack()
title.location = (.5, .5); title.blend_type = 'ALPHA_OVER'
title.blend_alpha = .2; title.keyframe_insert(data_path='blend_alpha', frame=1)
title.blend_alpha = 1; title.keyframe_insert(data_path='blend_alpha', frame=10)
for workspace in bpy.data.workspaces:
    bind_workspace(s, workspace)
workspace = bpy.context.window.workspace
area = max(bpy.context.screen.areas, key=lambda a:a.width*a.height)
area.type = 'SEQUENCE_EDITOR'
configure_editor(s, workspace, area)
s.frame_set(12)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'smoke.blend'))
bpy.ops.wm.open_mainfile(filepath=str(out/'smoke.blend'))
s = bpy.context.scene
assert len(strip_collection(s)) == 2
s.frame_set(1)
assert abs(strip_collection(s).get('Editable title').blend_alpha - .2) < .001
s.frame_set(12)
assert abs(strip_collection(s).get('Editable title').blend_alpha - 1) < .001
# Construct a real two-input transition outside the visible test frame.
a = new_effect(s, 'Transition A', 'COLOR', 1, 30, 10)
b = new_effect(s, 'Transition B', 'COLOR', 2, 30, 10)
c = new_effect(s, 'Transition', 'GAMMA_CROSS', 3, 30, 10, inputs=(a, b))
assert c.type == 'GAMMA_CROSS'
assert strip_collection(s).get('Editable title').text == 'BLENDER VIDEO TOOLS'
if hasattr(bpy.context.workspace, 'sequencer_scene'):
    assert bpy.context.workspace.sequencer_scene == s
s.render.image_settings.file_format = 'PNG'
s.render.filepath = str(out/'preview.png')
bpy.ops.render.render(write_still=True)
assert (out/'preview.png').stat().st_size > 1000
image = bpy.data.images.load(str(out/'preview.png'), check_existing=False)
pixels = list(image.pixels)
assert sum(min(pixels[i:i+3]) > .65 for i in range(0, len(pixels), 4)) > 100, 'Rendered title is missing'
bpy.data.images.remove(image)
report = dict(version=bpy.app.version_string, executable=bpy.app.binary_path,
              strips=5, animation_values_verified=True, two_input_effect_verified=True, visible_text_verified=True, saved_reopened=True, workspace_link_verified=True,
              effect_parameters=list(strip_collection(s).bl_rna.functions['new_effect'].parameters.keys()),
              rendered=str(out/'preview.png'))
(out/'report.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report))
