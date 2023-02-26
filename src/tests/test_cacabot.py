class TestCacabot:
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
