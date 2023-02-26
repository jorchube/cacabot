from datetime import datetime
import sqlite3

from src.caca import Caca
from src.caca_factory import CacaFactory
from src.command import Command


class Repository:
    _instance = None

    @classmethod
    def get(self) -> "Repository":
        return Repository._instance

    @classmethod
    def initialize(self, in_memory=False) -> None:
        Repository._instance = Repository(in_memory=in_memory)

    def __init__(self, in_memory=False) -> None:
        self._db_path = ":memory:" if in_memory else "cacabot.db"
        self._connection = sqlite3.connect(self._db_path)
        self._cursor = self._connection.cursor()

        self._create_cacas_table()
        self._create_commands_table()

    def _create_cacas_table(self):
        self._cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cacas(
                update_id PRIMARY KEY,
                timestamp,
                chat_id,
                chat_name,
                chat_member_id,
                chat_member_name)
            """
        )

    def _create_commands_table(self):
        self._cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS commands(
                update_id PRIMARY KEY,
                chat_id,
                command)
            """
        )

    def store_or_update_caca(self, caca: Caca) -> None:
        update_id = caca.update_id

        if self._is_update_id_already_stored(update_id):
            self._update_caca(caca)
        else:
            self._insert_caca(caca)

        self._connection.commit()

    def _insert_caca(self, caca):
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

    def _update_caca(self, caca):
        update_id = caca.update_id
        timestamp = caca.datetime.timestamp()
        chat_id = caca.chat_id
        chat_name = caca.chat_name
        chat_member_id = caca.chat_member_id
        chat_member_name = caca.chat_member_name

        self._cursor.execute(
            f"""
            UPDATE cacas
            SET
                timestamp = {timestamp},
                chat_id = {chat_id},
                chat_name = '{chat_name}',
                chat_member_id = {chat_member_id},
                chat_member_name = '{chat_member_name}'
            WHERE
                update_id = {update_id}
            """
        )

    def _is_update_id_already_stored(self, update_id) -> bool:
        results = self._cursor.execute(
            f"""
            SELECT 1
            FROM cacas
            WHERE update_id={update_id}
            """
        ).fetchall()

        return len(results) > 0

    def get_all_cacas(self) -> list[Caca]:
        results = self._cursor.execute(
            """
            SELECT update_id, timestamp, chat_id, chat_name, chat_member_id, chat_member_name
            FROM cacas
            """
        ).fetchall()

        return [CacaFactory.caca_from_repository_result(result) for result in results]

    def get_all_cacas_for_chat(self, chat_id) -> list[Caca]:
        results = self._cursor.execute(
            f"""
            SELECT update_id, timestamp, chat_id, chat_name, chat_member_id, chat_member_name
            FROM cacas
            WHERE chat_id={chat_id}
            """
        ).fetchall()

        return [CacaFactory.caca_from_repository_result(result) for result in results]

    def is_command_stored(self, command: Command):
        update_id = command.update_id
        results = self._cursor.execute(
            f"""
            SELECT 1
            FROM commands
            WHERE update_id={update_id}
            """
        ).fetchall()

        return len(results) > 0

    def store_command(self, command: Command):
        self._cursor.execute(
            f"""
            INSERT INTO commands(update_id, chat_id, command)
            VALUES (
                {command.update_id},
                {command.chat_id},
                '{command.command}'
            )
            """
        )
        self._connection.commit()
