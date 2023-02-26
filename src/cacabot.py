import requests
from src.caca import Caca
from src.caca_factory import CacaFactory


class Cacabot:
    def __init__(self, auth_token) -> None:
        self._get_udpates_url = f"https://api.telegram.org/bot{auth_token}/getupdates"

    def get_updates(self):
        response = requests.post(self._get_udpates_url)

        response_json = response.json()
        updates = response_json["result"]

        return updates