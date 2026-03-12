#!/usr/bin/env python3
"""
GitHub AI 雷达 - 数据获取与 AI 分析脚本
每日自动获取 GitHub Python 趋势项目并进行 VC 视角分析
"""

import json
import os
import sys
import re
import urllib.request
import urllib.error
from datetime import datetime
from typing import List, Dict, Any

# GitHub API 配置
GITHUB_API_BASE = "https://api.github.com"
# 使用 GitHub Token 提高 API 限制
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

def get_headers():
    """获取 API 请求头"""
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "GitHub-Radar-Bot"
    }
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    return headers

def fetch_trending_repos(language: str = "python", since: str = "daily", count: int = 15) -> List[Dict]:
    """
    获取 GitHub 趋势项目
    由于 GitHub API 没有直接的 trending endpoint，使用 search API 模拟
    """
    # 获取最近一周创建的项目，按 stars 排序
    one_week_ago = (datetime.now().timestamp() - 7 * 24 * 3600)
    date_str = datetime.fromtimestamp(one_week_ago).strftime("%Y-%m-%d")
    
    # 构建搜索查询
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

def fetch_repo_readme(owner: str, repo: str) -> str:
    """获取仓库 README 内容"""
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/readme"
    
    try:
        req = urllib.request.Request(url, headers=get_headers())
        with urllib.request.urlopen(req, timeout=30) as response:
            import base64
            data = json.loads(response.read().decode('utf-8'))
            content = data.get("content", "")
            # Base64 解码
            return base64.b64decode(content.replace('\n', '')).decode('utf-8', errors='ignore')[:2000]
    except Exception as e:
        print(f"⚠️ 获取 README 失败 {owner}/{repo}: {e}")
        return ""

def analyze_with_ai(repo_data: Dict, readme: str) -> Dict:
    """
    使用 AI 分析项目的 Vibecoding 变现潜力
    返回包含评分和分析结果的字典
    """
    # 这里应该调用实际的 AI API 进行分析
    # 为了演示，返回模拟的分析结果
    # 实际使用时，需要集成 OpenAI、Claude 或其他 AI API
    
    # 模拟 AI 分析（实际部署时需要替换为真实 AI 调用）
    description = repo_data.get("description", "") or ""
    
    # 简单启发式评分（仅用于演示）
    scores = {
        "vibecoding_ease": 2,  # 1-3: 实现难度
        "logic_moat": 2,       # 0-2: 护城河
        "track_fit": 1,        # 0-2: 赛道匹配
        "growth_potential": 2  # 0-2: 增长潜力
    }
    
    # 根据关键词简单调整分数
    desc_lower = description.lower()
    if any(kw in desc_lower for kw in ["agent", "ai", "llm", "gpt", "claude"]):
        scores["track_fit"] = 2
        scores["growth_potential"] = 2
    
    total = sum(scores.values())
    
    return {
        "description": description or "暂无描述",
        "metaphor": f"这个项目就像「{repo_data.get('name', '某工具')}」... (需要 AI 生成)",
        "scores": {
            **scores,
            "total": total
        },
        "score_reasons": {
            "vibecoding_ease": "需要 AI 分析生成",
            "logic_moat": "需要 AI 分析生成",
            "track_fit": "需要 AI 分析生成",
            "growth_potential": "需要 AI 分析生成"
        }
    }

def generate_project_entry(repo: Dict, date_str: str, index: int) -> Dict:
    """生成项目条目"""
    owner = repo.get("owner", {}).get("login", "")
    name = repo.get("name", "")
    
    # 获取 README
    readme = fetch_repo_readme(owner, name)
    
    # AI 分析
    analysis = analyze_with_ai(repo, readme)
    
    return {
        "date": date_str,
        "id": f"{date_str}-{index:03d}",
        "title": f"{owner} / {name}",
        "url": repo.get("html_url", ""),
        "raw_description": repo.get("description", "") or "",
        "description": analysis["description"],
        "metaphor": analysis["metaphor"],
        "scores": analysis["scores"],
        "is_top": analysis["scores"]["total"] >= 8,
        "score_reasons": analysis["score_reasons"],
        "stars": repo.get("stargazers_count", 0),
        "forks": repo.get("forks_count", 0),
        "language": repo.get("language", "")
    }

def load_existing_data(filepath: str) -> List[Dict]:
    """加载现有数据"""
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ 加载现有数据失败: {e}")
    return []

def save_data(filepath: str, data: List[Dict]):
    """保存数据到文件"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ 数据已保存到 {filepath}")

def main():
    """主函数"""
    # 获取今天的日期
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"📅 今日日期: {today}")
    
    # 项目目录
    project_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(project_dir, "radar_history.json")
    
    # 加载现有数据
    print("📂 加载现有数据...")
    existing_data = load_existing_data(data_file)
    print(f"   已有 {len(existing_data)} 条记录")
    
    # 检查今天是否已有数据
    today_existing = [p for p in existing_data if p.get("date") == today]
    if today_existing:
        print(f"⚠️ 今天 ({today}) 已有 {len(today_existing)} 条记录，跳过获取")
        return
    
    # 获取趋势项目
    print("🔍 获取 GitHub Python 趋势项目...")
    repos = fetch_trending_repos(language="python", count=15)
    print(f"   获取到 {len(repos)} 个项目")
    
    if not repos:
        print("⚠️ 未获取到项目，退出")
        return
    
    # 生成项目条目
    print("🤖 分析项目 (AI 评分)...")
    new_entries = []
    for i, repo in enumerate(repos, 1):
        print(f"   [{i}/{len(repos)}] {repo.get('full_name', 'Unknown')}...", end=" ")
        try:
            entry = generate_project_entry(repo, today, i)
            new_entries.append(entry)
            print(f"总分 {entry['scores']['total']}")
        except Exception as e:
            print(f"失败: {e}")
    
    # 合并数据
    all_data = existing_data + new_entries
    
    # 保存数据
    print(f"\n💾 保存数据...")
    save_data(data_file, all_data)
    print(f"   今日新增 {len(new_entries)} 个项目")
    print(f"   总计 {len(all_data)} 个项目")
    
    # 生成统计信息
    top_projects = [p for p in new_entries if p.get("is_top")]
    print(f"\n🏆 今日 Top 项目: {len(top_projects)} 个")
    for p in top_projects:
        print(f"   - {p['title']} (总分: {p['scores']['total']})")

if __name__ == "__main__":
    main()
