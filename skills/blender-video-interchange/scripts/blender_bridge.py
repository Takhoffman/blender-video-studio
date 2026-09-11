"""Run inside Blender: export a cuts plan, or import a plan into a new scene."""
import argparse
import json
import math
from pathlib import Path
import subprocess
import sys
import bpy


def collection(scene):
    ed=scene.sequence_editor_create()
    return ed.strips if hasattr(ed,'strips') else ed.sequences


def probe(path, rate, kind, ffprobe):
    data=json.loads(subprocess.check_output([ffprobe,'-v','error','-show_streams','-show_format','-of','json',str(path)]))
    streams=[s for s in data['streams'] if s['codec_type']==('video' if kind=='Video' else 'audio')]
    if len(streams)!=1: raise ValueError(f'Expected one {kind} stream: {path}')
    stream=streams[0]
    if kind=='Video':
        from fractions import Fraction
        actual=float(Fraction(stream['avg_frame_rate']))
        nominal=float(Fraction(stream['r_frame_rate']))
        if abs(actual-rate)>0.001 or abs(nominal-rate)>0.001:
            raise ValueError(f'Normalize video to constant timeline rate {rate} first: {path} ({actual})')
    return float(stream.get('duration', data.get('format',{}).get('duration',0)))


def export_plan(scene, ffprobe):
    rate=scene.render.fps/scene.render.fps_base
    plan={'name':scene.name,'rate':rate,'start':int(scene.get('interchange_source_timecode',scene.frame_start)),
          'duration':scene.frame_end-scene.frame_start+1,
          'resolution':[scene.render.resolution_x,scene.render.resolution_y], 'tracks':[]}
    issues=[]; tracks={}
    if scene.animation_data and (scene.animation_data.action or scene.animation_data.drivers or scene.animation_data.nla_tracks):
        issues.append('Scene animation requires baking or a clean cuts-only duplicate')
    if scene.timeline_markers: issues.append('Timeline markers are not transferred')
    for s in collection(scene):
        # Strips wholly outside output range are not part of the exchange.
        lo=max(scene.frame_start,s.frame_final_start); hi=min(scene.frame_end+1,s.frame_final_end)
        if hi<=lo: continue
        if s.type not in ['MOVIE','SOUND']:
            issues.append(f'{s.name}: unsupported {s.type}; render this element before exchange'); continue
        kind='Video' if s.type=='MOVIE' else 'Audio'
        problems=[]
        if s.mute: problems.append('muted strip')
        channels=scene.sequence_editor.channels
        if s.channel<len(channels) and channels[s.channel].mute: problems.append('muted channel')
        if getattr(s,'modifiers',[]): problems.append('modifiers')
        if getattr(s,'animation_offset_start',0) or getattr(s,'animation_offset_end',0): problems.append('animation offsets')
        if getattr(s,'speed_factor',1)!=1 or getattr(s,'use_reverse_frames',False): problems.append('retiming')
        if hasattr(s,'retiming_keys') and len(s.retiming_keys): problems.append('retiming keys')
        if kind=='Video':
            t=s.transform; c=s.crop
            if any(abs(getattr(t,k)-v)>1e-6 for k,v in [('offset_x',0),('offset_y',0),('scale_x',1),('scale_y',1),('rotation',0)]): problems.append('transform')
            if any(getattr(c,k) for k in ['min_x','max_x','min_y','max_y']): problems.append('crop')
            if s.blend_alpha!=1 or s.blend_type not in ['REPLACE','ALPHA_OVER']: problems.append('blending')
            if getattr(s,'color_multiply',1)!=1 or getattr(s,'color_saturation',1)!=1: problems.append('color adjustment')
            if getattr(s,'use_flip_x',False) or getattr(s,'use_flip_y',False): problems.append('flip')
        else:
            if s.volume!=1 or s.pan!=0 or getattr(s,'pitch',1)!=1: problems.append('audio gain/pan/pitch')
        path=Path(bpy.path.abspath(s.filepath if kind=='Video' else s.sound.filepath)).resolve()
        try:
            seconds=probe(path,rate,kind,ffprobe)
            source=lo-s.frame_start
            duration=hi-lo
            if source<0 or (source+duration)/rate>seconds+1/rate: problems.append('source range exceeds file')
        except Exception as e: problems.append(str(e))
        if problems: issues.append(f'{s.name}: '+', '.join(problems)); continue
        key=(s.channel,kind)
        tracks.setdefault(key,[]).append({'name':s.name,'path':str(path),'start':lo-scene.frame_start,'source':source,'duration':duration})
    for (channel,kind), clips in sorted(tracks.items()):
        clips.sort(key=lambda c:c['start'])
        if any(a['start']+a['duration']>b['start'] for a,b in zip(clips,clips[1:])): issues.append(f'Channel {channel}: overlap')
        plan['tracks'].append({'name':f'{channel} / {kind}','kind':kind,'clips':clips})
    return plan,issues


