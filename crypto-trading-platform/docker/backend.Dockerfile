FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install psycopg2-binary # Required for Postgres connection

# Copy source code
COPY . /app/crypto-trading-platform

# Expose FastAPI port
EXPOSE 8000

WORKDIR /app/crypto-trading-platform

CMD ["uvicorn", "backend.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
