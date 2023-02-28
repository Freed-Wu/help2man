"""Test."""
import os
from argparse import ArgumentParser
from pathlib import Path

from help2man import parser2man

txt = os.path.join(os.path.dirname(__file__), "txt")
MAN = (Path(txt) / "test.man").read_text()


class Test:
    """Test."""

    def test_parser2man(self) -> None:
        """Test parser2man.

        :rtype: None
        """
        parser = ArgumentParser(
            "test", "Test program", description="A test program"
        )
        parser.add_argument(
            "--version",
            action="version",
            version=r"""0.0.1
Copyright (C) 2022-2022
Written by Wu Zhenyu.
""",
        )
        parser.add_argument("files", help="input files")
        man = parser2man(parser)
        # the 2nd line contains date
        assert man.strip().split("\n")[2:] == MAN.strip().split("\n")[2:]
