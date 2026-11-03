#!/usr/bin/env bash
# Build both IEEE versions.  Requires TeX Live with the IEEEtran class
# (Debian/Ubuntu: sudo apt install texlive-publishers texlive-latex-extra).
set -e
build () {
  name="$1"
  pdflatex -interaction=nonstopmode "$name" >/dev/null || true
  bibtex "$name"        >/dev/null || true
  pdflatex -interaction=nonstopmode "$name" >/dev/null || true
  pdflatex -interaction=nonstopmode "$name" >/dev/null || true
  echo "built $name.pdf"
}
build main             # two-column journal version (camera-ready style)
build main_peerreview  # single-column, double-spaced submission version
