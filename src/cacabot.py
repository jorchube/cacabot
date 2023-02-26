import logging
import requests
from caca import Caca
from caca_factory import CacaFactory


class Cacabot:
    def __init__(self, auth_token: str) -> None:
        self._get_udpates_url = f"https://api.telegram.org/bot{auth_token}/getupdates"

    def get_updates(self):
        response = requests.post(self._get_udpates_url, json={"timeout": 60})

        response_json = response.json()
        updates = response_json["result"]

        logging.info(f"Cacabot got {len(updates)} updates")

        return updates
