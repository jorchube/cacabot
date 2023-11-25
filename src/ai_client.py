from dataclasses import dataclass

import requests


class AIClientException(Exception):
    pass

@dataclass
class AIClientResponse:
    response_message: str
    conversation_context: list[int]


class AIClient:
    MODEL = "llama2-uncensored"

    def __init__(self, url: str, port: int):
        self._url = url
        self._port = port

    def send(self, text:str, context: list[int]=None) -> AIClientResponse:
        body = {
            "model": self.MODEL,
            "prompt": text,
            "stream": False
        }

        if context:
            body["context"] = context

        response = requests.post(
            url=f"{self._url}:{self._port}/api/generate",
            json=body
        )

        if response.ok is False:
            raise AIClientException(message=f"{response}")

        response_json = response.json()

        return AIClientResponse(
            response_message=response_json["response"],
            conversation_context=response_json["context"]
        )
