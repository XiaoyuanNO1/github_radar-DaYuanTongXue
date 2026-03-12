#!/bin/bash
# 每天更新部分历史项目的 stars

cd "$(dirname "$0")"

python3 << 'PYTHON'
import json
import time
import urllib.request

def fetch_stars(name):
    try:
        url = f'https://api.github.com/repos/{name.replace(" / ", "/")}'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode())
            return data.get('stargazers_count', 0)
    except:
        return 0

with open('radar_history.json', 'r') as f:
    data = json.load(f)

# 只更新 10 个（避免 rate limit）
zero_projects = [p for p in data if p.get('stars', 0) == 0][:10]

if not zero_projects:
    print('所有项目都已更新！')
    exit(0)

print(f'更新 {len(zero_projects)} 个项目...')
updated = 0

for p in zero_projects:
    stars = fetch_stars(p['title'])
    if stars > 0:
        p['stars'] = stars
        updated += 1
        print(f"  {p['title']}: {stars}")
    time.sleep(3)

with open('radar_history.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'完成: {updated}/{len(zero_projects)}')
PYTHON

# 推送到 GitHub
if [ -f radar_history.json ]; then
    git add radar_history.json
    git commit -m "📊 自动更新历史项目 stars" || true
    git push origin main || true
fi
