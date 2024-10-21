import pytest

from src.requests_api import create_new_user


@pytest.fixture
def create_user():
    user = create_new_user()
    return user
