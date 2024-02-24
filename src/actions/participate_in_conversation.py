import logging
import random

from cacabot import Cacabot
from conversation_engine import ConversationEngine, ConversationEngineError
from conversation_message import ConversationMessage

PARTICIPATION_PROBABILITY = 0.0


class ParticipateInConversation:
    def __init__(
        self,
        cacabot: Cacabot,
        conversation_engine: ConversationEngine,
        participation_probability: int = PARTICIPATION_PROBABILITY,
    ) -> None:
        self._conversation_engine = conversation_engine
        self._cacabot = cacabot
        self._participation_probability = participation_probability

    def do(self, conversation_message: ConversationMessage) -> None:
        if self._will_participate(conversation_message):
            self._participate(conversation_message)

    def _will_participate(self, conversation_message):
        if self._conversation_engine.is_botname(conversation_message.mention):
            return True

        if self._participation_probability >= random.random():
            return True

        if self._conversation_engine.context_is_valid():
            return True

        return False

    def _participate(self, conversation_message):
        try:
            response = self._conversation_engine.generate_response(
                message=conversation_message.message
            )
        except ConversationEngineError as error:
            logging.error(f"Failed to participate in conversation: {error}")
            return

        self._cacabot.send_message_to_chat(
            chat_id=conversation_message.chat_id, message=response
        )
