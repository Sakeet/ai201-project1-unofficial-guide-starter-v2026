"""Criterion 5: borderline questions, 3 runs each, gate decision recorded separately."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import config
import gate
from store import search
from generate import answer_from_chunks

BORDERLINE = [
    "Do international students get priority in the housing lottery?",
    "What happens if I miss the fifteen-day grade appeal window?",
    "Can I pay for a parking permit in installments?",
    "Is there an exception to the meal plan change deadline for financial hardship?",
    "Does the work-study income exemption still apply during summer session?",
]
label = sys.argv[1] if len(sys.argv) > 1 else "before"
lines = [f"# Criterion 5 — borderline questions ({label})",
         f"Produced by: `tools/borderline.py`, gate `gate.py::check`, cutoff {config.THRESHOLD}", ""]

for run in range(1, 4):
    for q in BORDERLINE:
        results = search(q, top_k=config.TOP_K)
        decision = gate.check(results)
        answer = (answer_from_chunks(q, results, cache=False)
                  if decision.passed else gate.REFUSAL)
        gate_word = "passed" if decision.passed else "REFUSED"
        print(f"run {run}: gate {gate_word} ({decision.best_distance:.3f})  {q}")
        lines += [f"### {q} — run {run}",
                  f"- Best distance: {decision.best_distance:.3f} · gate {gate_word}",
                  "```", answer, "```", ""]

out = config.RESULTS_DIR / f"borderline_{label}.md"
out.write_text("\n".join(lines), encoding="utf-8")
print(f"\nWrote {out}")