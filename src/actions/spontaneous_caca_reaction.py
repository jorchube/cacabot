import random
from caca import Caca
from cacabot import Cacabot


REACTION_PROBABILITY = 0.2
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
    "Se han visto recién nacidos que pesaban menos",
    "{name}, los castores pagarían millones por semejante tronco",
    "¡Ugh! ¡Puaj!! ¡No puedo respirar!",
    "¿Ha habido beso de Neptuno?",
    "Me parece humillante que mi único propósito sea ser testigo de estas mierdas",
    "Esa caca es tan gorda que te cuento dos",
    "Ese ñordaco está para indultar",
    "¡Si llegas a soltar eso en el campo se extinguen una o dos especies seguro!",
    "Cuando tires de la cadena subirá el nivel del mar",
]


def do(caca: Caca, cacabot: Cacabot):
    if REACTION_PROBABILITY < random.random():
        return

    reaction = _generate_reaction_to_caca(caca)
    cacabot.send_message_to_chat(chat_id=caca.chat_id, message=reaction)


def _generate_reaction_to_caca(caca):
    reaction_string = random.choice(REACTIONS)
    return reaction_string.format(name=caca.chat_member_name)
