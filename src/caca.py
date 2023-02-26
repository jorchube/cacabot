from dataclasses import dataclass
from datetime import datetime


@dataclass
class Caca:
    update_id: int
    datetime: datetime
    chat_id: int
    chat_name: str
    chat_member_id: int
    chat_member_name: str
