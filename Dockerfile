
# Stage build
FROM python:3.12-slim AS builder
RUN pip install uv

ENV UV_LINK_MODE=copy \ 
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project
COPY . .

RUN uv sync --frozen

# Stage FINAL RUNNER
FROM python:3.12-slim AS runner
WORKDIR /app
COPY --from=builder /app/app /app
COPY --from=builder /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"
ENV PORT=8000

CMD ["sh","-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}" ]




