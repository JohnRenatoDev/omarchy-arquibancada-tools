#!/usr/bin/env python3
"""Check actual cloth pixels under the two placement-constrained shirt marks.

Run after a visual fit: Vasco's cross must stay on white sash fabric and
Flamengo's monogram on red fabric. This complements the geometric/unit checks.
Requires the same rsvg-convert/ImageMagick tools as the wallpaper build.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from badge_surface import render


def pixels(path, channel=None, resize=None):
    args=['magick',str(path)]
    if resize:args+=['-resize',resize]
    if channel:args+=['-alpha','extract']
    args+=['-depth','8',('gray:-' if channel else 'rgb:-')]
    return subprocess.check_output(args)


def main():
    layouts=json.loads((ROOT/'src/mascotes-layout.json').read_text())
    results={}
    with tempfile.TemporaryDirectory(prefix='arquibancada-regions-') as temporary:
        for slug in ('vasco','flamengo'):
            kit=layouts[slug]
            svg=Path(temporary)/(slug+'.svg');png=svg.with_suffix('.png')
            svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="3344" height="1882" viewBox="0 0 1672 941">'+render(ROOT/'assets'/kit['badge'],kit['shirt_surface'])+'</svg>')
            subprocess.run(['rsvg-convert','-o',str(png),str(svg)],check=True)
            mask=pixels(png,True)
            cloth=pixels(ROOT/'assets/mascotes-generated'/(slug+'.png'),resize='3344x1882!')
            mark=pixels(png)
            inside=matched=stars=stars_on_black=0
            for i,alpha in enumerate(mask):
                if alpha<230:continue
                r,g,b=cloth[i*3:i*3+3]
                if slug=='flamengo':
                    ink=mark[i*3:i*3+3]
                    if max(ink)-min(ink)>40:
                        # In the photographed 2026 shirt the gold star sits on
                        # the black yoke, above the white CRF on the red band.
                        stars+=1
                        stars_on_black+=bool(max(r,g,b)<95)
                        continue
                inside+=1
                if slug=='vasco':
                    good=min(r,g,b)>95 and max(r,g,b)-min(r,g,b)<80
                else:
                    good=r>1.4*g+15 and r>1.4*b+15
                matched+=bool(good)
            fraction=matched/inside
            results[slug]={'solid_mark_pixels':inside,'matching_cloth_fraction':round(fraction,5),'region':'white sash' if slug=='vasco' else 'red chest band'}
            assert fraction>=.97,f'{slug}: only {fraction:.1%} of the mark lies on the intended cloth'
            if slug=='flamengo':
                results[slug]['gold_star_pixels']=stars
                results[slug]['star_on_black_fraction']=stars_on_black/stars
                assert stars_on_black/stars>=.9,'Flamengo star outside black shoulder yoke'
    print(json.dumps(results,indent=2))


if __name__=='__main__':main()
