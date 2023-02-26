from datetime import datetime
from zoneinfo import ZoneInfo
from src.caca import Caca


class CacaFactory:
    @classmethod
    def caca_from_valid_update(self, update) -> Caca:
        datetime = self._datetime_from_update(update)
        return Caca(
            update_id=update["update_id"],
            datetime=datetime,
            chat_id=update["message"]["chat"]["id"],
            chat_name=update["message"]["chat"]["title"],
            chat_member_name=update["message"]["from"]["first_name"],
            chat_member_id=update["message"]["from"]["id"],
        )

    @classmethod
    def caca_from_repository_result(self, result):
        update_id = result[0]
        datetime = self._datetime_from_timestamp(result[1])
        chat_id = result[2]
        chat_name = result[3]
        chat_member_id = result[4]
        chat_member_name = result[5]

        return Caca(
            update_id=update_id,
            datetime=datetime,
            chat_id=chat_id,
            chat_name=chat_name,
            chat_member_id=chat_member_id,
            chat_member_name=chat_member_name,
        )

    @classmethod
    def _datetime_from_update(self, update):
        timestamp = update["message"]["date"]
        return self._datetime_from_timestamp(timestamp)

    @classmethod
    def _datetime_from_timestamp(self, timestamp):
        timezone = ZoneInfo("Europe/Madrid")
        return datetime.fromtimestamp(timestamp, timezone)
