from datetime import datetime
from unittest.mock import ANY
import pytest
from responses import matchers

from caca import Caca
from main import get_and_handle_updates


class TestNumberOfCacasTrophy:
    @pytest.fixture
    def create_cacas_for_member_in_chat(self, in_memory_repository):
        def callback(chat_member_id, chat_id, update_id):
            caca = Caca(
                update_id=update_id,
                datetime=datetime(2023, 3, 12, 17, 3),
                chat_id=chat_id,
                chat_name="ChatName",
                chat_member_id=chat_member_id,
                chat_member_name="John",
            )
            in_memory_repository.store_or_update_caca(caca)

        return callback

    def test_it_does_not_send_a_trophy_for_a_non_awarded_number_of_cacas(
        self, test_bot, create_cacas_for_member_in_chat, mock_responses, auth_token
    ):
        for update_id in range(37):
            create_cacas_for_member_in_chat(123, 987, update_id)

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

        get_and_handle_updates(test_bot)

    @pytest.mark.parametrize(
        ("number_of_cacas", "expected_trophy_image_path"),
        [
            (50, "src/imgs/50cacas.png"),
            (100, "src/imgs/100cacas.png"),
            (500, "src/imgs/500cacas.png"),
            (1000, "src/imgs/1000cacas.png"),
        ],
    )
    def test_it_sends_a_trophy_for_an_awarded_number_of_cacas(
        self,
        test_bot,
        create_cacas_for_member_in_chat,
        mock_responses,
        auth_token,
        number_of_cacas,
        expected_trophy_image_path,
    ):
        for update_id in range(number_of_cacas - 1):
            create_cacas_for_member_in_chat(123, 987, update_id)

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

        with open(expected_trophy_image_path, "rb") as photo_data:
            mock_responses.post(
                url=f"https://api.telegram.org/bot{auth_token}/sendphoto",
                status=200,
                match=[
                    matchers.multipart_matcher(
                        {"photo": photo_data},
                        data={"chat_id": 987, "caption": "🏆 OLE PEPA!!! 🏆"},
                    )
                ],
                json={
                    "ok": True,
                    "result": [{"update_id": 803079898, "something": "..."}],
                },
            )

        get_and_handle_updates(test_bot)
