from command_callbacks import cuentacacas_callback

class CommandsMap:
    _map = {
        "/cuentacacas": cuentacacas_callback.callback
    }

    @classmethod
    def get_callback_for_command(self, command):
        null_callback = lambda command: None

        for key, value in self._map.items():
            if command.command.startswith(key):
                return value

        return null_callback
