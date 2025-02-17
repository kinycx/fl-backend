{pkgs}: {
  deps = [
    pkgs.cacert
    pkgs.zlib
    pkgs.tk
    pkgs.tcl
    pkgs.openjpeg
    pkgs.libxcrypt
    pkgs.libwebp
    pkgs.libtiff
    pkgs.libjpeg
    pkgs.libimagequant
    pkgs.lcms2
    pkgs.freetype
    pkgs.pgadmin4
    pkgs.libpg_query
    pkgs.libpqxx
    pkgs.libpqxx_6
    pkgs.postgresql
    pkgs.python3
    pkgs.python3Packages.psycopg
    pkgs.gcc
    pkgs.pkg-config
    pkgs.xcodebuild
  ];
}
