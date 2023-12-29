{
  description = "Application packaged using poetry2nix";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryApplication defaultPoetryOverrides;
      in
      {
        packages = {
          k8s-app-bootstrap = mkPoetryApplication { 
            projectDir = self;
            propogatedBuildInputs = [ pkgs.util-linux pkgs.gnutar ];
            overrides = defaultPoetryOverrides.extend
            (self: super: {
              filebrowser-client = super.filebrowser-client.overridePythonAttrs
              (
                old: {
                  buildInputs = (old.buildInputs or [ ]) ++ [ super.setuptools super.poetry ];
                }
              );
            });
          };
          default = self.packages.${system}.k8s-app-bootstrap;
          dockerImage = pkgs.dockerTools.buildLayeredImage {
              name = "k8s-app-bootstrap";
              contents = [ self.packages.${system}.k8s-app-bootstrap pkgs.util-linux pkgs.gnutar ];
              config.Cmd = [ "app" ];
            };
        };

        devShells.default = pkgs.mkShell {
          inputsFrom = [ self.packages.${system}.k8s-app-bootstrap ];
          packages = [ pkgs.poetry ];
        };
      });
}
