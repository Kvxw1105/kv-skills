#!/usr/bin/env python3
"""Lightweight heuristic QA for Chinese high-pressure awakening copy."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


DANGEROUS_PATTERNS = {
    "sleep_deprivation": [r"不需要睡", r"牺牲睡眠", r"睡眠.*弱者", r"永远不休息"],
    "injury_glorification": [r"练到.*流血", r"受伤.*继续", r"身体.*叫停.*不?停"],
    "mental_health_dismissal": [r"心理健康.*屁话", r"抑郁.*软弱", r"焦虑.*借口"],
}

FORMULA_PATTERNS = {
    "not_but": r"你不是.{0,30}而是",
    "true_is": r"真正的.{0,20}是",
    "act_now": r"现在就行动",
}

SIGNALS = {
    "hope": ["还有时间", "门还没有关", "仍然可以", "还来得及", "仍有机会"],
    "action": ["完成", "打开", "提交", "发布", "投递", "训练", "做完", "留下证据"],
    "identity": ["成为", "训练谁", "身份", "替你作决定的人", "怎样的人"],
    "future_cost": ["一年后", "六十岁", "未来", "失去", "选择越来越少", "心气"],
}


def count_matches(text: str, patterns: list[str]) -> int:
    return sum(len(re.findall(pattern, text)) for pattern in patterns)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    text = args.path.read_text(encoding="utf-8")
    problems: list[str] = []

    for label, patterns in DANGEROUS_PATTERNS.items():
        count = count_matches(text, patterns)
        if count:
            problems.append(f"danger:{label}={count}")

    for label, pattern in FORMULA_PATTERNS.items():
        count = len(re.findall(pattern, text))
        if count > 2:
            problems.append(f"formula_overuse:{label}={count}")

    for label, terms in SIGNALS.items():
        if not any(term in text for term in terms):
            problems.append(f"missing_signal:{label}")

    print(f"characters={len(text)}")
    if problems:
        print("status=review")
        for problem in problems:
            print(problem)
        return 1

    print("status=pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
