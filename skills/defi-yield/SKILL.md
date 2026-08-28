---
name: defi-yield
description: DeFi 收益策略 — 跨协议收益对比、流动性分析、质押策略制定，基于链上数据做决策
source:
  type: derived
  repo: skills-repo/blockchain-developer
  path: skills/defi-yield/SKILL.md
  url: https://skills.sh/emblemcompany/agent-skills/emblem-defi-yield
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
  - defi
  - yield
  - staking
  - liquidity
---

# DeFi Yield — DeFi 收益策略

> DeFi 收益率一天一变，靠推特炒币不如靠数据决策。本技能帮你跨协议对比收益、评估风险、制定质押和流动性策略。

## 能力

- 跨协议收益对比：Lido / Aave / Compound / EigenLayer 等收益数据比较
- 流动性策略分析：LP 做市收益 vs 无常损失评估
- 质押方案设计：单一质押、流动性质押（LST）、再质押（LRT）的选择逻辑
- 仓位健康检查：基于 Nansen 等工具审查已有 DeFi 头寸
- 收益来源拆解：交易费 vs 代币激励 vs 基差收益

## 使用方式

```
/defi-yield 比较一下 ETH 在 Lido 和 EigenLayer 的当前收益差
/defi-yield 我有 10 万 USDC，帮我设计一个低风险的收益策略
/defi-yield 帮我分析这个 LP 对的过去 30 天无常损失
```

## 工作流

1. **目标确认** — 风险偏好（保守/平衡/激进）、锁定期、目标链
2. **协议扫描** — 列出目标链上符合条件的协议及其当前 APY
3. **风险分析** — 智能合约风险 + 协议治理风险 + 无常损失预估
4. **策略设计** — 单一协议 vs 组合策略，含再平衡触发条件
5. **仓位监控** — 设置收益偏离阈值和退出条件

## 核心原则

### 收益来源决定风险等级
> 交易费收益 < 质押收益 < 协议补贴 < 代币通胀激励。收益越高，越要问钱从哪来。

### 不追最高 APY
> 1,000% APY 的代币激励通常意味着你在接盘。可持续的收益来自真实的经济活动。

### 无常损失不是"无常"
> LP 做市的 IL 一旦提取就是永久损失。只有在交易费收益 > IL + 持有成本时，LP 才是赚的。

### 智能合约风险是最大风险
> 再高的 APY 也抵不过一次协议被黑。检查审计报告、TVL 排名、运行时间——老协议比高收益更安全。

## 适用场景

- 有闲置加密资产想获得被动收益
- 不确定该选 Lido 质押还是自己做 LP
- 持有 LP 仓位但不确定是否该退出
- 想了解跨链收益机会（Ethereum / Solana / Base 等）

## 限制

- 不提供实时 APY 数据（需用户自己查看协议前端或 DeFiLlama）
- 不覆盖杠杆挖矿策略（杠杆放大风险，不适合本技能定位）
- 非同质化 DeFi（如 NFT 借贷、RWA）不在覆盖范围
- 税务影响需咨询专业人士

## 相关参考（Playbook）

- DeFi 收益与 Tokenomics 分析（真实收益率、解锁冲击、收益来源四象限）→ `../../references/defi-tokenomics.md`
