from datetime import datetime
from zoneinfo import ZoneInfo
from src.caca import Caca


class CacaFactory:
    @classmethod
    def create_caca_from_valid_update(self, update) -> Caca:
        datetime = self._extract_datetime_from_update(update)
        return Caca(
            update_offset=update["update_id"],
            datetime=datetime,
            chat_id=str(update["message"]["chat"]["id"]),
            chat_name=str(update["message"]["chat"]["title"]),
            chat_member_name=str(update["message"]["from"]["first_name"]),
            chat_member_id=str(update["message"]["from"]["id"]),
        )


    @classmethod
    def _extract_datetime_from_update(self, update):
        timestamp = update["message"]["date"]
        timezone = ZoneInfo("Europe/Madrid")
        return datetime.fromtimestamp(timestamp, timezone)
