# Install & Uninstall

## [AUR](https://aur.archlinux.org/packages/python-help2man)

Install:

```sh
yay -S python-help2man
```

uninstall:

```sh
sudo pacman -R python-help2man
```

## [PYPI](https://pypi.org/project/help2man)

Install:

```sh
pip install help2man
```

Since now, pip don't support installing man and shell completions.
You must install them manually.

Download shell completions and man from
[releases](https://github.com/Freed-Wu/help2man/releases) to the correct
paths:

- bash: `/usr/share/bash-completion/completions/trans`
- zsh: `/usr/share/zsh/site-functions/_trans`
- tcsh: `/etc/profile.d/trans.csh`
- man: `/usr/share/man/man1/trans.1.gz`

**NOTE**: the paths of man and shell completion vary from different OS. The path
of the above code is just for GNU/Linux. For other OSs, do a substitution:

- GNU/Linux, Windows (msys/Msys2, Cygwin): `/usr/share`, `/etc`
- Windows (non-msys/Msys2): `$MINGW_PREFIX/share`,`/etc`
- BSD, Darwin, GNU/Linux (Homebrew): `/usr/local/share`, `/usr/local/etc`
- Android (Termux): `/data/data/com.termux/files/usr/share`,
  `/data/data/com.termux/files/usr/etc`
- Android (Magisk): `/system/usr/share`, `/system/etc`

Uninstall:

```sh
pip uninstall help2man
```

Delete shell completions and man by yourself.
