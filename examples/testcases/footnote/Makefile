.SUFFIXES: .dvi .pdf
all: test.pdf longtest.pdf
DIR:=$(shell dirname `find ../../..  -name paratext2.tex`)
.tex.pdf:
	TEXINPUTS=.:$(DIR) xetex $<
	TEXINPUTS=.:$(DIR) xetex $<
	

test.pdf: test.tex usfmTex-ext.tex usfmTex-settings.tex test.usfm $(DIR)/*.tex *.sty
longtest.pdf: longtest.tex usfmTex-ext.tex usfmTex-settings.tex longtest.usfm $(DIR)/*.tex *.sty

auto:
	echo Source code in $(DIR)
	while inotifywait -e close_write . $(DIR) ; do make all ; done < /dev/null
autotest:
	echo Source code in $(DIR)
	while inotifywait -e close_write . $(DIR) ; do make test.pdf ; done < /dev/null
autolong:
	echo Source code in $(DIR)
	while inotifywait -e close_write . $(DIR) ; do make longtest.pdf ; done < /dev/null


bisect:
	mkdir ../bisect || rm -f ../bisect/*
	cp *.tex *.usfm *.sty Makefile ../bisect


