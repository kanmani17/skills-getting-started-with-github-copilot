import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture
def reset_activities():
    """Reset the in-memory activity data before and after each test."""
    original_state = copy.deepcopy(app_module.activities)

    app_module.activities.clear()
    app_module.activities.update(original_state)

    yield app_module.activities

    app_module.activities.clear()
    app_module.activities.update(original_state)


@pytest.fixture
def client():
    with TestClient(app_module.app) as test_client:
        yield test_client
