import logging
import requests


class Cacabot:
    def __init__(self, auth_token: str) -> None:
        self._update_offset = 0
        self._get_udpates_url = f"https://api.telegram.org/bot{auth_token}/getupdates"
        self._send_message_url = f"https://api.telegram.org/bot{auth_token}/sendmessage"
        self._send_image_url = f"https://api.telegram.org/bot{auth_token}/sendphoto"

    def get_updates(self):
        response = requests.post(
            self._get_udpates_url, json={"timeout": 60, "offset": self._update_offset}
        )

        response_json = response.json()
        updates = response_json["result"]

        logging.debug(f"Cacabot got {len(updates)} updates")

        if len(updates) == 0:
            return list()

        self._refresh_update_offset(updates)

        return updates

    def _refresh_update_offset(self, updates):
        update_ids = [update["update_id"] for update in updates]
        max_update_id = max(update_ids)
        self._update_offset = max_update_id + 1

    def send_message_to_chat(self, chat_id, message):
        logging.info(f"Sendind message to chat_id {chat_id}")

        response = requests.post(
            self._send_message_url, json={"chat_id": chat_id, "text": message}
        )

        if response.status_code != 200:
            logging.error(f"Failed to send message: {response}")
            return

        response_json = response.json()
        if response_json["ok"] == False:
            logging.error(f"Failed to send message: {response}")

        logging.debug(f"Message to chat_id {chat_id} sent successfully: {response}")

    def send_image_to_chat(self, chat_id, image_path, caption=None):
        params = {"chat_id": chat_id, "caption": caption}

        with open(image_path, "rb") as image:
            response = requests.post(
                self._send_image_url, params, files={"photo": image}
            )

        if response.status_code != 200:
            logging.error(f"Failed to send message: {response}")
            return

        response_json = response.json()
        if response_json["ok"] == False:
            logging.error(f"Failed to send message: {response}")

        logging.debug(f"Image to chat_id {chat_id} sent successfully: {response}")
