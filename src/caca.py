from dataclasses import dataclass
from datetime import datetime


@dataclass
class Caca:
    update_offset: int
    datetime: datetime
    chat_id: str
    chat_name: str
    chat_member_id: str
    chat_member_name: str
