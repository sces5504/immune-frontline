#!/usr/bin/env python3
"""Package the latest game or a released backup for GitHub Pages."""
import argparse, hashlib, json, re, shutil
from pathlib import Path
from version_navigation import decorate_game
root = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser()
p.add_argument('--version', default='')
p.add_argument('--out', default='site')
a = p.parse_args()
records = json.loads((root / 'outputs/versions/manifest.json').read_text())
for x in records:
    data = (root / 'outputs/versions' / x['file']).read_bytes()
    if hashlib.sha256(data).hexdigest() != x['sha256']:
        raise SystemExit('Released backup was altered: '+x['version'])
source = root / 'outputs/immune-frontline.html'
if a.version:
    version = a.version.removeprefix('v')
    record = next((x for x in records if x['version'] == version), None)
    if record is None:
        raise SystemExit('Unknown released version: '+a.version)
    source = root / 'outputs/versions' / record['file']
if not a.version and hashlib.sha256(source.read_bytes()).hexdigest() != records[-1]['sha256']:
    raise SystemExit('Latest source has no matching release backup. Run scripts/release.py before publishing.')
target = root / a.out
target.mkdir(parents=True, exist_ok=True)
current = a.version.removeprefix('v') if a.version else records[-1]['version']
(target / 'index.html').write_text(decorate_game(source.read_text(), current, 'versions/navigation.js?release='+records[-1]['version']))
shutil.copytree(root / 'outputs/versions', target / 'versions', dirs_exist_ok=True)
for x in records:
    backup = root / 'outputs/versions' / x['file']
    (target / 'versions' / x['file']).write_text(decorate_game(backup.read_text(), x['version'], 'navigation.js?release='+records[-1]['version']))
(target / '.nojekyll').touch()
print('Packaged '+str(source.relative_to(root)))
