#!/usr/bin/env python3
"""DeFi 收益与 Tokenomics 确定性速算器。

把 references/defi-tokenomics.md 与 references/onchain-research.md 中
"手算核对" 的几个口径固化成可重复执行的命令，避免每次重写公式或口误：

  apy        APR → APY 复利换算
  real-yield 真实收益率（剔除代币排放后的净收益）
  unlock     解锁冲击比（解锁额 / 日均成交量）
  tvl-mcap   TVL / MCap 比
  screen     一次跑完上述四项并给出汇总判定

阈值来源（与 playbook 一致，改阈值请同步改 playbook）：
  解锁冲击比 > 0.3        → 显著抛压信号
  TVL/MCap  < 0.1        → 代币估值相对锁仓过高，脆弱
  真实收益率 <= 0         → 收益全靠代币排放，视为庞氏结构

用法示例：
  python3 scripts/defi_yield_calc.py apy --apr 0.45
  python3 scripts/defi_yield_calc.py real-yield --revenue 1200000 --emissions 900000 --staked-tvl 25000000
  python3 scripts/defi_yield_calc.py unlock --tokens 5000000 --price 1.2 --daily-volume 8000000
  python3 scripts/defi_yield_calc.py tvl-mcap --tvl 40000000 --mcap 500000000
  python3 scripts/defi_yield_calc.py screen --apr 0.45 --revenue 1200000 --emissions 900000 \
      --staked-tvl 25000000 --tokens 5000000 --price 1.2 --daily-volume 8000000 \
      --tvl 40000000 --mcap 500000000 --json
"""

from __future__ import annotations

import argparse
import json
import sys

UNLOCK_PRESSURE_THRESHOLD = 0.3
TVL_MCAP_FRAGILE_THRESHOLD = 0.1


def _positive(value: str) -> float:
    """argparse 类型：必须为正数（金额/价格/成交量不允许 0 或负）。"""
    try:
        num = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"不是合法数字: {value!r}")
    if num <= 0:
        raise argparse.ArgumentTypeError(f"必须为正数: {value}")
    return num


def _non_negative(value: str) -> float:
    try:
        num = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"不是合法数字: {value!r}")
    if num < 0:
        raise argparse.ArgumentTypeError(f"不允许为负: {value}")
    return num


def calc_apy(apr: float, compounds: int) -> dict:
    """APY = (1 + APR/n)^n - 1。n 为每年复利频次。"""
    apy = (1 + apr / compounds) ** compounds - 1
    return {
        "metric": "apy",
        "apr": apr,
        "compounds_per_year": compounds,
        "apy": apy,
        "compounding_gain": apy - apr,
        "note": "横向比较用 APY，但仍需先确认收益来源，再看是否为真实收益。",
    }


def calc_real_yield(revenue: float, emissions: float, staked_tvl: float) -> dict:
    """真实收益率 = (协议收入 - 代币排放价值) / 质押 TVL，均为年化同口径。"""
    net = revenue - emissions
    real_yield = net / staked_tvl
    if net <= 0:
        verdict = "庞氏结构：收益完全由代币排放支撑，排放停止即崩，回避"
    elif real_yield < 0.02:
        verdict = "真实收益极薄（<2%），不足以补偿智能合约与脱锚风险"
    else:
        verdict = "存在真实收益，可进入可持续性评估"
    return {
        "metric": "real_yield",
        "protocol_revenue": revenue,
        "emissions_usd": emissions,
        "net_revenue": net,
        "staked_tvl": staked_tvl,
        "real_yield": real_yield,
        "emission_dependency": emissions / revenue if revenue else None,
        "verdict": verdict,
    }


def calc_unlock(tokens: float, price: float, daily_volume: float) -> dict:
    """解锁冲击比 = 解锁额 / 日均成交量。> 0.3 视为显著抛压信号。"""
    unlock_usd = tokens * price
    ratio = unlock_usd / daily_volume
    if ratio > UNLOCK_PRESSURE_THRESHOLD:
        verdict = f"显著抛压信号（>{UNLOCK_PRESSURE_THRESHOLD}），结论需折价计入"
    else:
        verdict = f"抛压可被流动性吸收（<={UNLOCK_PRESSURE_THRESHOLD}）"
    return {
        "metric": "unlock_impact",
        "unlock_tokens": tokens,
        "price": price,
        "unlock_usd": unlock_usd,
        "daily_volume": daily_volume,
        "ratio": ratio,
        "threshold": UNLOCK_PRESSURE_THRESHOLD,
        "verdict": verdict,
    }


