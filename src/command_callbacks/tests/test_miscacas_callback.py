from datetime import datetime
from zoneinfo import ZoneInfo
import pytest
from caca import Caca
from command import Command
from command_callbacks import miscacas_callback


@pytest.mark.usefixtures("in_memory_repository")
class TestMiscacasCallback:
    @pytest.fixture
    def caca(self):
        return Caca(
            update_id=33,
            chat_id=-123,
            chat_member_id=789,
            chat_member_name="John",
            chat_name="SupahChat",
            datetime=datetime(2023, 2, 25, 13, 33, tzinfo=ZoneInfo("Europe/Madrid")),
        )

    def test_it_returns_mis_cacas_when_no_cacas_are_stored(self):
        command = Command(
            update_id=123,
            chat_id=-123,
            command="/miscacas",
            chat_member_id=789,
            chat_member_name="John",
        )
        result = miscacas_callback.callback(command)

        assert result == (
            """Estas son tus cacas John:
"""
        )

    def test_it_returns_mis_cacas_when_one_caca_is_stored(
        self, in_memory_repository, caca
    ):
        in_memory_repository.store_or_update_caca(caca)

        command = Command(
            update_id=123,
            chat_id=-123,
            command="/miscacas",
            chat_member_id=789,
            chat_member_name="John",
        )
        result = miscacas_callback.callback(command)

        assert result == (
            """Estas son tus cacas John:
💩"""
        )

    def test_it_returns_mis_cacas_when_many_cacas_are_stored(
        self, in_memory_repository, caca
    ):
        in_memory_repository.store_or_update_caca(caca)
        caca.update_id = 999999
        in_memory_repository.store_or_update_caca(caca)

        command = Command(
            update_id=123,
            chat_id=-123,
            command="/miscacas",
            chat_member_id=789,
            chat_member_name="John",
        )
        result = miscacas_callback.callback(command)

        assert result == (
            """Estas son tus cacas John:
💩💩"""
        )

    def test_it_returns_mis_cacas_when_many_cacas_are_stored_ignoring_cacas_from_other_chat_members(
        self, in_memory_repository, caca
    ):
        in_memory_repository.store_or_update_caca(caca)
        caca.update_id = 999999
        caca.chat_member_id = 90909090
        in_memory_repository.store_or_update_caca(caca)

        command = Command(
            update_id=123,
            chat_id=-123,
            command="/miscacas",
            chat_member_id=789,
            chat_member_name="John",
        )
        result = miscacas_callback.callback(command)

        assert result == (
            """Estas son tus cacas John:
💩"""
        )

    def test_it_returns_mis_cacas_when_many_cacas_are_stored_ignoring_cacas_from_other_chats(
        self, in_memory_repository, caca
    ):
        in_memory_repository.store_or_update_caca(caca)
        caca.update_id = 999999
        caca.chat_id = 90909090
        in_memory_repository.store_or_update_caca(caca)

        command = Command(
            update_id=123,
            chat_id=-123,
            command="/miscacas",
            chat_member_id=789,
            chat_member_name="John",
        )
        result = miscacas_callback.callback(command)

        assert result == (
            """Estas son tus cacas John:
💩"""
        )
