from fastapi import APIRouter
from pydantic import BaseModel
from compiler.solver.feasibility_solver import run_feasibility

router = APIRouter(tags=["feasibility"])

class FeasibilityRequest(BaseModel):
    parcel_id: str
    jurisdiction: str

@router.post("/feasibility")
def feasibility(req: FeasibilityRequest):
    # In production: load parcel, run RAG/LLM interpretation, compile IR, solve, persist artifacts.
    result = run_feasibility(parcel_id=req.parcel_id, jurisdiction=req.jurisdiction)
    return result
