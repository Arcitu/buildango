import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

_REPO_ROOT = Path(__file__).resolve().parent.parent


def ensure_run_dir(run_id: str) -> Path:
    """Create frozen_runs/<run_id>/ (relative to repo root) if missing."""
    run_dir = _REPO_ROOT / "frozen_runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def write_json(path: Path | str, obj: Any) -> None:
    """Write JSON-serializable object to path."""
    data = obj.model_dump() if hasattr(obj, "model_dump") else obj
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def write_run_bundle(
    run_id: str,
    input_obj: Any,
    ir_obj: Any,
    output_obj: Any,
    metadata_obj: Any,
) -> None:
    """Write input.json, ir.json, output.json, metadata.json to frozen_runs/<run_id>/."""
    run_dir = ensure_run_dir(run_id)
    write_json(run_dir / "input.json", input_obj)
    write_json(run_dir / "ir.json", ir_obj)
    write_json(run_dir / "output.json", output_obj)
    write_json(run_dir / "metadata.json", metadata_obj)


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
