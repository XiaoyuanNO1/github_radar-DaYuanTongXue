# GitHub 部署配置指南

## 方式 1：通过 Token 部署

### 你需要提供：

1. **GitHub Personal Access Token (PAT)**
   - 访问: https://github.com/settings/tokens
   - 点击 "Generate new token (classic)"
   - 权限勾选: `repo` (完整仓库权限)
   - 复制生成的 token

2. **目标仓库地址**
   - 选项 A: 推送到现有仓库
     - 格式: `https://github.com/用户名/仓库名.git`
   - 选项 B: 创建新仓库（推荐）
     - 在 GitHub 上新建仓库（如 `github-radar-site`）
     - 留空 README，不初始化
     - 给我仓库地址

### 安全提示
- Token 是敏感信息，建议通过私信/安全渠道发送
- Token 只用于此次部署，不会存储
- 可以在 GitHub 上随时撤销 Token

## 方式 2：你自己配置（更安全）

如果你不想分享 Token，可以自己完成最后一步：

```bash
cd ~/.openclaw/workspace/projects/github-radar-site

# 1. 配置用户信息
git config user.name "你的名字"
git config user.email "你的邮箱"

# 2. 添加远程仓库
git remote add origin https://github.com/你的用户名/仓库名.git

# 3. 推送到 GitHub
git branch -m main  # 重命名分支为 main
git push -u origin main

# 4. 配置自动推送（需要 Token）
# 编辑 push_update.sh 中的 git push 命令，使用带 Token 的 URL
```

## 部署后配置 GitHub Pages

1. 进入 GitHub 仓库 → Settings → Pages
2. Source 选择 "Deploy from a branch"
3. Branch 选择 "main" / "/ (root)"
4. 保存后等待 1-2 分钟即可访问

## 配置自动更新（可选）

如果希望每日自动推送，需要：
1. 将 Token 配置到环境变量
2. 或使用 GitHub Actions（推荐）

### GitHub Actions 配置（推荐）

在项目根目录创建 `.github/workflows/daily-update.yml`：

```yaml
name: Daily Radar Update
on:
  schedule:
    - cron: '0 8 * * *'  # 每天早上 8 点
  workflow_dispatch:  # 允许手动触发

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: pip install requests
      - name: Run radar update
        run: python fetch_and_analyze.py
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      - name: Commit and push
        run: |
          git config user.name "GitHub Action"
          git config user.email "action@github.com"
          git add radar_history.json
          git diff --quiet && git diff --staged --quiet || git commit -m "🤖 每日雷达更新 $(date +%Y-%m-%d)"
          git push
```

这样就不需要本地定时任务，GitHub 会自动运行。
