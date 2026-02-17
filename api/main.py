from fastapi import FastAPI
from api.routes.feasibility import router as feasibility_router
from api.routes.runs import router as runs_router

app = FastAPI(title="Buildango API", version="0.1.0")

app.include_router(feasibility_router, prefix="/v1")
app.include_router(runs_router, prefix="/v1")

@app.get("/healthz")
def healthz():
    return {"ok": True}
