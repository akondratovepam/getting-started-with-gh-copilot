import copy
from urllib.parse import quote

import pytest

import src.app as app_module
from fastapi.testclient import TestClient

original_activities = copy.deepcopy(app_module.activities)

@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities = copy.deepcopy(original_activities)

@pytest.fixture
def client():
    return TestClient(app_module.app)
