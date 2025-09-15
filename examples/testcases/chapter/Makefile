.SUFFIXES: .dvi .pdf
all: test.pdf
DIR:=$(shell dirname `find ../../..  \( -name test -prune \) -o -name paratext2.tex -print` )
.tex.pdf:
	-mkdir 1 2 3 4
	TEXINPUTS=.:$(DIR) xetex $<
	cp test.pdf test.parlocs test.delayed test.log 1
	if grep Rerun test.log ; then TEXINPUTS=.:$(DIR) xetex $<  && cp test.pdf test.parlocs test.delayed test.log 2; else rm  -f 2/* ; fi 
	if grep Rerun test.log ; then TEXINPUTS=.:$(DIR) xetex $<  && cp test.pdf test.parlocs test.delayed test.log 3;  else rm  -f 3/* ; fi 
	if grep Rerun test.log ; then TEXINPUTS=.:$(DIR) xetex $<  && cp test.pdf test.parlocs test.delayed test.log 4; else rm  -f 4/* ; fi 
	

test.pdf: test.tex usfmTex-ext.tex usfmTex-settings.tex test.usfm $(DIR)/*.tex *.sty test.usfm test.usfm.piclist

bisect:
	-mkdir ../bisect || rm -f ../bisect/*
	cp *.tex *.usfm *.sty *.piclist Makefile image.jpg *.png ../bisect

auto:
	echo Source code in $(DIR)
	while inotifywait -e close_write . $(DIR) ; do sleep 2; make test.pdf ; date; done < /dev/null

1:
	rename -f 's/\./.1./' test.pdf test.parlocs test.delayed
