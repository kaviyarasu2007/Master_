import os
import asyncio
import httpx
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .safety import SecurityController
from .websocket import ConnectionManager

app = FastAPI()
manager = ConnectionManager()
validator = SecurityController()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENROUTER_KEY = "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"
MODEL_ID = "openai/gpt-oss-120b:free"
SKILLS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../skills"))

class PromptRequest(BaseModel):
    message: str

def parse_local_skills() -> str:
    context = "System Capabilities (Anthropic Skills Data):\n"
    if not os.path.exists(SKILLS_DIR):
        return context + "Status: Local capability folder unpopulated.\n"
        
    count = 0
    for root, _, files in os.walk(SKILLS_DIR):
        if "SKILL.md" in files:
            count += 1
            if count <= 10:  # Restricting window size limits context overhead
                try:
                    with open(os.path.join(root, "SKILL.md"), "r", errors="ignore") as f:
                        context += f"\n[Capability Definition]\n{f.read(1000)}\n"
                except Exception:
                    pass
    return context

@app.websocket("/ws/logs")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/api/chat")
async def handle_agent_transaction(request: PromptRequest):
    skills_payload = parse_local_skills()
    
    system_instruction = f"""You are a localized autonomous operations assistant.
    You evaluate system tasks using the following knowledge context:
    {skills_payload}
    
    If local system diagnostics are required, specify exactly one system instruction wrapped inside tags: <cmd>your_command_here</cmd>."""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL_ID,
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": request.message}
        ]
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers, timeout=45.0)
            response_json = response.json()
            ai_text = response_json["choices"][0]["message"]["content"]
        except Exception as e:
            return {"reply": f"API Gateway Transaction Fault: {str(e)}"}

    if "<cmd>" in ai_text and "</cmd>" in ai_text:
        extracted_cmd = ai_text.split("<cmd>")[1].split("</cmd>")[0]
        check = validator.validate_command(extracted_cmd)
        
        if check["status"] == "AUTHORIZED":
            asyncio.create_task(manager.execute_and_stream(check["command"]))
            ai_text += f"\n\n[System Alert: Executing authorized process... View Output Terminal]"
        elif check["status"] == "SIMULATED":
            await manager.broadcast_log(f"SIMULATION RUN: {check['command']}", "system")
            await manager.broadcast_log(f"[Mock Log Output]: Operation simulated successfully under policy restrictions.", "terminal")
            ai_text += f"\n\n[System Alert: Target operation simulated under safety policy constraints.]"
        else:
            await manager.broadcast_log(f"REJECTED COMMAND: {extracted_cmd} -> {check['reason']}", "error")
            ai_text += f"\n\n[System Matrix Error: Action blocked by Security Controller.]"

    return {"reply": ai_text}
