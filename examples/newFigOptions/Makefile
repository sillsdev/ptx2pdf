.SUFFIXES: .dvi .pdf
all: test.pdf
DIR:=$(shell dirname `find ../../..  -name paratext2.tex`)
.tex.pdf:
	TEXINPUTS=.:$(DIR) xetex $<
	TEXINPUTS=.:$(DIR) xetex $<
	

test.pdf: test.tex usfmTex-ext.tex usfmTex-settings.tex test.usfm.piclist test.usfm $(DIR)/*.tex *.sty

auto:
	while inotifywait -e close_write . $(DIR) ; do sleep 1 ; make test.pdf ; done </dev/null
bisect:
	mkdir ../bisect || rm -f ../bisect/*
	cp *.tex *.usfm *.sty Makefile ../bisect


