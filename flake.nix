{
  description = "python_api_sample";

  inputs = {
    nixpkgs.url = "github:NixOs/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { nixpkgs, flake-utils, ... }: flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = import nixpkgs {
        inherit system;
      };
    in rec {
      devShell = pkgs.mkShell {
        buildInputs = with pkgs; [
          (python3.withPackages (
            python-packages:
            with python-packages;
            [
              requests
              beautifulsoup4
              transformers
              pytorch
 
              (buildPythonPackage rec {
                pname = "germansentiment";
                version = "1.1.0";
                src = fetchPypi {
                  inherit pname version;
                  sha256 = "sha256-ZJ/l1nHwUQqBbpkCNl6Kcvq60f9KNqMmR9Dh2KUgzng=";
                };
                doCheck = false;
              })
            ]))

        ];
      };
    }
  );
}
