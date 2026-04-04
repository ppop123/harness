#!/usr/bin/env python3
"""Build the thin harness-init skill bundle from repo source."""

from __future__ import annotations

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "skills" / "harness-init"
DEFAULT_OUTPUT = ROOT / "harness-init.skill"
ARCHIVE_ROOT = "harness-init/"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output .skill path (default: %(default)s)",
    )
    return parser.parse_args()


def add_directory_entry(archive: ZipFile, name: str) -> None:
    info = ZipInfo(name)
    archive.writestr(info, "")


def main() -> int:
    args = parse_args()
    output_path = args.output.resolve()

    if not SOURCE_DIR.exists():
        raise SystemExit(f"Missing skill source directory: {SOURCE_DIR}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with ZipFile(output_path, "w", compression=ZIP_DEFLATED) as archive:
        add_directory_entry(archive, ARCHIVE_ROOT)
        for path in sorted(SOURCE_DIR.rglob("*")):
            if path.is_file():
                archive.write(path, ARCHIVE_ROOT + path.relative_to(SOURCE_DIR).as_posix())

    print(f"Built {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
