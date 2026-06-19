import asyncio
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast_log(self, message: str, message_type: str = "terminal"):
        payload = {"type": message_type, "data": message}
        for connection in self.active_connections:
            try:
                await connection.send_json(payload)
            except Exception:
                pass

    async def execute_and_stream(self, command: str):
        await self.broadcast_log(f"Executing local subprocess: {command}\n", "system")
        
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            async def stream_pipe(pipe, label):
                while True:
                    line = await pipe.readline()
                    if not line:
                        break
                    await self.broadcast_log(line.decode().rstrip(), label)

            await asyncio.gather(
                stream_pipe(process.stdout, "terminal"),
                stream_pipe(process.stderr, "error")
            )
            
            await process.wait()
            await self.broadcast_log(f"\n[Execution Completed with Exit Status {process.returncode}]\n", "system")
        except Exception as e:
            await self.broadcast_log(f"Subprocess failure: {str(e)}", "error")
