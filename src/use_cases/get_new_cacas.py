from src.caca import Caca
from src.cacabot import Cacabot


def do(bot: Cacabot) -> list[Caca]:

    cacas = bot.get_new_cacas()

    return cacas
