from dataclasses import dataclass


@dataclass
class ConversationMessage:
    update_id: int
    chat_id: int
    message: str
    chat_member_id: int
    chat_member_name: str
