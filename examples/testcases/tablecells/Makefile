.SUFFIXES: .dvi .pdf
all: test.pdf
DIR:=$(shell dirname `find ../../..  -name paratext2.tex`)
.tex.pdf:
	TEXINPUTS=.:$(DIR) xetex -no-pdf $<
	TEXINPUTS=.:$(DIR) xetex $<
	

test.pdf: test.tex usfmTex-ext.tex usfmTex-settings.tex test.usfm $(DIR)/*.tex *.sty

bisect:
	mkdir ../bisect || rm -f ../bisect/*
	cp *.tex *.usfm *.sty Makefile ../bisect

auto:
	echo Source code in $(DIR)
	while inotifywait -e close_write . $(DIR) ; do make test.pdf ; done < /dev/null

