#!/usr/bin/env python3
"""
GitHub AI 雷达 - 原始榜单获取
获取当天 GitHub Python 趋势项目，保存原始数据（不打分）
"""

import json
import os
import urllib.request
from datetime import datetime
from typing import List, Dict

GITHUB_API_BASE = "https://api.github.com"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

def get_headers():
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "GitHub-Radar-Bot"
    }
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    return headers

def fetch_trending_repos(language: str = "python", count: int = 30) -> List[Dict]:
    """获取 GitHub 趋势项目（原始数据）"""
    # 获取最近一周创建的项目
    one_week_ago = (datetime.now().timestamp() - 7 * 24 * 3600)
    date_str = datetime.fromtimestamp(one_week_ago).strftime("%Y-%m-%d")
    
    query = f"language:{language} created:>{date_str}"
    url = f"{GITHUB_API_BASE}/search/repositories?q={urllib.parse.quote(query)}&sort=stars&order=desc&per_page={count}"
    
    try:
        req = urllib.request.Request(url, headers=get_headers())
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get("items", [])
    except Exception as e:
        print(f"⚠️ 获取趋势项目失败: {e}")
        return []

def fetch_repo_topics(owner: str, repo: str) -> List[str]:
    """获取仓库 topics"""
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/topics"
    try:
        req = urllib.request.Request(url, headers={**get_headers(), "Accept": "application/vnd.github.v3+json"})
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get("names", [])
    except:
        return []

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"📅 今日日期: {today}")
    
    project_dir = os.path.dirname(os.path.abspath(__file__))
    raw_data_file = os.path.join(project_dir, "raw_trending.json")
    
    print("🔍 获取 GitHub Python 趋势项目（原始数据）...")
    repos = fetch_trending_repos(count=30)
    print(f"   获取到 {len(repos)} 个项目")
    
    if not repos:
        print("⚠️ 未获取到项目")
        return
    
    # 构建原始榜单数据
    raw_entries = []
    for i, repo in enumerate(repos, 1):
        owner = repo.get("owner", {}).get("login", "")
        name = repo.get("name", "")
        
        print(f"   [{i}/{len(repos)}] {owner}/{name}...", end=" ")
        
        # 获取 topics
        topics = fetch_repo_topics(owner, name)
        
        entry = {
            "rank": i,
            "date": today,
            "title": f"{owner} / {name}",
            "url": repo.get("html_url", ""),
            "description": repo.get("description", "暂无描述") or "暂无描述",
            "stars": repo.get("stargazers_count", 0),
            "forks": repo.get("forks_count", 0),
            "language": repo.get("language", ""),
            "topics": topics,
            "created_at": repo.get("created_at", ""),
            "updated_at": repo.get("updated_at", ""),
            "homepage": repo.get("homepage", "")
        }
        raw_entries.append(entry)
        print(f"⭐ {entry['stars']}")
    
    # 保存原始数据
    with open(raw_data_file, 'w', encoding='utf-8') as f:
        json.dump({
            "date": today,
            "total": len(raw_entries),
            "projects": raw_entries
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 原始榜单已保存到 {raw_data_file}")
    print(f"   共 {len(raw_entries)} 个项目")
    
    # 显示前5名
    print(f"\n🏆 今日 Top 5:")
    for p in raw_entries[:5]:
        print(f"   {p['rank']}. {p['title']} ⭐ {p['stars']}")
        print(f"      {p['description'][:60]}...")

if __name__ == "__main__":
    main()
