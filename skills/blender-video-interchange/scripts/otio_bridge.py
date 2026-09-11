"""Run in ordinary Python with opentimelineio installed. Strict cuts-only interchange."""
import argparse
import json
import math
from pathlib import Path
from urllib.parse import urlparse, unquote
import opentimelineio as otio


def frames(time, rate):
    value = time.rescaled_to(rate).value
    if abs(value - round(value)) > 0.001:
        raise ValueError(f'Non-frame-aligned time: {value} at {rate}')
    return round(value)


def encode(plan):
    rate = plan['rate']
    if not math.isfinite(rate) or rate <= 0: raise ValueError('Invalid frame rate')
    if not isinstance(plan['duration'],int) or plan['duration']<=0: raise ValueError('Invalid duration')
    rt = lambda n: otio.opentime.RationalTime(n, rate)
    timeline = otio.schema.Timeline(name=plan['name'], global_start_time=rt(plan['start']))
    timeline.metadata['blender_video_studio'] = {'rate': rate, 'resolution': plan['resolution']}
    for track in plan['tracks']:
        if track['kind'] not in ['Video','Audio']: raise ValueError('Invalid track kind')
        result = otio.schema.Track(name=track['name'], kind=track['kind'])
        cursor = 0
        for clip in sorted(track['clips'], key=lambda c: c['start']):
            if any(not isinstance(clip[k],int) for k in ['start','source','duration']): raise ValueError('Frame values must be integers')
            if clip['source']<0 or clip['duration']<=0 or clip['start']+clip['duration']>plan['duration']: raise ValueError('Invalid clip range')
            if clip['start'] < cursor:
                raise ValueError('Overlapping clips within one track')
            if clip['start'] > cursor:
                result.append(otio.schema.Gap(duration=rt(clip['start']-cursor)))
            result.append(otio.schema.Clip(
                name=clip['name'],
                media_reference=otio.schema.ExternalReference(target_url=Path(clip['path']).resolve().as_uri()),
                source_range=otio.opentime.TimeRange(rt(clip['source']), rt(clip['duration']))))
            cursor = clip['start'] + clip['duration']
        if cursor < plan['duration']:
            result.append(otio.schema.Gap(duration=rt(plan['duration']-cursor)))
        timeline.tracks.append(result)
    return timeline


def decode(timeline, directory, rate=None):
    if not isinstance(timeline, otio.schema.Timeline):
        raise ValueError('Expected an OTIO Timeline')
    rate = rate or (timeline.global_start_time.rate if timeline.global_start_time else None)
    if not rate or not math.isfinite(rate) or rate<=0:
        raise ValueError('No timeline rate: pass --fps explicitly')
    def simple(item):
        if getattr(item, 'effects', []) or getattr(item, 'markers', []):
            raise ValueError(f'Effects/markers require manual conform: {item.name}')
        if not getattr(item, 'enabled', True):
            raise ValueError(f'Disabled item requires manual conform: {item.name}')
    simple(timeline.tracks)
    if timeline.tracks.source_range is not None:
        raise ValueError('Trimmed root stack unsupported')
    plan = {'name': timeline.name, 'rate': rate, 'start': 1,
            'source_timecode': frames(timeline.global_start_time, rate) if timeline.global_start_time else 0,
            'duration': frames(timeline.duration(), rate),
            'resolution': list(timeline.metadata.get('blender_video_studio', {}).get('resolution', [1920,1080])), 'tracks': []}
    for track in timeline.tracks:
        if not isinstance(track, otio.schema.Track) or track.kind not in ['Video', 'Audio']:
            raise ValueError('Only flat video/audio tracks supported')
        simple(track)
        if track.source_range is not None:
            raise ValueError('Trimmed tracks unsupported')
        dest = {'name': track.name, 'kind': track.kind, 'clips': []}
        for item in track:
            simple(item)
            if isinstance(item, otio.schema.Gap):
                continue
            if not isinstance(item, otio.schema.Clip):
                raise ValueError('Transitions and nested sequences require manual conform')
            ref = item.media_reference
            if not isinstance(ref, otio.schema.ExternalReference):
                raise ValueError('Only external single-file media supported')
            uri = urlparse(ref.target_url)
            if uri.scheme not in ['', 'file'] or uri.netloc not in ['', 'localhost']:
                raise ValueError('Relink media to local files before importing')
            path = Path(unquote(uri.path))
            if not path.is_absolute(): path = directory/path
            if not path.is_file(): raise FileNotFoundError(path)
            sr = item.trimmed_range()
            source = sr.start_time
            if ref.available_range:
                source = source - ref.available_range.start_time.rescaled_to(source.rate)
            source = frames(source, rate)
            if source < 0: raise ValueError('Negative media offset')
            dest['clips'].append({'name': item.name, 'path': str(path.resolve()),
                'start': frames(track.range_of_child(item).start_time, rate),
                'source': source, 'duration': frames(sr.duration, rate)})
        plan['tracks'].append(dest)
    return plan


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode', choices=['encode','decode'])
    p.add_argument('input', type=Path); p.add_argument('output', type=Path)
    p.add_argument('--fps', type=float)
    a=p.parse_args()
    if a.output.exists(): raise FileExistsError(a.output)
    try:
        if a.mode=='encode':
            otio.adapters.write_to_file(encode(json.loads(a.input.read_text())),str(a.output))
        else:
            result=decode(otio.adapters.read_from_file(str(a.input)),a.input.parent,a.fps)
            a.output.write_text(json.dumps(result,indent=2)+'\n')
    except Exception as e:
        a.output.with_suffix(a.output.suffix+'.report.json').write_text(json.dumps({'status':'blocked','reason':str(e)},indent=2))
        raise
    a.output.with_suffix(a.output.suffix+'.report.json').write_text(json.dumps({'status':'converted','scope':'cuts-only; application validation still required'},indent=2))

if __name__=='__main__': main()