def calc_tvl_mcap(tvl: float, mcap: float) -> dict:
    """TVL / MCap 比。< 0.1 通常意味着代币估值相对锁仓过高。"""
    ratio = tvl / mcap
    if ratio < TVL_MCAP_FRAGILE_THRESHOLD:
        verdict = f"脆弱（<{TVL_MCAP_FRAGILE_THRESHOLD}）：估值相对锁仓过高"
    else:
        verdict = f"锁仓对估值有支撑（>={TVL_MCAP_FRAGILE_THRESHOLD}）"
    return {
        "metric": "tvl_mcap",
        "tvl": tvl,
        "mcap": mcap,
        "ratio": ratio,
        "threshold": TVL_MCAP_FRAGILE_THRESHOLD,
        "verdict": verdict,
    }


def _fmt_pct(x: float) -> str:
    return f"{x * 100:.2f}%"


def render(result: dict) -> str:
    m = result["metric"]
    if m == "apy":
        return (
            f"APR {_fmt_pct(result['apr'])} @ 每年复利 {result['compounds_per_year']} 次\n"
            f"  APY          = {_fmt_pct(result['apy'])}\n"
            f"  复利增益     = {_fmt_pct(result['compounding_gain'])}\n"
            f"  提示: {result['note']}"
        )
    if m == "real_yield":
        dep = result["emission_dependency"]
        dep_s = _fmt_pct(dep) if dep is not None else "n/a"
        return (
            f"协议收入 {result['protocol_revenue']:,.0f} - 排放 {result['emissions_usd']:,.0f}"
            f" = 净收入 {result['net_revenue']:,.0f}\n"
            f"  真实收益率   = {_fmt_pct(result['real_yield'])}"
            f"（质押 TVL {result['staked_tvl']:,.0f}）\n"
            f"  排放依赖度   = {dep_s}\n"
            f"  判定: {result['verdict']}"
        )
    if m == "unlock_impact":
        return (
            f"解锁 {result['unlock_tokens']:,.0f} 枚 × {result['price']:,.4f}"
            f" = {result['unlock_usd']:,.0f} USD\n"
            f"  解锁冲击比   = {result['ratio']:.3f}"
            f"（日均成交 {result['daily_volume']:,.0f}，阈值 {result['threshold']}）\n"
            f"  判定: {result['verdict']}"
        )
    if m == "tvl_mcap":
        return (
            f"TVL {result['tvl']:,.0f} / MCap {result['mcap']:,.0f}\n"
            f"  TVL/MCap     = {result['ratio']:.3f}（阈值 {result['threshold']}）\n"
            f"  判定: {result['verdict']}"
        )
    raise ValueError(f"未知 metric: {m}")


