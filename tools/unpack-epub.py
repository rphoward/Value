#!/usr/bin/env python3
"""Unpack a DRM-free EPUB into workproduct for agent reading (HTML + images)."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "workproduct" / "epub-extract"


def safe_name(part: str) -> str:
    part = part.replace("\\", "/").lstrip("/")
    part = re.sub(r"[^a-zA-Z0-9._/\-]+", "_", part)
    return part or "unnamed"


def unpack(epub_path: Path, out_dir: Path) -> dict[str, int]:
    if not epub_path.is_file():
        raise FileNotFoundError(f"EPUB not found: {epub_path}")
    if epub_path.suffix.lower() != ".epub":
        raise ValueError(f"Expected .epub, got: {epub_path.name}")

    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    counts = {"files": 0, "html": 0, "images": 0, "other": 0}
    image_ext = {".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp"}

    with zipfile.ZipFile(epub_path) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            target = out_dir / safe_name(info.filename)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(zf.read(info.filename))
            counts["files"] += 1
            ext = target.suffix.lower()
            if ext in {".xhtml", ".html", ".htm"}:
                counts["html"] += 1
            elif ext in image_ext:
                counts["images"] += 1
            else:
                counts["other"] += 1

    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("epub", type=Path, help="Path to .epub file")
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help=f"Output directory (default: {DEFAULT_OUT}/<epub-stem>)",
    )
    args = parser.parse_args()

    epub = args.epub.resolve()
    out = args.out or (DEFAULT_OUT / epub.stem)
    out = out.resolve()

    try:
        counts = unpack(epub, out)
    except (FileNotFoundError, ValueError, zipfile.BadZipFile) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"unpacked: {epub}")
    print(f"output:   {out}")
    print(
        "counts:   "
        f"{counts['files']} files, "
        f"{counts['html']} html, "
        f"{counts['images']} images, "
        f"{counts['other']} other"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
