"""Inside Blender; pass a fresh test directory containing picture.mp4 and sound.wav."""
import bpy,sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from blender_bridge import collection,export_plan
root=Path(sys.argv[sys.argv.index('--')+1]).resolve()
s=bpy.context.scene;s.name='Cuts Round Trip';s.render.fps=24;s.frame_start=1;s.frame_end=84
s.render.resolution_x=320;s.render.resolution_y=180;s.render.resolution_percentage=100
col=collection(s)
for name,start,source,duration,channel in [('A',7,12,24,2),('B',43,36,30,2),('Overlay',19,48,12,3)]:
 t=col.new_movie(name,str(root/'picture.mp4'),channel=channel,frame_start=start-source)
 t.frame_final_start=start;t.frame_final_end=start+duration;t.blend_type='REPLACE'
a=col.new_sound('Tone',str(root/'sound.wav'),channel=1,frame_start=-5)
a.frame_final_start=7;a.frame_final_end=55
plan,issues=export_plan(s,'ffprobe');assert not issues,issues
(root/'original.json').write_text(json.dumps(plan,indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(root/'original.blend'))
for frame in [7,19,30,42,43,72]:
 s.frame_set(frame);s.render.filepath=str(root/f'original-{frame}.png');bpy.ops.render.render(write_still=True)
# Unsupported title is diagnosed, never silently lost.
params=col.bl_rna.functions['new_effect'].parameters.keys()
kwargs={'length':19} if 'length' in params else {'frame_end':20}
x=col.new_effect('Unsupported title',type='TEXT',channel=4,frame_start=1,**kwargs)
_,issues=export_plan(s,'ffprobe');assert any('TEXT' in i for i in issues)
print('Fixture and unsupported-title check passed')
