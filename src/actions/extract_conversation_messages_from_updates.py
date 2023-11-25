from conversation_message import ConversationMessage
from updates_service import UpdatesService


def do(updates) -> list[ConversationMessage]:
    conversation_messages = list()
    for update in updates:
        if UpdatesService().update_is_command(update):
            continue
        if UpdatesService().update_is_conversation_message(update):
            conversation_messages.append(_conversation_message_from_update(update))

    return conversation_messages

def _conversation_message_from_update(update):
    update_id = update["update_id"]
    chat_id = update["message"]["chat"]["id"]
    message = update["message"]["text"]
    chat_member_id = update["message"]["from"]["id"]
    chat_member_name = update["message"]["from"]["first_name"]
    mention = UpdatesService().get_mention_from_update(update)

    return ConversationMessage(
        update_id=update_id,
        chat_id=chat_id,
        message=message,
        chat_member_id=chat_member_id,
        chat_member_name=chat_member_name,
        mention=mention
    )
