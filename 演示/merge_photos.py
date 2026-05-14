from __future__ import annotations

import argparse
from math import ceil
from pathlib import Path

from PIL import Image, ImageOps


IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="将文件夹中的图片合成为一张合照")
    parser.add_argument("input_dir", help="包含图片的文件夹路径")
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="输出文件路径，默认输出到输入目录同级目录下",
    )
    parser.add_argument("--cols", type=int, default=5, help="每行图片数量，默认 5")
    parser.add_argument("--thumb-width", type=int, default=260, help="单张缩略图宽度")
    parser.add_argument("--thumb-height", type=int, default=320, help="单张缩略图高度")
    return parser.parse_args()


def collect_images(input_dir: Path) -> list[Path]:
    if not input_dir.exists() or not input_dir.is_dir():
        raise FileNotFoundError(f"输入文件夹不存在: {input_dir}")

    images = sorted(
        path
        for path in input_dir.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
    )
    if not images:
        raise ValueError(f"文件夹中未找到可用图片: {input_dir}")
    return images


def build_output_path(input_dir: Path, output: str | None) -> Path:
    if output:
        return Path(output)
    return input_dir.parent / f"{input_dir.name}_group_photo.jpg"


def merge_photos(
    image_paths: list[Path],
    output_path: Path,
    cols: int,
    thumb_width: int,
    thumb_height: int,
) -> Path:
    cols = max(cols, 1)
    gap = 24
    margin = 40
    label_height = 36
    rows = ceil(len(image_paths) / cols)

    canvas_width = margin * 2 + cols * thumb_width + (cols - 1) * gap
    canvas_height = margin * 2 + rows * (thumb_height + label_height) + (rows - 1) * gap
    canvas = Image.new("RGB", (canvas_width, canvas_height), (245, 240, 232))

    for index, image_path in enumerate(image_paths):
        row = index // cols
        col = index % cols
        x = margin + col * (thumb_width + gap)
        y = margin + row * (thumb_height + label_height + gap)

        image = Image.open(image_path).convert("RGB")
        fitted = ImageOps.fit(
            image,
            (thumb_width, thumb_height),
            method=Image.Resampling.LANCZOS,
            centering=(0.5, 0.35),
        )
        framed = ImageOps.expand(fitted, border=4, fill=(255, 255, 255))
        canvas.paste(framed, (x, y))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output_path, quality=95)
    return output_path


def main() -> None:
    args = parse_args()
    input_dir = Path(args.input_dir).resolve()
    image_paths = collect_images(input_dir)
    output_path = build_output_path(input_dir, args.output).resolve()
    result = merge_photos(
        image_paths=image_paths,
        output_path=output_path,
        cols=args.cols,
        thumb_width=args.thumb_width,
        thumb_height=args.thumb_height,
    )
    print(result)


if __name__ == "__main__":
    main()
