import pytest

from src.api_requests import create_new_user


@pytest.fixture
def create_user():
    user = create_new_user()
    return user
