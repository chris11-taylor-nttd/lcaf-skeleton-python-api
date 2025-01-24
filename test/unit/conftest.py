# conftest.py holds the fixtures that are used in the unit tests and makes them available to tests in this folder.
import datetime
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from src.app import app
from src.dependencies import people_data, people_storage
from src.models.people import Person


@pytest.fixture
def example_users():
    """This fixture provides a dictionary of example users with fixed UUIDs for testing purposes."""
    return {
        UUID("a11c3000-0000-4000-8000-000000000000"): Person(
            identifier=UUID("a11c3000-0000-4000-8000-000000000000"),
            name="Alice",
            birthday="2001-01-01",
        ),
        UUID("b0b00000-0000-4000-8000-000000000000"): Person(
            identifier=UUID("b0b00000-0000-4000-8000-000000000000"),
            name="Bob",
            birthday="2002-02-02",
        ),
        UUID("c4a211e0-0000-4000-8000-000000000000"): Person(
            identifier=UUID("c4a211e0-0000-4000-8000-000000000000"),
            name="Charlie",
            birthday="2003-03-03",
        ),
    }


@pytest.fixture
def example_users_response(example_users):
    """Transforms the example users into a dictionary of dictionaries for comparison in tests."""
    return {
        str(k): {att_key: str(att_val) for att_key, att_val in v.model_dump().items()}
        for k, v in example_users.items()
    }


@pytest.fixture(scope="function")
def empty_server_client():
    """Fixture to provide a TestClient instance for the FastAPI app without any user data loaded."""
    people_storage.clear()
    yield TestClient(app)


@pytest.fixture(scope="function")
def populated_server_client(example_users):
    """Fixture to prpovid a TestClient instance for the FastAPI app with example user data pre-loaded."""

    async def override_people_data():
        return example_users

    app.dependency_overrides[people_data] = override_people_data
    yield TestClient(app)


@pytest.fixture
def yesterday():
    """Fixture to provide a date object representing yesterday."""
    return datetime.date.today() - datetime.timedelta(days=1)


@pytest.fixture
def today():
    """Fixture to provide a date object representing today."""
    return datetime.date.today()
