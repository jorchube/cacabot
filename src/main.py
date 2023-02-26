import logging
import traceback
import auth_token
from actions import extract_cacas_from_updates, store_new_cacas, extract_commands_from_updates, execute_command
from cacabot import Cacabot
from persistence.repository import Repository


LOGLEVEL = logging.DEBUG

AUTH_TOKEN_FILE = "secret.json"

def get_and_handle_updates(cacabot: Cacabot):
    updates = cacabot.get_updates()

    cacas = extract_cacas_from_updates.do(updates)
    store_new_cacas.do(cacas)

    commands = extract_commands_from_updates.do(updates)
    for command in commands:
        output = execute_command.do(command)

        logging.debug(f"Command output: {output}")

        if output is not None:
            cacabot.send_message_to_chat(command.chat_id, output)

def run_loop(cacabot):
    while True:
        try:
            get_and_handle_updates(cacabot)
        except Exception as e:
            logging.error(traceback.format_exc())

def main():
    logging.basicConfig(format="[%(asctime)s] %(levelname)s: %(message)s", level=LOGLEVEL)

    bot_auth_token = auth_token.get(AUTH_TOKEN_FILE)
    cacabot = Cacabot(bot_auth_token)
    Repository.initialize()

    run_loop(cacabot)

if __name__ == "__main__":
    main()
