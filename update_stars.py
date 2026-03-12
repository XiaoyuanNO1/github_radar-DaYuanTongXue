#!/usr/bin/env python3
"""
批量更新历史项目的 stars（带延时避免 rate limit）
"""

import json
import time
import urllib.request
from datetime import datetime

GITHUB_API_BASE = "https://api.github.com"

def get_headers():
    return {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "GitHub-Radar-Bot"
    }

def fetch_repo_stars(full_name: str) -> int:
    """获取仓库当前 stars 数"""
    clean_name = full_name.replace(' / ', '/').strip()
    url = f"{GITHUB_API_BASE}/repos/{clean_name}"
    try:
        req = urllib.request.Request(url, headers=get_headers())
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get("stargazers_count", 0)
    except Exception as e:
        print(f"  ⚠️ 失败: {e}")
        return 0

def main():
    with open('radar_history.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 找出需要更新 stars 的项目
    need_update = [p for p in data if p.get('stars', 0) == 0]
    print(f"需要更新 {len(need_update)} 个项目\n")
    
    updated = 0
    for i, project in enumerate(need_update, 1):
        print(f"[{i}/{len(need_update)}] {project['title']}...", end=" ")
        stars = fetch_repo_stars(project['title'])
        if stars > 0:
            project['stars'] = stars
            updated += 1
            print(f"⭐ {stars}")
        else:
            print("❌ 失败")
        
        # 延时避免 rate limit
        if i < len(need_update):
            time.sleep(2)
    
    # 保存
    with open('radar_history.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 成功更新 {updated}/{len(need_update)} 个项目")

if __name__ == "__main__":
    main()
