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

# 1. 获取和分析数据
echo "🔍 步骤 1: 获取 GitHub 趋势项目..." >> "$LOG_FILE"
python3 "$SCRIPT_DIR/fetch_and_analyze.py" >> "$LOG_FILE" 2>&1 || {
    echo "❌ 数据获取失败" >> "$LOG_FILE"
    exit 1
}

# 2. 推送到 GitHub（如果配置了 git）
if [ -d "$SCRIPT_DIR/.git" ]; then
    echo "📤 步骤 2: 推送到 GitHub..." >> "$LOG_FILE"
    bash "$SCRIPT_DIR/push_update.sh" >> "$LOG_FILE" 2>&1 || {
        echo "⚠️ 推送失败（可能无变更或无 git 配置）" >> "$LOG_FILE"
    }
else
    echo "ℹ️  步骤 2: 跳过推送（未配置 git）" >> "$LOG_FILE"
fi

echo "✅ [$(date '+%Y-%m-%d %H:%M:%S')] 更新完成" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# 只保留最近 30 天的日志
tail -n 500 "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"
