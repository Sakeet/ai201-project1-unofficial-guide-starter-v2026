"""Criterion 4: what share of chunks are at least 250 characters?"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import config
from ingest import load_documents
from chunker import split_documents

label = sys.argv[1] if len(sys.argv) > 1 else "before"
chunks = split_documents(load_documents(config.CORPUS))
lengths = sorted(len(c.text) for c in chunks)
long_enough = sum(n >= 250 for n in lengths)

lines = [
    f"# Criterion 4 — chunk lengths ({label})",
    "Produced by: `tools/chunk_lengths.py`, chunks from `chunker.py::split_documents`",
    "",
    f"- Total chunks: {len(lengths)}",
    f"- Chunks >= 250 chars: {long_enough} ({long_enough / len(lengths):.1%})",
    f"- Shortest: {lengths[0]} · Longest: {lengths[-1]} · "
    f"Average: {sum(lengths) / len(lengths):.0f}",
]
out = config.RESULTS_DIR / f"chunk_lengths_{label}.md"
out.write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines) + f"\n\nWrote {out}")