import base64
import uuid

USERS = {
    "admin": "123",
    "user": "abc"
}

SESSIONS = {}

def check_cookie(headers):
    # TODO CODE

    return None

def require_auth(func):
    async def async_wrapper(*args, **kwargs):
        headers = kwargs.get("headers", {})

        user = check_cookie(headers)

        if not user:
            return (
                b"HTTP/1.1 401 Unauthorized\r\n"
                b"WWW-Authenticate: Basic realm=\"Login Required\"\r\n"
                b"Content-Length: 12\r\n\r\nUnauthorized"
            )

        return await func(*args, **kwargs)

    def sync_wrapper(*args, **kwargs):
        headers = kwargs.get("headers", {})

        user = check_cookie(headers) or check_basic_auth(headers)

        if not user:
            return (
                b"HTTP/1.1 401 Unauthorized\r\n"
                b"WWW-Authenticate: Basic realm=\"Login Required\"\r\n"
                b"Content-Length: 12\r\n\r\nUnauthorized"
            )

        return func(*args, **kwargs)

    import inspect
    if inspect.iscoroutinefunction(func):
        return async_wrapper
    return sync_wrapper


def create_session(username):
    session_id = str(uuid.uuid4())
    SESSIONS[session_id] = username
    return session_id