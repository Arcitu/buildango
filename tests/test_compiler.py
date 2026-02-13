from compiler.solver.feasibility_solver import run_feasibility

def test_run_feasibility_smoke():
    out = run_feasibility("P-1", "DemoCity")
    assert out["ok"] is True
    assert "result" in out
