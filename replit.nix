{pkgs}: {
  deps = [
    pkgs.postgresql
    pkgs.python3
    pkgs.python3Packages.psycopg
    pkgs.gcc
    pkgs.pkg-config
  ];
}
