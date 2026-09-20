# The Unofficial Guide

Sakeet Kopparapu — corpus: campus_life

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.

---

# Unit 1

## What This Does

This is a retrieval-augmented question-answering system for the campus_life corpus — student-written posts about admin deadlines, course workloads, dining halls, and housing. It answers plain-language questions like "is the housing lottery actually random?" by retrieving the most relevant chunks from 88 documents, checking whether the best match is close enough to trust, and generating a grounded answer that names its source document.

## Chunking Strategy

**Chunk size:** 3 sentences per chunk
**Overlap:** 1 sentence

The starter's fixed 800-character chunker never split anything on this corpus — 88 documents produced 88 chunks, since no document exceeds 800 characters (average ~317 chars/doc). But several documents bundle 2-3 distinct facts into one post (e.g. the parking permits doc covers west-lot demand, east-lot availability, and the no-waitlist workaround as three separate ideas), so one-chunk-per-document buried multiple facts together.

I changed my approach partway through. I first tried grouping 2 sentences per chunk, which produced 367 chunks but left a 31-character chunk that was just a document's title line treated as its own sentence — not enough to answer anything on its own. I fixed that by merging short title-like fragments into the following sentence, and moved to 3 sentences per chunk, which produced 181 chunks averaging 194 characters (shortest 37, longest 378) with noticeably more complete, self-contained chunks.

## Sample Chunks

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

**Chunk 2** — source: `course_cs_340.txt#2` — produced by: `chunker.py::split_documents`

**Chunk 3** — source: `dining_halden_hall.txt#0` — produced by: `chunker.py::split_documents`

**Chunk 4** — source: `dining_verrill_street_grill.txt#2` — produced by: `chunker.py::split_documents`

**Chunk 5** — source: `housing_morrow_house.txt#2` — produced by: `chunker.py::split_documents`

## Sample Answer

**Question:** Is the housing lottery actually random?

**Answer:**

**My relevance cutoff:** 0.6 (the starter default — my data confirmed it sits well inside a clean gap)

| Question | In corpus? | Best distance |
|---|---|---|
| What's the deadline to drop a course versus add one? | Yes | 0.256 |
| Does work-study income affect my financial aid the same way a regular job does? | Yes | 0.249 |
| Is there a penalty for declaring my major late? | Yes | 0.217 |
| Is the housing lottery actually random? | Yes | 0.273 |
| How many days do I have to raise a grade appeal after grades are posted? | Yes | 0.171 |
| What is the capital of Mongolia? | No | 0.825 |
| How do I change the oil in a diesel engine? | No | 0.934 |
| Who won the 1994 World Cup? | No | 0.886 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.844 |
| How do I write a for loop in Rust? | No | 0.896 |

In-corpus distances ranged 0.171–0.273. Out-of-scope distances ranged 0.825–0.934. That's a clean gap of about 0.55 with no overlap between the two groups, so the starter's 0.6 cutoff sits comfortably in the middle with wide margin on both sides.

## How I Used AI

**1.** I pasted my new `split_documents` body into `chunker.py` by replacing just the function, but I accidentally deleted the `Chunk` dataclass, the `Document` import, and the `fallback_split`/`describe` functions along with it, which broke the file (`NameError: name 'Chunk' is not defined`). I asked Claude to help debug it, and it had me rebuild the whole file from a complete version rather than guess at the missing piece, which fixed it.

**2.** I asked Claude to help me pick a threshold for chunk length after noticing my shortest chunk was only 31 characters — a document title line treated as its own sentence. It suggested merging short fragments into the next sentence rather than discarding them, which I implemented; that dropped my shortest chunk from 31 to 37 characters and reduced total chunk count from 367 to 181 by using 3-sentence groups instead of 2.