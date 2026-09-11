"""Small RNA-detected compatibility helpers. Import inside Blender."""
import bpy


def strip_collection(scene):
    editor = scene.sequence_editor_create()
    if hasattr(editor, 'strips'):
        return editor.strips
    return editor.sequences


def new_effect(scene, name, kind, channel, start, duration, inputs=()):
    if duration <= 0:
        raise ValueError('duration must be positive')
    collection = strip_collection(scene)
    params = collection.bl_rna.functions['new_effect'].parameters.keys()
    kwargs = dict(name=name, type=kind, channel=channel, frame_start=start)
    if 'length' in params:
        kwargs['length'] = duration
    elif 'frame_end' in params:
        kwargs['frame_end'] = start + duration
    else:
        raise RuntimeError('Unsupported effect timing parameters: ' + str(list(params)))
    if len(inputs) > 2:
        raise ValueError('At most two input strips are supported')
    for i, strip in enumerate(inputs, 1):
        key = next((key for key in (f'input{i}', f'seq{i}') if key in params), None)
        if key is None:
            raise RuntimeError(f'No supported input {i} parameter')
        kwargs[key] = strip
    return collection.new_effect(**kwargs)


def bind_workspace(scene, workspace):
    if hasattr(workspace, 'sequencer_scene'):
        workspace.sequencer_scene = scene


def configure_editor(scene, workspace, area):
    """Call after the area has become a SEQUENCE_EDITOR; UI may need a timer."""
    bind_workspace(scene, workspace)
    space = next((s for s in area.spaces if s.type == 'SEQUENCE_EDITOR'), None)
    if space is None:
        raise RuntimeError('Set area.type to SEQUENCE_EDITOR and allow UI initialization first')
    space.view_type = 'SEQUENCER_PREVIEW'
    space.show_region_channels = True
    space.display_channel = 0
    if hasattr(space, 'use_zoom_to_fit'):
        space.use_zoom_to_fit = True
    return space
