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

def generate_chinese_summary(title: str, description: str, topics: list, readme: str = "") -> dict:
    """生成纯中文的项目简介和比喻（不使用英文原文）"""
    desc_lower = (description or "").lower()
    name_lower = title.lower()
    
    # 判断项目类型，生成纯中文描述
    if any(kw in desc_lower or kw in name_lower for kw in ["ai", "llm", "gpt", "claude", "agent", "machine learning", "deep learning"]):
        category = "AI/机器学习"
        detailed_description = "这是一个 AI 相关的开源项目。它利用人工智能技术，帮助用户自动化处理复杂任务，提升工作效率。可以应用于智能对话、内容生成、数据分析等场景。"
        metaphor = "💡 它就像你的「智能助手」——你告诉它要做什么，它就能理解并帮你完成，就像一个24小时在线的得力帮手。"
        usage = "适合想用 AI 提升效率的开发者，或者想快速搭建智能应用的创业者"
    elif any(kw in desc_lower for kw in ["web", "flask", "django", "fastapi", "server"]):
        category = "Web开发"
        detailed_description = "这是一个 Web 开发相关项目。提供网站或 Web 服务开发所需的框架、库或工具，帮助开发者快速搭建互联网应用。"
        metaphor = "💡 它就像「乐高积木」——提供标准化的模块和接口，让你像搭积木一样快速搭建自己想要的网站或应用。"
        usage = "适合想快速搭建网站、API 服务的开发者"
    elif any(kw in desc_lower for kw in ["data", "pandas", "numpy", "analysis", "visualization"]):
        category = "数据分析"
        detailed_description = "这是一个数据处理工具。帮你分析、处理和可视化数据，将复杂的原始数据转化为易懂的图表和结论，适合数据分析需求。"
        metaphor = "💡 它就像「数据翻译官」——把晦涩难懂的原始数据，翻译成一目了然的图表和结论，让数据会说话。"
        usage = "适合需要处理数据、做数据分析的人，比如运营、产品经理"
    elif any(kw in desc_lower for kw in ["automation", "bot", "scraping", "crawler", "schedule"]):
        category = "自动化工具"
        detailed_description = "这是一个自动化工具项目。它能够帮你自动完成重复性工作，比如定时任务、数据抓取、流程自动化等，节省大量手动操作时间。"
        metaphor = "💡 它就像「自动洗衣机」——你把任务丢进去，设定好程序，它自动帮你完成，你完全不用盯着。"
        usage = "适合想节省时间、让电脑帮你干活的人，处理重复性任务"
    elif any(kw in desc_lower for kw in ["cli", "command", "terminal", "shell", "tool"]):
        category = "命令行工具"
        detailed_description = "这是一个命令行工具。通过终端命令就能快速使用，适合程序员和开发者提高工作效率，通常体积小巧但功能强大。"
        metaphor = "💡 它就像「瑞士军刀」——小巧便携，但集成了多种实用功能，是程序员工具箱里的必备利器。"
        usage = "适合程序员和开发者，喜欢用命令行提高效率的人"
    elif any(kw in desc_lower for kw in ["game", "gaming"]):
        category = "游戏开发"
        detailed_description = "这是一个游戏开发相关项目。提供游戏开发所需的引擎、框架或工具，帮助开发者快速构建游戏应用。"
        metaphor = "💡 它就像「游戏引擎」——提供基础框架和工具，让你专注于创造游戏内容，不用从零开始造轮子。"
        usage = "适合游戏开发者和想制作游戏的人"
    else:
        category = "开发工具"
        detailed_description = "这是一个 Python 开源项目。解决特定的开发需求或提供实用功能，可以根据具体场景灵活使用。"
        metaphor = "💡 它就像「万能扳手」——虽然不是最耀眼的工具，但能帮你解决很多实际问题，是开发者的好帮手。"
        usage = "适合有特定需求的开发者，可以灵活使用"
    
    # 提取核心功能
    if "framework" in desc_lower:
        function = "提供开发框架"
    elif "library" in desc_lower or "package" in desc_lower:
        function = "提供功能库"
    elif "tool" in desc_lower or "utility" in desc_lower:
        function = "提供实用工具"
    elif "platform" in desc_lower:
        function = "提供平台服务"
    else:
        function = "解决特定场景需求"
    
    # 生成简介
    summary = f"【{category}】{function}"
    
    if topics:
        summary += f"，主要涉及 {', '.join(topics[:3])} 等技术"
    
    return {
        "summary": summary,
        "metaphor": metaphor,
        "detailed_description": detailed_description,
        "category": category,
        "usage": usage
    }

def load_previous_stars(filepath: str) -> Dict[str, int]:
    """加载前一天的 stars 数据"""
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return {p["title"]: p.get("stars", 0) for p in data.get("projects", [])}
    except:
        return {}

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"📅 今日日期: {today}")
    
    project_dir = os.path.dirname(os.path.abspath(__file__))
    raw_data_file = os.path.join(project_dir, "raw_trending.json")
    
    # 加载前一天的 stars 数据
    previous_stars = load_previous_stars(raw_data_file)
    
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
        
        # 生成中文简介（详细版）
        raw_desc = repo.get("description", "") or "暂无描述"
        analysis = generate_chinese_summary(name, raw_desc, topics)
        
        current_stars = repo.get("stargazers_count", 0)
        prev_stars = previous_stars.get(f"{owner} / {name}", current_stars)
        stars_growth = current_stars - prev_stars
        
        entry = {
            "rank": i,
            "date": today,
            "title": f"{owner} / {name}",
            "url": repo.get("html_url", ""),
            "description": raw_desc,
            "chinese_summary": analysis["summary"],
            "detailed_description": analysis["detailed_description"],
            "metaphor": analysis["metaphor"],
            "category": analysis["category"],
            "usage": analysis["usage"],
            "stars": current_stars,
            "stars_growth": stars_growth,
            "forks": repo.get("forks_count", 0),
            "language": repo.get("language", ""),
            "topics": topics,
            "created_at": repo.get("created_at", ""),
            "updated_at": repo.get("updated_at", ""),
            "homepage": repo.get("homepage", "")
        }
        raw_entries.append(entry)
        print(f"⭐ {current_stars} (+{stars_growth})")
    
    # 按 stars 增量排序
    raw_entries.sort(key=lambda x: x["stars_growth"], reverse=True)
    # 更新 rank
    for i, entry in enumerate(raw_entries, 1):
        entry["rank"] = i
    
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
        print(f"      {p['chinese_summary']}")

if __name__ == "__main__":
    main()
