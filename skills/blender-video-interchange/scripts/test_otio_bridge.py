"""Run with the same Python environment as otio_bridge.py."""
import tempfile
import unittest
from pathlib import Path
import opentimelineio as otio
from otio_bridge import encode, decode, frames

class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name).resolve()
        self.media=self.root/'clip with spaces.mp4'; self.media.touch()
        self.plan={'name':'fixture','rate':24,'start':86400,'duration':96,'resolution':[320,180],
            'tracks':[{'name':'V1','kind':'Video','clips':[
                {'name':'A','path':str(self.media),'start':12,'source':24,'duration':18},
                {'name':'B','path':str(self.media),'start':48,'source':6,'duration':24}]}]}
    def tearDown(self): self.temp.cleanup()
    def test_ranges_gaps_and_timecode(self):
        result=decode(encode(self.plan),self.root)
        self.assertEqual(result['tracks'],self.plan['tracks'])
        self.assertEqual(result['duration'],96)
        self.assertEqual(result['source_timecode'],86400)
    def test_fractional_rate(self):
        self.plan['rate']=24000/1001
        self.assertEqual(decode(encode(self.plan),self.root)['tracks'],self.plan['tracks'])
    def test_effect_rejected(self):
        t=encode(self.plan);t.tracks[0][1].effects.append(otio.schema.LinearTimeWarp(time_scalar=2))
        with self.assertRaises(ValueError): decode(t,self.root)
    def test_missing_media_rejected(self):
        self.media.unlink()
        with self.assertRaises(FileNotFoundError): decode(encode(self.plan),self.root)
    def test_overlap_rejected(self):
        self.plan['tracks'][0]['clips'][1]['start']=20
        with self.assertRaises(ValueError): encode(self.plan)
    def test_source_timecode_origin(self):
        t=encode(self.plan);c=t.tracks[0][1]
        c.media_reference.available_range=otio.opentime.TimeRange(otio.opentime.RationalTime(86400,24),otio.opentime.RationalTime(100,24))
        c.source_range=otio.opentime.TimeRange(otio.opentime.RationalTime(86424,24),otio.opentime.RationalTime(18,24))
        self.assertEqual(decode(t,self.root)['tracks'][0]['clips'][0]['source'],24)
    def test_subframe_rejected(self):
        with self.assertRaises(ValueError):frames(otio.opentime.RationalTime(0.5,24),24)

if __name__=='__main__':unittest.main()
