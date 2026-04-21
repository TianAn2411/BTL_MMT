import json
import asyncio
import inspect
from request import Request
from response import Response

class HttpAdapter:
    def __init__(self, ip, port, conn, connaddr, routes):
        self.ip = ip
        self.port = port
        self.conn = conn
        self.connaddr = connaddr
        self.routes = routes
        self.request = Request()

    def handle_client(self, conn, addr, routes):
        msg = conn.recv(4096).decode()

        if not msg:
            conn.close()
            return

        req = self.request
        req.prepare(msg, routes)

        print(f"[HttpAdapter] {req.method} {req.path}")

        if req.hook:
            handler = req.hook

            kwargs = {
                "headers": req.headers,
                "body": req.body
            }

            if inspect.iscoroutinefunction(handler):
                response_body = asyncio.run(handler(**kwargs))
            else:
                response_body = handler(**kwargs)
        else:
            conn.sendall(Response().build_notfound())
            conn.close()
            return

        resp = Response(req)
        if req.path == "/login" and req.method == "POST":
            try:
                data = json.loads(response_body)
                session_id = data.get("session")

                if session_id:
                    resp.set_cookie("session", session_id)

                    del data["session"]
                    response_body = json.dumps(data).encode()
            except:
                pass


        response = resp.build_response(response_body)

        conn.sendall(response)
        conn.close()