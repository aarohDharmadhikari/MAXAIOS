"""Verify the installed package and the real HTTP application boundary."""

from importlib import import_module

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from max.api.app import create_app


@pytest.mark.parametrize(
    "module_name", ["max", "max.api", "max.core", "max.reasoning", "max.llm", "max.cli"]
)
def test_package_imports(module_name: str) -> None:
    assert import_module(module_name).__name__ == module_name


def test_factory_creates_independent_applications() -> None:
    app = create_app()
    assert isinstance(app, FastAPI)
    assert app is not create_app()


def test_health_after_application_startup() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {"status": "ok"}


def test_health_is_read_only() -> None:
    with TestClient(create_app()) as client:
        assert client.post("/health").status_code == 405


def test_unknown_route_is_not_available() -> None:
    with TestClient(create_app()) as client:
        assert client.get("/unknown").status_code == 404
