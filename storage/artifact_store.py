from dataclasses import dataclass
from typing import Optional

@dataclass
class ArtifactPointers:
    input_uri: str
    ir_uri: str
    output_uri: str
    report_uri: Optional[str] = None

def artifact_paths(run_id: str) -> ArtifactPointers:
    # For GCS: gs://<bucket>/runs/<run_id>/...
    base = f"runs/{run_id}"
    return ArtifactPointers(
        input_uri=f"{base}/input.json",
        ir_uri=f"{base}/ir.json",
        output_uri=f"{base}/output.json",
        report_uri=f"{base}/report.pdf",
    )
