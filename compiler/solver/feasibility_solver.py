from compiler.ir.schema import BuildangoIR, Parcel, ZoningContext
from compiler.ir.validator import validate_ir
from compiler.rules.zoning_rules import apply_zoning_rules
from compiler.solver.constraint_engine import solve_constraints

def run_feasibility(parcel_id: str, jurisdiction: str) -> dict:
    ir = BuildangoIR(
        parcel=Parcel(parcel_id=parcel_id),
        zoning=ZoningContext(jurisdiction=jurisdiction),
        provenance={"note": "skeleton run"},
    )
    ir = apply_zoning_rules(ir)
    errors = validate_ir(ir)
    if errors:
        return {"ok": False, "errors": errors, "ir": ir.model_dump()}
    res = solve_constraints(ir.constraints)
    return {
        "ok": True,
        "ir": ir.model_dump(),
        "result": {
            "feasible": res.feasible,
            "confidence": res.confidence,
            **res.outputs,
        },
    }
