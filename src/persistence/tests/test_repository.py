from datetime import datetime
from zoneinfo import ZoneInfo
import pytest
from caca import Caca
from command import Command
from persistence.repository import Repository


class TestRepository:
    @pytest.fixture
    def in_memory_repository(self):
        return Repository(in_memory=True)

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

    @pytest.fixture
    def command(self):
        return Command(
            update_id=33,
            chat_id=-44,
            command="/a_command",
            chat_member_id=55,
            chat_member_name="John",
        )

    def test_it_skips_an_already_applied_migration(self, in_memory_repository):
        in_memory_repository._execute_migrations()
        in_memory_repository._execute_migrations()

    def test_it_stores_and_retrieves_one_caca(self, in_memory_repository, caca):
        in_memory_repository.store_or_update_caca(caca)

        cacas = in_memory_repository.get_all_cacas()

        assert len(cacas) == 1
        assert cacas[0] == caca

    def test_it_updates_a_caca_with_an_already_stored_update_id(
        self, in_memory_repository, caca
    ):
        in_memory_repository.store_or_update_caca(caca)

        caca.chat_member_name = "Another name"
        in_memory_repository.store_or_update_caca(caca)

        cacas = in_memory_repository.get_all_cacas()

        assert len(cacas) == 1
        assert cacas[0] == caca

    def test_it_stores_a_command(self, in_memory_repository, command):
        in_memory_repository.store_command(command)

        assert in_memory_repository.is_command_stored(command) is True
