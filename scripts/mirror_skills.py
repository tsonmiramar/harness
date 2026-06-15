#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

MODES = ("copy", "symlink")
LAYOUTS = ("cursor",)


def build_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(
    description=(
      "Mirror project skills from .agents/skills/ into a native client skills "
      "directory for discovery."
    )
  )
  parser.add_argument("--target", required=True, help="Project root to mirror into")
  parser.add_argument("--layout", choices=LAYOUTS, default="cursor")
  parser.add_argument("--mode", choices=MODES, default="symlink")
  parser.add_argument(
    "--skill",
    action="append",
    help="Mirror only this skill name. Repeat to mirror multiple skills.",
  )
  parser.add_argument(
    "--dry-run",
    action="store_true",
    help="Print the mirror plan without modifying destination paths.",
  )
  parser.add_argument(
    "--force",
    action="store_true",
    help="Replace existing destination skill paths.",
  )
  return parser


def fail(message: str) -> int:
  print(f"ERROR: {message}", file=sys.stderr)
  return 1


def native_skills_root(root: Path, layout: str) -> Path:
  if layout == "cursor":
    return root / ".cursor" / "skills"
  raise ValueError(f"Unsupported layout: {layout}")


def remove_path(path: Path) -> None:
  if path.is_symlink() or path.is_file():
    path.unlink()
  elif path.exists():
    shutil.rmtree(path)


def mirror_destination(source: Path, destination: Path, mode: str) -> None:
  destination.parent.mkdir(parents=True, exist_ok=True)
  if mode == "copy":
    shutil.copytree(
      source,
      destination,
      ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    return

  destination.symlink_to(source, target_is_directory=True)


def discover_sources(shared_root: Path, only: list[str] | None) -> list[Path]:
  if not shared_root.exists():
    return []

  sources = sorted(path for path in shared_root.iterdir() if path.is_dir())
  if only is None:
    return sources

  wanted = set(only)
  return [path for path in sources if path.name in wanted]


def main() -> int:
  parser = build_parser()
  args = parser.parse_args()

  root = Path(args.target).expanduser().resolve()
  if not root.exists() or not root.is_dir():
    return fail(f"Project target is not a directory: {root}")

  shared_root = root / ".agents" / "skills"
  if not shared_root.exists():
    return fail(f"Missing shared skills directory: {shared_root}")

  native_root = native_skills_root(root, args.layout)
  sources = discover_sources(shared_root, args.skill)
  if not sources:
    return fail(f"No skills found to mirror under {shared_root}")

  destinations: list[tuple[Path, Path]] = [
    (source, native_root / source.name) for source in sources
  ]

  if args.dry_run:
    print(f"Dry run: mirror skills using {args.mode} mode with {args.layout} layout.")
    for source, destination in destinations:
      state = "exists" if destination.exists() or destination.is_symlink() else "missing"
      print(f"- {source.name}: {source} -> {destination} [{state}]")
    print("Dry run only; no changes made.")
    return 0

  existing = [
    destination
    for _, destination in destinations
    if destination.exists() or destination.is_symlink()
  ]
  if existing and not args.force:
    joined = ", ".join(str(path) for path in existing)
    return fail(f"Destination already exists; rerun with --force to replace: {joined}")

  if args.force:
    for destination in existing:
      remove_path(destination)

  for source, destination in destinations:
    mirror_destination(source, destination, args.mode)

  print(f"Mirrored {len(destinations)} skill(s) using {args.mode} mode with {args.layout} layout.")
  for source, destination in destinations:
    print(f"- {source.name}: {destination}")

  return 0


if __name__ == "__main__":
  raise SystemExit(main())