def render_screen(results: list[dict], flags: list[str]) -> str:
    body = "\n\n".join(render(r) for r in results)
    if flags:
        tail = "\n".join(f"  - {f}" for f in flags)
        head = f"\n\n综合判定: {len(flags)} 项风险信号\n{tail}"
    else:
        head = "\n\n综合判定: 四项速算均未触发风险阈值（不构成投资建议）"
    return body + head


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="defi_yield_calc.py",
        description="DeFi 收益与 Tokenomics 确定性速算器（APY / 真实收益率 / 解锁冲击 / TVL-MCap）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "阈值: 解锁冲击比 > 0.3 显著抛压 | TVL/MCap < 0.1 脆弱 | 真实收益率 <= 0 庞氏\n"
            "配套 playbook: references/defi-tokenomics.md、references/onchain-research.md"
        ),
    )
    p.add_argument("--json", action="store_true", help="以 JSON 输出，便于写入报告或二次处理")

    # --json 同时挂到每个子命令上，使其在子命令前后都能生效；
    # SUPPRESS 保证未显式传入时不覆盖主解析器已解析的值（argparse 默认值覆盖陷阱）。
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "--json", action="store_true", default=argparse.SUPPRESS,
        help="以 JSON 输出，便于写入报告或二次处理",
    )

    sub = p.add_subparsers(dest="command", metavar="子命令", parser_class=argparse.ArgumentParser)

    def add(name: str, help_text: str) -> argparse.ArgumentParser:
        return sub.add_parser(name, help=help_text, parents=[common])

    s = add("apy", "APR → APY 复利换算")
    s.add_argument("--apr", type=_positive, required=True, help="年化利率，小数形式（0.45 表示 45%%）")
    s.add_argument("--compounds", type=int, default=365, help="每年复利频次，默认 365（每日）")

    s = add("real-yield", "真实收益率（剔除代币排放）")
    s.add_argument("--revenue", type=_non_negative, required=True, help="年化协议收入 USD")
    s.add_argument("--emissions", type=_non_negative, required=True, help="年化代币排放价值 USD")
    s.add_argument("--staked-tvl", type=_positive, required=True, help="质押 / LP 锁仓 USD")

    s = add("unlock", "解锁冲击比（解锁额 / 日均成交量）")
    s.add_argument("--tokens", type=_positive, required=True, help="本次解锁代币数量")
    s.add_argument("--price", type=_positive, required=True, help="代币价格 USD")
    s.add_argument("--daily-volume", type=_positive, required=True, help="日均成交量 USD")

    s = add("tvl-mcap", "TVL / MCap 比")
    s.add_argument("--tvl", type=_positive, required=True, help="锁仓总值 USD")
    s.add_argument("--mcap", type=_positive, required=True, help="流通市值 USD")

    s = add("screen", "一次跑完四项速算并汇总判定")
    s.add_argument("--apr", type=_positive, required=True)
    s.add_argument("--compounds", type=int, default=365)
    s.add_argument("--revenue", type=_non_negative, required=True)
    s.add_argument("--emissions", type=_non_negative, required=True)
    s.add_argument("--staked-tvl", type=_positive, required=True)
    s.add_argument("--tokens", type=_positive, required=True)
    s.add_argument("--price", type=_positive, required=True)
    s.add_argument("--daily-volume", type=_positive, required=True)
    s.add_argument("--tvl", type=_positive, required=True)
    s.add_argument("--mcap", type=_positive, required=True)
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    if args.command == "apy":
        if args.compounds < 1:
            parser.error("--compounds 必须 >= 1")
        result = calc_apy(args.apr, args.compounds)
    elif args.command == "real-yield":
        result = calc_real_yield(args.revenue, args.emissions, args.staked_tvl)
    elif args.command == "unlock":
        result = calc_unlock(args.tokens, args.price, args.daily_volume)
    elif args.command == "tvl-mcap":
        result = calc_tvl_mcap(args.tvl, args.mcap)
    elif args.command == "screen":
        if args.compounds < 1:
            parser.error("--compounds 必须 >= 1")
        results = [
            calc_apy(args.apr, args.compounds),
            calc_real_yield(args.revenue, args.emissions, args.staked_tvl),
            calc_unlock(args.tokens, args.price, args.daily_volume),
            calc_tvl_mcap(args.tvl, args.mcap),
        ]
        flags = []
        if results[1]["net_revenue"] <= 0:
            flags.append("真实收益率 <= 0：收益全靠排放")
        if results[2]["ratio"] > UNLOCK_PRESSURE_THRESHOLD:
            flags.append(f"解锁冲击比 {results[2]['ratio']:.3f} > {UNLOCK_PRESSURE_THRESHOLD}")
        if results[3]["ratio"] < TVL_MCAP_FRAGILE_THRESHOLD:
            flags.append(f"TVL/MCap {results[3]['ratio']:.3f} < {TVL_MCAP_FRAGILE_THRESHOLD}")
        if args.json:
            print(json.dumps({"metrics": results, "risk_flags": flags}, ensure_ascii=False, indent=2))
        else:
            print(render_screen(results, flags))
        return 1 if flags else 0
    else:  # pragma: no cover - argparse 已拦截
        parser.error(f"未知子命令: {args.command}")
        return 2

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
