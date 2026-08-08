#!/usr/bin/env python3
"""
solidity_lint.py — Solidity 合约静态安全初筛（确定性、可复现）

扫描 .sol 文件，定位常见高危模式：浮动 pragma、旧编译器版本、tx.origin 鉴权、
未检查外部调用、unchecked 块、已废弃函数等。用于部署前自检基线。

用法:
    python3 solidity_lint.py contracts/                 # 扫描目录
    python3 solidity_lint.py a.sol b.sol                # 指定文件
    python3 solidity_lint.py contracts/ --json          # 机器可读
    python3 solidity_lint.py contracts/ --strict        # 有 high 时退出码 1

不替代专业审计；仅做快速初筛。
"""
import argparse
import json
import os
import re
import sys

# (规则id, 严重度, 正则, 说明)
RULES = [
    ("FLOAT_PRAGMA", "medium",
     r"pragma\s+solidity\s*\^",
     "浮动 pragma (^) 会随构建环境漂移，应锁定精确版本"),
    ("OLD_VERSION", "high",
     r"pragma\s+solidity\s+0\.[0-7]\.",
     "编译器版本 < 0.8.0 默认无溢出检查，需 SafeMath 或升级"),
    ("TX_ORIGIN", "high",
     r"tx\.origin",
     "用 tx.origin 鉴权可被中间合约钓鱼，应改用 msg.sender"),
    ("UNCHECKED", "low",
     r"unchecked\s*\{",
     "unchecked 块关闭溢出检查，需确认已手工保证安全"),
    ("DEPRECATED", "medium",
     r"\b(sha3|callcode|suicide|throw)\b",
     "已废弃函数 (sha3/callcode/suicide/throw)，应替换"),
    ("BLOCK_TIMESTAMP", "low",
     r"(block\.timestamp|now)\b",
     "block.timestamp/now 可被矿工轻微操纵，勿用于强随机"),
    ("LOW_LEVEL_CALL", "low",
     r"\.(call|delegatecall|staticcall)\s*\(",
     "低级调用返回值需显式检查，否则失败静默"),
]

SEV_ORDER = {"high": 3, "medium": 2, "low": 1}


def lint_file(path):
    findings = []
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except OSError as e:
        return [{"file": path, "line": 0, "rule": "READ_ERROR",
                 "severity": "high", "message": str(e)}]
    text = "".join(lines)
    for rule_id, sev, pattern, msg in RULES:
        for m in re.finditer(pattern, text):
            ln = text.count("\n", 0, m.start()) + 1
            findings.append({"file": path, "line": ln, "rule": rule_id,
                             "severity": sev, "message": msg})
    return findings


def collect_targets(paths):
    files = []
    for p in paths:
        if os.path.isdir(p):
            for root, _, names in os.walk(p):
                for n in sorted(names):
                    if n.endswith(".sol"):
                        files.append(os.path.join(root, n))
        elif p.endswith(".sol") or os.path.isfile(p):
            files.append(p)
    return files


def main():
    ap = argparse.ArgumentParser(description="Solidity 合约安全静态初筛")
    ap.add_argument("paths", nargs="+", help=".sol 文件或目录")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--strict", action="store_true",
                    help="存在 high 级发现时退出码 1")
    args = ap.parse_args()

    files = collect_targets(args.paths)
    if not files:
        print("未发现 .sol 文件", file=sys.stderr)
        return 2

    all_findings = []
    for fp in files:
        all_findings.extend(lint_file(fp))

    if args.json:
        print(json.dumps({"files": len(files),
                          "findings": all_findings}, ensure_ascii=False, indent=2))
    else:
        if not all_findings:
            print(f"✅ 未发现高危模式（扫描 {len(files)} 个文件）")
        else:
            by_sev = sorted(all_findings,
                            key=lambda x: -SEV_ORDER.get(x["severity"], 0))
            for f in by_sev:
                loc = f["file"] if f["line"] == 0 else f"{f['file']}:{f['line']}"
                print(f"[{f['severity'].upper()}] {loc} ({f['rule']})\n  {f['message']}")
            print(f"\n共 {len(all_findings)} 条发现，扫描 {len(files)} 个文件")

    if args.strict and any(f["severity"] == "high" for f in all_findings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
