#!/usr/bin/env python3

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CODEX_VALIDATOR = ROOT / "scripts" / "validate_codex_port.py"

CURSOR_REQUIRED_FILES = [
  ROOT / "docs/compatibility/cursor.md",
  ROOT / ".agents/skills/harness/references/cursor-orchestration.md",
  ROOT / "scripts/mirror_skills.py",
  ROOT / "scripts/validate_cursor_port.py",
]

CURSOR_DOC_EXPECTATIONS = {
  "docs/compatibility/cursor.md": [
    ".agents/skills/harness/",
    "~/.agents/skills/harness/",
    ".cursor/skills/harness/",
    "~/.cursor/skills/harness/",
    "python3 scripts/install_harness.py --scope project --target /path/to/repo --layout cursor",
    "python3 scripts/mirror_skills.py --target /path/to/repo --layout cursor",
    "user-invocable: true",
    "disable-model-invocation: true",
    "cursor-orchestration.md",
  ],
  ".agents/skills/harness/references/cursor-orchestration.md": [
    "fan-out/fan-in",
    "subagent_type",
    "mirror_skills.py",
    "user-invocable: true",
    "disable-model-invocation: true",
  ],
}

MAIN_SKILL_CURSOR_TOKENS = [
  "references/cursor-orchestration.md",
  "phase 0:",
  ".cursor/skills/",
  ".cursor/rules/",
  "mirror_skills.py",
]


def fail(message: str, failures: list[str]) -> None:
  failures.append(message)


def read_text(path: Path) -> str:
  return path.read_text(encoding="utf-8")


def check_required_files(failures: list[str]) -> None:
  for path in CURSOR_REQUIRED_FILES:
    if not path.exists():
      fail(f"Missing required Cursor file: {path.relative_to(ROOT)}", failures)


def check_cursor_docs(failures: list[str]) -> None:
  for relative_path, required_tokens in CURSOR_DOC_EXPECTATIONS.items():
    text = read_text(ROOT / relative_path)
    for token in required_tokens:
      if token not in text:
        fail(f"{relative_path} is missing required Cursor guidance: {token}", failures)


def check_main_skill_cursor_guidance(failures: list[str]) -> None:
  path = ROOT / ".agents/skills/harness/SKILL.md"
  text = read_text(path).casefold()
  for token in MAIN_SKILL_CURSOR_TOKENS:
    if token not in text:
      fail(f"Main skill is missing Cursor guidance token: {token}", failures)


def check_installer_layout(failures: list[str]) -> None:
  installer_text = read_text(ROOT / "scripts/install_harness.py")
  if '"cursor"' not in installer_text:
    fail("Installer is missing cursor layout support", failures)


def run_codex_validator(failures: list[str]) -> None:
  result = subprocess.run(
    [sys.executable, str(CODEX_VALIDATOR)],
    cwd=ROOT,
    text=True,
    capture_output=True,
    check=False,
  )
  if result.returncode != 0:
    fail("Base validator failed: scripts/validate_codex_port.py", failures)
    if result.stdout.strip():
      failures.append(result.stdout.strip())
    if result.stderr.strip():
      failures.append(result.stderr.strip())


def main() -> int:
  failures: list[str] = []
  check_required_files(failures)
  if not failures:
    check_cursor_docs(failures)
    check_main_skill_cursor_guidance(failures)
    check_installer_layout(failures)
    run_codex_validator(failures)

  if failures:
    for failure in failures:
      print(f"FAIL: {failure}")
    return 1

  print("OK: Cursor layout validation passed.")
  return 0


if __name__ == "__main__":
  sys.exit(main())
