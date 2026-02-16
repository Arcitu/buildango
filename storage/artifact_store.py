import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

# ----------------------------
# Config
# ----------------------------
_REPO_ROOT = Path(__file__).resolve().parent.parent

ARTIFACT_BACKEND = os.getenv("BUILDANGO_ARTIFACT_BACKEND", "local").strip().lower()
GCS_BUCKET = os.getenv("BUILDANGO_GCS_BUCKET", "").strip()
GCS_PREFIX = os.getenv("BUILDANGO_GCS_PREFIX", "runs").strip().strip("/")  # default: runs


def _jsonable(obj: Any) -> Any:
    """Convert pydantic models (v2) or other objects into JSON-serializable structures."""
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    return obj


def _dump_json_bytes(obj: Any) -> bytes:
    data = _jsonable(obj)
    return json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")


# ----------------------------
# Local backend
# ----------------------------
def ensure_run_dir(run_id: str) -> Path:
    """Create frozen_runs/<run_id>/ (relative to repo root) if missing."""
    run_dir = _REPO_ROOT / "frozen_runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def _run_dir_local(run_id: str) -> Path:
    """Path to frozen_runs/<run_id>/ (does not create)."""
    return _REPO_ROOT / "frozen_runs" / run_id


def _write_bundle_local(run_id: str, bundle: dict[str, Any]) -> None:
    run_dir = ensure_run_dir(run_id)
    for name, obj in bundle.items():
        path = run_dir / f"{name}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(_dump_json_bytes(obj))


def _load_bundle_local(run_id: str) -> dict[str, Any]:
    run_dir = _run_dir_local(run_id)
    if not run_dir.exists() or not run_dir.is_dir():
        raise FileNotFoundError(f"Run {run_id} not found")

    artifacts = ["input.json", "ir.json", "output.json", "metadata.json"]
    result: dict[str, Any] = {}
    for filename in artifacts:
        path = run_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Run {run_id} missing {filename}")
        result[filename.replace(".json", "")] = json.loads(path.read_text(encoding="utf-8"))
    return result


# ----------------------------
# GCS backend
# ----------------------------
def _require_gcs() -> None:
    if not GCS_BUCKET:
        raise RuntimeError(
            "GCS backend selected but BUILDANGO_GCS_BUCKET is not set. "
            "Set BUILDANGO_GCS_BUCKET and redeploy."
        )


def _gcs_client():
    # Import lazily so local dev doesn't require the dependency unless using gcs backend
    from google.cloud import storage  # type: ignore

    return storage.Client()


def _gcs_blob_path(run_id: str, name: str) -> str:
    # e.g., runs/<run_id>/input.json
    return f"{GCS_PREFIX}/{run_id}/{name}.json"


def _write_bundle_gcs(run_id: str, bundle: dict[str, Any]) -> None:
    _require_gcs()
    client = _gcs_client()
    bucket = client.bucket(GCS_BUCKET)

    for name, obj in bundle.items():
        blob = bucket.blob(_gcs_blob_path(run_id, name))
        blob.upload_from_string(_dump_json_bytes(obj), content_type="application/json; charset=utf-8")


def _load_bundle_gcs(run_id: str) -> dict[str, Any]:
    _require_gcs()
    client = _gcs_client()
    bucket = client.bucket(GCS_BUCKET)

    names = ["input", "ir", "output", "metadata"]
    result: dict[str, Any] = {}

    for name in names:
        blob = bucket.blob(_gcs_blob_path(run_id, name))
        if not blob.exists(client):
            raise FileNotFoundError(f"Run {run_id} missing {name}.json in gs://{GCS_BUCKET}/{GCS_PREFIX}/")
        data = blob.download_as_bytes()
        result[name] = json.loads(data.decode("utf-8"))

    return result


# ----------------------------
# Public API used by routes
# ----------------------------
def write_run_bundle(
    run_id: str,
    input_obj: Any,
    ir_obj: Any,
    output_obj: Any,
    metadata_obj: Any,
) -> None:
    """Write input.json, ir.json, output.json, metadata.json to the selected backend."""
    bundle = {
        "input": input_obj,
        "ir": ir_obj,
        "output": output_obj,
        "metadata": metadata_obj,
    }

    if ARTIFACT_BACKEND == "gcs":
        _write_bundle_gcs(run_id, bundle)
    else:
        _write_bundle_local(run_id, bundle)


def load_run_bundle(run_id: str) -> dict[str, Any]:
    """Load input, ir, output, metadata from the selected backend. Raises FileNotFoundError if not found."""
    if ARTIFACT_BACKEND == "gcs":
        return _load_bundle_gcs(run_id)
    return _load_bundle_local(run_id)


# ----------------------------
# Optional: URI helpers (useful for metadata / debugging)
# ----------------------------
@dataclass
class ArtifactPointers:
    input_uri: str
    ir_uri: str
    output_uri: str
    report_uri: Optional[str] = None


def artifact_paths(run_id: str) -> ArtifactPointers:
    # For local: file://...  For GCS: gs://...
    if ARTIFACT_BACKEND == "gcs":
        base = f"gs://{GCS_BUCKET}/{GCS_PREFIX}/{run_id}"
        return ArtifactPointers(
            input_uri=f"{base}/input.json",
            ir_uri=f"{base}/ir.json",
            output_uri=f"{base}/output.json",
            report_uri=f"{base}/report.pdf",
        )

    base = _run_dir_local(run_id)
    return ArtifactPointers(
        input_uri=str(base / "input.json"),
        ir_uri=str(base / "ir.json"),
        output_uri=str(base / "output.json"),
        report_uri=str(base / "report.pdf"),
    )
