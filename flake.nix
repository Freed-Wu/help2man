{
  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";
  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem
      (system:
        with nixpkgs.legacyPackages.${system};
        with python3.pkgs;
        {
          formatter = nixpkgs-fmt;
          packages.default = buildPythonApplication rec {
            pname = "help2man";
            version = "";
            src = self;
            disabled = pythonOlder "3.6";
            propagatedBuildInputs = [
              jinja2
            ];
            nativeCheckInputs = [
              setuptools
              shtab
            ];
            pythonImportsCheck = [
              "help2man"
            ];
          };
        }
      );
}
