.SUFFIXES: .dvi .pdf
all: test.pdf

DIR:=$(shell dirname `find ../../..  \( -name test -prune -or -name tmp -prune \) -or -name paratext2.tex -print`)
FONTS:=$(abspath $(DIR)/../fonts)
XETEX:=TEXINPUTS=.:$(DIR) TTFONTS=$(FONTS): FONTCONFIG_FILE=$(CURDIR)/fonts.conf xetex -no-pdf
.tex.pdf:
	$(XETEX) $<
	$(XETEX) $<
	dvipdfmx -C16 $(subst .tex,.xdv,$<)

test.pdf: test.tex test.usfm test.sty fonts.conf $(DIR)/*.tex $(DIR)/*.sty

# Charis comes from the repository fonts; this adds them for Source Code Pro too
fonts.conf:
	printf '<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "fonts.dtd"><fontconfig><include>/etc/fonts/fonts.conf</include><dir>%s</dir></fontconfig>\n' $(FONTS) > $@

# The PTXprint margin-note solver and rerun loop are in Python, so plain xetex
# cannot show the #1258 jitter. These drive RunJob.run_xetex() on this fixture.
# The targets share their names with run.py's output directories, so they must
# be phony, and each clears the previous evidence that run.py refuses to reuse.
PYTHON?=python3
.PHONY: converge reproduce
converge:
	rm -rf converge
	$(PYTHON) run.py --output converge --verify-convergence

reproduce:
	rm -rf reproduce
	$(PYTHON) run.py --output reproduce --verify-reproduction
