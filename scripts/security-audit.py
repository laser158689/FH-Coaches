#!/usr/bin/env python3
"""Fail-closed, redacted security scan for this public repository.

The scanner checks the tracked worktree, reachable default-branch history, and
every tracked ZIP member. It reports only rule names and paths; matched values
are never printed into CI or terminal logs.
"""

from __future__ import annotations

import argparse
import collections
import io
import math
import os
import pathlib
import re
import stat
import subprocess
import sys
import zipfile


MAX_BLOB_SIZE = 30 * 1024 * 1024
MAX_ZIP_MEMBER_SIZE = 25 * 1024 * 1024
MAX_ZIP_EXPANSION = 100 * 1024 * 1024

PRIVATE_PATH_PATTERN = (
    rb"(?:/"
    + rb"Users/[^/\s]+|/"
    + rb"home/[^/\s]+|[A-Za-z]:\\Users\\[^\\\s]+)"
)

CONTENT_RULES = {
    "private_key": re.compile(rb"-----BEGIN (?:[A-Z0-9 ]+ )?PRIVATE KEY-----"),
    "provider_token": re.compile(
        rb"(?:AKIA[0-9A-Z]{16}|ASIA[0-9A-Z]{16}|"
        rb"gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|"
        rb"sk-(?:proj-|ant-)?[A-Za-z0-9_-]{16,}|AIza[0-9A-Za-z_-]{30,}|"
        rb"xox[baprs]-[A-Za-z0-9-]{10,}|(?:sk|rk)_live_[0-9A-Za-z]{16,}|"
        rb"npm_[A-Za-z0-9]{20,}|hf_[A-Za-z0-9]{20,})"
    ),
    "credentialed_url": re.compile(rb"https?://[^\s/:@]+:[^\s@/]+@"),
    "private_path": re.compile(PRIVATE_PATH_PATTERN),
    "email": re.compile(rb"(?i:[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,})"),
    "ssn": re.compile(
        rb"(?<!\d)(?!000|666|9\d\d)\d{3}[- ]?(?!00)\d{2}[- ]?(?!0000)\d{4}(?!\d)"
    ),
    "us_phone": re.compile(
        rb"(?<!\d)(?:\+?1[-. (]*)?(?:[2-9]\d{2})[-. )]*[2-9]\d{2}[-. ]*\d{4}(?!\d)"
    ),
    "jwt": re.compile(
        rb"eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"
    ),
    "ssh_key_material": re.compile(
        rb"ssh-(?:rsa|ed25519|dss)\s+[A-Za-z0-9+/]{80,}={0,3}"
    ),
    "sensitive_assignment": re.compile(
        rb"""(?ix)
        (?:api[_-]?key|access[_-]?token|auth[_-]?token|client[_-]?secret|
        password|passwd|secret)\s*[:=]\s*["'][^"'\r\n]{6,}["']
        """
    ),
}

SENSITIVE_BASENAME = re.compile(
    r"""(?ix)
    ^(?:
      \.env(?:\..*)?|\.npmrc|\.pypirc|\.netrc|credentials?|
      id_(?:rsa|dsa|ecdsa|ed25519)(?:\.pub)?|
      .*?\.(?:pem|key|p12|pfx|jks|keystore|mobileprovision|kdbx|ovpn)
    )$
    """
)

CARD_CANDIDATE = re.compile(rb"(?<!\d)(?:\d[ -]?){13,19}(?!\d)")
HIGH_ENTROPY_CANDIDATE = re.compile(
    rb"(?<![A-Za-z0-9])[A-Za-z0-9+_=-]{32,}(?![A-Za-z0-9])"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--revision",
        default="origin/main",
        help="reachable history to scan (default: origin/main)",
    )
    parser.add_argument(
        "--no-history",
        action="store_true",
        help="scan only the tracked worktree",
    )
    return parser.parse_args()


def repo_root() -> pathlib.Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return pathlib.Path(os.fsdecode(result.stdout).strip()).resolve()


def git(root: pathlib.Path, *args: str, input_bytes: bytes | None = None) -> bytes:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    ).stdout


def is_probably_binary(data: bytes) -> bool:
    sample = data[:8192]
    if b"\0" in sample:
        return True
    if not sample:
        return False
    textish = sum(
        byte in b"\t\n\r\f\b" or 32 <= byte <= 126 or byte >= 128
        for byte in sample
    )
    return textish / len(sample) < 0.85


def luhn(number: str) -> bool:
    digits = [int(character) for character in number]
    checksum = 0
    parity = len(digits) % 2
    for index, digit in enumerate(digits):
        if index % 2 == parity:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
    return checksum % 10 == 0


def entropy(value: bytes) -> float:
    counts = collections.Counter(value)
    size = len(value)
    return -sum(
        (count / size) * math.log2(count / size) for count in counts.values()
    )


def looks_random(value: bytes) -> bool:
    character_classes = sum(
        (
            any(65 <= byte <= 90 for byte in value),
            any(97 <= byte <= 122 for byte in value),
            any(48 <= byte <= 57 for byte in value),
        )
    )
    return character_classes == 3 and entropy(value.rstrip(b"=")) >= 4.7


def scan_text(
    label: str,
    data: bytes,
    findings: set[tuple[str, str]],
) -> None:
    if is_probably_binary(data):
        return
    for rule_name, pattern in CONTENT_RULES.items():
        if pattern.search(data):
            findings.add((rule_name, label))
    for candidate in CARD_CANDIDATE.findall(data):
        digits = re.sub(rb"\D", b"", candidate).decode("ascii")
        if 13 <= len(digits) <= 19 and luhn(digits):
            findings.add(("payment_card_candidate", label))
            break
    if any(looks_random(candidate) for candidate in HIGH_ENTROPY_CANDIDATE.findall(data)):
        findings.add(("high_entropy_candidate", label))


