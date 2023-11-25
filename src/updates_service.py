class UpdatesService:
    def update_is_conversation_message(self, update):
        if "message" not in update:
            return False
        if "entities" in update["message"]:
            return False

        return True
