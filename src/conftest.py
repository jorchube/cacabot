import pytest
import responses

from src.cacabot import Cacabot


@pytest.fixture
def auth_token():
    return "AUTH_TOKEN"


@pytest.fixture
def test_bot(auth_token):
    return Cacabot(auth_token=auth_token)


@pytest.fixture
def mock_responses():
    with responses.RequestsMock() as r:
        yield r
