from responses import matchers


class TestCacabot:
    def test_it_retrieves_updates_when_no_updates_are_available(
        self, mock_responses, auth_token, test_bot
    ):
        mock_responses.post(
            url=f"https://api.telegram.org/bot{auth_token}/getupdates",
            status=200,
            json={"ok": True, "result": []},
        )

        updates = test_bot.get_updates()

        assert updates == []

    def test_it_retrieves_updates(self, mock_responses, auth_token, test_bot):
        mock_responses.post(
            url=f"https://api.telegram.org/bot{auth_token}/getupdates",
            status=200,
            json={
                "ok": True,
                "result": [
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
                ],
            },
        )

        updates = test_bot.get_updates()

        assert updates == [
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

    def test_it_retrieves_updates_from_the_last_update_offset_available(
        self, mock_responses, auth_token, test_bot
    ):
        mock_responses.post(
            url=f"https://api.telegram.org/bot{auth_token}/getupdates",
            status=200,
            match=[matchers.json_params_matcher({"timeout": 60, "offset": 0})],
            json={
                "ok": True,
                "result": [
                    {"update_id": 803079895, "something": "..."},
                    {"update_id": 803079896, "something": "..."},
                    {"update_id": 803079897, "something": "..."},
                ],
            },
        )

        mock_responses.post(
            url=f"https://api.telegram.org/bot{auth_token}/getupdates",
            status=200,
            match=[matchers.json_params_matcher({"timeout": 60, "offset": 803079898})],
            json={
                "ok": True,
                "result": [{"update_id": 803079898, "something": "..."}],
            },
        )

        updates = test_bot.get_updates()

        assert updates == [
            {"update_id": 803079895, "something": "..."},
            {"update_id": 803079896, "something": "..."},
            {"update_id": 803079897, "something": "..."},
        ]

        updates = test_bot.get_updates()

        assert updates == [{"update_id": 803079898, "something": "..."}]

    def test_it_sends_message_to_chat(self, mock_responses, auth_token, test_bot):
        mock_responses.post(
            url=f"https://api.telegram.org/bot{auth_token}/sendmessage",
            status=200,
            match=[matchers.json_params_matcher({"chat_id": 1234, "text": "Hello!"})],
            json={
                "ok": True,
                "result": [{"update_id": 803079898, "something": "..."}],
            },
        )

        test_bot.send_message_to_chat(1234, "Hello!")
