FROM python:3.11-slim

WORKDIR /app

# System deps needed by pymupdf / psycopg2 at build time
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements-render.txt .

# Lean install: no torch / sentence-transformers here. That combo alone
# adds 1-2GB+ and enough runtime RAM to OOM a free-tier instance the moment
# the embedding model loads. See requirements-render.txt for details.
# The full requirements.txt (with ML deps) is still available in the repo
# for local dev or a higher-RAM deploy - just swap the COPY line above and
# set ENABLE_SEMANTIC_MATCH=true below.
RUN pip install --no-cache-dir -r requirements-render.txt

COPY . .

# Semantic (embedding-based) skill matching is disabled by default in this
# image; backend/models/semantic_matcher.py falls back automatically to a
# lightweight difflib-based similarity check instead. Flip to "true" only
# if you've switched to the full requirements.txt with torch installed.
ENV ENABLE_SEMANTIC_MATCH=false

# Render (and platforms like Northflank) inject PORT; default to 8000 for local runs
ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "uvicorn backend.api.main:app --host 0.0.0.0 --port ${PORT}"]