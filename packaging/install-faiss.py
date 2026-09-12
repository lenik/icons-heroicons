#!/usr/bin/env python3
# Copyright (C) 2026 Lenik <lenik@bodz.net>
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Meson install helper: copy/decompress faiss* into pkgdatadir."""

from __future__ import annotations

import lzma
import os
import re
import sys
from pathlib import Path

_SHARD = re.compile(r"^faiss(?:\.\d+)?(?:\.(?:map|json))?$")


def _dest_root(pkgdatadir: str) -> Path:
    destdir = os.environ.get("DESTDIR", "")
    prefix = os.environ.get("MESON_INSTALL_PREFIX") or os.environ.get(
        "MESON_INSTALL_DESTDIR_PREFIX", ""
    )
    target = Path(pkgdatadir)
    if target.is_absolute():
        if destdir:
            # DESTDIR + absolute path (strip leading /)
            return Path(destdir) / str(target).lstrip("/")
        if prefix and str(target).startswith(str(Path(prefix))):
            return target
        # MESON_INSTALL_DESTDIR_PREFIX already includes DESTDIR+prefix
        mid = os.environ.get("MESON_INSTALL_DESTDIR_PREFIX")
        if mid:
            # pkgdatadir like /usr/share/icons-foo → replace prefix
            pref = os.environ.get("MESON_INSTALL_PREFIX", "/usr")
            rel = str(target).removeprefix(pref).lstrip("/")
            return Path(mid) / rel
        return target
    mid = Path(os.environ.get("MESON_INSTALL_DESTDIR_PREFIX", "/usr"))
    return mid / target


def _install_one(src: Path, dest_dir: Path) -> None:
    name = src.name
    if name.endswith(".xz"):
        out_name = name[: -len(".xz")]
        out = dest_dir / out_name
        out.parent.mkdir(parents=True, exist_ok=True)
        with lzma.open(src, "rb") as fh:
            out.write_bytes(fh.read())
        return
    dest = dest_dir / name
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(src.read_bytes())


def main() -> int:
    if len(sys.argv) < 3:
        print(
            f"usage: {sys.argv[0]} SOURCE_ROOT PKGDATADIR",
            file=sys.stderr,
        )
        return 2
    src_root = Path(sys.argv[1])
    dest_dir = _dest_root(sys.argv[2])
    dest_dir.mkdir(parents=True, exist_ok=True)
    installed = 0
    for child in sorted(src_root.iterdir()):
        name = child.name
        if name.endswith(".xz"):
            base = name[: -len(".xz")]
        else:
            base = name
        if not _SHARD.match(base):
            continue
        if not child.is_file():
            continue
        # Prefer .xz when both exist
        if not name.endswith(".xz"):
            if (src_root / f"{name}.xz").is_file():
                continue
        _install_one(child, dest_dir)
        installed += 1
    print(f"install-faiss: {installed} file(s) → {dest_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
