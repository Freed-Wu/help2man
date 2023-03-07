"""Provide ``__version__`` for
`importlib.metadata.version() <https://docs.python.org/3/library/importlib.metadata.html#distribution-versions>`_.
"""
import io
import logging
import re
from argparse import ArgumentParser, Namespace
from contextlib import nullcontext, redirect_stderr, redirect_stdout
from datetime import datetime
from pathlib import Path
from typing import Callable

from jinja2 import Template

try:
    from ._version import __version__, __version_tuple__  # type: ignore
except ImportError:
    # for `python -m build` use help2man to generate man page of help2man
    __version__ = "rolling"
    __version_tuple__ = (0, 0, 0, __version__, "")

PAT = re.compile(r"\x1b\[[0-9;]+?m")
logger = logging.getLogger(__name__)
ASSETS_PATH = Path(__file__).absolute().parent / "assets"
TEMPLATES = {
    "man": (ASSETS_PATH / "jinja2" / "template.man.j2").read_text(),
    "markdown": (ASSETS_PATH / "jinja2" / "template.md.j2").read_text(),
}
PAT_SECTION = re.compile(r"\n\n(?=\S)")
PAT_SPACE = re.compile("  +")
DEFAULTS = {
    "help_option": "--help",
    "version_option": "--version",
    "name": "Name",
    "section": "1",
    "manual": "User Commands",
    "source": "",
    "info_page": "",
    "no_discard_stderr": False,
}


def get_output(
    f: Callable,
    args: tuple = (),
    no_discard_stderr: bool = DEFAULTS["no_discard_stderr"],
) -> str:
    """Get stdout and stderr of a function.

    :param f:
    :type f: Callable
    :param args:
    :type args: tuple
    :param no_discard_stderr:
    :type no_discard_stderr: bool
    :rtype: str
    """
    string = io.StringIO()
    if no_discard_stderr:
        ctx = redirect_stderr(string)
    else:
        ctx = nullcontext()
    with redirect_stdout(string), ctx:
        f(*args)
    string.seek(0)
    output = string.read()
    return output


def parser2strings(
    parser: ArgumentParser,
    no_discard_stderr: bool = DEFAULTS["no_discard_stderr"],
) -> tuple[str, str]:
    """Convert a parser to help string and version string.

    :param parser:
    :type parser: ArgumentParser
    :param no_discard_stderr:
    :type no_discard_stderr: bool
    :rtype: tuple[str, str]
    """
    actions = parser._option_string_actions
    helpstr = get_output(parser.print_help, (), no_discard_stderr)
    try:
        versionstr = actions["--version"].version  # type: ignore
    except KeyError:
        versionstr = ""
    return helpstr, versionstr


def parser2man(
    parser: ArgumentParser,
    name: str = DEFAULTS["name"],
    section: str = DEFAULTS["section"],
    manual: str = DEFAULTS["manual"],
    source: str = DEFAULTS["source"],
    info_page: str = DEFAULTS["info_page"],
    template: str = TEMPLATES["man"],
) -> str:
    """Convert a parser to man.

    :param parser:
    :type parser: ArgumentParser
    :param name:
    :type name: str
    :param section:
    :type section: str
    :param manual:
    :type manual: str
    :param source:
    :type source: str
    :param info_page:
    :type info_page: str
    :param template:
    :type template: str
    :rtype: str
    """
    man = help2man(
        *parser2strings(parser),
        name,
        section,
        manual,
        source,
        info_page,
        template,
    )
    return man


def help2man(
    helpstr: str,
    versionstr: str,
    name: str = DEFAULTS["name"],
    section: str = DEFAULTS["section"],
    manual: str = DEFAULTS["manual"],
    source: str = DEFAULTS["source"],
    info_page: str = DEFAULTS["info_page"],
    template: str = TEMPLATES["man"],
) -> str:
    """Convert help string and version string to man.

    :param helpstr:
    :type helpstr: str
    :param versionstr:
    :type versionstr: str
    :param name:
    :type name: str
    :param section:
    :type section: str
    :param manual:
    :type manual: str
    :param source:
    :type source: str
    :param info_page:
    :type info_page: str
    :param template:
    :type template: str
    :rtype: str
    """
    helpstr = PAT.sub("", helpstr)
    paragraphs = PAT_SECTION.split(helpstr)
    prog = ""
    synopsis = ""
    i = -1
    for i, paragraph in enumerate(paragraphs):
        if paragraph.startswith("usage: ") or paragraph.startswith("Usage: "):
            synopsis = (
                paragraph.replace("usage: ", "")
                .replace("Usage: ", "")
                .replace("\n" + " " * len("usage: "), "\n")
            )
            prog = synopsis.split(" ")[0]
            break
        elif paragraph.startswith("usage:\n") or paragraph.startswith(
            "Usage:\n"
        ):
            synopsis = paragraph.replace("usage:\n", "").replace(
                "Usage:\n", ""
            )
            prog = synopsis.strip().split(" ")[0]
            break
    if i == 0:
        # argparse's description may be in 1-st paragraph
        if paragraphs[1].splitlines()[0].endswith(":"):
            description = ""
        else:
            description = paragraphs[1]
    elif i == 1:
        description = " ".join(paragraphs[0].split(" ")[1:])
    else:
        description = ""
    sections = []
    version = copyright = author = bug = ""
    for paragraph in paragraphs[2:]:
        lines = paragraph.splitlines()
        if not lines[0].endswith(":"):
            tokens = lines[0].split("Report bugs to ")
            if len(tokens) > 1:
                bug = tokens[1]
            break
        sec = Namespace(title=lines[0].strip(":"), contents=[])
        length = len(lines[1]) - len(lines[1].lstrip())
        paragraph = paragraph.replace("\n " + " " * length, "")
        lines = paragraph.splitlines()
        for line in lines[1:]:
            line = line[length:]
            tokens = PAT_SPACE.split(line)
            content = Namespace()
            if len(tokens) > 1:
                content.name = tokens[0]
                content.description = " ".join(tokens[1:])
            else:
                content.description = tokens[-1]
            sec.contents += [content]
        sections += [sec]
    lines = versionstr.splitlines()
    try:
        version = lines[0].split(" ")[-1]
        for line in lines[1:]:
            tokens = line.split("Copyright (C) ")
            if len(tokens) > 1:
                copyright = tokens[-1]
                continue
            tokens = line.split("Written by ")
            if len(tokens) > 1:
                author = tokens[-1]
    except IndexError:
        logger.warning("version format is not correct.")
    man = Template(template).render(
        help2man_version=__version__,
        date=datetime.now().strftime("%F"),
        prog=prog,
        synopsis=synopsis,
        description=description,
        sections=sections,
        bug=bug,
        author=author,
        version=version,
        copyright=copyright,
        name=name,
        section=section,
        manual=manual,
        source=source,
        info_page=info_page,
    )
    return man
