import pytest
from responses import matchers
from actions import spontaneous_caca_reaction

from main import get_and_handle_updates


@pytest.mark.usefixtures("in_memory_repository")
class TestSpontaneousCacaReaction:

    @pytest.mark.parametrize(
        ("configured_reaction", "expected_response"),
        [
            ("A configured reaction to a caca from {name}", "A configured reaction to a caca from Pepa"),
            ("A configured reaction to a caca", "A configured reaction to a caca")
        ]
    )
    def test_it_reacts_to_a_caca_when_the_probability_hits(
        self, mock_responses, auth_token, test_bot, configured_reaction, expected_response
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
                                "id": 123,
                                "is_bot": False,
                                "first_name": "Pepa",
                            },
                            "chat": {
                                "id": 987,
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

        mock_responses.post(
            url=f"https://api.telegram.org/bot{auth_token}/sendmessage",
            status=200,
            match=[
                matchers.json_params_matcher(
                    {"chat_id": 987, "text": expected_response}
                )
            ],
            json={
                "ok": True,
                "result": [{"update_id": 803079898, "something": "..."}],
            },
        )

        spontaneous_caca_reaction.REACTION_PROBABILITY = 1
        spontaneous_caca_reaction.REACTIONS = [configured_reaction]

        get_and_handle_updates(test_bot)


    def test_it_does_not_react_to_a_caca_when_the_probability_does_not_hit(self, mock_responses, auth_token, test_bot):
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
                                "id": 123,
                                "is_bot": False,
                                "first_name": "Pepa",
                            },
                            "chat": {
                                "id": 987,
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

        spontaneous_caca_reaction.REACTION_PROBABILITY = 0
        spontaneous_caca_reaction.REACTIONS = [
            "A configured reaction to a caca"
        ]

        get_and_handle_updates(test_bot)
