"""Project native badge artwork onto a small, individually fitted shirt surface.

A projective mesh keeps the original lettering; foreshortening comes from the
four measured shirt corners, rather than an arbitrary rotation of a flat sticker.
Coordinates use the unchanged 1672x941 mascot canvas.
"""
import base64
import math
import struct
import xml.etree.ElementTree as ET
from pathlib import Path


def solve(rows, rhs):
    """Small pivoted linear solve; no image library or external dependency."""
    n = len(rhs)
    a = [list(map(float, row)) + [float(value)] for row, value in zip(rows, rhs)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(a[row][col]))
        if abs(a[pivot][col]) < 1e-10:
            raise ValueError('Degenerate badge surface')
        a[col], a[pivot] = a[pivot], a[col]
        divisor = a[col][col]
        a[col] = [value / divisor for value in a[col]]
        for row in range(n):
            if row != col:
                factor = a[row][col]
                a[row] = [x - factor * y for x, y in zip(a[row], a[col])]
    return [row[-1] for row in a]


def validate_surface(surface):
    quad = surface['corners']
    if len(quad) != 4 or any(len(p) != 2 for p in quad):
        raise ValueError('Four shirt corners required in TL, TR, BR, BL order')
    for x, y in quad:
        if not math.isfinite(x + y) or not (0 < x < 1672 and 0 < y < 941):
            raise ValueError('Badge outside source frame')
    for i in range(4):
        a, b, c = quad[i], quad[(i + 1) % 4], quad[(i + 2) % 4]
        if (b[0]-a[0])*(c[1]-b[1]) - (b[1]-a[1])*(c[0]-b[0]) <= 0:
            raise ValueError('Mirrored or folded badge surface')
    area = sum(quad[i][0]*quad[(i+1)%4][1] - quad[(i+1)%4][0]*quad[i][1] for i in range(4))/2
    if not 400 <= area <= 9000 or abs(surface.get('curve', 0)) > 1.5:
        raise ValueError('Badge scale/curvature outside reviewed range')


def projection(surface):
    validate_surface(surface)
    rows, rhs = [], []
    for (u, v), (x, y) in zip(((0,0),(1,0),(1,1),(0,1)), surface['corners']):
        rows.extend(([u,v,1,0,0,0,-x*u,-x*v], [0,0,0,u,v,1,-y*u,-y*v]))
        rhs.extend((x, y))
    h = solve(rows, rhs)
    curve = surface.get('curve', 0)
    def point(u, v):
        denominator = h[6]*u + h[7]*v + 1
        return ((h[0]*u+h[1]*v+h[2])/denominator,
                (h[3]*u+h[4]*v+h[5])/denominator + curve*4*u*(1-u))
    return point


def native_aspect(path):
    if path.suffix == '.svg':
        bounds = list(map(float, ET.parse(path).getroot().get('viewBox').replace(',', ' ').split()))
        return bounds[3] / bounds[2]
    width, height = struct.unpack('>II', path.read_bytes()[16:24])
    return height / width


def _matrix(src, dst):
    rows = [[x, y, 1] for x, y in src]
    a, c, e = solve(rows, [p[0] for p in dst])
    b, d, f = solve(rows, [p[1] for p in dst])
    return f'matrix({a:.8f} {b:.8f} {c:.8f} {d:.8f} {e:.8f} {f:.8f})'


def render(path, surface):
    path = Path(path)
    point = projection(surface)
    ratio = native_aspect(path)
    mime = 'image/svg+xml' if path.suffix == '.svg' else 'image/png'
    uri = f'data:{mime};base64,' + base64.b64encode(path.read_bytes()).decode()
    triangles, clips = [], []
    grid = 8
    for j in range(grid):
        for i in range(grid):
            uv = [(i/grid,j/grid),((i+1)/grid,j/grid),((i+1)/grid,(j+1)/grid),(i/grid,(j+1)/grid)]
            for indices in ((0,1,2),(0,2,3)):
                source = [(uv[k][0]*100, uv[k][1]*100*ratio) for k in indices]
                dest = [point(*uv[k]) for k in indices]
                # Subpixel overlap removes antialias cracks between adjacent cells.
                cx, cy = (sum(p[k] for p in dest)/3 for k in (0,1))
                enlarged = []
                for x,y in dest:
                    distance = math.hypot(x-cx,y-cy)
                    enlarged.append((x+(x-cx)*.06/distance,y+(y-cy)*.06/distance))
                name = f'cell-{len(clips)}'
                coords = ' '.join(f'{x:.5f},{y:.5f}' for x,y in enlarged)
                clips.append(f'<clipPath id="{name}" clipPathUnits="userSpaceOnUse"><polygon points="{coords}"/></clipPath>')
                triangles.append(f'<g clip-path="url(#{name})"><use href="#badge-native" transform="{_matrix(source,dest)}"/></g>')
    quad = surface['corners']
    x = min(p[0] for p in quad)-2; y = min(p[1] for p in quad)-2
    width = max(p[0] for p in quad)-x+2; height = max(p[1] for p in quad)-y+2
    return f'''<g>
      <defs>
        <image id="badge-native" href="{uri}" width="100" height="{100*ratio}"/>
        {''.join(clips)}
        <g id="badge-projected">{''.join(triangles)}</g>
        <mask id="badge-alpha" mask-type="alpha" x="{x}" y="{y}" width="{width}" height="{height}" maskUnits="userSpaceOnUse"><use href="#badge-projected"/></mask>
        <linearGradient id="ink-light" x1="1" y1="0" x2="0" y2="1"><stop stop-color="#000" stop-opacity=".025"/><stop offset="1" stop-color="#000" stop-opacity=".17"/></linearGradient>
        <pattern id="ink-thread" width=".8" height=".8" patternUnits="userSpaceOnUse"><path d="M0 .7L.8 .1" stroke="#000" stroke-width=".09" opacity=".14"/></pattern>
        <filter id="ink-finish" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation=".10"/></filter>
      </defs>
      <g filter="url(#ink-finish)">
        <use href="#badge-projected"/>
        <g mask="url(#badge-alpha)"><rect x="{x}" y="{y}" width="{width}" height="{height}" fill="url(#ink-light)"/><rect x="{x}" y="{y}" width="{width}" height="{height}" fill="url(#ink-thread)"/></g>
      </g>
    </g>'''
