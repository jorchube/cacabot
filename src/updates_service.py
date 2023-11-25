class UpdatesService:
    def update_is_conversation_message(self, update):
        if "message" not in update:
            return False
        if update["message"]["text"] == "💩":
            return False

        return True

    def update_is_command(self, update):
        if "message" not in update:
            return False
        if "entities" not in update["message"]:
            return None

        for entity in update["message"]["entities"]:
            if entity["type"] == "bot_command":
                return True

        return False

    def get_mention_from_update(self, update):
        if "message" not in update:
            return None
        if "entities" not in update["message"]:
            return None

        for entity in update["message"]["entities"]:
            if entity["type"] == "mention":
                return entity["user"]["username"].strip("@")

        return None
