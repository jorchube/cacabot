from datetime import datetime
import sqlite3

from src.caca import Caca
from src.caca_factory import CacaFactory


class Repository:
    def __init__(self, in_memory=False) -> None:
        self._db_path = ":memory:" if in_memory else "cacabot.db"
        self._connection = sqlite3.connect(self._db_path)
        self._cursor = self._connection.cursor()

        self._create_cacas_table()

    def _create_cacas_table(self):
        self._cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cacas(
                update_id,
                timestamp,
                chat_id,
                chat_name,
                chat_member_id,
                chat_member_name)
            """
        )

    def store_caca(self, caca: Caca) -> None:
        update_id = caca.update_id
        timestamp = caca.datetime.timestamp()
        chat_id = caca.chat_id
        chat_name = caca.chat_name
        chat_member_id = caca.chat_member_id
        chat_member_name = caca.chat_member_name

        self._cursor.execute(
            f"""
            INSERT INTO cacas(update_id, timestamp, chat_id, chat_name, chat_member_id, chat_member_name)
            VALUES (
                {update_id},
                {timestamp},
                {chat_id},
                '{chat_name}',
                {chat_member_id},
                '{chat_member_name}'
            )
            """
        )
        self._connection.commit()

    def get_all_cacas(self) -> list[Caca]:
        results = self._cursor.execute(
            """
            SELECT update_id, timestamp, chat_id, chat_name, chat_member_id, chat_member_name
            FROM cacas
            """
        ).fetchall()

        return [CacaFactory.caca_from_repository_result(result) for result in results]
