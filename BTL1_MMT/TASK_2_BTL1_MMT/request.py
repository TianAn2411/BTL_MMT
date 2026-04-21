class Request:
    def __init__(self):
        self.method = None
        self.path = None
        self.version = None
        self.headers = {}
        self.body = ""
        self.routes = {}
        self.hook = None
        self.cookies = {}

    def extract_request_line(self, request):
        try:
            line = request.splitlines()[0]
            return line.split()
        except:
            return None, None, None

    def prepare_headers(self, raw_headers):
        headers = {}
        lines = raw_headers.split("\r\n")[1:]

        for line in lines:
            if ": " in line:
                k, v = line.split(": ", 1)
                headers[k.lower()] = v

        return headers

    def fetch_headers_body(self, request):
        parts = request.split("\r\n\r\n", 1)
        headers = parts[0]
        body = parts[1] if len(parts) > 1 else ""
        return headers, body

    def parse_cookies(self):
        cookie_header = self.headers.get("cookie")

        if not cookie_header:
            return

        cookies = {}
        parts = cookie_header.split(";")

        for p in parts:
            if "=" in p:
                k, v = p.strip().split("=", 1)
                cookies[k] = v

        self.cookies = cookies
        
    def prepare(self, request, routes=None):
        # TODO CODE