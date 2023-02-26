from datetime import datetime
from zoneinfo import ZoneInfo
import pytest
from src.caca import Caca
from src.persistence.repository import Repository


class TestRepository:
    @pytest.fixture
    def in_memory_repository(self):
        return Repository(in_memory=True)

    @pytest.fixture
    def caca(self):
        return Caca(
            chat_id="-123",
            chat_member_id="789",
            chat_member_name="John Doe",
            chat_name="SupahChat",
            datetime=datetime(2023, 2, 25, 13, 33, tzinfo=ZoneInfo("Europe/Madrid"))
        )

    def test_it_stores_and_retrieves_one_caca(self, in_memory_repository, caca):
        in_memory_repository.store_caca(caca)

        cacas = in_memory_repository.get_all_cacas()

        assert len(cacas) == 1
        assert cacas[0] == caca
