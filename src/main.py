import logging
import traceback

import auth_token
from actions import (award_a_caca, execute_command, extract_cacas_from_updates,
                     extract_commands_from_updates,
                     extract_conversation_messages_from_updates,
                     spontaneous_caca_reaction, store_new_cacas)
from actions.participate_in_conversation import ParticipateInConversation
from ai_client import AIClient
from cacabot import Cacabot
from conversation_engine import ConversationEngine
from persistence.repository import Repository

LOGLEVEL = logging.INFO

AUTH_TOKEN_FILE = "secret.json"


def get_and_handle_updates(cacabot: Cacabot, conversation_engine: ConversationEngine):
    updates = cacabot.get_updates()

    cacas = extract_cacas_from_updates.do(updates)
    store_new_cacas.do(cacas)

    for caca in cacas:
        award_a_caca.do(caca, cacabot)
        spontaneous_caca_reaction.do(caca, cacabot)

    commands = extract_commands_from_updates.do(updates)
    for command in commands:
        output = execute_command.do(command)

        logging.debug(f"Command output: {output}")

        if output is not None:
            cacabot.send_message_to_chat(command.chat_id, output)

    conversation_messages = extract_conversation_messages_from_updates.do(updates)
    for conversation_message in conversation_messages:
        ParticipateInConversation(cacabot=cacabot, conversation_engine=conversation_engine).do(conversation_message)


def run_loop(cacabot: Cacabot, conversation_engine: ConversationEngine):
    while True:
        try:
            get_and_handle_updates(cacabot, conversation_engine)
        except Exception as e:
            backtrace = traceback.format_exc()
            logging.error(backtrace)


def main():
    logging.basicConfig(
        format="[%(asctime)s] %(levelname)s: %(message)s",
        level=LOGLEVEL,
        handlers=[logging.FileHandler("cacabot.log"), logging.StreamHandler()],
    )

    bot_auth_token = auth_token.get(AUTH_TOKEN_FILE)
    cacabot = Cacabot(bot_auth_token)
    ai_client = AIClient("http://192.168.1.136", 11434)
    conversation_engine = ConversationEngine(ai_client=ai_client, botname=["hecesquiel_bot", "cacabot"])
    Repository.initialize()

    run_loop(cacabot, conversation_engine)


if __name__ == "__main__":
    main()
