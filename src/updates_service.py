import re


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
                mention = self._extract_mention(update["message"]["text"])
                return mention.strip("@")

        return None

    def _extract_mention(self, text):
        regex = re.compile(".*(@[A-z]+).*")
        match = regex.match(text)
        if len(match.groups()) == 0:
            return ""

        return match.groups(1)[0]
