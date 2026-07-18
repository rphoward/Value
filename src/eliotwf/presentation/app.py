"""Minimal Starlette app factory for local scaffold smoke."""

from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route


async def health(_request):
    return PlainTextResponse("ok")


def create_app() -> Starlette:
    return Starlette(routes=[Route("/health", health)])


app = create_app()
