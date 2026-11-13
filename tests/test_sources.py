"""Tests for the source manifest, the SOURCES.md generator and the downloader.

Downloads use a fake downloader, so these tests never touch the network.
"""

import hashlib
from pathlib import Path

import pytest

from grow_guide_qa import sources
from grow_guide_qa.sources import ChecksumMismatchError, ManifestError, Source

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
PDF_BYTES = b"%PDF-1.7 pretend this is a guide"


def make_source(**overrides) -> Source:
    fields = {
        "id": "doc-1",
        "title": "A Guide",
        "authors": "A. Author",
        "publisher": "Some Extension",
        "year": 2024,
        "topic": "microgreens",
        "url": "https://example.org/doc.pdf",
        "landing_page": "https://example.org/doc",
        "license": "All rights reserved",
        "license_note": "No license stated.",
        "redistribute": False,
        "vendored": False,
        "sha256": hashlib.sha256(PDF_BYTES).hexdigest(),
    }
    fields.update(overrides)
    return Source(**fields)


class FakeDownloader:
    def __init__(self, payload: bytes):
        self.payload = payload
        self.calls: list[str] = []

    def __call__(self, url: str) -> bytes:
        self.calls.append(url)
        return self.payload


# The real manifest and the files committed with it


def test_real_manifest_is_valid():
    manifest = sources.load_manifest(DATA_DIR / "sources.toml")
    assert len(manifest.sources) >= 5
    assert any(s.vendored for s in manifest.sources)


def test_vendored_pdfs_are_committed_with_matching_checksums():
    manifest = sources.load_manifest(DATA_DIR / "sources.toml")
    for s in manifest.sources:
        if s.vendored:
            path = s.path(DATA_DIR)
            assert path.exists(), f"{path} is missing"
            assert sources.sha256_file(path) == s.sha256, f"{path} does not match the manifest"


def test_sources_md_is_up_to_date():
    manifest = sources.load_manifest(DATA_DIR / "sources.toml")
    committed = (ROOT / "SOURCES.md").read_text(encoding="utf-8")
    assert committed == sources.render_markdown(manifest), (
        "SOURCES.md is stale: run `python -m grow_guide_qa.sources render`"
    )


# Manifest validation


def test_rejects_vendoring_a_document_we_may_not_redistribute():
    with pytest.raises(ManifestError, match="redistribution"):
        sources.validate_sources([make_source(vendored=True, redistribute=False)])


def test_rejects_duplicate_ids():
    with pytest.raises(ManifestError, match="duplicate"):
        sources.validate_sources([make_source(), make_source()])


def test_rejects_malformed_checksum():
    with pytest.raises(ManifestError, match="sha256"):
        sources.validate_sources([make_source(sha256="abc123")])


def test_rejects_entry_with_missing_fields(tmp_path):
    manifest = tmp_path / "sources.toml"
    manifest.write_text(
        'checked = "2026-01-01"\n[[source]]\nid = "doc-1"\ntitle = "A Guide"\n',
        encoding="utf-8",
    )
    with pytest.raises(ManifestError, match="missing"):
        sources.load_manifest(manifest)


# Downloading and verifying


def test_downloads_and_verifies_a_missing_document(tmp_path):
    source = make_source()
    fake = FakeDownloader(PDF_BYTES)
    assert sources.ensure_source(source, tmp_path, fake) == "downloaded"
    assert source.path(tmp_path).read_bytes() == PDF_BYTES
    assert fake.calls == [source.url]


def test_skips_the_download_when_the_file_already_matches(tmp_path):
    source = make_source()
    sources.ensure_source(source, tmp_path, FakeDownloader(PDF_BYTES))
    fake = FakeDownloader(PDF_BYTES)
    assert sources.ensure_source(source, tmp_path, fake) == "present"
    assert fake.calls == []


def test_rejects_a_changed_download_and_writes_nothing(tmp_path):
    source = make_source()
    with pytest.raises(ChecksumMismatchError, match="publisher may have changed"):
        sources.ensure_source(source, tmp_path, FakeDownloader(b"edited upstream"))
    assert not any(tmp_path.iterdir())


def test_replaces_a_stale_download(tmp_path):
    source = make_source()
    stale = source.path(tmp_path)
    stale.parent.mkdir(parents=True)
    stale.write_bytes(b"an older version")
    assert sources.ensure_source(source, tmp_path, FakeDownloader(PDF_BYTES)) == "downloaded"
    assert stale.read_bytes() == PDF_BYTES


def test_never_downloads_in_place_of_a_missing_committed_file(tmp_path):
    source = make_source(vendored=True, redistribute=True)
    fake = FakeDownloader(PDF_BYTES)
    with pytest.raises(FileNotFoundError, match="committed"):
        sources.ensure_source(source, tmp_path, fake)
    assert fake.calls == []


def test_fetch_all_keeps_going_past_a_failure(tmp_path):
    bad = make_source(id="bad", sha256="0" * 64)
    good = make_source(id="good")
    manifest = sources.Manifest(checked="2026-01-01", sources=(bad, good), excluded=())
    messages: list[str] = []
    failures = sources.fetch_all(manifest, tmp_path, FakeDownloader(PDF_BYTES), out=messages.append)
    assert failures == ["bad"]
    assert good.path(tmp_path).exists()
    assert any("FAILED bad" in m for m in messages)


# SOURCES.md rendering


def test_markdown_lists_every_source_and_where_its_copy_lives():
    vendored = make_source(id="in-repo", vendored=True, redistribute=True)
    downloaded = make_source(id="fetched")
    manifest = sources.Manifest(
        checked="2026-01-01",
        sources=(vendored, downloaded),
        excluded=(sources.Excluded(title="Gone", url="https://example.org/x", reason="404"),),
    )
    text = sources.render_markdown(manifest)
    assert "| `in-repo` |" in text and "| In repo |" in text
    assert "| `fetched` |" in text and "| Downloaded |" in text
    assert "[Gone](https://example.org/x): 404" in text
