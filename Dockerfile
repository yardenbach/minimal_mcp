FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends tini && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch==2.3.1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY mcp_server.py .

ENV HOST=0.0.0.0 \
    PORT=8080 \
    HF_MODEL=facebook/bart-large-cnn \
    HF_TOKEN=""

EXPOSE 8080

ENTRYPOINT ["/usr/bin/tini","--"]
CMD ["python","mcp_server.py"]
