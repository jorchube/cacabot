from unittest import mock

import pytest
from freezegun import freeze_time

from actions.participate_in_conversation import ParticipateInConversation
from ai_client import AIClient, AIClientException, AIClientResponse
from cacabot import Cacabot
from conversation_engine import ConversationEngine
from conversation_message import ConversationMessage


class TestParticipatInConversation:
    def test_it_participates_in_conversation(self):
        ai_client = mock.create_autospec(AIClient)
        ai_client.send.return_value = AIClientResponse(
            response_message="a response", conversation_context=[1, 2]
        )

        cacabot = mock.create_autospec(Cacabot)

        conversation_message = ConversationMessage(
            update_id=890,
            chat_id=12345,
            message="A conversation message",
            chat_member_id=678,
            chat_member_name="asdf",
        )
        conversation_engine = ConversationEngine(
            ai_client=ai_client, botname=["botname"]
        )
        ParticipateInConversation(
            cacabot=cacabot,
            conversation_engine=conversation_engine,
            participation_probability=1,
        ).do(conversation_message)

        ai_client.send.assert_called_once_with(
            text="A conversation message", context=None
        )

        cacabot.send_message_to_chat.assert_called_once_with(
            chat_id=12345, message="a response"
        )

    def test_it_fails_participating_in_conversation(self):
        ai_client = mock.create_autospec(AIClient)
        ai_client.send.side_effect = AIClientException

        cacabot = mock.create_autospec(Cacabot)

        conversation_message = ConversationMessage(
            update_id=890,
            chat_id=12345,
            message="A conversation message",
            chat_member_id=678,
            chat_member_name="asdf",
        )

        conversation_engine = ConversationEngine(
            ai_client=ai_client, botname=["botname"]
        )
        ParticipateInConversation(
            cacabot=cacabot,
            conversation_engine=conversation_engine,
            participation_probability=1,
        ).do(conversation_message)

        ai_client.send.assert_called_once_with(
            text="A conversation message", context=None
        )

        cacabot.send_message_to_chat.assert_not_called()

    @pytest.mark.parametrize("botname", ["name1", "name2"])
    def test_participates_when_mentioned(self, botname):
        ai_client = mock.create_autospec(AIClient)
        ai_client.send.return_value = AIClientResponse(
            response_message="a response", conversation_context=[1, 2]
        )

        cacabot = mock.create_autospec(Cacabot)

        conversation_message = ConversationMessage(
            update_id=890,
            chat_id=12345,
            message="A conversation message @botname",
            chat_member_id=678,
            chat_member_name="asdf",
            mention=botname,
        )

        conversation_engine = ConversationEngine(
            ai_client=ai_client, botname=["name1", "name2"]
        )
        ParticipateInConversation(
            cacabot=cacabot,
            conversation_engine=conversation_engine,
            participation_probability=0,
        ).do(conversation_message)

        ai_client.send.assert_called_once_with(
            text="A conversation message @botname", context=None
        )

        cacabot.send_message_to_chat.assert_called_once_with(
            chat_id=12345, message="a response"
        )

    def test_continues_conversation_within_3_minutes_from_an_intervention(self):
        ai_client = mock.create_autospec(AIClient)
        ai_client.send.return_value = AIClientResponse(
            response_message="a response", conversation_context=[1, 2]
        )

        cacabot = mock.create_autospec(Cacabot)

        conversation_message_1 = ConversationMessage(
            update_id=890,
            chat_id=12345,
            message="A conversation message @botname",
            chat_member_id=678,
            chat_member_name="asdf",
            mention="botname",
        )
        conversation_message_2 = ConversationMessage(
            update_id=890,
            chat_id=12345,
            message="A follow up",
            chat_member_id=678,
            chat_member_name="asdf",
        )
        conversation_message_3 = ConversationMessage(
            update_id=890,
            chat_id=12345,
            message="forgotten conversation",
            chat_member_id=678,
            chat_member_name="asdf",
        )

        conversation_engine = ConversationEngine(
            ai_client=ai_client, botname=["botname"]
        )

        with freeze_time("2023-06-06T16:00:00"):
            ParticipateInConversation(
                cacabot=cacabot,
                conversation_engine=conversation_engine,
                participation_probability=1,
            ).do(conversation_message_1)

        with freeze_time("2023-06-06T16:02:59"):
            ParticipateInConversation(
                cacabot=cacabot,
                conversation_engine=conversation_engine,
                participation_probability=0,
            ).do(conversation_message_2)

        with freeze_time("2023-06-06T16:06:00"):
            ParticipateInConversation(
                cacabot=cacabot,
                conversation_engine=conversation_engine,
                participation_probability=0,
            ).do(conversation_message_3)

        assert ai_client.send.call_count == 2

        ai_client.send.assert_has_calls(
            [
                mock.call(text="A conversation message @botname", context=None),
                mock.call(text="A follow up", context=[1, 2]),
            ]
        )

        cacabot.send_message_to_chat.assert_has_calls(
            [
                mock.call(chat_id=12345, message="a response"),
                mock.call(chat_id=12345, message="a response"),
            ]
        )
