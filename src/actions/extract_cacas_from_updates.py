from src.caca import Caca
from src.caca_factory import CacaFactory
from src.cacabot import Cacabot


def do(updates) -> list[Caca]:
    return _get_cacas_from_updates(updates)

def _get_cacas_from_updates(updates) -> list[Caca]:
    cacas = list()
    for update in updates:
        if not _is_a_text_message(update):
            continue
        if not _is_valid_caca(update):
            continue

        caca = CacaFactory.caca_from_valid_update(update)
        cacas.append(caca)

    return cacas

def _is_a_text_message(update):
    return "message" in update and "text" in update["message"]

def _is_valid_caca(update):
    update_text = update["message"]["text"]
    return update_text == "💩"
