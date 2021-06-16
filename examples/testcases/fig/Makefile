.SUFFIXES: .dvi .pdf
all: test.pdf
DIR:=$(shell dirname `find ../../..  -name paratext2.tex`)
test.pdf:test.tex
	-mkdir 1 2 3 4 5 6 7 8 9
	TEXINPUTS=.:$(DIR) xetex $<
	cp test.pdf test.parlocs test.delayed test.log 1
	if grep Rerun test.log ; then TEXINPUTS=.:$(DIR) xetex $<  && cp test.pdf test.parlocs test.delayed test.log 2; else rm  -f 2/* ; fi 
	if grep Rerun test.log ; then TEXINPUTS=.:$(DIR) xetex $<  && cp test.pdf test.parlocs test.delayed test.log 3;  else rm  -f 3/* ; fi 
	if grep Rerun test.log ; then TEXINPUTS=.:$(DIR) xetex $<  && cp test.pdf test.parlocs test.delayed test.log 4; else rm  -f 4/* ; fi 
	if grep Rerun test.log ; then TEXINPUTS=.:$(DIR) xetex $<  && cp test.pdf test.parlocs test.delayed test.log 5; else rm  -f 5/* ; fi 
	if grep Rerun test.log ; then TEXINPUTS=.:$(DIR) xetex $<  && cp test.pdf test.parlocs test.delayed test.log 6; else rm  -f 6/* ; fi 
	if grep Rerun test.log ; then TEXINPUTS=.:$(DIR) xetex $<  && cp test.pdf test.parlocs test.delayed test.log 7; else rm  -f 7/* ; fi 
	if grep Rerun test.log ; then TEXINPUTS=.:$(DIR) xetex $<  && cp test.pdf test.parlocs test.delayed test.log 8; else rm  -f 8/* ; fi 
	if grep Rerun test.log ; then TEXINPUTS=.:$(DIR) xetex $<  && cp test.pdf test.parlocs test.delayed test.log 9; else rm  -f 9/* ; fi 
	

test.pdf: test.tex usfmTex-ext.tex usfmTex-settings.tex test.usfm $(DIR)/*.tex *.sty test.usfm test.usfm.piclist

bisect:
	mkdir ../bisect || rm -f ../bisect/*
	cp *.tex *.usfm *.sty *.piclist Makefile image.jpg ../bisect

map.jpg:?/test.pdf Makefile
	for  A in `seq 1 8` ; do test -f $$A/test.pdf && gs -q -dNOPAUSE -dSAFER -sDEVICE=jpeg -dFirstPage=1 -dLastPage=1 -dBATCH -r144x144 -dTextAlphaBits=4 -dDownScaleFactor=2 -sOutputFile=$$A/test.jpg $$A/test.pdf  ; done
	montage [0-9]/test.jpg -tile 4x3 -geometry +0+0 maps.jpg

	
auto:
	echo Source code in $(DIR)
	while inotifywait -e close_write . $(DIR) ; do make test.pdf ; done < /dev/null

1:
	rename -f 's/\./.1./' test.pdf test.parlocs test.delayed
