from unittest.mock import Mock
import pytest
from actions import execute_command
from command import Command
from command_callbacks.callback_map import CommandsMap


@pytest.mark.usefixtures("in_memory_repository")
class TestExecuteCommand:
    @pytest.fixture
    def mock_command(self):
        command = Command(update_id=23, chat_id=123, command="/a_command")
        return command

    @pytest.fixture
    def mock_callback(self):
        return Mock()

    def test_it_executes_a_command(self, mock_command, mock_callback):
        CommandsMap._map = {mock_command.command: mock_callback}

        execute_command.do(mock_command)

        mock_callback.assert_called_once_with(mock_command)

    def test_it_does_nothing_when_command_has_already_been_accounted_for(
        self, mock_command, mock_callback
    ):
        CommandsMap._map = {mock_command.command: mock_callback}
        execute_command.do(mock_command)
        mock_callback.reset_mock()

        execute_command.do(mock_command)

        mock_callback.assert_not_called()

    def test_it_does_nothing_for_an_unknown_command(self, mock_command, mock_callback):
        CommandsMap._map = {mock_command.command: mock_callback}

        unknown_command = Command(update_id=23, chat_id=123, command="/unknown_command")

        execute_command.do(unknown_command)

        mock_callback.assert_not_called()
