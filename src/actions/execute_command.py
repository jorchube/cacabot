from src.command import Command
from src.command_callbacks.callback_map import CommandsMap
from src.persistence.repository import Repository


def do(command: Command):
    if _is_command_already_executed(command):
        return

    _account_for_command(command)

    callback = CommandsMap.get_callback_for_command(command)
    callback(command)

def _is_command_already_executed(command):
    repository = Repository.get()

    return repository.is_command_stored(command)

def _account_for_command(command):
    repository = Repository.get()

    repository.store_command(command)
