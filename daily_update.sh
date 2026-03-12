#!/bin/bash
# ===== GitHub AI 雷达 · 每日自动更新脚本 =====
# 每天早上 8 点自动运行，获取趋势项目并推送

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 日志文件
LOG_FILE="$SCRIPT_DIR/daily_update.log"

echo "========================================" >> "$LOG_FILE"
echo "📡 [$(date '+%Y-%m-%d %H:%M:%S')] 开始每日雷达更新" >> "$LOG_FILE"

# 1. 获取 AI 分析数据
echo "🔍 步骤 1: 获取 AI 分析榜单..." >> "$LOG_FILE"
python3 "$SCRIPT_DIR/fetch_and_analyze.py" >> "$LOG_FILE" 2>&1 || {
    echo "❌ AI 分析数据获取失败" >> "$LOG_FILE"
}

# 2. 获取原始榜单数据
echo "🔍 步骤 2: 获取原始趋势榜单..." >> "$LOG_FILE"
python3 "$SCRIPT_DIR/fetch_raw_trending.py" >> "$LOG_FILE" 2>&1 || {
    echo "❌ 原始榜单获取失败" >> "$LOG_FILE"
}

# 3. 推送到 GitHub
echo "📤 步骤 3: 推送到 GitHub..." >> "$LOG_FILE"
bash "$SCRIPT_DIR/push_update.sh" >> "$LOG_FILE" 2>&1 || {
    echo "⚠️ 推送失败（可能无变更）" >> "$LOG_FILE"
}

echo "✅ [$(date '+%Y-%m-%d %H:%M:%S')] 更新完成" >> "$LOG_FILE"

# 4. 生成并保存简报
echo "📧 步骤 4: 生成简报..." >> "$LOG_FILE"
python3 << 'PYTHON' >> "$LOG_FILE" 2>&1
import json
from datetime import datetime

try:
    with open('radar_history.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    today = datetime.now().strftime("%Y-%m-%d")
    today_projects = [p for p in data if p['date'] == today]
    
    if today_projects:
        top3 = sorted(today_projects, key=lambda x: x['scores']['total'], reverse=True)[:3]
        
        report = f"📡 GitHub AI 雷达 · {today} 简报\n\n"
        report += f"🏆 今日黑马 Top 3\n\n"
        
        for i, p in enumerate(top3, 1):
            report += f"{i}. {p['title']}\n"
            report += f"   ⭐ {p.get('stars', 0)} | 总分: {p['scores']['total']}/10\n"
            report += f"   💡 {p['metaphor'][:40]}...\n\n"
        
        report += f"📊 今日新增 {len(today_projects)} 个项目\n"
        report += f"🌐 https://xiaoyuanno1.github.io/github_radar-DaYuanTongXue/"
        
        with open('/tmp/github_radar_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        
        print("简报已生成: /tmp/github_radar_report.txt")
    else:
        print("今日无数据")
except Exception as e:
    print(f"简报生成失败: {e}")
PYTHON

echo "" >> "$LOG_FILE"

# 只保留最近 30 天的日志
tail -n 500 "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"
