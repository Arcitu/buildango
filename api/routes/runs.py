from fastapi import APIRouter, HTTPException

from storage.artifact_store import load_run_bundle

router = APIRouter(tags=["runs"])


@router.get("/runs/{run_id}")
def get_run(run_id: str):
    try:
        bundle = load_run_bundle(run_id)
        return bundle
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Run {run_id} not found")
