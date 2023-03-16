import random
from caca import Caca
from cacabot import Cacabot


REACTION_PROBABILITY = 0.05
REACTIONS = [
    "{name}... ¡Menudo montón de mierda!",
    "En ese chorongo hay calidad, {name}",
    "Una ñoca como mandan los cánones, si señor",
    "¡La verga, que pestazo {name}!",
    "Uy...¿Eso que asoma es maíz {name}?",
    "¿Habéis visto la textura de esa cacota?",
    "Ese olor me embriaga, {name}",
    "¿Te habrás quedado en la gloria después de parir semejande monstruosidad, no?",
    "¿El WC se va a tragar eso?",
    "¡Pero ponle nombre al muñeco!",
    "Incorpora más fibra en la dieta, {name}",
    "Si flota es que quiere vivir",
    "¿Hay derrape?",
    "Acuérdate de usar la escobilla {name}",
    "Ahora pesas medio kilo menos",
]

def do(caca: Caca, cacabot: Cacabot):
    if REACTION_PROBABILITY < random.random():
        return

    reaction = _generate_reaction_to_caca(caca)
    cacabot.send_message_to_chat(chat_id=caca.chat_id, message=reaction)

def _generate_reaction_to_caca(caca):
    reaction_string = random.choice(REACTIONS)
    return reaction_string.format(name=caca.chat_member_name)
