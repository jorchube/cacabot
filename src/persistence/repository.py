import sqlite3
import logging

from caca import Caca
from caca_factory import CacaFactory
from command import Command


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

        self._execute_migrations()

    def _create_cacas_table(self):
        self._execute_sql(
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
        self._execute_sql(
            """
            CREATE TABLE IF NOT EXISTS commands(
                update_id PRIMARY KEY,
                chat_id,
                command)
            """
        )

    def _execute_migrations(self):
        self._add_chat_member_data_to_commands_table()

    def _add_chat_member_data_to_commands_table(self):
        results = self._execute_sql(
            "SELECT count(*) as num_columns FROM pragma_table_info('commands')"
        )
        number_of_columns = results[0][0]

        if number_of_columns == 3:
            self._execute_sql("ALTER TABLE commands ADD COLUMN chat_member_id")
            self._execute_sql("ALTER TABLE commands ADD COLUMN chat_member_name")

    def store_or_update_caca(self, caca: Caca) -> None:
        update_id = caca.update_id

        if self._is_update_id_already_stored(update_id):
            self._update_caca(caca)
            logging.info(f"Updated caca: {caca}")
        else:
            self._insert_caca(caca)
            logging.info(f"Created caca: {caca}")

        self._connection.commit()

    def _insert_caca(self, caca):
        update_id = caca.update_id
        timestamp = caca.datetime.timestamp()
        chat_id = caca.chat_id
        chat_name = caca.chat_name
        chat_member_id = caca.chat_member_id
        chat_member_name = caca.chat_member_name

        self._execute_sql(
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

        self._execute_sql(
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
        results = self._execute_sql(
            f"""
            SELECT 1
            FROM cacas
            WHERE update_id={update_id}
            """
        )

        return len(results) > 0

    def get_all_cacas(self) -> list[Caca]:
        results = self._execute_sql(
            """
            SELECT update_id, timestamp, chat_id, chat_name, chat_member_id, chat_member_name
            FROM cacas
            """
        )

        return [CacaFactory.caca_from_repository_result(result) for result in results]

    def get_all_cacas_for_chat(self, chat_id) -> list[Caca]:
        results = self._execute_sql(
            f"""
            SELECT update_id, timestamp, chat_id, chat_name, chat_member_id, chat_member_name
            FROM cacas
            WHERE chat_id={chat_id}
            """
        )

        return [CacaFactory.caca_from_repository_result(result) for result in results]

    def is_command_stored(self, command: Command):
        update_id = command.update_id
        results = self._execute_sql(
            f"""
            SELECT 1
            FROM commands
            WHERE update_id={update_id}
            """
        )
        return len(results) > 0

    def store_command(self, command: Command):
        self._execute_sql(
            f"""
            INSERT INTO commands(update_id, chat_id, command, chat_member_id, chat_member_name)
            VALUES (
                {command.update_id},
                {command.chat_id},
                '{command.command}',
                {command.chat_member_id},
                '{command.chat_member_name}'
            )
            """
        )
        self._connection.commit()

    def count_cacas_for_member_in_chat(self, chat_member_id: int, chat_id: int) -> int:
        result = self._execute_sql(
            f"""
            SELECT count(*)
            FROM cacas
            WHERE chat_id={chat_id} and chat_member_id={chat_member_id}
            """
        )

        return result[0][0]

    def _execute_sql(self, sql):
        logging.debug(f"Executing sql: {sql}")

        return self._cursor.execute(sql).fetchall()
