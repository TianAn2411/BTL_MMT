class Response:
    def __init__(self, request=None):
        self.status_code = 200
        self.reason = "OK"
        self.cookies = {}
        self.request = request

    def set_cookie(self, key, value):
        self.cookies[key] = value

    def build_header(self, content_length):
        # TODO CODE

    def build_response(self, body: bytes):
        # TODO CODE

    def build_notfound(self):
        return (
            b"HTTP/1.1 404 Not Found\r\n"
            b"Content-Type: text/plain\r\n"
            b"Content-Length: 13\r\n"
            b"Connection: close\r\n\r\n"
            b"404 Not Found"
        )