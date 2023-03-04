from command import Command
from persistence.repository import Repository


def callback(command: Command) -> str:
    repository = Repository.get()
    number_of_cacas = repository.count_cacas_for_member_in_chat(command.chat_member_id, command.chat_id)

    return _format_for_chat(number_of_cacas, command.chat_member_name)

def _format_for_chat(number_of_cacas, chat_member_name):
    cacas = "💩" * number_of_cacas

    return f"Estas son tus cacas {chat_member_name}:\n" + cacas
