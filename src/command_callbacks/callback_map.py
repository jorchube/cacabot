from typing import Callable
from command import Command
from command_callbacks import cuentacacas_callback, miscacas_callback

# cuentacacas - Conteo de cacas
# miscacas - Te enseño todas tus cacas

class CommandsMap:
    _map = {
        "/cuentacacas": cuentacacas_callback.callback,
        "/miscacas": miscacas_callback.callback
    }

    @classmethod
    def get_callback_for_command(self, command) -> Callable[[Command], str]:
        null_callback = lambda command: None

        for key, value in self._map.items():
            if command.command.startswith(key):
                return value

        return null_callback
