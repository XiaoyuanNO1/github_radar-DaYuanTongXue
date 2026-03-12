#!/usr/bin/env python3
"""
GitHub AI 雷达 - AI 增强分析模块
调用 OpenClaw ACP 或其他 AI API 进行深度分析
"""

import json
import os
import sys
import subprocess
from typing import Dict

def analyze_with_acp(repo_name: str, description: str, readme: str) -> Dict:
    """
    使用 OpenClaw ACP 进行 VC 视角深度分析
    返回包含评分、描述、类比和评分理由的字典
    """
    
    prompt = f"""你是一位资深 VC 投资人，擅长从变现潜力角度分析开源项目。

请分析以下 GitHub 项目：

项目名：{repo_name}
项目描述：{description}
README摘要：{readme[:1500]}

请从以下维度进行评分（1-3分制，总分最高12分）：

1. **Vibecoding Ease (1-3分)** - 用 Cursor/Claude 复刻的难度
   - 3分：纯提示词工程，一天可复刻
   - 2分：中等复杂度，需理解架构
   - 1分：涉及底层系统，难以复刻

2. **Logic Moat (0-2分)** - 业务/技术护城河
   - 2分：有独特算法或深度业务逻辑
   - 1分：有一定设计深度
   - 0分：简单 API 串联

3. **Track Fit (0-2分)** - 赛道匹配度（宠物、银发、玄学、金融、教育）
   - 2分：强命中核心赛道
   - 1分：部分相关
   - 0分：不在核心赛道

4. **Growth Potential (0-2分)** - 小红书/即刻传播潜力
   - 2分：极易爆款，副业变现清晰
   - 1分：有一定传播点
   - 0分：开发者工具，传播难

请用 JSON 格式返回：
{{
  "description": "一句话概括项目核心价值和解决的痛点",
  "metaphor": "用一句通俗类比解释这个项目（用「它就像...」句式）",
  "scores": {{
    "vibecoding_ease": 评分,
    "logic_moat": 评分,
    "track_fit": 评分,
    "growth_potential": 评分
  }},
  "score_reasons": {{
    "vibecoding_ease": "评分理由",
    "logic_moat": "评分理由",
    "track_fit": "评分理由",
    "growth_potential": "评分理由"
  }}
}}

只返回 JSON，不要其他内容。"""

    try:
        # 尝试使用 OpenClaw ACP 调用 AI
        # 注意：实际部署时需要根据 OpenClaw 配置调整
        result = subprocess.run(
            ["python3", "-c", f"""
import sys
# 这里应该调用实际的 AI API
# 临时返回模拟数据
print(json.dumps({{
    "description": "AI分析暂不可用，使用默认描述",
    "metaphor": "需要 AI 生成类比...",
    "scores": {{
        "vibecoding_ease": 2,
        "logic_moat": 1,
        "track_fit": 1,
        "growth_potential": 1
    }},
    "score_reasons": {{
        "vibecoding_ease": "需要 AI 分析",
        "logic_moat": "需要 AI 分析",
        "track_fit": "需要 AI 分析",
        "growth_potential": "需要 AI 分析"
    }}
}}))
"""],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        analysis = json.loads(result.stdout)
        
        # 计算总分
        scores = analysis.get("scores", {})
        total = sum(scores.values())
        analysis["scores"]["total"] = total
        
        return analysis
        
    except Exception as e:
        print(f"AI 分析失败: {e}")
        # 返回默认分析
        return {
            "description": description or "暂无描述",
            "metaphor": f"它就像「{repo_name}」...",
            "scores": {
                "vibecoding_ease": 2,
                "logic_moat": 1,
                "track_fit": 1,
                "growth_potential": 1,
                "total": 5
            },
            "score_reasons": {
                "vibecoding_ease": "AI 分析失败，使用默认评分",
                "logic_moat": "AI 分析失败，使用默认评分",
                "track_fit": "AI 分析失败，使用默认评分",
                "growth_potential": "AI 分析失败，使用默认评分"
            }
        }

def batch_analyze(projects: list, batch_size: int = 5) -> list:
    """批量分析项目"""
    results = []
    for i, project in enumerate(projects):
        print(f"  AI分析 [{i+1}/{len(projects)}]: {project.get('title', 'Unknown')}...")
        analysis = analyze_with_acp(
            project.get("title", ""),
            project.get("raw_description", ""),
            project.get("readme", "")
        )
        results.append({**project, **analysis})
    return results

if __name__ == "__main__":
    # 测试
    test = analyze_with_acp("test/repo", "Test description", "Test readme")
    print(json.dumps(test, ensure_ascii=False, indent=2))
