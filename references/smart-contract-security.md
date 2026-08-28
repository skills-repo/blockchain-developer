# 智能合约安全 Playbook

> 部署即不可逆。本 playbook 给出一套可复用的合约安全审计方法论：漏洞目录 → 审计工作流 → 检查清单，配合 `scripts/solidity_lint.py` 做静态初筛。

## 决策树：发现风险时怎么处理

```
发现可疑代码
  ├─ 是否影响资金流转/权限？(是)
  │    ├─ 重入 / 算术溢出 / 访问控制缺失 → 阻断级，必须修
  │    └─ 其他 → 进入检查清单
  ├─ 是否可被外部操纵？(是) → 视为高危，加测试 + 形式化验证
  └─ 仅代码风格/可维护性 → 低危，记录即可
```

## 高危漏洞目录（按出现频率排序）

1. **重入（Reentrancy）**：外部调用（`.call` / `transfer` / ERC721 `safeTransfer`）前未更新状态。
   - 修复：Checks-Effects-Interactions 模式 + `nonReentrant` 守卫 + 拉取模式（pull over push）。
2. **算术溢出（<0.8.0）**：旧编译器无默认溢出检查。
   - 修复：升级到 0.8.x；或用 `SafeMath` / 显式 `unchecked` 并注释理由。
3. **访问控制缺失**：`onlyOwner` / `AccessControl` 未覆盖特权函数。
   - 修复：所有 `mint` / `pause` / `upgrade` / `withdraw` 必须鉴权；默认拒绝。
4. **`tx.origin` 鉴权**：可被中间合约钓鱼。
   - 修复：一律用 `msg.sender`。
5. **前置交易 / 价格预言机操纵**：`block.timestamp` / 单点预言机做随机数或定价。
   - 修复：TWAP 预言机、提交-揭示方案、链下随机数（VRF）。
6. **未检查返回值**：`transfer` 失败静默吞掉（ERC20 非标准）。
   - 修复：用 `safeTransfer` 或检查返回值。
7. **`delegatecall` 到可控地址**：逻辑可替换。
   - 修复：地址白名单 / 不可变 / 多签治理。

## 审计工作流（5 步）

1. **静态初筛**：`python3 scripts/solidity_lint.py contracts/ --json` 扫浮动 pragma、旧版本、`tx.origin`、`unchecked`、已废弃函数。
2. **人工走查**：逐函数确认资金路径、权限、外部调用顺序。
3. **单元测试**：对每条修复路径写 fuzz / invariant 测试（Foundry `invariant`）。
4. **对手模拟**：假设攻击者视角重放关键路径（升级、提现、清算）。
5. **外部审计 + 形式化**：上线前至少一轮第三方审计；高价值合约加形式化验证。

## 上线前检查清单（详见 `assets/contract-audit-checklist.md`）

- [ ] 所有特权函数有访问控制
- [ ] 无浮动 pragma（`^`），锁定点版本
- [ ] 外部调用前已完成状态更新
- [ ] 无 `tx.origin` 鉴权
- [ ] 价格来源抗操纵（TWAP / VRF）
- [ ] 已覆盖关键路径的测试与清算/升级演练
- [ ] 已做第三方审计或等价评审

## 边界

- 本 playbook 不替代专业审计；仅做部署前自检基线。
- 不替用户决定"是否上线"——产出报告，拍板留给用户。

## 相关子技能与层次边界

- **落地动作（L3）**：需要按漏洞目录逐条修复、写安全合约代码 → `skills/solidity-security/SKILL.md`；需要把合约/经济风险纳入项目研究 → `skills/crypto-report/SKILL.md`。
- **配套资源**：静态初筛用 `scripts/solidity_lint.py`（浮动 pragma / 旧编译器 / `tx.origin` / `unchecked` / 废弃函数）；上线前逐项核对 `assets/contract-audit-checklist.md`。
- **兄弟参考**：收益/经济面风险不在本文范围，见 `references/defi-tokenomics.md`。
- **层次边界**：本 playbook 只讲"漏洞目录 + 审计工作流 + 检查清单"（方法论层）；具体修复代码段与 CEI/Pull-over-Push 模式落地由 `skills/solidity-security/` 负责，本文不重复。
