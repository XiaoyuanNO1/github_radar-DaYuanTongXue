# GitHub AI 雷达 · 维护文档

## 📋 项目概述

每日自动扫描 GitHub Python 趋势项目，从 VC 视角深度分析，筛选最具 Vibecoding 变现潜力的项目。

## 📁 文件结构

```
github-radar-site/
├── index.html              # 主页面
├── style.css               # 样式文件
├── app.js                  # 前端逻辑
├── radar_history.json      # 项目数据（自动生成）
├── fetch_and_analyze.py    # 数据获取与基础分析
├── ai_analyzer.py          # AI 深度分析模块
├── daily_update.sh         # 每日更新脚本
├── push_update.sh          # GitHub 推送脚本
└── daily_update.log        # 更新日志
```

## ⚙️ 配置说明

### 1. GitHub Token（可选但推荐）

设置 GitHub Token 以提高 API 请求限制：

```bash
export GITHUB_TOKEN="your_github_token_here"
```

或在 crontab 中设置：
```
GITHUB_TOKEN=your_token
0 8 * * * cd /path/to/github-radar-site && bash daily_update.sh
```

### 2. AI 分析配置

当前 `ai_analyzer.py` 使用占位实现。要启用真实 AI 分析，需要：

1. 配置 OpenClaw ACP 或其他 AI API
2. 修改 `ai_analyzer.py` 中的 `analyze_with_acp()` 函数
3. 参考 OpenClaw 文档配置 AI 调用

## 🚀 手动运行

### 立即获取今日数据
```bash
cd ~/.openclaw/workspace/projects/github-radar-site
python3 fetch_and_analyze.py
```

### 完整更新（包括推送）
```bash
cd ~/.openclaw/workspace/projects/github-radar-site
bash daily_update.sh
```

## ⏰ 定时任务

已配置每天早上 8 点自动运行：

```cron
0 8 * * * cd /root/.openclaw/workspace/projects/github-radar-site && bash daily_update.sh
```

### 查看定时任务
```bash
crontab -l
```

### 修改定时任务
```bash
crontab -e
```

### 查看执行日志
```bash
tail -f ~/.openclaw/workspace/projects/github-radar-site/daily_update.log
```

## 📊 数据格式

`radar_history.json` 中的每个项目：

```json
{
  "date": "2026-03-12",
  "id": "2026-03-12-001",
  "title": "owner / repo",
  "url": "https://github.com/owner/repo",
  "raw_description": "原始描述",
  "description": "AI分析后的中文描述",
  "metaphor": "通俗类比",
  "scores": {
    "vibecoding_ease": 2,
    "logic_moat": 1,
    "track_fit": 1,
    "growth_potential": 2,
    "total": 6
  },
  "is_top": false,
  "score_reasons": {
    "vibecoding_ease": "评分理由",
    "logic_moat": "评分理由",
    "track_fit": "评分理由",
    "growth_potential": "评分理由"
  },
  "stars": 1000,
  "forks": 100,
  "language": "Python"
}
```

## 🔧 维护操作

### 重新获取今日数据
如果今天数据有问题，可以删除后重新获取：

```bash
cd ~/.openclaw/workspace/projects/github-radar-site
# 备份当前数据
cp radar_history.json radar_history.json.backup
# 编辑文件删除今日数据
nano radar_history.json
# 重新获取
python3 fetch_and_analyze.py
```

### 修改评分维度
编辑 `fetch_and_analyze.py` 中的 `analyze_with_ai()` 函数。

### 调整获取项目数量
修改 `fetch_trending_repos()` 中的 `count` 参数（默认 15）。

## 🐛 故障排查

### 问题：API 请求失败
- 检查网络连接
- 设置 GITHUB_TOKEN 提高 API 限制

### 问题：AI 分析失败
- 检查 AI 模块配置
- 查看日志文件 `daily_update.log`

### 问题：数据未更新
- 检查今天是否已有数据（去重逻辑）
- 手动运行脚本查看错误信息

## 📝 更新日志

### 2026-03-12
- 初始部署
- 配置定时任务（每天 8 点）
- 创建维护文档

## 👤 维护者

- 当前维护：大元同学
- 原项目作者：XiaoyuanNO1
