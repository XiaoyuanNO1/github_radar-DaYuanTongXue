#!/bin/bash
# ===== 发送每日简报到 Feishu =====

if [ -f /tmp/github_radar_report.txt ]; then
    REPORT=$(cat /tmp/github_radar_report.txt)
    
    # 使用 message 工具发送
    # 注意：此脚本需要在 OpenClaw 环境中运行
    echo "$REPORT"
    
    # 清理简报文件
    rm -f /tmp/github_radar_report.txt
fi
