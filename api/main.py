from fastapi import FastAPI
from api.routes.feasibility import router as feasibility_router

app = FastAPI(title="Buildango API", version="0.1.0")

app.include_router(feasibility_router, prefix="/v1")

@app.get("/healthz")
def healthz():
    return {"ok": True}
