from command import Command
from persistence.repository import Repository


def callback(command: Command):
    repository = Repository.get()

    all_cacas = repository.get_all_cacas_for_chat(command.chat_id)

    return _count_cacas_per_chat_member(all_cacas)

def _count_cacas_per_chat_member(all_cacas):
    result = dict()

    for caca in all_cacas:
        chat_member_id = caca.chat_member_id
        chat_member_name = caca.chat_member_name

        if chat_member_id not in result:
            result[chat_member_id] = {
                "name": chat_member_name,
                "count": 0
            }

        result[chat_member_id] = {
            "name": chat_member_name,
            "count": result[chat_member_id]["count"] + 1
        }

    return result
