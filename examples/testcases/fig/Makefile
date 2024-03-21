.SUFFIXES: .dvi .pdf
all: test.pdf
DIR:=$(shell dirname `find ../../..  -name paratext2.tex`)
test.pdf:test.tex $(DIR)/*.tex
	-rm test.delayed
	TEXINPUTS=.:$(DIR) FONTCONFIG_FILE=~/.config/ptxprint/fonts.conf xetex $< && cp test.pdf test.parlocs test.delayed test.log 1
	A=1 ; while grep Rerun test.log ; do FONTCONFIG_FILE=~/.config/ptxprint/fonts.conf TEXINPUTS=.:$(DIR) xetex $<  && mkdir $$A ; cp test.pdf test.parlocs test.delayed test.log $$A; A=$$((A+1)); if [ $$A -gt 20 ] ; then break ; fi ;  done ; echo last one: $$A  ; for A in `seq $$A 15` ; do rm $$A/*;done
	
testpages.pdf:testpages.tex
	xetex testpages.tex
	cp testpages.pdf "test pages.pdf"

test.pdf: test.tex usfmTex-ext.tex usfmTex-settings.tex test.usfm $(DIR)/*.tex *.sty test.usfm test.usfm.piclist testpages.pdf

bisect:
	-mkdir ../bisect || rm -f ../bisect/* 
	cp *.tex *.usfm *.sty *.piclist Makefile image.jpg tiger.pdf ../bisect

map.jpg:?/test.pdf Makefile
	for  A in `seq 1 8` ; do test -f $$A/test.pdf && gs -q -dNOPAUSE -dSAFER -sDEVICE=jpeg -dFirstPage=1 -dLastPage=1 -dBATCH -r144x144 -dTextAlphaBits=4 -dDownScaleFactor=2 -sOutputFile=$$A/test.jpg $$A/test.pdf   || true ; done
	montage [0-9]/test.jpg -tile 4x3 -geometry +0+0 maps.jpg

	
auto:
	echo Source code in $(DIR)
	while inotifywait -e close_write . $(DIR) ; do make test.pdf ; done < /dev/null

1:
	rename -f 's/\./.1./' test.pdf test.parlocs test.delayed
