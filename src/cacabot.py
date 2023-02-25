import requests
from src.caca import Caca


class Cacabot:
    def __init__(self, auth_token) -> None:
        self._get_udpates_url = f"https://api.telegram.org/bot{auth_token}/getupdates"

    def get_new_cacas(self) -> list[Caca]:
        response = requests.post(self._get_udpates_url)

        response_json = response.json()
        updates = response_json["result"]

        cacas = self._get_cacas_from_updates(updates)
        return cacas

    def _get_cacas_from_updates(self, updates) -> list[Caca]:
        cacas = list()
        for update in updates:
            if not self._is_a_text_message(update):
                continue
            if not self._is_valid_caca(update):
                continue

            caca = self._create_caca_from_update(update)
            cacas.append(caca)

        return cacas

    def _create_caca_from_update(self, update):
        return Caca(
            update_offset=update["update_id"],
            chat_id=str(update["message"]["chat"]["id"]),
            chat_name=str(update["message"]["chat"]["title"]),
            chat_member_name=str(update["message"]["from"]["first_name"]),
            chat_member_id=str(update["message"]["from"]["id"]),
        )

    def _is_a_text_message(self, update):
        return "message" in update and "text" in update["message"]

    def _is_valid_caca(self, update):
        update_text = update["message"]["text"]
        return update_text == "💩"
