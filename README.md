# Buildango – Production Repo Skeleton

This is a modular skeleton designed to keep the **compiler core** isolated while supporting:
- FastAPI on Cloud Run
- Postgres/PostGIS
- Ray-distributed workers
- vLLM inference
- Databricks pipelines (later phase)
- Demo-freeze artifact storage (GCS)

## Quick start (local)
1) Create a virtualenv and install deps:
```bash
python -m venv .venv
source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -e ".[dev]"
```

2) Run the API:
```bash
uvicorn api.main:app --reload --port 8000
```

3) Run tests:
```bash
pytest
```

## Demo-freeze concept
Each feasibility run should persist:
- `input.json`
- `ir.json`
- `output.json`
- `report.pdf`

See `scripts/freeze_demo.sh` and `storage/artifact_store.py`.
