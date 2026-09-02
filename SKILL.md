---
name: blockchain-developer
description: >-
  区块链开发者技能库：智能合约安全审计、DeFi 收益与 Tokenomics 分析、加密市场情报、
  链上项目研究。覆盖合约漏洞发现、收益来源判断、链上指标解读与竞争格局分析。
  触发词："solidity-security、defi-yield、crypto-market-rank、crypto-report、合约审计、tokenomics、链上研究"。
agent_created: true
metadata:
  version: 1.0.0
  category: 区块链
  difficulty: 进阶
  architecture: superpower
---

# 区块链开发者

> 把 AI 助手变成一名 Web3 全流程搭档：先审计再部署，先分析再投资，先研究再决策。

本技能采用 **superpower 架构**：`SKILL.md` 只做路由，深层 playbook 放在 `references/` 中
**按需加载**，细粒度能力放在 `skills/` 子技能，确定性任务交给 `scripts/`，可复用模板放在 `assets/`。

## 何时使用

- 编写或审计 Solidity 合约，需要系统化漏洞排查
- 评估一个 DeFi 协议的收益来源与可持续性
- 追踪加密市场热度、聪明钱与社交情绪
- 对某个区块链项目做 tokenomics / 链上 / 竞争的深入研究

## 能力索引（超级技能路由）

本技能采用渐进式加载（progressive disclosure）。`SKILL.md` 仅作路由，**按需**读取下列
`references/` 中的完整 playbook，避免一次性占满上下文。

| 任务 | 读取 / 调用 | 关键词（grep 线索） |
|------|------------|---------------------|
| 智能合约安全审计方法论（漏洞目录/工作流/清单） | `references/smart-contract-security.md` | 重入 溢出 访问控制 tx.origin 审计 漏洞 solidity 安全 |
| DeFi 收益与 Tokenomics 分析（来源/真实收益率/解锁） | `references/defi-tokenomics.md` | defi yield tokenomics 真实收益率 解锁 apy 通胀 排放 |
| 链上研究方法论（指标/竞争/风险论题） | `references/onchain-research.md` | 链上研究 onchain tvl 活跃地址 竞争格局 bull bear |
| 加密市场分析 — 热门排行、聪明钱追踪、社交情绪、Meme 币发现 | `skills/crypto-market-rank/SKILL.md` | 加密市场 热门排行 聪明钱 社交情绪 meme 币 |
| 加密货币研究 — tokenomics、链上指标、竞争格局综合分析 | `skills/crypto-report/SKILL.md` | 加密货币研究 tokenomics 链上指标 竞争格局 |
| DeFi 收益策略 — 跨协议对比、流动性分析、质押方案 | `skills/defi-yield/SKILL.md` | defi 收益 跨协议 流动性 质押 策略 |
| 智能合约安全 — 漏洞发现、安全模式、最佳实践 | `skills/solidity-security/SKILL.md` | 智能合约 安全 审计 漏洞 重入 溢出 |

> 路由规则：方法论 / 决策类任务读 `references/`；要落地具体动作（扫市场、出报告、定策略、审合约）直接调 `skills/`。

## 内置脚本（确定性、可重复执行）

放在 `scripts/`，优先用脚本处理重复/确定性任务，而非每次重写代码：

- `scripts/solidity_lint.py <文件/目录> [--json] [--strict]` — 静态初筛 Solidity 合约：浮动 pragma、旧编译器、tx.origin、unchecked、已废弃函数，输出分级发现。
- `scripts/defi_yield_calc.py <子命令> [--json]` — DeFi 收益与 Tokenomics 确定性速算（APY / 真实收益率 / 解锁冲击比 / TVL-MCap），阈值与 `references/defi-tokenomics.md` 同步；`screen` 子命令一次跑完四项并汇总风险信号（命中阈值退出码 1）。

运行示例：

```bash
python3 scripts/solidity_lint.py contracts/ --strict
# DeFi 收益/解锁压力速算：APY 换算 + 真实收益率 + 解锁冲击 + TVL/MCap 四项汇总
python3 scripts/defi_yield_calc.py screen --apr 0.45 --revenue 1200000 --emissions 900000 \
    --staked-tvl 25000000 --tokens 5000000 --price 1.2 --daily-volume 8000000 \
    --tvl 40000000 --mcap 500000000 --json
```

## 模板资源

`assets/` 提供可直接套用的配置与模板：

- `assets/contract-audit-checklist.md` — 部署前安全审计检查清单（访问控制/算术/外部调用/经济/测试）。

## 核心原则（始终遵循）

1. **先审计再部署**：任何合约上线前必须过安全基线。
2. **收益来自理解**：用真实收益率而非名义 APY 做判断。
3. **渐进式加载**：先读路由表与对应 `references/`，再动手；不凭记忆猜命令与 API。
4. **数据可追溯**：所有链上结论标注快照时间，警惕刷量与滞后。
5. **明确边界**：只出报告与框架，不替用户拍板是否上线或下单。

## 与其他技能协作

- 需要全栈把分析结果做成产品 → 调用 `skills-repo/ai-fullstack-engineer`
- 需要把研究结论写成文档 → 调用 `skills-repo/docs-writer`
