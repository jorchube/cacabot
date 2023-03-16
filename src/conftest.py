import pytest
import responses
from actions import spontaneous_caca_reaction

from cacabot import Cacabot
from persistence.repository import Repository


@pytest.fixture(autouse=True)
def no_spontaneous_caca_reactions():
    spontaneous_caca_reaction.REACTION_PROBABILITY = 0


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


@pytest.fixture
def in_memory_repository():
    Repository.initialize(in_memory=True)
    return Repository.get()
