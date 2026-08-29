#!/usr/bin/env python3
"""把逐頁 PNG 組成數張可人工檢視的聯絡表。"""

from __future__ import annotations

import argparse
import math
import re
from pathlib import Path

from PIL import Image, ImageDraw


def natural_key(path: Path) -> list[object]:
    return [int(part) if part.isdigit() else part for part in re.split(r"(\d+)", path.name)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("output_stem", type=Path)
    parser.add_argument("--columns", type=int, default=4)
    parser.add_argument("--pages-per-sheet", type=int, default=8)
    parser.add_argument("--thumb-width", type=int, default=340)
    args = parser.parse_args()

    pages = sorted(args.input_dir.glob("*.png"), key=natural_key)
    if not pages:
        raise SystemExit(f"找不到 PNG：{args.input_dir}")

    args.output_stem.parent.mkdir(parents=True, exist_ok=True)
    label_height = 26
    gap = 14
    border = 12

    for sheet_index, start in enumerate(range(0, len(pages), args.pages_per_sheet), start=1):
        batch = pages[start : start + args.pages_per_sheet]
        opened = [Image.open(path).convert("RGB") for path in batch]
        thumb_height = round(args.thumb_width * opened[0].height / opened[0].width)
        rows = math.ceil(len(batch) / args.columns)
        width = border * 2 + args.columns * args.thumb_width + (args.columns - 1) * gap
        height = border * 2 + rows * (thumb_height + label_height) + (rows - 1) * gap
        sheet = Image.new("RGB", (width, height), "#d8dde5")
        draw = ImageDraw.Draw(sheet)

        for index, (path, page) in enumerate(zip(batch, opened)):
            row, column = divmod(index, args.columns)
            x = border + column * (args.thumb_width + gap)
            y = border + row * (thumb_height + label_height + gap)
            page.thumbnail((args.thumb_width, thumb_height), Image.Resampling.LANCZOS)
            canvas = Image.new("RGB", (args.thumb_width, thumb_height), "white")
            canvas.paste(page, ((args.thumb_width - page.width) // 2, 0))
            sheet.paste(canvas, (x, y))
            draw.rectangle((x, y + thumb_height, x + args.thumb_width, y + thumb_height + label_height), fill="white")
            draw.text((x + 8, y + thumb_height + 6), path.stem, fill="#26364a")

        output = args.output_stem.with_name(f"{args.output_stem.name}-{sheet_index:02d}.png")
        sheet.save(output, optimize=True)
        print(output)


if __name__ == "__main__":
    main()
