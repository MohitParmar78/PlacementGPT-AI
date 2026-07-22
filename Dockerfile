FROM python:3.11-slim

WORKDIR /app

# System deps needed by pymupdf / psycopg2 at build time
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install CPU-only torch first (the default PyPI wheel pulls CUDA libs
# and adds 1-2GB+ to the image, which will blow past free-tier build limits)
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Install everything else, skipping torch since it's already installed above
RUN grep -v "^torch$" requirements.txt > requirements.nogpu.txt \
    && pip install --no-cache-dir -r requirements.nogpu.txt

COPY . .

# Northflank injects PORT; default to 8000 for local runs
ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "uvicorn backend.api.main:app --host 0.0.0.0 --port ${PORT}"]