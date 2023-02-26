from datetime import datetime
from zoneinfo import ZoneInfo
from src.caca import Caca


class CacaFactory:
    @classmethod
    def caca_from_valid_update(self, update) -> Caca:
        datetime = self._datetime_from_update(update)
        return Caca(
            datetime=datetime,
            chat_id=str(update["message"]["chat"]["id"]),
            chat_name=str(update["message"]["chat"]["title"]),
            chat_member_name=str(update["message"]["from"]["first_name"]),
            chat_member_id=str(update["message"]["from"]["id"]),
        )

    @classmethod
    def caca_from_repository_result(self, result):
        datetime = self._datetime_from_timestamp(result[0])
        chat_id = result[1]
        chat_name = result[2]
        chat_member_id = result[3]
        chat_member_name = result[4]

        return Caca(
            datetime=datetime,
            chat_id=chat_id,
            chat_name=chat_name,
            chat_member_id=chat_member_id,
            chat_member_name=chat_member_name
        )

    @classmethod
    def _datetime_from_update(self, update):
        timestamp = update["message"]["date"]
        return self._datetime_from_timestamp(timestamp)

    @classmethod
    def _datetime_from_timestamp(self, timestamp):
        timezone = ZoneInfo("Europe/Madrid")
        return datetime.fromtimestamp(timestamp, timezone)
