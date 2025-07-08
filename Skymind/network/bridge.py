import asyncio
import websockets
import threading
import json
from core.router import handle_command
from core.state import telemetry
from flask import Flask, request

# --- WebSocket Handler ---
async def ws_handler(websocket):
    async for msg in websocket:
        handle_command(msg)
        await websocket.send(json.dumps(telemetry))

def start_ws():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    ws_server = websockets.serve(ws_handler, "localhost", 8765)
    loop.run_until_complete(ws_server)
    loop.run_forever()

# --- REST API ---
app = Flask(__name__)

@app.route("/api/command", methods=["POST"])
def command():
    try:
        data = request.get_json()
        handle_command(json.dumps(data))
        return {"status": "ok", "telemetry": telemetry}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def start_rest():
    app.run(port=5000)

# --- Server Boot ---
def start_server():
    threading.Thread(target=start_ws, daemon=True).start()
    threading.Thread(target=start_rest, daemon=True).start()
