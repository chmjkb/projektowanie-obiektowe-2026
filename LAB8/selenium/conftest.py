"""Wspólne fixtures dla testów Selenium LAB8."""

from __future__ import annotations

import os
import time
import uuid

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,800")
    drv = webdriver.Chrome(options=options)
    drv.implicitly_wait(2)
    yield drv
    drv.quit()


@pytest.fixture
def frontend_url() -> str:
    return os.environ.get("FRONTEND_URL", "http://localhost:5173")


@pytest.fixture
def backend_url() -> str:
    return os.environ.get("BACKEND_URL", "http://localhost:8000")


@pytest.fixture
def unique_user() -> dict[str, str]:
    suffix = uuid.uuid4().hex[:8]
    return {
        "username": f"user_{suffix}",
        "email": f"user_{suffix}@example.com",
        "password": "secret123",
    }


def wait_until(predicate, timeout: float = 5.0, interval: float = 0.1):
    """Prosty helper - czeka aż predicate zwróci truthy lub timeout."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        result = predicate()
        if result:
            return result
        time.sleep(interval)
    return predicate()
