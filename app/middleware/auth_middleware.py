from __future__ import annotations

import os
from typing import Callable, Iterable, Awaitable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.utils.auth import get_user_id_from_token


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        protected_prefixes: Iterable[str] | None = None,
    ):
        super().__init__(app)
        self.protected_prefixes = list(protected_prefixes)

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]):
        if request.method == "OPTIONS":
            return await call_next(request)

        path = request.url.path

        if not any(path.startswith(prefix) for prefix in self.protected_prefixes):
            return await call_next(request)

        auth_header = request.headers.get("Authorization", "")
        scheme, _, token = auth_header.partition(" ")
        if scheme.lower() != "bearer" or not token:
            return JSONResponse(status_code=401, content={"detail": "Not authenticated"})

        try:
            user_id = get_user_id_from_token(token)
            request.state.user_id = user_id
        except Exception:
            return JSONResponse(status_code=403, content={"detail": "Invalid or expired token"})

        return await call_next(request)
