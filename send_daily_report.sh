#!/bin/bash
# ===== GitHub AI 雷达 · 每日简报发送 =====
# 在数据更新后自动生成并发送简报

cd "$(dirname "$0")"

# 生成简报内容
python3 << 'PYTHON'
import json
import sys
from datetime import datetime

# 读取今天的数据
with open('radar_history.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

today = datetime.now().strftime("%Y-%m-%d")
today_projects = [p for p in data if p['date'] == today]

if not today_projects:
    print("今日无数据", file=sys.stderr)
    sys.exit(1)

# 排序取 Top 3
top3 = sorted(today_projects, key=lambda x: x['scores']['total'], reverse=True)[:3]

# 生成简报
report = f"""📡 GitHub AI 雷达 · {today} 简报

🏆 今日黑马 Top 3

"""

for i, p in enumerate(top3, 1):
    report += f"""
{i}. {p['title']}
   ⭐ {p.get('stars', 0)} | 总分: {p['scores']['total']}/10
   Vibe:{p['scores']['vibecoding_ease']} 护城河:{p['scores']['logic_moat']} 赛道:{p['scores']['track_fit']} 增长:{p['scores']['growth_potential']}
   💡 {p['metaphor'][:50]}...
   🔗 {p['url']}
"""

report += f"""
📊 今日统计
• 新增项目: {len(today_projects)} 个
• 最高评分: {top3[0]['scores']['total']}/10
• 网站: https://xiaoyuanno1.github.io/github_radar-DaYuanTongXue/

—— 由大元同学自动发送 🤖
"""

# 输出简报
print(report)

# 保存到文件供发送
with open('/tmp/daily_report.txt', 'w', encoding='utf-8') as f:
    f.write(report)

PYTHON

# 发送简报（通过 message 工具）
if [ -f /tmp/daily_report.txt ]; then
    echo "简报已生成，准备发送..."
    cat /tmp/daily_report.txt
fi
