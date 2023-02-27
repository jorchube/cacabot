import logging
from command import Command
from persistence.repository import Repository


def callback(command: Command):
    logging.info(f"Executing command: {command}")

    repository = Repository.get()

    all_cacas = repository.get_all_cacas_for_chat(command.chat_id)

    results = _count_cacas_per_chat_member(all_cacas)

    if len(results) == 0:
        return None

    return _format_for_chat(results)


def _format_for_chat(results):
    message = "Total de cacas:\n"
    for key, value in results.items():
        name = value["name"]
        count = value["count"]
        partial = f"{name}: {count}"
        message = "\n".join([message, partial])

    return message


def _count_cacas_per_chat_member(all_cacas):
    result = dict()

    for caca in all_cacas:
        chat_member_id = caca.chat_member_id
        chat_member_name = caca.chat_member_name

        if chat_member_id not in result:
            result[chat_member_id] = {"name": chat_member_name, "count": 0}

        result[chat_member_id] = {
            "name": chat_member_name,
            "count": result[chat_member_id]["count"] + 1,
        }

    return result
