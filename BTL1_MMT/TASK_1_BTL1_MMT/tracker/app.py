from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import time

app = FastAPI(title="Tracker")

peers = {}

@app.post("/register")
async def register_peer(request: Request):
    data = await request.json()
    ip = data.get("ip")
    port = data.get("port")
    name = data.get("name", f"{ip}:{port}")
    peers[name] = {"ip": ip, "port": port, "last_seen": time.time()}
    return JSONResponse({"status": "registered", "peers": list(peers.values())})

@app.get("/peers")
def list_peers():
    return JSONResponse({"peers": list(peers.values())})
