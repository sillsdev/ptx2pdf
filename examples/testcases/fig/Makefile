.SUFFIXES: .dvi .pdf
all: test.pdf
DIR:=$(shell dirname `find ../../..  -name paratext2.tex`)
.tex.pdf:
	-mkdir 1 2 3
	TEXINPUTS=.:$(DIR) xetex $<
	cp test.pdf test.parlocs test.delayed 1
	TEXINPUTS=.:$(DIR) xetex $< 
	cp test.pdf test.parlocs test.delayed 2
	TEXINPUTS=.:$(DIR) xetex $<
	cp test.pdf test.parlocs test.delayed 3
	TEXINPUTS=.:$(DIR) xetex $<
	

test.pdf: test.tex usfmTex-ext.tex usfmTex-settings.tex test.usfm $(DIR)/*.tex *.sty test.usfm test.usfm.piclist

bisect:
	mkdir ../bisect || rm -f ../bisect/*
	cp *.tex *.usfm *.sty *.piclist Makefile image.jpg ../bisect

auto:
	echo Source code in $(DIR)
	while inotifywait -e close_write . $(DIR) ; do make test.pdf ; done < /dev/null

1:
	rename -f 's/\./.1./' test.pdf test.parlocs test.delayed
