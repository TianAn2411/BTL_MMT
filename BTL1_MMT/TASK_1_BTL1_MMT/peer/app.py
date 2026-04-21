from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx
import os
import asyncio
from datetime import datetime

app = FastAPI(title="Peer")

# --- Environment variables ---
TRACKER_URL = os.getenv("TRACKER_URL", "http://tracker:9001")
PEER_NAME = os.getenv("PEER_NAME", "peerX")
PEER_PORT = int(os.getenv("PEER_PORT", 9002))
SELF_IP = PEER_NAME

connected_peers = []
channels = {"general": []}  # [(sender, msg, time)]

# --- Mount static files ---
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# --- HTML page ---
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={"name": PEER_NAME}
    )


# --- Register with tracker ---
@app.post("/register")
async def register_peer():
    async with httpx.AsyncClient() as client:
        await client.post(f"{TRACKER_URL}/register",
                          json={"ip": SELF_IP, "port": PEER_PORT, "name": PEER_NAME})
    return JSONResponse({"status": "registered"})

# --- Get peer list from tracker ---
@app.get("/peers")
async def get_peers():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{TRACKER_URL}/peers")
        data = r.json()
        global connected_peers
        connected_peers = data["peers"]
    return JSONResponse(data)

# --- Broadcast a message to all peers ---
@app.post("/broadcast")
async def broadcast_message(request: Request):
    data = await request.json()
    msg = data["msg"]
    now = datetime.now().strftime("%H:%M:%S")

    # Save self message locally
    channels["general"].append((PEER_NAME, msg, now))

    # Send to others
    tasks = []
    for peer in connected_peers:
        if peer["port"] != PEER_PORT:
            url = f"http://{peer['ip']}:{peer['port']}/message"
            tasks.append(send_msg(url, msg, now))
    await asyncio.gather(*tasks)
    return JSONResponse({"status": "broadcasted"})

async def send_msg(url, msg, timestamp):
    async with httpx.AsyncClient() as client:
        try:
            await client.post(url, json={"from": PEER_NAME, "msg": msg, "time": timestamp})
        except Exception:
            pass

# --- Receive message ---
@app.post("/message")
async def receive_message(request: Request):
    data = await request.json()
    sender = data["from"]
    msg = data["msg"]
    time = data.get("time", datetime.now().strftime("%H:%M:%S"))

    print(f"[{time}] {sender} → {PEER_NAME}: {msg}")
    channels["general"].append((sender, msg, time))
    return JSONResponse({"status": "received"})

# --- Get stored messages ---
@app.get("/messages")
async def get_messages():
    formatted = [
        {"sender": s, "msg": m, "time": t}
        for (s, m, t) in channels["general"]
    ]
    return JSONResponse({"messages": formatted})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PEER_PORT)
