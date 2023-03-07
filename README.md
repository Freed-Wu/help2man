# help2man

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Freed-Wu/help2man/main.svg)](https://results.pre-commit.ci/latest/github/Freed-Wu/help2man/main)
[![github/workflow](https://github.com/Freed-Wu/help2man/actions/workflows/main.yml/badge.svg)](https://github.com/Freed-Wu/help2man/actions)
[![codecov](https://codecov.io/gh/Freed-Wu/help2man/branch/main/graph/badge.svg)](https://codecov.io/gh/Freed-Wu/help2man)
[![readthedocs](https://shields.io/readthedocs/help2man)](https://help2man.readthedocs.io)

[![github/downloads](https://shields.io/github/downloads/Freed-Wu/help2man/total)](https://github.com/Freed-Wu/help2man/releases)
[![github/downloads/latest](https://shields.io/github/downloads/Freed-Wu/help2man/latest/total)](https://github.com/Freed-Wu/help2man/releases/latest)
[![github/issues](https://shields.io/github/issues/Freed-Wu/help2man)](https://github.com/Freed-Wu/help2man/issues)
[![github/issues-closed](https://shields.io/github/issues-closed/Freed-Wu/help2man)](https://github.com/Freed-Wu/help2man/issues?q=is%3Aissue+is%3Aclosed)
[![github/issues-pr](https://shields.io/github/issues-pr/Freed-Wu/help2man)](https://github.com/Freed-Wu/help2man/pulls)
[![github/issues-pr-closed](https://shields.io/github/issues-pr-closed/Freed-Wu/help2man)](https://github.com/Freed-Wu/help2man/pulls?q=is%3Apr+is%3Aclosed)
[![github/discussions](https://shields.io/github/discussions/Freed-Wu/help2man)](https://github.com/Freed-Wu/help2man/discussions)
[![github/milestones](https://shields.io/github/milestones/all/Freed-Wu/help2man)](https://github.com/Freed-Wu/help2man/milestones)
[![github/forks](https://shields.io/github/forks/Freed-Wu/help2man)](https://github.com/Freed-Wu/help2man/network/members)
[![github/stars](https://shields.io/github/stars/Freed-Wu/help2man)](https://github.com/Freed-Wu/help2man/stargazers)
[![github/watchers](https://shields.io/github/watchers/Freed-Wu/help2man)](https://github.com/Freed-Wu/help2man/watchers)
[![github/contributors](https://shields.io/github/contributors/Freed-Wu/help2man)](https://github.com/Freed-Wu/help2man/graphs/contributors)
[![github/commit-activity](https://shields.io/github/commit-activity/w/Freed-Wu/help2man)](https://github.com/Freed-Wu/help2man/graphs/commit-activity)
[![github/last-commit](https://shields.io/github/last-commit/Freed-Wu/help2man)](https://github.com/Freed-Wu/help2man/commits)
[![github/release-date](https://shields.io/github/release-date/Freed-Wu/help2man)](https://github.com/Freed-Wu/help2man/releases/latest)

[![github/license](https://shields.io/github/license/Freed-Wu/help2man)](https://github.com/Freed-Wu/help2man/blob/main/LICENSE)
[![github/languages](https://shields.io/github/languages/count/Freed-Wu/help2man)](https://github.com/Freed-Wu/help2man)
[![github/languages/top](https://shields.io/github/languages/top/Freed-Wu/help2man)](https://github.com/Freed-Wu/help2man)
[![github/directory-file-count](https://shields.io/github/directory-file-count/Freed-Wu/help2man)](https://github.com/Freed-Wu/help2man)
[![github/code-size](https://shields.io/github/languages/code-size/Freed-Wu/help2man)](https://github.com/Freed-Wu/help2man)
[![github/repo-size](https://shields.io/github/repo-size/Freed-Wu/help2man)](https://github.com/Freed-Wu/help2man)
[![github/v](https://shields.io/github/v/release/Freed-Wu/help2man)](https://github.com/Freed-Wu/help2man)

[![pypi/status](https://shields.io/pypi/status/help2man)](https://pypi.org/project/help2man/#description)
[![pypi/v](https://shields.io/pypi/v/help2man)](https://pypi.org/project/help2man/#history)
[![pypi/downloads](https://shields.io/pypi/dd/help2man)](https://pypi.org/project/help2man/#files)
[![pypi/format](https://shields.io/pypi/format/help2man)](https://pypi.org/project/help2man/#files)
[![pypi/implementation](https://shields.io/pypi/implementation/help2man)](https://pypi.org/project/help2man/#files)
[![pypi/pyversions](https://shields.io/pypi/pyversions/help2man)](https://pypi.org/project/help2man/#files)

Convert `--help` and `--version` to man page.

## Similar Projects

- [GNU help2man](https://www.gnu.org/software/help2man) Generate manpage for
  any program with `--help` and `--version`. Written in perl.
- [click-man](https://github.com/click-contrib/click-man) Generate manpage for
  click-based python program. Written in python.
- [cli2man](https://github.com/tobimensch/cli2man) Generate manpage and
  markdown for any program with `--help` and `--version`. Written in python.
- This project:  Generate manpage, markdown or any format (if you provide
  a [jinja](https://docs.jinkan.org/docs/jinja2/templates.html) template) for
  any program with `--help` and `--version` or any argparse-based python
  program.

## Intention

This a python version of [GNU help2man](https://www.gnu.org/software/help2man). It
solves the following problems[^email]:

### `GNU help2man` cannot convert `argparse` correctly

Because [argparse](https://docs.python.org/3/library/argparse.html) outputs:

```text
usage: help2man [-h] ...
                executable ...

Convert --help and --version to man page.

positional arguments:
  executable            executable program name
  ...

options:
  -h                    show this help message and exit
  ...
```

`help2man` will ignore `positional arguments:` and `options:` because it only
detect `Options:`. And it only detect first line as synopsis and detect other
lines as description incorrectly.

### `GNU help2man` cannot customize template

I provide `help2man --template XXX` and `help2man --template-file XXX` to do
it. The template language is
[jinja2](http://docs.jinkan.org/docs/jinja2/templates.html). See
[template](https://github.com/Freed-Wu/help2man/tree/main/src/help2man/assets/jinja2)
as examples.

### GNU help2man don't provide any programming API

Now you can use it in python. If you want to generate man pages automatically
when you build a python project, you can see
[setuptools-generate](https://pypi.org/project/setuptools-generate):

See [document](https://help2man.readthedocs.io) to know more.

[^email]: I send email to the author of `GNU help2man` but got no response.
