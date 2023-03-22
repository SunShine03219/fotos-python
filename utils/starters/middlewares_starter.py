from typing import Callable, List

from fastapi import FastAPI
from starlette.exceptions import HTTPException

from utils.middlewares.exception_handler import internal_exception_handler


class MiddlewareDefiner:
    def __init__(self):
        self._handlers: List[Callable] = [internal_exception_handler]

    def define_handlers(self, app: FastAPI):
        for handler in self._handlers:
            app.add_exception_handler(HTTPException, handler)
