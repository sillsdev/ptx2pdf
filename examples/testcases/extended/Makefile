.SUFFIXES: .dvi .pdf
all: test.pdf
DIR:=$(shell dirname `find ../../..  -name paratext2.tex`)
.tex.pdf:
	#TEXINPUTS=.:$(DIR) xetex -no-pdf $<
	TEXINPUTS=.:$(DIR) xetex $<
	TEXINPUTS=.:$(DIR) xetex $<
	

test.pdf: test.tex usfmTex-ext.tex usfmTex-settings.tex test.usfm $(DIR)/*.tex *.sty cover.usfm test.usfm.adj
test2.pdf: test2.tex usfmTex-ext.tex usfmTex-settings.tex test2.usfm $(DIR)/*.tex *.sty test.usfm.adj

bisect:
	mkdir ../bisect || rm -fr ../bisect/*
	cp *.tex *.usfm *.jpg inner_include.pdf *.sty Makefile ../bisect

auto: test.pdf
	echo Source code in $(DIR)
	while inotifywait -e close_write . $(DIR) ; do sleep 0.5; make test.pdf ; done < /dev/null
auto2: test2.pdf
	echo Source code in $(DIR)
	while inotifywait -e close_write . $(DIR) ; do make test2.pdf ; done < /dev/null
