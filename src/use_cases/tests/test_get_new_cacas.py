from src.use_cases import get_new_cacas


class TestGetNewCacas:
    def test_it_gets_new_cacas_for_empty_updates(self, mock_responses, auth_token, test_bot):
        mock_responses.post(
            url=f"https://api.telegram.org/bot{auth_token}/getupdates",
            status=200,
            json={
                "ok": True,
                "result": []
            }
        )

        new_cacas = get_new_cacas.do(test_bot)

        assert len(new_cacas) == 0

    def test_it_gets_new_cacas_for_one_new_update(self, mock_responses, auth_token, test_bot):
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
                                "first_name": "Pepa"
                            },
                            "chat": {
                                "id": -859646311,
                                "title": "AwesomeGroup",
                                "type": "group",
                                "all_members_are_administrators": True
                            },
                            "date": 1677331026,
                            "text": "💩"
                        }
                    },
                ]
            }
        )

        new_cacas = get_new_cacas.do(test_bot)

        assert len(new_cacas) == 1
        caca = new_cacas[0]

        assert caca.update_offset == 803079895
        assert caca.chat_id == "-859646311"
        assert caca.chat_name == "AwesomeGroup"
        assert caca.chat_member_id == "5963758344"
        assert caca.chat_member_name == "Pepa"
