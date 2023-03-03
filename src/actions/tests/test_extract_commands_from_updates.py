from actions import extract_commands_from_updates


class TestExtractCommandsFromUpdates:
    def test_it_gets_commands_from_empy_updates(self):
        updates = []

        commands = extract_commands_from_updates.do(updates)

        assert len(commands) == 0

    def test_it_gets_commands_from_one_update(self):
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
            }
        ]

        commands = extract_commands_from_updates.do(updates)

        assert len(commands) == 1

        command = commands[0]
        assert command.update_id == 803079927
        assert command.chat_id == 344365000
        assert command.command == "/a_command"
        assert command.chat_member_id == 344365000
        assert command.chat_member_name == "John"

    def test_it_gets_commands_from_many_updates(self):
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
                "update_id": 803079929,
                "message": {
                    "message_id": 49,
                    "from": {
                        "id": 344365001,
                        "is_bot": False,
                        "first_name": "Jane",
                        "last_name": "Doe",
                        "language_code": "en",
                    },
                    "chat": {
                        "id": 344365001,
                        "first_name": "Jane",
                        "last_name": "Doe",
                        "type": "private",
                    },
                    "date": 1677426214,
                    "text": "/another_command",
                    "entities": [{"offset": 0, "length": 5, "type": "bot_command"}],
                },
            },
        ]

        commands = extract_commands_from_updates.do(updates)

        assert len(commands) == 2

        command = commands[0]
        assert command.update_id == 803079927
        assert command.chat_id == 344365000
        assert command.command == "/a_command"
        assert command.chat_member_id == 344365000
        assert command.chat_member_name == "John"

        command = commands[1]
        assert command.update_id == 803079929
        assert command.chat_id == 344365001
        assert command.command == "/another_command"
        assert command.chat_member_id == 344365001
        assert command.chat_member_name == "Jane"

    def test_it_ignores_non_commands_messages_from_many_updates(self):
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
                    "text": "This is not a command",
                },
            },
        ]

        commands = extract_commands_from_updates.do(updates)

        assert len(commands) == 1

        command = commands[0]
        assert command.update_id == 803079927
        assert command.chat_id == 344365000
        assert command.command == "/a_command"
        assert command.chat_member_id == 344365000
        assert command.chat_member_name == "John"
