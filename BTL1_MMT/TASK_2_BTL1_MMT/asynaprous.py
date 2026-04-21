import inspect
from backend import create_backend

class AsynapRous:
    def __init__(self):
        self.routes = {}
        self.ip = None
        self.port = None

    def prepare_address(self, ip, port):
        self.ip = ip
        self.port = port

    def route(self, path, methods=['GET']):
        def decorator(func):
            for method in methods:
                self.routes[(method.upper(), path)] = func

            func._route_path = path
            func._route_methods = methods

            if inspect.iscoroutinefunction(func):
                async def async_wrapper(*args, **kwargs):
                    print(f"[AsynapRous] ASYNC {methods} {path}")
                    return await func(*args, **kwargs)
                return async_wrapper
            else:
                def sync_wrapper(*args, **kwargs):
                    print(f"[AsynapRous] SYNC {methods} {path}")
                    return func(*args, **kwargs)
                return sync_wrapper

        return decorator

    def run(self):
        if not self.ip or not self.port:
            raise Exception("Call prepare_address first")

        create_backend(self.ip, self.port, self.routes)