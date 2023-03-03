from datetime import datetime
from zoneinfo import ZoneInfo
import pytest
from caca import Caca
from command import Command
from command_callbacks import cuentacacas_callback


@pytest.mark.usefixtures("in_memory_repository")
class TestCuentacacasCallback:
    @pytest.fixture
    def caca(self):
        return Caca(
            update_id=33,
            chat_id=-123,
            chat_member_id=789,
            chat_member_name="John Doe",
            chat_name="SupahChat",
            datetime=datetime(2023, 2, 25, 13, 33, tzinfo=ZoneInfo("Europe/Madrid")),
        )

    def test_it_counts_cacas_for_empty_repository(self):
        command = Command(update_id=123, chat_id=-123, command="/cuentacacas", chat_member_id=789, chat_member_name=-123)
        result = cuentacacas_callback.callback(command)

        assert result == None

    def test_it_counts_cacas_for_one_chat_member_in_the_repository(
        self, in_memory_repository, caca
    ):
        in_memory_repository.store_or_update_caca(caca)

        command = Command(update_id=123, chat_id=-123, command="/cuentacacas", chat_member_id=789, chat_member_name=-123)
        result = cuentacacas_callback.callback(command)

        assert result == (
            """Total de cacas:

John Doe: 1"""
        )

    def test_it_counts_many_cacas_for_many_chat_member_in_the_repository(
        self, in_memory_repository, caca
    ):
        in_memory_repository.store_or_update_caca(caca)

        caca.update_id = 300
        in_memory_repository.store_or_update_caca(caca)

        caca.update_id = 400
        caca.chat_member_id = 9876654
        caca.chat_member_name = "Jane Doe"
        in_memory_repository.store_or_update_caca(caca)

        command = Command(update_id=123, chat_id=-123, command="/cuentacacas", chat_member_id=789, chat_member_name=-123)
        result = cuentacacas_callback.callback(command)

        assert result == (
            """Total de cacas:

John Doe: 2
Jane Doe: 1"""
        )

    def test_it_counts_many_cacas_for_one_chat_member_in_the_repository_given_a_chat_member_id_using_the_last_chat_member_name(
        self, in_memory_repository, caca
    ):
        in_memory_repository.store_or_update_caca(caca)

        caca.update_id = 300
        in_memory_repository.store_or_update_caca(caca)

        caca.update_id = 400
        caca.chat_member_name = "Jane Doe"
        in_memory_repository.store_or_update_caca(caca)

        command = Command(update_id=123, chat_id=-123, command="/cuentacacas", chat_member_id=789, chat_member_name=-123)
        result = cuentacacas_callback.callback(command)

        assert result == (
            """Total de cacas:

Jane Doe: 3"""
        )

    def test_it_counts_cacas_only_for_the_chat_id_specified_in_the_given_command(
        self, in_memory_repository, caca
    ):
        in_memory_repository.store_or_update_caca(caca)

        caca.chat_id = 9999
        caca.update_id = 898
        in_memory_repository.store_or_update_caca(caca)

        command = Command(update_id=123, chat_id=-123, command="/cuentacacas", chat_member_id=789, chat_member_name=-123)
        result = cuentacacas_callback.callback(command)

        assert result == (
            """Total de cacas:

John Doe: 1"""
        )
