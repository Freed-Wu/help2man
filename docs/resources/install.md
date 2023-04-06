# Install

## [AUR](https://aur.archlinux.org/packages/help2man)

```sh
yay -S help2man
```

## [Nix](https://nixos.org)

For NixOS, add the following code to `/etc/nixos/configuration.nix`:

```nix
{ config, pkgs, ... }:
{
  nix.settings.experimental-features = [ "flakes" ];
  environment.systemPackages =
    let
      help2man = (
        builtins.getFlake "github:Freed-Wu/help2man"
      ).packages.${builtins.currentSystem}.default;
    in
    [
      help2man
    ];
}
```

For nix,

```sh
nix shell github:Freed-Wu/help2man
```

Or just take a try without installation:

```sh
nix run github:Freed-Wu/help2man -- --help
```

## [PYPI](https://pypi.org/project/help2man)

```sh
pip install help2man
```
