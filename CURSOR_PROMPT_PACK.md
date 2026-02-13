# Cursor Prompt Pack — Buildango

## Repo operating principles (paste into Cursor Rules / .cursorrules)
- The **compiler/** directory is sacred core IP. Keep it deterministic; no network calls from compiler.
- Any LLM calls live under **inference/** and must be optional/fallback.
- Any persistence lives under **db/** and **storage/**.
- New features must add tests under **tests/**.
- Every feasibility run must be reproducible via: (input + versions) → output.

## High-leverage prompts

### A) “Implement a minimal end-to-end feasibility run with artifacts”
Goal: API POST /v1/feasibility writes artifacts (input/ir/output) to local folder (later GCS).
Constraints: keep compiler deterministic; no external calls.

### B) “Add 15 deterministic IR validators”
Add checks for: height bounds, setback presence, FAR ranges, density, allowed uses, overlay conflicts, and provenance completeness.
Return list[str] errors; include unit tests.

### C) “Introduce Ray worker mode”
Add a /v1/feasibility/batch endpoint that enqueues a job and returns job_id.
Workers pull and compute; store results in DB.

### D) “Add vLLM adapter for zoning extraction”
Define a function `extract_zoning_context(text) -> dict` under inference/.
No compiler dependencies.

## Suggested development loop
1) Describe desired behavior + acceptance tests
2) Implement smallest change
3) Run tests
4) Refactor once green
