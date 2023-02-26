import auth_token
from actions import extract_cacas_from_updates, store_new_cacas, extract_commands_from_updates, execute_command
from cacabot import Cacabot
from persistence.repository import Repository


AUTH_TOKEN_FILE = "secret.json"

def get_and_handle_updates(cacabot: Cacabot):
    updates = cacabot.get_updates()

    cacas = extract_cacas_from_updates.do(updates)
    store_new_cacas.do(cacas)

    commands = extract_commands_from_updates(updates)
    for command in commands:
        execute_command(command)

def run_loop(cacabot):
    while True:
        get_and_handle_updates(cacabot)

def main():
    bot_auth_token = auth_token.get(AUTH_TOKEN_FILE)
    cacabot = Cacabot(bot_auth_token)
    Repository.initialize()

    run_loop(cacabot)

if __name__ == "__main__":
    main()
