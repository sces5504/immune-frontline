#!/usr/bin/env python3
"""Create an immutable, playable backup; never overwrite a released version."""
import argparse, hashlib, html, json, re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
from version_navigation import write_pages
root = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser()
p.add_argument('--version', required=True)
p.add_argument('--title', required=True)
p.add_argument('--notes', required=True)
a = p.parse_args()
if not re.fullmatch(r'\d+\.\d+\.\d+', a.version):
    p.error('Use a semantic version such as 2.0.0')
folder = root / 'outputs/versions'
folder.mkdir(parents=True, exist_ok=True)
manifest = folder / 'manifest.json'
records = json.loads(manifest.read_text()) if manifest.exists() else []
source = (root / 'outputs/immune-frontline.html').read_bytes()
marker = re.search(rb'data-game-version="([^"]+)"', source)
if marker and marker.group(1).decode() != a.version:
    p.error('The game version marker must match the release version.')
target = folder / f'v{a.version}.html'
if target.exists() or any(x['version'] == a.version for x in records):
    p.error('This version already exists; released backups are immutable.')
target.write_bytes(source)
records.append(dict(version=a.version, title=a.title, notes=a.notes,
                    date=datetime.now(ZoneInfo('Asia/Taipei')).strftime('%Y-%m-%d %H:%M'),
                    file=target.name, sha256=hashlib.sha256(source).hexdigest()))
manifest.write_text(json.dumps(records, ensure_ascii=False, indent=2)+'\n')
write_pages(folder, records)
print(f'Archived {a.version}: {target.relative_to(root)}')
