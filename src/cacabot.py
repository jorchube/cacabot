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
            caca = Caca(
                update_offset=update["update_id"],
                chat_id=str(update["message"]["chat"]["id"]),
                chat_name=str(update["message"]["chat"]["title"]),
                chat_member_name=str(update["message"]["from"]["first_name"]),
                chat_member_id=str(update["message"]["from"]["id"]),
            )
            cacas.append(caca)

        return cacas
