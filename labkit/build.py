#!/usr/bin/env python3
"""Build and validate the deterministic learner LabKit archive."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import sys
import tempfile
import zipfile
import urllib.request


ROOT = Path(__file__).resolve().parent.parent
KIT_ROOT = ROOT / "labkit"
APK_DIR = KIT_ROOT / "input" / "apk"
PINNED_MANIFEST = KIT_ROOT / "manifest.sha256"
README = KIT_ROOT / "README.md"
ARCHIVE_PREFIX = "LabKit/"
OUTPUT_MANIFEST = "LabKit/manifest.sha256"
DEFAULT_OUTPUT = ROOT / "docs" / "assets" / "labkit" / "LabKit-linux-x86_64.zip"
VENDOR_MANIFEST = KIT_ROOT / "vendor-manifest.json"


class LabKitError(Exception):
    """Raised when a source tree or archive violates the LabKit contract."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pinned_apks() -> dict[str, str]:
    if not PINNED_MANIFEST.is_file():
        raise LabKitError(f"Missing pinned APK manifest: {PINNED_MANIFEST}")

    expected: dict[str, str] = {}
    for line_number, line in enumerate(PINNED_MANIFEST.read_text().splitlines(), 1):
        if not line.strip():
            continue
        try:
            digest, filename = line.split("  ", 1)
        except ValueError as error:
            raise LabKitError(f"Invalid manifest line {line_number}") from error
        if len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest):
            raise LabKitError(f"Invalid SHA-256 on manifest line {line_number}")
        if Path(filename).name != filename or filename in expected:
            raise LabKitError(f"Invalid or duplicate APK path on manifest line {line_number}")
        expected[filename] = digest

    if not expected:
        raise LabKitError("Pinned APK manifest is empty")
    actual_names = {path.name for path in APK_DIR.iterdir() if path.is_file()} if APK_DIR.is_dir() else set()
    if actual_names != set(expected):
        missing = sorted(set(expected) - actual_names)
        extra = sorted(actual_names - set(expected))
        raise LabKitError(f"APK input set differs from manifest (missing={missing}, extra={extra})")
    for filename, digest in expected.items():
        path = APK_DIR / filename
        if path.is_symlink() or sha256_file(path) != digest:
            raise LabKitError(f"APK hash mismatch: {filename}")
    return expected


def source_files() -> dict[str, Path]:
    if not README.is_file() or README.is_symlink():
        raise LabKitError("Missing or unsafe labkit/README.md")
    files = {"README.md": README}
    for filename in pinned_apks():
        files[f"apk/{filename}"] = APK_DIR / filename

    for root_file in ("setup.sh", "install-apk.sh"):
        path = KIT_ROOT / root_file
        if path.exists():
            if not path.is_file() or path.is_symlink():
                raise LabKitError(f"labkit/{root_file} must be a regular file")
            files[root_file] = path

    payload = KIT_ROOT / "payload"
    if payload.exists():
        if not payload.is_dir() or payload.is_symlink():
            raise LabKitError("labkit/payload must be a regular directory")
        for directory, dirnames, filenames in os.walk(payload, followlinks=False):
            current = Path(directory)
            for dirname in dirnames:
                candidate = current / dirname
                if candidate.is_symlink():
                    raise LabKitError(f"Symlink is not allowed in payload: {candidate}")
            for filename in filenames:
                path = current / filename
                if path.is_symlink() or not path.is_file():
                    raise LabKitError(f"Payload entries must be regular files: {path}")
                relative = path.relative_to(payload).as_posix()
                if not is_safe_member(f"{ARCHIVE_PREFIX}{relative}"):
                    raise LabKitError(f"Unsafe payload path: {relative}")
                if relative in files:
                    raise LabKitError(f"Duplicate LabKit source path: {relative}")
                files[relative] = path

    if VENDOR_MANIFEST.parent == KIT_ROOT:
        for member, asset in json.loads(VENDOR_MANIFEST.read_text()).items():
            if not is_safe_member(f"{ARCHIVE_PREFIX}{member}") or member in files:
                raise LabKitError(f"Unsafe or duplicate vendored asset: {member}")
            cached = KIT_ROOT / "vendor" / Path(member).name
            if not cached.is_file() or cached.is_symlink() or sha256_file(cached) != asset["sha256"]:
                raise LabKitError(f"Missing or unverified {member}; run python3 labkit/build.py --fetch-vendor")
            files[member] = cached
    return files


