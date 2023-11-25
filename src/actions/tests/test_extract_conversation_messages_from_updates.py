from actions import extract_conversation_messages_from_updates


class TestExtractConversationUpdatesFromMessages:
    def test_gets_conversation_messages_from_empty_updates(self):
        updates = []

        conversation_messages = extract_conversation_messages_from_updates.do(updates)

        assert len(conversation_messages) == 0


    def test_gets_conversation_messages_from_updates(self):
        updates = [
            {
                "update_id": 803079927,
                "message": {
                    "message_id": 46,
                    "from": {
                        "id": 344365000,
                        "is_bot": False,
                        "first_name": "John",
                        "last_name": "Doe",
                        "language_code": "en",
                    },
                    "chat": {
                        "id": 344365000,
                        "first_name": "John",
                        "last_name": "Doe",
                        "type": "private",
                    },
                    "date": 1677426214,
                    "text": "/a_command",
                    "entities": [{"offset": 0, "length": 5, "type": "bot_command"}],
                },
            },
            {
                "update_id": 803079925,
                "message": {
                    "message_id": 59,
                    "from": {
                        "id": 344365000,
                        "is_bot": False,
                        "first_name": "John",
                        "last_name": "Doe",
                        "language_code": "en",
                    },
                    "chat": {
                        "id": 344365000,
                        "first_name": "John",
                        "last_name": "Doe",
                        "type": "private",
                    },
                    "date": 1677426214,
                    "text": "Conversation message 1",
                },
            },
            {
                "update_id": 803079929,
                "message": {
                    "message_id": 49,
                    "from": {
                        "id": 344365000,
                        "is_bot": False,
                        "first_name": "John",
                        "last_name": "Doe",
                        "language_code": "en",
                    },
                    "chat": {
                        "id": 344365000,
                        "first_name": "John",
                        "last_name": "Doe",
                        "type": "private",
                    },
                    "date": 1677426214,
                    "text": "💩",
                },
            },
            {
                "update_id": 803079925,
                "message": {
                    "message_id": 59,
                    "from": {
                        "id": 344365000,
                        "is_bot": False,
                        "first_name": "John",
                        "last_name": "Doe",
                        "language_code": "en",
                    },
                    "chat": {
                        "id": 344365000,
                        "first_name": "John",
                        "last_name": "Doe",
                        "type": "private",
                    },
                    "date": 1677426214,
                    "text": "Conversation message 2",
                },
            },
        ]

        conversation_messages = extract_conversation_messages_from_updates.do(updates)

        conversation_message = conversation_messages[0]
        assert conversation_message.message == "Conversation message 1"

        conversation_message = conversation_messages[1]
        assert conversation_message.message == "Conversation message 2"
