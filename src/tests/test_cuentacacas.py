import pytest
from responses import matchers

from main import get_and_handle_updates


@pytest.mark.usefixtures("in_memory_repository")
class TestCuentacacas:
    def test_it_sends_nothing_when_there_are_no_results(
        self, mock_responses, auth_token, test_bot
    ):
        mock_responses.post(
            url=f"https://api.telegram.org/bot{auth_token}/getupdates",
            status=200,
            json={
                "ok": True,
                "result": [
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
                            "text": "/cuentacacas",
                            "entities": [{"offset": 0, "length": 5, "type": "bot_command"}],
                        },
                    }
                ],
            },
        )

        get_and_handle_updates(test_bot)

    def test_it_sends_cuentacacas_command_response_when_there_are_results(
        self, mock_responses, auth_token, test_bot
    ):
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
                                "id": -859646311,
                                "first_name": "John",
                                "last_name": "Doe",
                                "type": "private",
                            },
                            "date": 1677426214,
                            "text": "/cuentacacas",
                            "entities": [{"offset": 0, "length": 5, "type": "bot_command"}],
                        },
                    }
                ],
            },
        )

        mock_responses.post(
            url=f"https://api.telegram.org/bot{auth_token}/sendmessage",
            status=200,
            match=[matchers.json_params_matcher({"chat_id": -859646311, "text": "Total de cacas:\n\nPepa: 1"})],
            json={
                "ok": True,
                "result": [{"update_id": 803079898, "something": "..."}],
            },
        )

        get_and_handle_updates(test_bot)

    def test_it_sends_cuentacacas_command_response_when_there_are_results_for_several_users(
        self, mock_responses, auth_token, test_bot
    ):
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
                    {
                        "update_id": 803079896,
                        "message": {
                            "message_id": 14,
                            "from": {
                                "id": 596370000,
                                "is_bot": False,
                                "first_name": "John",
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
                        "update_id": 803079000,
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
                                "id": -859646311,
                                "first_name": "John",
                                "last_name": "Doe",
                                "type": "private",
                            },
                            "date": 1677426214,
                            "text": "/cuentacacas",
                            "entities": [{"offset": 0, "length": 5, "type": "bot_command"}],
                        },
                    }
                ],
            },
        )

        mock_responses.post(
            url=f"https://api.telegram.org/bot{auth_token}/sendmessage",
            status=200,
            match=[matchers.json_params_matcher({"chat_id": -859646311, "text": "Total de cacas:\n\nPepa: 2\nJohn: 1"})],
            json={
                "ok": True,
                "result": [{"update_id": 803079898, "something": "..."}],
            },
        )

        get_and_handle_updates(test_bot)


    def test_it_sends_cuentacacas_command_response_when_there_are_results_ignoring_other_chats(
        self, mock_responses, auth_token, test_bot
    ):
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
                    {
                        "update_id": 803079000,
                        "message": {
                            "message_id": 14,
                            "from": {
                                "id": 5963758344,
                                "is_bot": False,
                                "first_name": "Pepa",
                            },
                            "chat": {
                                "id": -666666666,
                                "title": "AnotherGroup",
                                "type": "group",
                                "all_members_are_administrators": True,
                            },
                            "date": 1677331026,
                            "text": "💩",
                        },
                    },
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
                                "id": -859646311,
                                "first_name": "John",
                                "last_name": "Doe",
                                "type": "private",
                            },
                            "date": 1677426214,
                            "text": "/cuentacacas",
                            "entities": [{"offset": 0, "length": 5, "type": "bot_command"}],
                        },
                    }
                ],
            },
        )

        mock_responses.post(
            url=f"https://api.telegram.org/bot{auth_token}/sendmessage",
            status=200,
            match=[matchers.json_params_matcher({"chat_id": -859646311, "text": "Total de cacas:\n\nPepa: 1"})],
            json={
                "ok": True,
                "result": [{"update_id": 803079898, "something": "..."}],
            },
        )

        get_and_handle_updates(test_bot)
