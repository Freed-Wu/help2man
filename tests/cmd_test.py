"""Test cmd."""
import os
from contextlib import suppress
from pathlib import Path

from help2man.__main__ import DESCRIPTION, EPILOG, VERSION, get_parser

parser = get_parser()

txt = os.path.join(os.path.dirname(__file__), "txt")
USAGE = (Path(txt) / "usage.txt").read_text()
OPTIONS = (Path(txt) / "options.txt").read_text()
HELP = "\n".join([USAGE, DESCRIPTION, OPTIONS, EPILOG])


class Test:
    """Test."""

    def test_help(self, capsys) -> None:
        """Test help.

        :param capsys:
        :rtype: None
        """
        with suppress(SystemExit):
            parser.parse_args(["--help"])
        captured = capsys.readouterr()
        assert captured.out == HELP

    def test_version(self, capsys) -> None:
        """Test version.

        :param capsys:
        :rtype: None
        """
        with suppress(SystemExit):
            parser.parse_args(["--version"])
        captured = capsys.readouterr()
        assert captured.out == VERSION
