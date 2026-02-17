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


def test_get_run_returns_bundle():
    client = TestClient(app)
    create_resp = client.post(
        "/v1/feasibility",
        json={"parcel_id": "P-get-test", "jurisdiction": "DemoCity"},
    )
    assert create_resp.status_code == 200
    run_id = create_resp.json()["run_id"]

    try:
        get_resp = client.get(f"/v1/runs/{run_id}")
        assert get_resp.status_code == 200
        bundle = get_resp.json()
        assert "input" in bundle
        assert "ir" in bundle
        assert "output" in bundle
        assert "metadata" in bundle
        assert bundle["input"]["parcel_id"] == "P-get-test"
        assert bundle["metadata"]["run_id"] == run_id
    finally:
        run_dir = _REPO_ROOT / "frozen_runs" / run_id
        if run_dir.exists():
            shutil.rmtree(run_dir)


def test_get_run_returns_404_when_not_found():
    client = TestClient(app)
    response = client.get("/v1/runs/nonexistent_run_id_12345")
    assert response.status_code == 404
