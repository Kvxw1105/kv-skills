#!/usr/bin/env python3
"""Split a UTF-8 prompt into paragraph-aware packets under a character budget."""

from __future__ import annotations

import argparse
from pathlib import Path


def split_long_block(block: str, limit: int) -> list[str]:
    parts: list[str] = []
    remaining = block.strip()
    punctuation = "。！？；\n"
    while len(remaining) > limit:
        cut = max(remaining.rfind(ch, 0, limit + 1) for ch in punctuation)
        if cut < max(1, int(limit * 0.55)):
            cut = limit
        else:
            cut += 1
        parts.append(remaining[:cut].strip())
        remaining = remaining[cut:].strip()
    if remaining:
        parts.append(remaining)
    return parts


def pack(text: str, limit: int) -> list[str]:
    if limit < 200:
        raise ValueError("limit must be at least 200 characters")

    raw_blocks = [block.strip() for block in text.replace("\r\n", "\n").split("\n\n") if block.strip()]
    blocks: list[str] = []
    for block in raw_blocks:
        blocks.extend(split_long_block(block, limit))

    packets: list[str] = []
    current = ""
    for block in blocks:
        candidate = block if not current else f"{current}\n\n{block}"
        if len(candidate) <= limit:
            current = candidate
        else:
            if current:
                packets.append(current)
            current = block
    if current:
        packets.append(current)
    return packets


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="UTF-8 text or Markdown file")
    parser.add_argument("--limit", type=int, default=1200, help="maximum characters per packet")
    parser.add_argument("--output-dir", type=Path, required=True, help="directory for packet files")
    args = parser.parse_args()

    if not args.input.is_file():
        parser.error(f"input file not found: {args.input}")

    text = args.input.read_text(encoding="utf-8")
    packets = pack(text, args.limit)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    for index, packet in enumerate(packets, start=1):
        header = f"【提示词分包 {index}/{len(packets)}】\n"
        (args.output_dir / f"packet-{index:02d}.txt").write_text(header + packet + "\n", encoding="utf-8")

    print(f"created {len(packets)} packet(s) in {args.output_dir}")


if __name__ == "__main__":
    main()
