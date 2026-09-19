#!/usr/bin/env python3
"""Zip a digital download folder with a customer-facing README."""

from __future__ import annotations

import argparse
import shutil
import tempfile
import zipfile
from datetime import date
from pathlib import Path

SKIP_NAMES = {".ds_store", "thumbs.db", ".git", ".gitignore", "__macosx"}


def should_skip(path: Path) -> bool:
    return path.name.lower() in SKIP_NAMES or path.name.startswith(".")


def default_readme(product_name: str) -> str:
    return (
        f"{product_name}\n"
        f"{'=' * len(product_name)}\n\n"
        "Thanks for your purchase.\n\n"
        "What's inside\n"
        "-------------\n"
        "- Your digital files (see folders in this ZIP)\n"
        "- This README\n\n"
        "Getting started\n"
        "---------------\n"
        "1. Unzip this archive to a folder on your computer.\n"
        "2. Open the main file or template that matches your use case.\n"
        "3. Keep a backup copy of the original ZIP.\n\n"
        "Support\n"
        "-------\n"
        "If a file is missing or won't open, reply to your purchase receipt\n"
        "or contact the seller with your order email.\n\n"
        f"Packed on: {date.today().isoformat()}\n"
    )


def copy_tree(src: Path, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    for item in src.rglob("*"):
        rel = item.relative_to(src)
        if any(should_skip(part) for part in rel.parts):
            continue
        target = dest / rel
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif item.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)


def make_zip(folder: Path, zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for item in sorted(folder.rglob("*")):
            if item.is_file():
                zf.write(item, arcname=str(item.relative_to(folder)))


def pack(source: Path, name: str, out_dir: Path, readme_path: Path | None) -> Path:
    if not source.is_dir():
        raise SystemExit(f"Source folder not found: {source}")

    out_dir.mkdir(parents=True, exist_ok=True)
    zip_path = out_dir / f"{name}.zip"

    with tempfile.TemporaryDirectory(prefix="zip-packer-") as tmp:
        build = Path(tmp) / name
        copy_tree(source, build)

        readme_text = (
            readme_path.read_text(encoding="utf-8")
            if readme_path
            else default_readme(name)
        )
        (build / "README.txt").write_text(readme_text, encoding="utf-8")

        if zip_path.exists():
            zip_path.unlink()
        make_zip(build, zip_path)

    return zip_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Pack a digital download ZIP with README")
    parser.add_argument("source", type=Path, help="Folder of product files to pack")
    parser.add_argument("--name", required=True, help="Product / ZIP base name")
    parser.add_argument("--out", type=Path, default=Path("dist"), help="Output directory")
    parser.add_argument("--readme", type=Path, default=None, help="Optional README template path")
    args = parser.parse_args()

    result = pack(args.source, args.name, args.out, args.readme)
    print(f"Created {result}")


if __name__ == "__main__":
    main()
