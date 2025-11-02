"""Middleware module"""

from uuid import uuid4

from starlette.types import ASGIApp, Receive, Scope, Send

from hello_world.database.sessions import AsyncScopedSession, set_db_session_context


class DatabaseSessionMiddleware:
    def __init__(
        self,
        app: ASGIApp,
    ) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in (
            "http",
            "websocket",
        ):  # pragma: no cover
            await self.app(scope, receive, send)
            return

        session_id = str(uuid4())
        set_db_session_context(session_id=session_id)
        try:
            await self.app(scope, receive, send)
        finally:
            await AsyncScopedSession.remove()  # this includes closing the session as well
            set_db_session_context(session_id=None)