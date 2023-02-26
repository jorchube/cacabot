import requests
from src.caca import Caca
from src.caca_factory import CacaFactory


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

            caca = CacaFactory.caca_from_valid_update(update)
            cacas.append(caca)

        return cacas

    def _is_a_text_message(self, update):
        return "message" in update and "text" in update["message"]

    def _is_valid_caca(self, update):
        update_text = update["message"]["text"]
        return update_text == "💩"
