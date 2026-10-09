#!/usr/bin/env python3
"""Create an immutable, playable backup; never overwrite a released version."""
import argparse, hashlib, html, json, re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
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
cards = '\n'.join(f'<article><div class="version">v{html.escape(x["version"])}</div><h2>{html.escape(x["title"])}</h2><p>{html.escape(x["notes"])}</p><small>{html.escape(x["date"])} · 不覆寫的獨立備份</small><a href="{html.escape(x["file"])}">玩這個版本 →</a></article>' for x in reversed(records))
page = '''<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>免疫前線｜版本檔案室</title><style>*{box-sizing:border-box}body{margin:0;background:#12182b;color:#f1eadc;font:16px/1.7 -apple-system,sans-serif}main{max-width:980px;margin:auto;padding:48px 24px}h1{font-size:32px}p,small{color:#a6b5c7}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}article{padding:24px;border:2px solid #34435b;background:#1a2539;box-shadow:5px 5px 0 #070c19}h2{font-size:19px}.version{color:#5bdfc7;font-weight:800}a{display:block;color:#5bdfc7;text-decoration:none;font-weight:bold;margin-top:18px}nav a{display:inline-block;margin:0}</style><main><nav><a href="../index.html" id="latest">← 最新版本</a></nav><h1>版本檔案室</h1><p>每個版本都是可直接遊玩的完整備份。開啟舊版不會更改目前上線版本。要把網站還原，可在 GitHub Actions 的部署流程填入版本號，或請我把指定版本重新發布。</p><div class="grid">'''+cards+'''</div></main><script>if(location.protocol==='file:')document.querySelector('#latest').href='../immune-frontline.html';</script></html>'''
(folder / 'index.html').write_text(page)
print(f'Archived {a.version}: {target.relative_to(root)}')
