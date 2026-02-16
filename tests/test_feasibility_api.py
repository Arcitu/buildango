import shutil
from pathlib import Path

from fastapi.testclient import TestClient

from api.main import app

_REPO_ROOT = Path(__file__).resolve().parent.parent


def test_post_feasibility_creates_artifacts():
    client = TestClient(app)
    response = client.post(
        "/v1/feasibility",
        json={"parcel_id": "P-test-123", "jurisdiction": "DemoCity"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "run_id" in data
    run_id = data["run_id"]

    run_dir = _REPO_ROOT / "frozen_runs" / run_id
    try:
        assert run_dir.exists()
        assert run_dir.is_dir()

        artifacts = ["input.json", "ir.json", "output.json", "metadata.json"]
        for name in artifacts:
            path = run_dir / name
            assert path.exists(), f"{name} should exist"
            content = path.read_text()
            assert len(content.strip()) > 0, f"{name} should be non-empty"
    finally:
        if run_dir.exists():
            shutil.rmtree(run_dir)
