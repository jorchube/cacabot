from src.command import Command


def do(updates) -> list[Command]:
    commands = list()

    for update in updates:
        if not _update_is_command(update):
            continue

        command = _command_from_update(update)
        commands.append(command)

    return commands

def _command_from_update(update):
    update_id = update["update_id"]
    chat_id = update["message"]["chat"]["id"]
    command = update["message"]["text"]

    return Command(update_id=update_id, chat_id=chat_id, command=command)

def _update_is_command(update):
    if "message" not in update:
        return False
    if "entities" not in update["message"]:
        return False

    for entity in update["message"]["entities"]:
        if _entity_is_bot_command(entity):
            return True

    return False

def _entity_is_bot_command(entity):
    return entity["type"] == "bot_command"
