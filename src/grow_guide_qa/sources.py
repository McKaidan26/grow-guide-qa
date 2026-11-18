"""Source documents: the manifest, the SOURCES.md generator and the downloader.

`data/sources.toml` is the single source of truth for which documents are in
the corpus, where each comes from and under what license. Documents whose
license allows redistribution are committed under `data/vendored/`; the rest
are downloaded from the publisher at setup time into `data/raw/`, which git
ignores.

Every file is checked against a pinned SHA-256 checksum. That makes the corpus,
and every score measured on it, reproducible, and it means a document that
changes upstream is caught instead of silently invalidating the evaluation set.

Usage:
    python -m grow_guide_qa.sources fetch    # download missing documents, verify all
    python -m grow_guide_qa.sources render   # regenerate SOURCES.md from the manifest
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
import tomllib
import urllib.request
from collections.abc import Callable, Iterable
from dataclasses import dataclass, fields
from pathlib import Path

DATA_DIR = Path("data")
MANIFEST_NAME = "sources.toml"
SOURCES_MD = Path("SOURCES.md")

_ID_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
_SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
_DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# Takes a URL, returns the response body. Injected so tests never touch the network.
Downloader = Callable[[str], bytes]


class ManifestError(ValueError):
    """The manifest is malformed or inconsistent."""


class ChecksumMismatchError(RuntimeError):
    """A document's bytes do not match the checksum pinned in the manifest."""


@dataclass(frozen=True)
class Source:
    id: str
    title: str
    authors: str
    publisher: str
    year: int
    topic: str
    url: str
    landing_page: str
    license: str
    license_note: str
    redistribute: bool
    vendored: bool
    sha256: str
    checked: str  # ISO date the license was checked against the publication

    def path(self, data_dir: Path = DATA_DIR) -> Path:
        """Local location of the PDF: committed (vendored) or downloaded (raw)."""
        folder = "vendored" if self.vendored else "raw"
        return data_dir / folder / f"{self.id}.pdf"


@dataclass(frozen=True)
class Excluded:
    title: str
    url: str
    reason: str


@dataclass(frozen=True)
class Manifest:
    sources: tuple[Source, ...]
    excluded: tuple[Excluded, ...]


def load_manifest(path: Path = DATA_DIR / MANIFEST_NAME) -> Manifest:
    with path.open("rb") as f:
        raw = tomllib.load(f)
    sources = tuple(_build(Source, entry) for entry in raw.get("source", []))
    excluded = tuple(_build(Excluded, entry) for entry in raw.get("excluded", []))
    validate_sources(sources)
    return Manifest(sources=sources, excluded=excluded)


def _build(cls: type, entry: dict) -> object:
    """Construct a dataclass from a TOML table, rejecting missing or unknown keys."""
    expected = {f.name for f in fields(cls)}
    missing = sorted(expected - entry.keys())
    unknown = sorted(entry.keys() - expected)
    if missing or unknown:
        label = entry.get("id") or entry.get("title") or "<unnamed>"
        problems = []
        if missing:
            problems.append(f"missing {missing}")
        if unknown:
            problems.append(f"unknown {unknown}")
        raise ManifestError(f"{cls.__name__} entry {label!r}: {', '.join(problems)}")
    return cls(**entry)


def validate_sources(sources: Iterable[Source]) -> None:
    seen: set[str] = set()
    for s in sources:
        if not _ID_PATTERN.match(s.id):
            raise ManifestError(f"{s.id!r}: ids must be lowercase words joined by hyphens")
        if s.id in seen:
            raise ManifestError(f"duplicate id {s.id!r}")
        seen.add(s.id)
        if not isinstance(s.year, int) or not isinstance(s.vendored, bool):
            raise ManifestError(f"{s.id!r}: year must be an integer and vendored a boolean")
        if not _SHA256_PATTERN.match(s.sha256):
            raise ManifestError(f"{s.id!r}: sha256 must be 64 lowercase hex characters")
        if not _DATE_PATTERN.match(s.checked):
            raise ManifestError(f'{s.id!r}: checked must be a quoted date like "2026-01-31"')
        if not s.url.startswith("https://"):
            raise ManifestError(f"{s.id!r}: url must use https")
        if s.vendored and not s.redistribute:
            raise ManifestError(
                f"{s.id!r} is marked vendored, but its license does not allow redistribution"
            )


def sha256_file(path: Path) -> str:
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def http_get(url: str, timeout: float = 60.0) -> bytes:
    """Download a URL. Uses urllib's default User-Agent: honest about being a script."""
    with urllib.request.urlopen(url, timeout=timeout) as response:
        return response.read()


