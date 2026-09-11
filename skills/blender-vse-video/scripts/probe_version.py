"""Read-only capability report. Run with Blender --background --python."""
import bpy, json

def properties(type_name):
    cls = getattr(bpy.types, type_name, None)
    return set(cls.bl_rna.properties.keys()) if cls else set()

scene_props = properties('Scene')
workspace_props = properties('WorkSpace')
editor_props = properties('SequenceEditor')
strip_props = properties('Strip') or properties('Sequence')
text_props = properties('TextStrip') or properties('TextSequence')
collection_type = getattr(bpy.types, 'StripsTopLevel', None) or getattr(bpy.types, 'SequencesTopLevel', None)
params = list(collection_type.bl_rna.functions['new_effect'].parameters.keys()) if collection_type else []
print(json.dumps({
    'version': bpy.app.version_string,
    'binary': bpy.app.binary_path,
    'workspace_sequencer_scene': 'sequencer_scene' in workspace_props,
    'strip_collection': 'strips' if 'strips' in editor_props else 'sequences' if 'sequences' in editor_props else None,
    'effect_parameters': params,
    'modern_timing': {name: name in strip_props for name in ['left_handle','right_handle','content_start','content_end','duration']},
    'text_anchors': {name: name in text_props for name in ['anchor_x','anchor_y','align_x','align_y']},
    'note': 'Capability discovery only; run smoke_test.py and review real media before claiming compatibility.'
}, indent=2))
