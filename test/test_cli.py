"""Test: CLI."""

import pytest

from click.testing import CliRunner
from gibica.gibica import main


@pytest.fixture
def runner():
    """Instantiation of CLI runner."""
    return CliRunner()


def test_cli_standard(runner):
    """Test of the standard CLI behavior."""

    with runner.isolated_filesystem():
        with open('script.gbc', 'w') as f:
            f.write('int a = 2; int b = a + 1;')

        result = runner.invoke(main, ['script.gbc'])
        assert result.exit_code == 0
        assert result.output == ''


def test_cli_debug(runner):
    """Test of the CLI behavior in debug mode."""

    with runner.isolated_filesystem():
        with open('script.gbc', 'w') as f:
            f.write('int a = 2; int b = a + 1;')

        result = runner.invoke(main, ['script.gbc', '--debug'])
        assert result.exit_code == 0
        assert result.output == (
                                    "SYMBOL TABLE: [<a:int>, <b:int>]\n"
                                    "GLOBAL MEMORY: {'a': 2, 'b': 3}\n"
                                )