def ensure_source(
    source: Source, data_dir: Path = DATA_DIR, download: Downloader = http_get
) -> str:
    """Make sure a source's PDF is on disk and matches its pinned checksum.

    Returns "present" if a matching file was already there, or "downloaded".
    Committed (vendored) files are only verified, never downloaded over.
    """
    target = source.path(data_dir)
    if target.exists():
        actual = sha256_file(target)
        if actual == source.sha256:
            return "present"
        if source.vendored:
            raise ChecksumMismatchError(
                f"{target}: committed file has SHA-256 {actual}, manifest pins {source.sha256}"
            )
        target.unlink()  # A stale or partial earlier download: never leave it to be ingested.
    elif source.vendored:
        raise FileNotFoundError(f"{target}: this document should be committed to the repository")

    data = download(source.url)
    actual = hashlib.sha256(data).hexdigest()
    if actual != source.sha256:
        raise ChecksumMismatchError(
            f"{source.id}: downloaded file has SHA-256 {actual}, but the manifest pins "
            f"{source.sha256}. The publisher may have changed the document. Check it, then "
            "update the checksum and any evaluation questions that cite it."
        )
    target.parent.mkdir(parents=True, exist_ok=True)
    partial = target.with_name(target.name + ".part")
    partial.write_bytes(data)
    partial.replace(target)  # Rename is atomic, so a crash never leaves a half-written PDF.
    return "downloaded"


def fetch_all(
    manifest: Manifest,
    data_dir: Path = DATA_DIR,
    download: Downloader = http_get,
    out: Callable[[str], None] = print,
) -> list[str]:
    """Ensure every source is present. Keeps going past failures; returns the failed ids."""
    failures = []
    for source in manifest.sources:
        try:
            status = ensure_source(source, data_dir, download)
        except (OSError, ChecksumMismatchError) as exc:  # urllib errors are OSErrors
            failures.append(source.id)
            out(f"    FAILED {source.id}: {exc}")
        else:
            out(f"{status:>10} {source.id}")
    return failures


def render_markdown(manifest: Manifest) -> str:
    lines = [
        "# Sources",
        "",
        "<!-- Generated from data/sources.toml by `python -m grow_guide_qa.sources render`."
        " Edit the manifest, not this file. -->",
        "",
        f"The corpus is {len(manifest.sources)} public guides on growing microgreens and"
        " indoor farming. Each license was checked against the publication itself; the date"
        " of each check is in the license notes.",
        "",
        "- **In repo:** the license allows redistribution, so the PDF is committed under"
        " `data/vendored/`.",
        "- **Downloaded:** the PDF is fetched from the publisher at setup time into"
        " `data/raw/`, which git ignores. Run `python -m grow_guide_qa.sources fetch`.",
        "",
        "Every file is checked against the SHA-256 checksum pinned in the manifest, so the"
        " corpus behind the evaluation results can be reproduced exactly.",
        "",
        "| ID | Document | Publisher | Year | Topic | License | Copy |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for s in manifest.sources:
        copy = "In repo" if s.vendored else "Downloaded"
        lines.append(
            f"| `{s.id}` | [{s.title}]({s.landing_page}) | {s.publisher} | {s.year} "
            f"| {s.topic} | {s.license} | {copy} |"
        )
    lines += ["", "## License notes", ""]
    for s in manifest.sources:
        lines += [
            f"### `{s.id}`",
            "",
            f"*{s.title}*, by {s.authors}. {s.publisher}, {s.year}.",
            "",
            f"- PDF: <{s.url}>",
            f"- License (checked {s.checked}): {s.license}. {s.license_note}",
            "",
        ]
    if manifest.excluded:
        lines += ["## Considered and left out", ""]
        lines += [f"- [{e.title}]({e.url}): {e.reason}" for e in manifest.excluded]
    return "\n".join(lines).rstrip("\n") + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m grow_guide_qa.sources",
        description="Manage the source documents listed in data/sources.toml.",
    )
    parser.add_argument("--data-dir", type=Path, default=DATA_DIR)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("fetch", help="download missing documents and verify every checksum")
    render = commands.add_parser("render", help="regenerate SOURCES.md from the manifest")
    render.add_argument("--output", type=Path, default=SOURCES_MD)
    args = parser.parse_args(argv)

    manifest = load_manifest(args.data_dir / MANIFEST_NAME)
    if args.command == "fetch":
        failures = fetch_all(manifest, args.data_dir)
        if failures:
            print(f"{len(failures)} document(s) failed: {', '.join(failures)}", file=sys.stderr)
            return 1
        print(f"All {len(manifest.sources)} documents present and verified.")
        return 0
    args.output.write_text(render_markdown(manifest), encoding="utf-8", newline="\n")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
