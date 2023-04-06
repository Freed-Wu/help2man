#!/usr/bin/env python
"""Set up."""
import logging
import sys
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path

from setuptools import setup
from shtab import complete

here = Path(__file__).absolute().parent
src = here / "src"
sys.path.insert(0, str(src))

from help2man import __version__, parser2man  # type: ignore # noqa: E402
from help2man.__main__ import get_parser  # noqa: E402

logger = logging.getLogger(__name__)
parser = get_parser()
prog = parser.prog
shells = {
    "bash": prog,
    "zsh": "_" + prog,
    "tcsh": prog + ".csh",
}
sdist = here / "sdist"
sdist.mkdir(exist_ok=True, parents=True)
man = sdist / (prog + ".1")
txt = src / "help2man" / "assets" / "txt"
templates = here / "templates"


def generate_completions(
    parser: ArgumentParser, shells: dict[str, str], path: Path
) -> None:
    """Generate completions.

    :param parser:
    :type parser: ArgumentParser
    :param shells:
    :type shells: dict[str, str]
    :param path:
    :type path: Path
    :rtype: None
    """
    for shell, name in shells.items():
        content = complete(parser, shell)
        with open(path / name, "w") as f:
            f.write(content)


def generate_man(man: Path) -> None:
    """Generate man.

    :param man:
    :type man: Path
    :rtype: None
    """
    output = parser2man(parser)
    with open(man, "w") as f:
        f.write(output)


def update_assets() -> None:
    """Update assets.

    :rtype: None
    """
    try:
        import tomllib  # type: ignore
    except ImportError:
        try:
            import tomli as tomllib
        except ImportError:
            return None

    with open(here / "pyproject.toml", "rb") as f:
        project = tomllib.load(f)["project"]
    with open(txt / "description.txt", "w") as f:
        f.write(project["description"] + "\n")
    with open(templates / "epilog.txt") as f:
        template = f.read()
    with open(txt / "epilog.txt", "w") as f:
        f.write(template.format(bug=project["urls"]["Bug Report"]))
    with open(templates / "version.txt") as f:
        template = f.read()
    with open(txt / "version.txt", "w") as f:
        f.write(
            template.format(
                version=__version__,
                author=project["authors"][0]["name"],
                copyright="2022-" + str(datetime.now().year),
            )
        )


if __name__ == "__main__":
    update_assets()
    generate_completions(parser, shells, sdist)
    generate_man(man)
    setup()