def scan_zip(
    label: str,
    data: bytes,
    findings: set[tuple[str, str]],
) -> None:
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            total_uncompressed = 0
            for member in archive.infolist():
                member_name = member.filename
                normalized = pathlib.PurePosixPath(member_name.replace("\\", "/"))
                total_uncompressed += member.file_size
                if (
                    normalized.is_absolute()
                    or ".." in normalized.parts
                    or re.match(r"^[A-Za-z]:", member_name)
                ):
                    findings.add(("zip_unsafe_member_path", f"{label}!{member_name}"))
                unix_mode = member.external_attr >> 16
                if stat.S_ISLNK(unix_mode):
                    findings.add(("zip_symlink_member", f"{label}!{member_name}"))
                if unix_mode and stat.S_ISREG(unix_mode) and unix_mode & 0o111:
                    findings.add(("zip_executable_member", f"{label}!{member_name}"))
                if member.flag_bits & 0x1:
                    findings.add(("zip_encrypted_member", f"{label}!{member_name}"))
                if SENSITIVE_BASENAME.match(normalized.name):
                    findings.add(("zip_sensitive_member_name", f"{label}!{member_name}"))
                if member.file_size > MAX_ZIP_MEMBER_SIZE:
                    findings.add(("zip_oversized_member", f"{label}!{member_name}"))
                    continue
                if member.compress_size and member.file_size / member.compress_size > 200:
                    findings.add(
                        ("zip_suspicious_compression_ratio", f"{label}!{member_name}")
                    )
                if member.is_dir():
                    continue
                try:
                    scan_text(f"{label}!{member_name}", archive.read(member), findings)
                except (RuntimeError, NotImplementedError, zipfile.BadZipFile):
                    findings.add(("zip_unreadable_member", f"{label}!{member_name}"))
            if total_uncompressed > MAX_ZIP_EXPANSION:
                findings.add(("zip_oversized_expansion", label))
    except zipfile.BadZipFile:
        findings.add(("invalid_zip", label))


def scan_blob(
    label: str,
    data: bytes,
    findings: set[tuple[str, str]],
) -> None:
    basename = pathlib.PurePosixPath(label.split(":", 1)[-1]).name
    if SENSITIVE_BASENAME.match(basename):
        findings.add(("sensitive_filename", label))
    if zipfile.is_zipfile(io.BytesIO(data)):
        scan_zip(label, data, findings)
    else:
        scan_text(label, data, findings)


def scan_worktree(root: pathlib.Path) -> set[tuple[str, str]]:
    findings: set[tuple[str, str]] = set()
    tracked = [
        os.fsdecode(item)
        for item in git(root, "ls-files", "-z").split(b"\0")
        if item
    ]
    for relative in tracked:
        path = root / relative
        try:
            data = path.read_bytes()
        except FileNotFoundError:
            continue
        scan_blob(relative, data, findings)
    return findings


def history_blobs(
    root: pathlib.Path,
    revision: str,
) -> list[tuple[str, int, str]]:
    objects = git(root, "rev-list", "--objects", revision).splitlines()
    object_ids = [line.split(b" ", 1)[0] for line in objects]
    metadata = git(
        root,
        "cat-file",
        "--batch-check=%(objectname) %(objecttype) %(objectsize)",
        input_bytes=b"\n".join(object_ids) + b"\n",
    ).decode("utf-8", "replace").splitlines()
    paths: dict[str, str] = {}
    for line in objects:
        parts = line.decode("utf-8", "surrogateescape").split(" ", 1)
        if len(parts) == 2:
            paths.setdefault(parts[0], parts[1])
    blobs = []
    for line in metadata:
        object_id, object_type, size = line.split(" ", 2)
        if object_type == "blob":
            blobs.append((object_id, int(size), paths.get(object_id, "[unknown-path]")))
    return blobs


def scan_history(
    root: pathlib.Path,
    revision: str,
) -> set[tuple[str, str]]:
    findings: set[tuple[str, str]] = set()
    for object_id, size, path in history_blobs(root, revision):
        label = f"{object_id[:12]}:{path}"
        if size > MAX_BLOB_SIZE:
            findings.add(("oversized_historical_blob", label))
            continue
        scan_blob(label, git(root, "cat-file", "blob", object_id), findings)
    return findings


def print_findings(title: str, findings: set[tuple[str, str]]) -> None:
    print(f"{title}: {len(findings)} finding(s)")
    grouped: dict[str, list[str]] = collections.defaultdict(list)
    for rule, path in sorted(findings):
        grouped[rule].append(path)
    for rule, paths in sorted(grouped.items()):
        print(f"- {rule}: {len(paths)}")
        for path in paths[:50]:
            print(f"  {path}")
        if len(paths) > 50:
            print(f"  ... {len(paths) - 50} more")


def main() -> int:
    args = parse_args()
    root = repo_root()
    worktree = scan_worktree(root)
    history: set[tuple[str, str]] = set()
    if not args.no_history:
        history = scan_history(root, args.revision)
    print_findings("Tracked worktree", worktree)
    if not args.no_history:
        print_findings(f"Reachable history ({args.revision})", history)
    if worktree or history:
        print("SECURITY AUDIT FAILED")
        return 1
    print("SECURITY AUDIT PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
