# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
My corpus currently has one chunk per document, so most facts — like the
add/drop deadline or the work-study financial aid rule — live in exactly one
chunk with no redundancy elsewhere in the corpus. If retrieval misses that
single chunk for either of those two questions, there's nothing else to fall
back on. I expect the other three (major declaration, housing lottery, grade
appeals) to be easier since they're either more distinctive topics or, like
housing, get reinforced by related documents. 4 of 5 accounts for the
possibility that one of the two riskier ones doesn't come back cleanly.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
Every one of my test questions produced a "Source:" line in the output,
without exception, across all 5 questions I ran. This isn't a coincidence —
the system's output format always includes a source line whether it answers
or refuses, so unlike retrieval accuracy or gate correctness (which depend on
how close a match actually is), source attribution is a structural part of
every response. That's why I set this at 100% rather than 4 of 5: there's no
realistic scenario in my testing where an answer comes back with no source at
all.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
My five in-scope test questions had best distances between 0.171 and 0.256,
while my five out-of-scope questions had best distances between 0.825 and
0.934 — a clean gap of about 0.57 with no overlap between the two groups. My
0.6 cutoff sits comfortably in the middle of that gap. Given how wide and
clean the separation is, I'd actually expect the gate to catch all 5 out-of-
scope questions reliably, but I kept the target at 4 of 5 to match the
baseline the assignment provides, since a single unlucky embedding or an
unusually-phrased question could still occasionally slip through even with a
strong gap like this.

---

## 4. Chunks are long enough to stand alone

At least 90% of chunks are at least 250 characters long.

**Why this target:**
My shortest chunk right now is 178 characters, which reads as a fragment rather than a complete thought — not enough to answer a question on its own. I didn't require 100% because a few genuinely short pieces of content (like a one-line policy fact) will always fall under 250 characters no matter how good my chunking strategy is. 90% still means the vast majority of chunks are substantial enough to stand alone.

---

## 5. The relevance gate catches borderline questions, not just obvious ones

When I ask 5 borderline questions — plausible-sounding but not actually covered by my documents — the relevance gate refuses at least 4 of the 5.

**Borderline test questions and results:**

| Question | Best distance | Result |
|---|---|---|
| Do international students get priority in the housing lottery? | 0.350 | Refused |
| What happens if I miss the fifteen-day grade appeal window? | 0.380 | Partial answer (not a clean refusal) |
| Can I pay for a parking permit in installments? | 0.593 | Refused |
| Is there an exception to the meal plan change deadline for financial hardship? | 0.348 | Refused |
| Does the work-study income exemption still apply during summer session? | 0.541 | Refused |

4 of 5 refused cleanly, meeting the target. The grade-appeal question got a partial, hedged answer rather than a clean refusal — the system answered the part it could ("skipping the instructor step wastes the appeal window") while explicitly flagging what it couldn't answer, rather than confidently guessing. That's arguably good behavior, but it doesn't match this
criterion's literal "I don't have enough information about that" wording, so I'm counting it as a miss against the strict target.

**Why this target:**
I tested this against 5 borderline questions built from real corpus topics (e.g. asking whether international students get lottery priority, when the lottery doc only discusses class-year ordering). 4 of 5 refused cleanly, with distances (0.348–0.593) sitting in a clear middle zone between my in-corpus range (0.171–0.273) and out-of-scope range (0.825–0.934) — confirming borderline questions really do occupy distinct territory in this embedding space. I set the target at 4 of 5 because a wrong guess here means the system confidently states something false, which is worse than a minor quality issue, but even a good gate can miss the hardest case — the grade-appeal question got a hedged partial answer rather than a clean refusal.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
