from unittest.mock import Mock

import pytest
import responses

from actions import participate_in_conversation, spontaneous_caca_reaction
from ai_client import AIClientException
from cacabot import Cacabot
from persistence.repository import Repository


@pytest.fixture(autouse=True)
def no_spontaneous_caca_reactions():
    spontaneous_caca_reaction.REACTION_PROBABILITY = 0


@pytest.fixture(autouse=True)
def no_conversation_participation():
    participate_in_conversation.PARTICIPATION_PROBABILITY = 0


@pytest.fixture
def auth_token():
    return "AUTH_TOKEN"


@pytest.fixture
def test_bot(auth_token):
    return Cacabot(auth_token=auth_token)


@pytest.fixture
def null_ai_client():
    mock = Mock()
    mock.send.side_effect = AIClientException
    return mock

@pytest.fixture
def mock_responses():
    with responses.RequestsMock() as r:
        yield r


@pytest.fixture
def in_memory_repository():
    Repository.initialize(in_memory=True)
    return Repository.get()
