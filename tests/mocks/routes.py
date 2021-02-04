from typing import Callable

ROUTES = {}


def route(method: str, path: str) -> Callable:
    def register(handler: Callable) -> Callable:
        if method not in ROUTES:
            ROUTES[method] = {}
        ROUTES[method][path] = handler
        return handler

    return register
