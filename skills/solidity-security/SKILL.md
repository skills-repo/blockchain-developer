---
name: solidity-security
description: 智能合约安全 — 发现并修复常见漏洞（重入、溢出、访问控制、前置交易），编写安全 Solidity 代码
source:
  type: derived
  repo: skills-repo/blockchain-developer
  path: skills/solidity-security/SKILL.md
  url: https://skills.sh/wshobson/agents/solidity-security
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
  - solidity
  - security
  - smart-contract
  - audit
---

# Solidity Security — 智能合约安全

> 智能合约一旦部署就无法修改，安全不是可选项是前提。本技能覆盖常见合约漏洞的识别、修复和安全开发模式。

## 能力

- 识别并修复重入攻击、整数溢出、访问控制失败等高频漏洞
- 应用 Checks-Effects-Interactions 模式防止状态变更后重入
- 设计 Pull-over-Push 支付模式避免拒绝服务
- 审查函数可见性和访问控制逻辑的正确性
- 实施紧急停止机制和时间锁等安全网
- 检测前置交易（front-running）风险点并提出缓解方案

## 使用方式

```
/solidity-security 审查我的 ERC20 合约的转账逻辑
/solidity-security 这段 delegatecall 代码有没有安全问题？
/solidity-security 帮我设计一个带时间锁的 DAO 金库合约
```

## 工作流

1. **漏洞扫描** — 对照 OWASP 级合约漏洞清单逐项检查
2. **模式审查** — 验证 CEI（Checks-Effects-Interactions）模式是否到位
3. **权限验证** — 检查 `onlyOwner` / role-based 访问控制是否有越权路径
4. **经济安全** — 检查闪电贷攻击、价格操纵、套利攻击等经济型攻击面
5. **修复建议** — 给出安全代码片段和最佳实践对照

## 核心原则

### Checks-Effects-Interactions
> 先检查条件 → 再修改状态 → 最后才外部调用。这是 Solidity 安全的第一条军规。

违反此模式的代码是重入攻击的主要来源。

### Pull over Push
> 让用户来提款（pull），而不是合约主动转账（push）。避免一笔失败的转账阻塞整个流程。

### 最小权限原则
> 每个函数只应拥有完成工作所需的最小权限。`onlyOwner` 应覆盖尽可能少的代码路径。

### 输入验证是第一道防线
> 永远不信任外部输入。参数范围检查、地址有效性验证、返回值检查——每一项都不能省。

## 适用场景

- 编写新的 Solidity 智能合约
- 审查已有合约的安全性（内部 audit 前自查）
- 从其他链迁移合约到新链时的安全适配
- 学习智能合约安全最佳实践

## 限制

- 不替代专业审计公司（Trail of Bits / OpenZeppelin 等）
- 不覆盖非 EVM 链（Solana/Rust、Move 等有独立安全模型）
- MEV / 区块级攻击需要额外专业工具（如 Flashbots）
- 不覆盖前端/桥接/预言机的非合约层攻击面

## 相关参考（Playbook）

- 智能合约安全审计方法论（漏洞目录、5 步工作流、上线前清单）→ `../../references/smart-contract-security.md`
- 静态初筛脚本 `../../scripts/solidity_lint.py`；上线前检查清单 `../../assets/contract-audit-checklist.md`
