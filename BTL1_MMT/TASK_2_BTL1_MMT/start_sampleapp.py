import json
from asynaprous import AsynapRous
from auth import create_session, USERS, require_auth

app = AsynapRous()

@app.route('/login', methods=['POST'])
def login(headers="guest", body="anonymous"):
    try:
        data = json.loads(body)
        username = data.get("username")
        password = data.get("password")
    except:
        return json.dumps({"error": "invalid json"}).encode()

    if USERS.get(username) != password:
        return json.dumps({"error": "unauthorized"}).encode()

    session_id = create_session(username)

    return json.dumps({
        "message": "login success",
        "session": session_id
    }).encode()

@app.route('/echo', methods=['POST'])
@require_auth
def echo(headers="guest", body="anonymous"):
    try:
        data = json.loads(body)
        return json.dumps({"received": data}).encode()
    except:
        return json.dumps({"error": "invalid json"}).encode()

@app.route('/hello', methods=['PUT'])
@require_auth
async def hello(headers, body):
    print("[App] async hello")
    return json.dumps({"msg": "hello async"}).encode()

if __name__ == "__main__":
    app.prepare_address("0.0.0.0", 2026)
    app.run()