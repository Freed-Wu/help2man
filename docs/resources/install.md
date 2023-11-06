# Install

## [AUR](https://aur.archlinux.org/packages/help2man)

```bash
yay -S python-help2man
```

## [NUR](https://nur.nix-community.org/repos/freed-wu)

```nix
{ config, pkgs, ... }:
{
  nixpkgs.config.packageOverrides = pkgs: {
    nur = import
      (
        builtins.fetchTarball
          "https://github.com/nix-community/NUR/archive/master.tar.gz"
      )
      {
        inherit pkgs;
      };
  };
  environment.systemPackages = with pkgs;
      (
        python3.withPackages (
          p: with p; [
            nur.repos.Freed-Wu.help2man
          ]
        )
      )
}
```

## [Nix](https://nixos.org)

```sh
nix shell github:Freed-Wu/help2man
```

Run without installation:

```sh
nix run github:Freed-Wu/help2man -- --help
```

## [PYPI](https://pypi.org/project/help2man)

```sh
pip install help2man
```
