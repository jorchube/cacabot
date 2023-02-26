from actions import extract_cacas_from_updates


class TestExtractCacasFromUpdates:
    def test_it_gets_new_cacas_for_empty_updates(self):
        updates = list()

        new_cacas = extract_cacas_from_updates.do(updates)

        assert len(new_cacas) == 0

    def test_it_gets_new_cacas_for_one_new_update(self):
        updates = [
            {
                "update_id": 803079895,
                "message": {
                    "message_id": 14,
                    "from": {
                        "id": 5963758344,
                        "is_bot": False,
                        "first_name": "Pepa",
                    },
                    "chat": {
                        "id": -859646311,
                        "title": "AwesomeGroup",
                        "type": "group",
                        "all_members_are_administrators": True,
                    },
                    "date": 1677331026,
                    "text": "💩",
                },
            },
        ]

        new_cacas = extract_cacas_from_updates.do(updates)

        assert len(new_cacas) == 1
        caca = new_cacas[0]

        assert caca.update_id == 803079895
        assert caca.datetime.isoformat() == "2023-02-25T14:17:06+01:00"
        assert caca.chat_id == -859646311
        assert caca.chat_name == "AwesomeGroup"
        assert caca.chat_member_id == 5963758344
        assert caca.chat_member_name == "Pepa"

    def test_it_gets_new_cacas_for_many_new_updates(self):
        updates = [
            {
                "update_id": 803079895,
                "message": {
                    "message_id": 14,
                    "from": {
                        "id": 5963758344,
                        "is_bot": False,
                        "first_name": "Pepa",
                    },
                    "chat": {
                        "id": -859646311,
                        "title": "AwesomeGroup",
                        "type": "group",
                        "all_members_are_administrators": True,
                    },
                    "date": 1677331026,
                    "text": "💩",
                },
            },
            {
                "update_id": 803079896,
                "message": {
                    "message_id": 15,
                    "from": {
                        "id": 9999999999,
                        "is_bot": False,
                        "first_name": "Fulanito",
                    },
                    "chat": {
                        "id": -859646311,
                        "title": "AwesomeGroup",
                        "type": "group",
                        "all_members_are_administrators": True,
                    },
                    "date": 1677331028,
                    "text": "💩",
                },
            },
        ]

        new_cacas = extract_cacas_from_updates.do(updates)

        assert len(new_cacas) == 2
        caca = new_cacas[0]

        assert caca.update_id == 803079895
        assert caca.datetime.isoformat() == "2023-02-25T14:17:06+01:00"
        assert caca.chat_id == -859646311
        assert caca.chat_name == "AwesomeGroup"
        assert caca.chat_member_id == 5963758344
        assert caca.chat_member_name == "Pepa"

        caca = new_cacas[1]
        assert caca.update_id == 803079896
        assert caca.datetime.isoformat() == "2023-02-25T14:17:08+01:00"
        assert caca.chat_id == -859646311
        assert caca.chat_name == "AwesomeGroup"
        assert caca.chat_member_id == 9999999999
        assert caca.chat_member_name == "Fulanito"

    def test_it_gets_new_cacas_for_many_new_updates_ignoring_invalid_text_messages(self):
        updates = [
            {
                "update_id": 803079895,
                "message": {
                    "message_id": 14,
                    "from": {
                        "id": 5963758344,
                        "is_bot": False,
                        "first_name": "Pepa",
                    },
                    "chat": {
                        "id": -859646311,
                        "title": "AwesomeGroup",
                        "type": "group",
                        "all_members_are_administrators": True,
                    },
                    "date": 1677331026,
                    "text": "This caca is not valid 💩",
                },
            },
            {
                "update_id": 803079896,
                "message": {
                    "message_id": 15,
                    "from": {
                        "id": 9999999999,
                        "is_bot": False,
                        "first_name": "Fulanito",
                    },
                    "chat": {
                        "id": -859646311,
                        "title": "AwesomeGroup",
                        "type": "group",
                        "all_members_are_administrators": True,
                    },
                    "date": 1677331028,
                    "text": "Not even a caca here",
                },
            },
        ]

        new_cacas = extract_cacas_from_updates.do(updates)

        assert len(new_cacas) == 0

    def test_it_gets_new_cacas_for_many_new_updates_ignoring_non_text_message_updates(
        self, mock_responses, auth_token, test_bot
    ):
        updates = [
            {"update_id": 803079895, "edited_message": {"stuff": "..."}},
            {
                "update_id": 803079896,
                "message": {
                    "message_id": 15,
                    "from": {
                        "id": 9999999999,
                        "is_bot": False,
                        "first_name": "Fulanito",
                    },
                    "chat": {
                        "id": -859646311,
                        "title": "AwesomeGroup",
                        "type": "group",
                        "all_members_are_administrators": True,
                    },
                    "date": 1677331028,
                    "sticker": "???",
                },
            },
        ]

        new_cacas = extract_cacas_from_updates.do(updates)

        assert len(new_cacas) == 0
