
import asyncio, json, re, os
import websockets
from typing import List, Dict, Any
try:
  from transformers import pipeline
except Exception as _e:
    pipeline = None


### env -- :
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8080"))
HF_TOKEN = os.getenv("HF_TOKEN", "")
HF_MODEL = os.getenv("HF_MODEL", "facebook/bart-large-cnn") 


summarizer_pipeline = pipeline("summarization", model=HF_MODEL, token=HF_TOKEN)
summarizer_generation_pipeline = pipeline("text-generation", model=HF_MODEL, token=HF_TOKEN)

            

def simple_sentences(text: str) -> List[str]:
    parts = re.split(r'(?<=[.!?])\s+|\n+', text.strip())
    return [s.strip() for s in parts if s.strip()]



###### TOOL 1:
def summarize_text(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Summarize using Hugging Face. Prefer 'summarization'; fall back to 'text-generation' with a prompt.
    Falls back to a naive heuristic if no HF pipelines are available.
    result = {'summary': str}
    """
    text = (params.get("text") or "").strip()
    if not text:
      return {"summary": "no text!"}

    try: 
      print("i used summarization")
      summary = summarizer_pipeline(text, max_length=120, min_length=20, do_sample=False)
      if isinstance(summary, list) and summary and "summary_text" in summary[0]:
        return {"summary": summary[0]["summary_text"].strip()}
    except Exception as e:
      print(f"[INFO] summarization failed, will try text-generation: {e}")
      
      try:
        print("i used text-generation")
        prompt = f"Please provide a short and clear summary of the following text:\n\n{text}\n\n. return your anser of 1-3 short sentences as a string that starts with 'Summary:' and then your answer. return only that and no additional text of objects"
        summary = summarizer_generation_pipeline(prompt, max_new_tokens=120, temperature=0.15)
        if isinstance(summary, list) and summary and "generated_text" in summary[0]:
          return {"summary" : summary[0]["generated_text"].strip()}
        return {"summary": str(summary).strip()}
      except Exception as e:
            print(f"[WARN] text-generation failed, will try baseline: {e}")
            return {"summary": "No summary"} # TODO: baseline
      

###### TOOL 2:
def title_from_text(params: Dict[str, Any]) -> Dict[str, Any]:
    """result = {'title': str}"""
    text = params.get("text") or ""
    max_words = int(params.get("max_words", 30))
    
    sents = simple_sentences(text)
    if not sents:
        return {"title": "No title"}
    first = sents[0].split()
    title = " ".join(first[:max_words]) + ("…" if len(first) > max_words else "")
    return {"title": title}



def list_tools(_: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "tools": [
            {"name": "summarize_text", "description": "Summarize a given text", "parameters": {"text": "str"}},
            {"name": "title_from_text", "description": "Generate a title for a given text", "parameters": {"text": "str", "max_words": "int"}}
                 ]
           }


# TOOLS register:
TOOLS = {
    "list_tools": list_tools,
    "summarize_text": summarize_text,
    "title_from_text": title_from_text,
}

async def handler(websocket):
  async for message in websocket:
    try:
      data = json.loads(message)
    except:
      await websocket.send(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error (invalid JSON)"}}))
      continue 

    _id = data.get("id")
    method = data.get("method")
    params = data.get("params") or {}
    if method not in TOOLS:
      await websocket.send(json.dumps({"jsonrpc": "2.0", "id": _id, "error": {"code": -32601, "message": f"Method not found: {method}"}}))
      continue
    
    try:
      result = TOOLS[method](params)
      await websocket.send(json.dumps({"jsonrpc": "2.0", "id": _id, "result": result }))
    except Exception as e:
      await websocket.send(json.dumps({"jsonrpc": "2.0", "id": _id, "error": {"code": -32000, "message": f"Internal error: {e}"}}))
              

async def main():
  async with websockets.serve(handler, HOST, PORT, ping_interval=20, ping_timeout=20):
    print(f"[MCP] MCP Server listening on ws://{HOST}:{PORT}")
    await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
