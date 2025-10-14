import os, sys, json, asyncio
from mcp.client import MCPClient   

WS_URL = os.getenv("WS_URL", "ws://localhost:8080")

async def main():
    if len(sys.argv) < 2:
        print('usage: python agent_mcpclient.py"')
        return
    text = sys.argv[1]

    client = MCPClient(WS_URL)
    await client.connect()                   
   
    tools = await client.list_tools()
    print("[agent] tools:", tools)

    s = await client.call_tool("summarize_text", {"text": text})
    summary = (s or {}).get("summary", "")

    t = await client.call_tool("title_from_text", {"text": summary or text, "max_words": 30})
    title = (t or {}).get("title", "No title")

    print(json.dumps({"title": title, "summary": summary}, ensure_ascii=False, indent=2))

    await client.close()                     

if __name__ == "__main__":
    asyncio.run(main())
