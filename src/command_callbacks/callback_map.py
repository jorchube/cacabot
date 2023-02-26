from command_callbacks import cuentacacas_callback

class CommandsMap:
    _map = {
        "/cuentacacas": cuentacacas_callback.callback
    }

    @classmethod
    def get_callback_for_command(self, command):
        null_callback = lambda command: None
        if command.command not in self._map:
            return null_callback

        return self._map[command.command]
