from unittest.mock import Mock

import pytest

from actions.participate_in_conversation import ParticipateInConversation
from ai_client import AIClientException
from conversation_message import ConversationMessage


class TestParticipatInConversation:
    def test_it_participates_in_conversation(self):
        ai_client = Mock()
        ai_client.send.return_value = "a response"

        cacabot = Mock()

        conversation_message = ConversationMessage(
            update_id=890,
            chat_id=12345,
            message="A conversation message",
            chat_member_id=678,
            chat_member_name="asdf"
        )

        ParticipateInConversation(cacabot=cacabot, ai_client=ai_client, participation_probability=1).do(conversation_message)

        ai_client.send.assert_called_once_with(
            text="A conversation message"
        )

        cacabot.send_message_to_chat.assert_called_once_with(
            chat_id=12345,
            message="a response"
        )

    def test_it_fails_participating_in_conversation(self):
        ai_client = Mock()
        ai_client.send.side_effect = AIClientException

        cacabot = Mock()

        conversation_message = ConversationMessage(
            update_id=890,
            chat_id=12345,
            message="A conversation message",
            chat_member_id=678,
            chat_member_name="asdf"
        )

        ParticipateInConversation(cacabot=cacabot, ai_client=ai_client, participation_probability=1).do(conversation_message)

        ai_client.send.assert_called_once_with(
            text="A conversation message"
        )

        cacabot.send_message_to_chat.assert_not_called()
