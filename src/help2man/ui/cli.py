"""Command Line Interface
=========================
"""
from argparse import Namespace

from .. import TEMPLATES, help2man
from . import init


def run(args: Namespace) -> None:
    """Run.

    :param args:
    :type args: Namespace
    :rtype: None
    """
    args = init(args)
    template = TEMPLATES[args.template]
    if args.template_file:
        with open(args.template_file) as f:
            template = f.read()
    output = help2man(
        args.helpstr,
        args.versionstr,
        args.name,
        args.section,
        args.manual,
        args.source,
        args.info_page,
        template,
    )
    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
    else:
        print(output)
