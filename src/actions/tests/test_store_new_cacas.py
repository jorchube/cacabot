from datetime import datetime
from zoneinfo import ZoneInfo
import pytest

from actions import store_new_cacas
from caca import Caca


class TestStoreNewCacas:
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
    def another_caca(self):
        return Caca(
            update_id=44,
            chat_id=-123,
            chat_member_id=456,
            chat_member_name="Jane Doe",
            chat_name="SupahChat",
            datetime=datetime(2023, 2, 25, 16, 33, tzinfo=ZoneInfo("Europe/Madrid")),
        )

    def test_it_stores_one_caca(self, caca, in_memory_repository):
        new_cacas = [caca]

        store_new_cacas.do(new_cacas)

        stored_cacas = in_memory_repository.get_all_cacas()
        assert len(stored_cacas) == 1
        assert caca in stored_cacas

    def test_it_stores_many_cacas(self, caca, another_caca, in_memory_repository):
        new_cacas = [caca, another_caca]

        store_new_cacas.do(new_cacas)

        stored_cacas = in_memory_repository.get_all_cacas()
        assert len(stored_cacas) == 2
        assert caca in stored_cacas
        assert another_caca in stored_cacas