def fetch_vendor() -> None:
    """Fetch release bytes once at build time; never accept an unverified cache."""
    cache = KIT_ROOT / "vendor"
    cache.mkdir(exist_ok=True)
    for member, asset in json.loads(VENDOR_MANIFEST.read_text()).items():
        destination = cache / Path(member).name
        if destination.exists():
            if destination.is_symlink() or sha256_file(destination) != asset["sha256"]:
                raise LabKitError(f"Unverified cache left untouched: {destination}")
        else:
            with tempfile.NamedTemporaryFile(dir=cache, prefix=destination.name + ".part-", delete=False) as output:
                temporary = Path(output.name)
            try:
                with urllib.request.urlopen(asset["url"], timeout=120) as source, temporary.open("wb") as output:
                    while chunk := source.read(1024 * 1024):
                        output.write(chunk)
                if sha256_file(temporary) != asset["sha256"]:
                    raise LabKitError(f"Vendored download failed SHA-256: {member}")
                temporary.rename(destination)
            finally:
                temporary.unlink(missing_ok=True)
        destination.chmod(0o755 if asset.get("executable") else 0o644)
        print(f"Verified vendored asset: {member}")


def is_safe_member(name: str) -> bool:
    if not name or "\\" in name or "\x00" in name:
        return False
    path = PurePosixPath(name)
    return (
        not path.is_absolute()
        and all(part not in ("", ".", "..") for part in path.parts)
        and path.parts[0] == "LabKit"
        and len(path.parts) > 1
    )


def expected_contents(files: dict[str, Path]) -> dict[str, bytes]:
    contents = {f"{ARCHIVE_PREFIX}{name}": path.read_bytes() for name, path in files.items()}
    manifest = "".join(
        f"{hashlib.sha256(contents[name]).hexdigest()}  {name.removeprefix(ARCHIVE_PREFIX)}\n"
        for name in sorted(contents)
    )
    contents[OUTPUT_MANIFEST] = manifest.encode()
    return contents


def validate_archive(archive_path: Path, expected: dict[str, bytes]) -> None:
    try:
        with zipfile.ZipFile(archive_path) as archive:
            infos = archive.infolist()
            names = [info.filename for info in infos]
            if len(names) != len(set(names)):
                raise LabKitError("Archive contains duplicate members")
            for info in infos:
                if not is_safe_member(info.filename) or info.is_dir():
                    raise LabKitError(f"Unsafe archive member: {info.filename!r}")
                mode = info.external_attr >> 16
                if stat.S_ISLNK(mode):
                    raise LabKitError(f"Archive contains a symbolic link: {info.filename}")
            if set(names) != set(expected):
                missing = sorted(set(expected) - set(names))
                extra = sorted(set(names) - set(expected))
                raise LabKitError(f"Archive member set mismatch (missing={missing}, extra={extra})")
            for name, content in expected.items():
                if archive.read(name) != content:
                    raise LabKitError(f"Archive content mismatch: {name}")
    except (OSError, zipfile.BadZipFile, RuntimeError) as error:
        raise LabKitError(f"Cannot read archive: {error}") from error


def build(output: Path) -> None:
    files = source_files()
    expected = expected_contents(files)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in sorted(expected):
            if name == OUTPUT_MANIFEST:
                source_mode = 0o100644
            else:
                source = files[name.removeprefix(ARCHIVE_PREFIX)]
                permissions = 0o755 if source.stat().st_mode & 0o111 else 0o644
                source_mode = stat.S_IFREG | permissions
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = source_mode << 16
            archive.writestr(info, expected[name], compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    validate_archive(output, expected)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--output", type=Path, metavar="ZIP", help="build the LabKit archive")
    group.add_argument("--check", type=Path, metavar="ZIP", help="validate a LabKit archive")
    group.add_argument("--fetch-vendor", action="store_true", help="fetch hash-pinned Lab 27 release dependencies before building")
    args = parser.parse_args()
    try:
        if args.fetch_vendor:
            fetch_vendor()
        elif args.check:
            validate_archive(args.check, expected_contents(source_files()))
            print(f"Verified {args.check}")
        else:
            output = args.output or DEFAULT_OUTPUT
            build(output)
            print(f"Built {output}")
    except (LabKitError, OSError) as error:
        print(f"LabKit error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
