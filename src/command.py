from dataclasses import dataclass


@dataclass
class Command:
    update_id: int
    chat_id: int
    command: str
