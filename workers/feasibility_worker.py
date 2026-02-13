# Ray worker stub
def run_batch(parcel_ids: list[str], jurisdiction: str) -> list[dict]:
    from compiler.solver.feasibility_solver import run_feasibility
    return [run_feasibility(pid, jurisdiction) for pid in parcel_ids]
