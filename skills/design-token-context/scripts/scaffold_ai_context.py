#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scaffold a reusable .ai-context folder into a target repository."
    )
    parser.add_argument(
        "--target",
        default=".",
        help="Target repository path. Defaults to current directory.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files in .ai-context.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    skill_dir = Path(__file__).resolve().parent.parent
    source_dir = skill_dir / "assets" / "ai-context"
    target_repo = Path(args.target).resolve()
    target_dir = target_repo / ".ai-context"

    if not source_dir.exists():
        print(f"Missing source scaffold: {source_dir}", file=sys.stderr)
        return 1

    target_dir.mkdir(parents=True, exist_ok=True)
    copied = []
    skipped = []

    for source_file in sorted(source_dir.iterdir()):
        if not source_file.is_file():
            continue

        target_file = target_dir / source_file.name
        if target_file.exists() and not args.force:
            skipped.append(target_file.name)
            continue

        shutil.copy2(source_file, target_file)
        copied.append(target_file.name)

    print(f"Target: {target_dir}")
    print(f"Copied: {', '.join(copied) if copied else '(none)'}")
    print(f"Skipped: {', '.join(skipped) if skipped else '(none)'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
