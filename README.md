# minimal_mcp

# MCP WS (JSON-RPC) — Summarize + Title

## Local
```bash
pip install -r requirements.txt
python mcp_server.py
```
```bash
WS_URL=ws://localhost:8080 python agent.py "טקסט לבדיקה"
```

# DOCKER
docker build -t minimal_mcp:latest .
docker run --rm -p 8080:8080 \
  -e HF_MODEL=facebook/bart-large-cnn \
  -e HF_TOKEN="" \
  minimal_mcp:latest