def import_plan(plan, ffprobe):
    rate=plan['rate']
    if not math.isfinite(rate) or rate<=0: raise ValueError('Invalid rate')
    if not isinstance(plan['duration'],int) or plan['duration']<=0: raise ValueError('Invalid timeline duration')
    if len(plan['tracks'])>128: raise ValueError('Too many Blender channels')
    # Preflight before mutating Blender; imported clips must fit real files.
    for track in plan['tracks']:
        if track['kind'] not in ['Video','Audio']: raise ValueError('Invalid track kind')
        cursor=0
        for c in sorted(track['clips'],key=lambda c:c['start']):
            if any(not isinstance(c[k],int) for k in ['source','duration','start']): raise ValueError('Frame values must be integers')
            if c['start']<cursor or c['start']+c['duration']>plan['duration']: raise ValueError('Overlapping or out-of-timeline clip')
            cursor=c['start']+c['duration']
            seconds=probe(c['path'],rate,track['kind'],ffprobe)
            if c['source']<0 or c['duration']<=0 or c['start']<0 or (c['source']+c['duration'])/rate>seconds+1/rate:
                raise ValueError('Invalid or unavailable source range: '+c['name'])
    scene=bpy.data.scenes.new(plan['name']+' / Imported')
    try:
        scene.render.fps=round(rate); scene.render.fps_base=round(rate)/rate
        scene.render.resolution_x,scene.render.resolution_y=plan['resolution']
        scene.render.resolution_percentage=100
        scene.frame_start=1; scene.frame_end=max(1,plan['duration'])
        scene['interchange_source_timecode']=plan.get('source_timecode',plan['start'])
        col=collection(scene)
        # Audio below video; OTIO video order is bottom to top.
        ordered=sorted(plan['tracks'],key=lambda t: t['kind']=='Video')
        for channel,track in enumerate(ordered,1):
            for c in track['clips']:
                start=1+c['start']; base=start-c['source']
                if track['kind']=='Video':
                    s=col.new_movie(c['name'],c['path'],channel=channel,frame_start=base)
                    s.blend_type='REPLACE'
                else: s=col.new_sound(c['name'],c['path'],channel=channel,frame_start=base)
                s.frame_final_start=start; s.frame_final_end=start+c['duration']
        for window in bpy.context.window_manager.windows:
            window.scene=scene
            if hasattr(window.workspace,'sequencer_scene'): window.workspace.sequencer_scene=scene
        return scene
    except Exception:
        bpy.data.scenes.remove(scene)
        raise


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode',choices=['export','import']);p.add_argument('file',type=Path)
    p.add_argument('--output',type=Path);p.add_argument('--ffprobe',default='ffprobe')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    report=a.file.with_suffix(a.file.suffix+'.blender-report.json')
    if a.mode=='export':
        if a.file.exists(): raise FileExistsError(a.file)
        plan,issues=export_plan(bpy.context.scene,a.ffprobe)
        report.write_text(json.dumps({'blender':bpy.app.version_string,'status':'blocked' if issues else 'exported','issues':issues,'scope':'edit decisions only; scene color management not transferred'},indent=2))
        if issues: raise ValueError(f'Unsupported elements: see {report}')
        a.file.write_text(json.dumps(plan,indent=2)+'\n')
    else:
        if not a.output: raise ValueError('--output new.blend is required')
        if a.output.exists(): raise FileExistsError(a.output)
        try:
            scene=import_plan(json.loads(a.file.read_text()),a.ffprobe)
        except Exception as e:
            report.write_text(json.dumps({'status':'blocked','reason':str(e)},indent=2))
            raise
        bpy.ops.wm.save_as_mainfile(filepath=str(a.output.resolve()))
        report.write_text(json.dumps({'blender':bpy.app.version_string,'status':'imported','scene':scene.name,'scope':'cuts only; inspect before delivery'},indent=2))

if __name__=='__main__': main()
