# Grow Guide QA

Ask a question about growing microgreens or farming indoors, and get an answer
that cites the exact passages it came from. The answers come from a small set of
public, freely licensed guides, such as university agricultural extension
publications.

The main point of the project is measuring how well it works: a hand-reviewed
set of test questions, retrieval and answer-quality scores, and experiments that
compare design choices on quality, cost and latency.

**Status:** work in progress. This README grows with each step.

## The documents

Fifteen guides from university extension services and the USDA, covering
microgreens, hydroponic and vertical-farm systems, and crop-specific growing
conditions (light, temperature, humidity). They are listed with their licenses
in [`SOURCES.md`](SOURCES.md). The eleven whose license allows redistribution
are committed in `data/vendored/`. The other four are downloaded from their
publishers, and every file is checked against a pinned checksum:

```bash
uv run python -m grow_guide_qa.sources fetch
```

## Development

Requires Python 3.11 or newer and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run pytest
uv run ruff check .
```

## License

The code is under the MIT License (see `LICENSE`). The source documents are not
covered by it; each keeps its own license, listed in `SOURCES.md`.
