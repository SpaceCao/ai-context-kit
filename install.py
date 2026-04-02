#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


SKILL_NAME = "design-token-context"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install the AI Context Kit Codex skill and optionally scaffold a target repository."
    )
    parser.add_argument(
        "--skill-home",
        help="Skill install directory. Defaults to $CODEX_HOME/skills or ~/.codex/skills.",
    )
    parser.add_argument(
        "--target",
        help="Optional target repository path to scaffold .ai-context into after installation.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing installed skill and existing .ai-context files in the target repository.",
    )
    return parser.parse_args()


def default_skill_home() -> Path:
    codex_home = Path.home() / ".codex"
    if "CODEX_HOME" in os.environ:
        codex_home = Path(os.environ["CODEX_HOME"])
    return codex_home / "skills"


def copy_skill(source: Path, destination: Path, force: bool) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)

    if destination.exists():
        if not force:
            raise FileExistsError(
                f"Skill already exists at {destination}. Re-run with --force to overwrite."
            )
        shutil.rmtree(destination)

    shutil.copytree(source, destination)


def scaffold_target(skill_dir: Path, target: Path, force: bool) -> None:
    script = skill_dir / "scripts" / "scaffold_ai_context.py"
    command = [sys.executable, str(script), "--target", str(target)]
    if force:
        command.append("--force")
    subprocess.run(command, check=True)


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    skill_source = repo_root / "skills" / SKILL_NAME
    skill_home = Path(args.skill_home).expanduser().resolve() if args.skill_home else default_skill_home()
    skill_destination = skill_home / SKILL_NAME

    if not skill_source.exists():
        print(f"Missing skill source: {skill_source}", file=sys.stderr)
        return 1

    try:
        copy_skill(skill_source, skill_destination, args.force)
    except FileExistsError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"Installed skill: {skill_destination}")

    if args.target:
        target_path = Path(args.target).expanduser().resolve()
        scaffold_target(skill_destination, target_path, args.force)
        print(f"Scaffolded .ai-context into: {target_path}")

    print()
    print("Next steps:")
    print(f"1. Use the installed skill from: {skill_destination}")
    print("2. Or initialize a repository with one of the following:")
    print(f"   - python3 {Path(__file__).name} --target /path/to/repo")
    print("   - bash bootstrap.sh /path/to/repo")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
