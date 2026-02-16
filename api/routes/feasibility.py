from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter
from pydantic import BaseModel

from compiler.solver.feasibility_solver import run_feasibility
from storage.artifact_store import write_run_bundle

router = APIRouter(tags=["feasibility"])


class FeasibilityRequest(BaseModel):
    parcel_id: str
    jurisdiction: str


@router.post("/feasibility")
def feasibility(req: FeasibilityRequest):
    run_id = uuid4().hex
    result = run_feasibility(parcel_id=req.parcel_id, jurisdiction=req.jurisdiction)

    input_obj = {"parcel_id": req.parcel_id, "jurisdiction": req.jurisdiction}
    ir_obj = result.get("ir", {})
    output_obj = result.get("result", {"errors": result.get("errors", [])})
    metadata_obj = {
        "run_id": run_id,
        "ok": result.get("ok", False),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    if not result.get("ok"):
        metadata_obj["errors"] = result.get("errors", [])

    write_run_bundle(run_id, input_obj, ir_obj, output_obj, metadata_obj)
    return {**result, "run_id": run_id}
