from src.caca import Caca


class CacaFactory:
    @classmethod
    def create_caca_from_valid_update(self, update) -> Caca:
        return Caca(
            update_offset=update["update_id"],
            chat_id=str(update["message"]["chat"]["id"]),
            chat_name=str(update["message"]["chat"]["title"]),
            chat_member_name=str(update["message"]["from"]["first_name"]),
            chat_member_id=str(update["message"]["from"]["id"]),
        )
