#!/usr/bin/env bash
# Build the Finite Fields and Their Applications manuscript.
# Requires TeX Live with the elsarticle class
# (Debian/Ubuntu: sudo apt install texlive-publishers texlive-latex-extra).
set -e
pdflatex -interaction=nonstopmode -halt-on-error main
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main
pdflatex -interaction=nonstopmode -halt-on-error main
echo "built main.pdf"
