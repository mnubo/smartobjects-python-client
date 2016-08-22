ROUTES = {}


def route(method, path):
    def register(handler):
        if method not in ROUTES:
            ROUTES[method] = {}
        ROUTES[method][path] = handler
        return handler
    return register
