#!/usr/bin/env bash
# Build both IEEE versions.  Requires TeX Live with the IEEEtran class
# (Debian/Ubuntu: sudo apt install texlive-publishers texlive-latex-extra).
set -e
build () {
  name="$1"
  pdflatex -interaction=nonstopmode -halt-on-error "$name"
  bibtex "$name"
  pdflatex -interaction=nonstopmode -halt-on-error "$name"
  pdflatex -interaction=nonstopmode -halt-on-error "$name"
  echo "built $name.pdf"
}
build main             # two-column journal version (camera-ready style)
build main_peerreview  # single-column, double-spaced submission version
