# Placeholder GEPA harness. Replace with your actual GEPA / LLM-as-judge loop.
from typing import Dict, Any

def score_run(output: Dict[str, Any]) -> Dict[str, float]:
    # Example sub-scores
    return {
        "determinism": 0.8,
        "code_citation": 0.2,
        "constraint_coverage": 0.3,
        "overall": 0.4,
    }
