#!/usr/bin/env python
"""This module can be called by
`python -m <https://docs.python.org/3/library/__main__.html>`_.
"""
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from typing import NoReturn

from . import ASSETS_PATH, DEFAULTS, __version__  # type: ignore
from .external import shtab

EPILOG = (ASSETS_PATH / "txt" / "epilog.txt").read_text()
VERSION = f"""help2man {__version__}
{(ASSETS_PATH / "txt" / "version.txt").read_text()}"""
DESCRIPTION = (ASSETS_PATH / "txt" / "description.txt").read_text().strip()
CMD = {"zsh": "{_command_names -e}"}
ARGS = {"zsh": "_normal"}


def get_parser() -> ArgumentParser:
    """Get a parser for unit test and help2man.
    Provide shell completions.

    :rtype: ArgumentParser
    """
    parser = ArgumentParser(
        "help2man",
        description=DESCRIPTION,
        epilog=EPILOG,
        formatter_class=RawDescriptionHelpFormatter,
    )
    parser.add_argument("-V", "--version", version=VERSION, action="version")
    shtab.add_argument_to(parser)
    parser.add_argument(
        "-n",
        "--name",
        help="description for the first paragraph, default: %(default)s",
    )
    parser.add_argument(
        "-s",
        "--section",
        help="section number for manual page, default: %(default)s",
    )
    parser.add_argument(
        "-m",
        "--manual",
        help="name of manual. default: %(default)s",
    )
    parser.add_argument(
        "-S",
        "--source",
        help="source of program (FSF, Debian, ...). default: %(default)s",
    )
    parser.add_argument(
        "-p",
        "--info-page",
        help="name of Texinfo manual, default: %(default)s",
    )
    parser.add_argument(
        "-i",
        "--include",
        help="include material from a file",
    ).complete = shtab.FILE  # type: ignore
    parser.add_argument(
        "-o",
        "--output",
        help="send output",
    ).complete = shtab.FILE  # type: ignore
    parser.add_argument(
        "--template",
        choices=["man", "markdown"],
        default="man",
        help="built-in template name. default: %(default)s",
    )
    parser.add_argument(
        "--template-file",
        help="template file.",
    ).complete = shtab.FILE  # type: ignore
    parser.add_argument(
        "--help-option",
        help="help option string, default: %(default)s",
    )
    parser.add_argument(
        "--version-option",
        help="version option string, default: %(default)s",
    )
    parser.add_argument(
        "--no-discard-stderr",
        action="store_true",
        help="include stderr when parsing option output",
    )
    parser.add_argument(
        "executable",
        nargs=1,
        help="executable program name",
    ).complete = CMD  # type: ignore
    parser.add_argument(
        "args",
        metavar="...",
        nargs="...",
        help="executable program arguments",
    ).complete = ARGS  # type: ignore
    for action in parser._actions:
        action.default = DEFAULTS.get(action.dest, action.default)
    return parser


def main() -> None | NoReturn:
    """``python -m translate_shell`` call this function.
    Parse arguments is before init configuration to provide ``--config``.

    :rtype: None | NoReturn
    """
    parser = get_parser()
    args = parser.parse_args()

    from .ui.cli import run

    run(args)


if __name__ == "__main__":
    main()
