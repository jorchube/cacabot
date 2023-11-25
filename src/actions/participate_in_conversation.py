import logging
import random

from ai_client import AIClient, AIClientException
from cacabot import Cacabot
from conversation_message import ConversationMessage

PARTICIPATION_PROBABILITY = 0.5

class ParticipateInConversation:
    def __init__(self, cacabot: Cacabot, ai_client = AIClient, participation_probability: int=PARTICIPATION_PROBABILITY) -> None:
        self._ai_client= ai_client
        self._cacabot = cacabot
        self._participation_probability = participation_probability

    def do(self, conversation_message: ConversationMessage) -> None:
        if self._participation_probability < random.random():
            return

        try:
            response = self._ai_client.send(text=conversation_message.message)
        except AIClientException as error:
            logging.error(f"Failed to participate in conversation: {error}")
            return

        self._cacabot.send_message_to_chat(
            chat_id=conversation_message.chat_id,
            message=response
        )
