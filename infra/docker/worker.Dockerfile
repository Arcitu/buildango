FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml README.md /app/
COPY workers /app/workers
COPY compiler /app/compiler
RUN pip install --no-cache-dir -e .
CMD ["python", "-c", "print('worker image stub')"]
