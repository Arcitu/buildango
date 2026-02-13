FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml README.md /app/
COPY api /app/api
COPY compiler /app/compiler
COPY db /app/db
COPY storage /app/storage
RUN pip install --no-cache-dir -e .
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]
