---
name: crypto-report
description: 加密货币研究 — 对区块链项目做 tokenomics、链上指标、竞争格局综合分析，产出研究报告
source:
  type: derived
  repo: skills-repo/blockchain-developer
  path: skills/crypto-report/SKILL.md
  url: https://skills.sh/claude-office-skills/skills/crypto-report
  version: 1.0.0
  updated: 2026-07-29
metadata:
  author: hope
  category: 区块链
  platform: 通用
  difficulty: 进阶
  version: 1.0.0
  created: 2026-07-29
tags:
  - crypto
  - research
  - tokenomics
  - analysis
---

# Crypto Report — 加密货币研究报告

> 加密世界信息过载，筛选信号比收集数据更难。本技能帮你对区块链项目做结构化分析，从 tokenomics 到链上指标到竞争格局，产出一份可操作的研究报告。

## 能力

- Tokenomics 分析：供应结构、分配比例、解锁时间表、通胀模型
- 协议机制评估：技术架构、共识机制、经济模型、治理结构
- 链上指标解读：活跃地址、交易量、TVL、手续费收入、用户留存
- 竞争格局分析：赛道定位、差异化、护城河
- 风险因素识别：监管风险、团队风险、代币集中度、流动性风险
- 投资论点构建：基于事实的 bull case / bear case 框架

## 使用方式

```
/crypto-report 帮我分析 Arbitrum 的 tokenomics 和竞争格局
/crypto-report 写一份 EigenLayer 再质押赛道的市场分析
/crypto-report 我在考虑买入 X 代币，帮我做一次全面分析
```

## 工作流

1. **确定范围** — 分析哪个项目/赛道？关注哪些维度？
2. **信息收集** — tokenomics 文档、白皮书、链上数据、社区讨论
3. **结构化分析** — 按模块拆解：代币、技术、市场、团队、风险
4. **竞争对比** — 与同赛道 2-3 个竞品做关键指标对比
5. **撰写报告** — 输出结构化的分析报告，含 bull case / bear case
6. **标注不确定性** — 明确区分数据和推测，不确定的地方诚实说不知道

## 分析框架

### Tokenomics 五问
1. **总供应量**：固定还是通胀？通胀率多少？
2. **流通量**：当前流通比例？解锁时间表对价格的潜在冲击？
3. **分配**：团队/投资人/社区/金库的分配比例？公平吗？
4. **价值捕获**：代币持有者如何受益？费用分红、治理权还是单纯的预期？
5. **需求驱动**：谁需要这个代币？为什么？

### 竞争格局四看
1. **赛道规模**：这个赛道的 TAM 是多少？还在增长吗？
2. **市场份额**：项目目前排第几？与第一名的差距？
3. **护城河**：技术、网络效应、品牌还是监管许可？
4. **替代威胁**：有没有更好的方案在解决同一个问题？

## 核心原则

### 数据 > 叙事
> 「L2 夏季」「AI 代理」这些都是叙事。叙事驱动价格，数据驱动价值。做研究时先看数据再看叙事。

### Tokenomics 是数学，不是魔法
> 6 个月后解锁的代币今天就要计入你的估值模型。解锁日不是「到时候再说」，而是已知的抛压事件。

### 没人能预测价格
> 研究报告的结论不是「会涨」或「会跌」，而是「在 X 条件下项目有/没有长期价值」。

## 适用场景

- 深入了解一个加密项目的基本面
- 比较同一赛道的多个项目
- 评估代币的长期持有价值
- 准备投资决策前的尽职调查

## 限制

- 不提供实时链上数据（需用户通过 Dune / Nansen / DeFiLlama 自取）
- 不预测短期价格走势
- 不构成投资建议——研究报告仅供信息参考
- 不对智能合约做技术审计
- 不覆盖非 EVM 生态的深层分析

## 相关参考（Playbook）

- Tokenomics 量化框架（收益来源、真实收益率、解锁冲击）→ `../../references/defi-tokenomics.md`
- 链上研究方法论（指标字典、验证叙事、竞争/风险论题）→ `../../references/onchain-research.md`
- 合约与经济安全维度（漏洞目录、审计工作流）→ `../../references/smart-contract-security.md`
