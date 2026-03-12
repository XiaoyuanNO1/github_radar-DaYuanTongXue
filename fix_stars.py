#!/usr/bin/env python3
"""
补充历史数据的 stars 信息
"""

import json
import os
import urllib.request
from datetime import datetime

GITHUB_API_BASE = "https://api.github.com"

def get_headers():
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "GitHub-Radar-Bot"
    }
    return headers

def fetch_repo_stars(full_name: str) -> int:
    """获取仓库当前 stars 数"""
    # 去除空格，构建正确的 owner/repo 格式
    clean_name = full_name.replace(' / ', '/').strip()
    url = f"{GITHUB_API_BASE}/repos/{clean_name}"
    try:
        req = urllib.request.Request(url, headers=get_headers())
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get("stargazers_count", 0)
    except Exception as e:
        print(f"  ⚠️ 获取 {full_name} stars 失败: {e}")
        return 0

def main():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(project_dir, "radar_history.json")
    
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 找出缺少 stars 或 stars 为 0 的项目（ today's data already has valid stars）
    # 只更新历史数据（非今天的数据）
    today = datetime.now().strftime("%Y-%m-%d")
    projects_to_update = [p for p in data if p['date'] != today and p.get('stars', 0) == 0]
    print(f"找到 {len(projects_to_update)} 个需要更新 stars 的历史项目")
    
    if not projects_to_update:
        print("所有历史项目都有 stars 数据，无需更新")
        return
    
    # 更新 stars
    for i, project in enumerate(projects_to_update, 1):
        title = project['title']
        print(f"[{i}/{len(projects_to_update)}] 获取 {title} 的 stars...", end=" ")
        stars = fetch_repo_stars(title)
        if stars > 0:
            project['stars'] = stars
            print(f"⭐ {stars}")
        else:
            # 如果获取失败，尝试获取当时的数据
            print(f"⚠️ 无法获取，保持 0")
    
    # 保存更新后的数据
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 已更新 {len(projects_to_update)} 个项目的 stars 数据")

if __name__ == "__main__":
    main()
