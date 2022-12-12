"""Provide CLI."""
import logging
from argparse import Namespace
from shlex import split
from subprocess import PIPE, STDOUT, run

from .. import DEFAULTS

logger = logging.getLogger(__name__)


def get_cmd_output(
    tokens: list[str], no_discard_stderr: bool = DEFAULTS["no_discard_stderr"]
) -> str:
    """Get cmd output.

    :param tokens:
    :type tokens: list[str]
    :param no_discard_stderr:
    :type no_discard_stderr: bool
    :rtype: str
    """
    if no_discard_stderr:
        rst = run(tokens, stdout=PIPE, stderr=STDOUT, universal_newlines=True)
    else:
        rst = run(tokens, capture_output=True, universal_newlines=True)
    return rst.stdout


def init(args: Namespace) -> Namespace:
    """Init.

    :param args:
    :type args: Namespace
    :rtype: Namespace
    """
    help_tokens = args.executable + args.args + split(args.help_option)
    version_tokens = args.executable + args.args + split(args.version_option)
    args.helpstr = get_cmd_output(help_tokens, args.no_discard_stderr)
    args.versionstr = get_cmd_output(version_tokens, args.no_discard_stderr)
    if args.include:
        try:
            with open(args.include) as f:
                args.help += f.read()
        except FileNotFoundError as e:
            logger.warning(e)
            logger.warning("ignore " + args.include)
    return args
