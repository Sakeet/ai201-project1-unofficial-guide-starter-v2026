"""
Stage 2 of the pipeline: splitting documents into chunks.
"""

import re
from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split documents into chunks. Splits on sentence boundaries, then groups
    sentences into chunks of up to 2, with 1 sentence of overlap between
    consecutive chunks. campus_life documents are short (avg ~317 chars) but
    often bundle 2-3 distinct facts into one post, so grouping by sentence
    keeps each chunk to one or two related facts instead of an arbitrary
    character cutoff. Short title-like fragments (e.g. "On the add/drop
    deadline") are merged into the following sentence instead of standing
    alone as a chunk, since a fragment that short can't answer a question by
    itself.
    """
    sentences_per_chunk = 3
    overlap_sentences = 1
    min_sentence_length = 40

    chunks: list[Chunk] = []
    for doc in documents:
        raw_sentences = re.split(r"(?<=[.!?])\s+", doc.text.strip())
        sentences = [s.strip() for s in raw_sentences if s.strip()]

        # Merge any very short leading fragment (like a title line with no
        # terminal punctuation) into the next sentence instead of treating
        # it as its own unit.
        merged = []
        i = 0
        while i < len(sentences):
            if len(sentences[i]) < min_sentence_length and i + 1 < len(sentences):
                merged.append(sentences[i] + " " + sentences[i + 1])
                i += 2
            else:
                merged.append(sentences[i])
                i += 1
        sentences = merged

        if not sentences:
            continue

        index = 0
        i = 0
        step = max(1, sentences_per_chunk - overlap_sentences)
        while i < len(sentences):
            group = sentences[i : i + sentences_per_chunk]
            text = " ".join(group)
            chunks.append(
                Chunk(
                    text=text,
                    source=doc.source,
                    index=index,
                    produced_by="chunker.py::split_documents",
                )
            )
            index += 1
            i += step

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))