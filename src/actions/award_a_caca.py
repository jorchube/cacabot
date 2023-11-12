import logging
from caca import Caca
from cacabot import Cacabot
from persistence.repository import Repository


AWARDED_CACAS = [
    {"number_of_cacas": 50, "trophy_image_path": "src/imgs/50cacas.png"},
    {"number_of_cacas": 100, "trophy_image_path": "src/imgs/100cacas.png"},
    {"number_of_cacas": 500, "trophy_image_path": "src/imgs/500cacas.png"},
    {"number_of_cacas": 666, "trophy_image_path": "src/imgs/666cacas.png"},
    {"number_of_cacas": 1000, "trophy_image_path": "src/imgs/1000cacas.png"},
]


def do(caca: Caca, cacabot: Cacabot):
    repository = Repository.get()

    chat_member_id = caca.chat_member_id
    chat_id = caca.chat_id

    number_of_cacas = repository.count_cacas_for_member_in_chat(chat_member_id, chat_id)

    if _is_awarded_caca(number_of_cacas):
        _give_award(number_of_cacas, caca, cacabot)


def _is_awarded_caca(number_of_cacas):
    awarded_amounts = [
        awarded_caca["number_of_cacas"] for awarded_caca in AWARDED_CACAS
    ]

    return number_of_cacas in awarded_amounts


def _give_award(number_of_cacas, caca, cacabot):
    chat_id = caca.chat_id
    chat_member_name = caca.chat_member_name
    chat_member_id = caca.chat_member_id

    logging.info(
        f"Awarding the {number_of_cacas} cacas award to {chat_member_name} ({chat_member_id}) in chat {chat_id}"
    )

    trophy_image_path = _get_trophy_image_path(number_of_cacas)

    trophy_caption = _create_trophy_caption(chat_member_name)
    cacabot.send_image_to_chat(chat_id, trophy_image_path, caption=trophy_caption)


def _get_trophy_image_path(number_of_cacas):
    for awarded_caca in AWARDED_CACAS:
        if number_of_cacas == awarded_caca["number_of_cacas"]:
            return awarded_caca["trophy_image_path"]


def _create_trophy_caption(chat_member_name):
    return f"🏆 OLE {chat_member_name.upper()}!!! 🏆"
