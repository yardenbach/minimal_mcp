# minimal_mcp

# MCP WS (JSON-RPC) — Summarize + Title

## Local
```bash
pip install -r requirements.txt
python mcp_server.py
```


# DOCKER
```bash
docker build -t minimal_mcp:latest .
docker run --rm -p 8080:8080 \
  -e HF_MODEL=facebook/bart-large-cnn \
  -e HF_TOKEN="" \
  minimal_mcp:latest
```
in other terminal:
```bash
WS_URL=ws://localhost:8080 python agent_as_client.py "החצוצרן וזמר הג'אז המפורסם, לואי ארמסטרונג, סבל מעוני רב בילדותו. אביו נטש את המשפחה כשארמסטרונג היה תינוק, ואמו נאלצה לעסוק בזנות כדי להתקיים. ארמסטרונג נאלץ להיאבק על קיומו כילד קטן. בני משפחת קרנופסקי, משפחה יהודית שהיגרה מליטא, ריחמו על הנער – ונתנו לו עבודות שונות בעסק ההובלה שהיה ברשותם. אֵם המשפחה התעקשה בכל יום שארמסטרונג לא יחזור לביתו לפני שאכל אצלה ארוחה מלאה. הקורנית הראשונה של ארמסטרונג נרכשה עבורו על ידי משפחת קרנופסקי. כהוקרה על היחס החם והתמיכה, ענד ארמסטרונג על צווארו, עד יומו האחרון, שרשרת ועליה מגן דוד."
```
