from datetime import datetime, timedelta

from ai_client import AIClient, AIClientException


CONVERSATION_ENGAGEMENT_TIMEOUT_MINUTES = 3


class ConversationEngineError(Exception):
    pass


class _ConversationContext:
    def __init__(self, token: list[int]) -> None:
        self._token = token
        self._valid_until = datetime.now() + timedelta(
            minutes=CONVERSATION_ENGAGEMENT_TIMEOUT_MINUTES
        )

    def is_valid(self):
        return self._valid_until >= datetime.now()

    def get(self):
        return self._token


class ConversationEngine:
    def __init__(self, ai_client: AIClient, botname: list[str]) -> None:
        self._ai_client = ai_client
        self._botnames = botname
        self._current_context = None

    def generate_response(self, message: str) -> str:
        context = None
        if self._current_context and self._current_context.is_valid():
            context = self._current_context.get()

        try:
            response = self._ai_client.send(text=message, context=context)
        except AIClientException as error:
            raise ConversationEngineError from error

        self._current_context = _ConversationContext(
            token=response.conversation_context
        )
        return response.response_message

    def is_botname(self, mentioned_name: str):
        return mentioned_name in self._botnames

    def context_is_valid(self):
        return self._current_context.is_valid()
