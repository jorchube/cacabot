import requests


class AIClientException(Exception):
    pass


class AIClient:
    MODEL = "llama2-uncensored"

    def __init__(self, url: str, port: int):
        self._url = url
        self._port = port

    def send(self, text:str) -> str:
        body = {
            "model": self.MODEL,
            "prompt": text,
            "stream": False
        }

        response = requests.post(
            url=f"{self._url}:{self._port}",
            json=body
        )

        if response.ok is False:
            raise AIClientException(message=f"{response}")

        return response.json()["response"]
