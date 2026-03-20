#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Iterable

DEFAULT_EXCLUDED_DIRS = {
    ".git", ".hg", ".svn",
    "node_modules",
    "dist", "build", "out", ".next", ".nuxt",
    ".venv", "venv", "__pycache__",
    ".pytest_cache", ".mypy_cache", ".ruff_cache",
    ".idea", ".vscode",
    "coverage", ".coverage",
}

DEFAULT_EXCLUDED_EXTS = {
    ".log",
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".bmp", ".tiff",
    ".pdf",
    ".zip", ".tar", ".gz", ".bz2", ".xz", ".7z",
    ".mp3", ".mp4", ".mov", ".mkv", ".avi",
    ".exe", ".dll", ".so", ".dylib",
    ".bin", ".dat",
    ".class", ".jar",
    ".pyc", ".pyo",
}

DEFAULT_EXCLUDED_FILES = {
    # common lockfiles / generated files you might not want (customize as desired)
    "project_dumpy.txt",
    "concat_project.py",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
}

SEPARATOR = "\n\n" + ("=" * 80) + "\n\n"


def is_probably_binary(path: Path, sniff_bytes: int = 4096) -> bool:
    """
    Heuristic: if it contains NUL bytes in the first sniff_bytes, treat as binary.
    """
    try:
        with path.open("rb") as f:
            chunk = f.read(sniff_bytes)
        return b"\x00" in chunk
    except Exception:
        # If we can't read it, skip it (treat as binary/unreadable)
        return True


def should_skip(path: Path, root: Path, excluded_dirs: set[str], excluded_exts: set[str], excluded_files: set[str]) -> bool:
    # Skip if any parent dir is excluded
    rel_parts = path.relative_to(root).parts
    if any(part in excluded_dirs for part in rel_parts[:-1]):
        return True

    if path.name in excluded_files:
        return True

    if path.suffix.lower() in excluded_exts:
        return True

    return False


def iter_files(root: Path, excluded_dirs: set[str]) -> Iterable[Path]:
    # Use os.walk so we can prune dirs efficiently
    for dirpath, dirnames, filenames in os.walk(root):
        # prune excluded dirs in-place
        dirnames[:] = [d for d in dirnames if d not in excluded_dirs]
        for name in filenames:
            yield Path(dirpath) / name


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Concatenate a project into one text file: filepath, two newlines, file contents."
    )
    ap.add_argument("--root", default=".", help="Project root to scan (default: .)")
    ap.add_argument("--out", default="project_dump.txt", help="Output file path (default: project_dump.txt)")
    ap.add_argument("--max-bytes", type=int, default=2_000_000, help="Skip files larger than this (default: 2,000,000 bytes)")
    ap.add_argument("--include-hidden", action="store_true", help="Include hidden files/dirs (dotfiles). Default: excluded if directory is excluded.")
    ap.add_argument("--no-skip-binary", action="store_true", help="Do not try to detect/skip binary files.")
    ap.add_argument("--extra-skip-ext", action="append", default=[], help="Extra extension(s) to skip, e.g. --extra-skip-ext .sqlite")
    ap.add_argument("--extra-skip-dir", action="append", default=[], help="Extra dir name(s) to skip, e.g. --extra-skip-dir .cache")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    out_path = Path(args.out).resolve()

    excluded_dirs = set(DEFAULT_EXCLUDED_DIRS) | set(args.extra_skip_dir)
    excluded_exts = set(DEFAULT_EXCLUDED_EXTS) | {e.lower() for e in args.extra_skip_ext}
    excluded_files = set(DEFAULT_EXCLUDED_FILES)

    # If they want hidden files, we won't auto-exclude dot-dirs unless explicitly in excluded_dirs
    # (Most dot-dirs like .git/.venv are already excluded.)
    if not args.include_hidden:
        # Add a generic rule: skip top-level dot-directories (except ones already included)
        # Note: handled by excluded_dirs only, so add nothing here; user can add exclusions as needed.
        pass

    count_included = 0
    count_skipped = 0

    with out_path.open("w", encoding="utf-8", newline="\n") as out:
        out.write(f"# Project dump\n# Root: {root}\n\n")

        for path in iter_files(root, excluded_dirs):
            # Skip output file itself if it lives under root
            if path.resolve() == out_path:
                continue

            # Optional: skip hidden files unless include_hidden is set
            if not args.include_hidden:
                rel_parts = path.relative_to(root).parts
                if any(p.startswith(".") for p in rel_parts):
                    # still allow files like .env if you want? change this rule if desired
                    # If you *do* want .env by default, comment this block out.
                    count_skipped += 1
                    continue

            if should_skip(path, root, excluded_dirs, excluded_exts, excluded_files):
                count_skipped += 1
                continue

            try:
                st = path.stat()
                if st.st_size > args.max_bytes:
                    count_skipped += 1
                    continue
            except Exception:
                count_skipped += 1
                continue

            if not args.no_skip_binary and is_probably_binary(path):
                count_skipped += 1
                continue

            rel = path.relative_to(root).as_posix()
            out.write(rel)
            out.write("\n\n")  # two newlines as requested

            # Read as text with replacement for weird encodings
            try:
                data = path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                count_skipped += 1
                continue

            out.write(data)
            out.write(SEPARATOR)
            count_included += 1

        out.write(f"\n# Included files: {count_included}\n# Skipped files: {count_skipped}\n")

    print(f"Wrote: {out_path}")
    print(f"Included files: {count_included}")
    print(f"Skipped files:  {count_skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())