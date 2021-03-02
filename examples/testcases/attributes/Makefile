.SUFFIXES: .dvi .pdf
all: test.pdf diglot.pdf

DIR:=$(shell dirname `find ../../..  -name paratext2.tex`)
.tex.pdf:
	TEXINPUTS=.:$(DIR) xetex -no-pdf $<
	TEXINPUTS=.:$(DIR) xetex $<
	

test.pdf: test.tex test.usfm test.sty $(DIR)/*.tex 
diglot.pdf: diglot.tex diglot.usfm diglot.sty $(DIR)/*.tex 

bisect:
	mkdir ../bisect || rm -f ../bisect/*
	cp *.tex *.usfm *.sty Makefile ../bisect

auto:
	echo Source code in $(DIR)
	while inotifywait -e close_write . $(DIR) ; do make ; done < /dev/null
