"""Minimal ASGI entry point for the Day 1 foundation."""

from fastapi import FastAPI


def health() -> dict[str, str]:
    """Report HTTP application liveness, not readiness of future MAX systems."""
    return {"status": "ok"}


def create_app() -> FastAPI:
    """Create the health-only MAX application without initializing any engines."""
    app = FastAPI(title="MAX AI OS", docs_url=None, redoc_url=None, openapi_url=None)
    app.add_api_route("/health", health, methods=["GET"])
    return app
