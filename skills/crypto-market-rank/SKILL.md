---
name: crypto-market-rank
description: 加密市场分析 — 热门代币排行、聪明钱追踪、社交情绪分析、Meme 币发现
source:
  type: derived
  repo: skills-repo/blockchain-developer
  path: skills/crypto-market-rank/SKILL.md
  url: https://skills.sh/binance/binance-skills-hub/crypto-market-rank
  version: 1.0.0
  updated: 2026-07-29
metadata:
  author: hope
  category: 区块链
  platform: 通用
  difficulty: 入门
  version: 1.0.0
  created: 2026-07-29
tags:
  - crypto
  - market-analysis
  - token-rank
  - social-sentiment
---

# Crypto Market Rank — 加密市场分析

> 加密市场的动向由三股力量驱动：趋势、情绪和聪明钱。本技能帮你从多个维度理解市场热度，不预测价格，只看信号。

## 能力

- 热门代币排行榜：按市值、交易量、持有人数等多维度排序
- 社交情绪分析：追踪代币的社交热度、讨论情绪和话题趋势
- 聪明钱追踪：识别聪明钱地址正在买入的代币
- Meme 币发现：从 Pulse 发射台数据中发现可能爆发的新 Meme 代币
- 交易员排行榜：追踪顶级地址的 PnL 和胜率
- 多链覆盖：BSC、Base、Solana

## 使用方式

```
/crypto-market-rank 最近 24 小时 BSC 上的热门代币有哪些？
/crypto-market-rank Solana 上聪明钱最近买了什么？
/crypto-market-rank 帮我看看 Meme 赛道现在什么代币热度最高
```

## 工作流

1. **确定目标** — 你想找什么类型的信息？趋势、聪明钱、情绪还是新项目？
2. **选维度和链** — 确定时间窗口（1h/4h/24h）和目标链（BSC/Base/Solana）
3. **获取数据** — 查询对应的排行榜/指标
4. **交叉验证** — 不要只看一个维度。热门 + 聪明钱买入 + 正面情绪 = 强信号
5. **输出摘要** — 列出 top 结果，标注值得关注的点，但不给出买卖建议

## 核心原则

### 追踪信号，不预测价格
> 社交热度上升 + 聪明钱流入 = 值得关注。但这不是买入信号——市场可能在 5 分钟内翻转。

### 聪明钱不是跟单
> 聪明钱地址可能是做市商、项目方或机器人。追踪他们买什么是为了研究，不是为了跟单。

### Meme 是注意力经济
> Meme 代币的爆发依赖社交传播和注意力聚集。算法评分是一个维度，社区活力和叙事同样重要。

### 时间窗口决定信号含义
> 1 小时数据 = 短线噪音，24 小时数据 = 日内趋势，7 天数据 = 中期信号。用错时间窗口得出错误结论。

## 适用场景

- 加密市场日常调研，了解当前什么在涨
- 研究特定赛道的热度变化
- 发现值得深入分析的代币（先看 ranking，再深挖 tokenomics）
- 监控社交情绪的异常波动

## 限制

- 不提供实时交易数据（需通过 API 获取，本技能指导分析思路）
- 社交情绪可能被操纵（刷量、机器人）
- 不覆盖 CEX 订单簿和衍生品数据
- 不给出买入或卖出建议——仅供研究参考
