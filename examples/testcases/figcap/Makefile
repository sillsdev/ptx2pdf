.SUFFIXES: .dvi .pdf
all: test.pdf
DIR:=$(shell dirname `find ../../.. \( -name test -prune \) -o  -name paratext2.tex -print`)
test.pdf:test.tex $(DIR)/*.tex
	-rm test.delayed
	TEXINPUTS=.:$(DIR)/:$(DIR)/contrib/ornaments: FONTCONFIG_FILE=~/.config/ptxprint/fonts.conf xetex $< && cp test.pdf test.parlocs test.delayed test.log 1
	A=1 ; while grep Rerun test.log ; do FONTCONFIG_FILE=~/.config/ptxprint/fonts.conf TEXINPUTS=.:$(DIR)// xetex $<  && mkdir $$A ; cp test.pdf test.parlocs test.delayed test.log $$A; A=$$((A+1)); if [ $$A -gt 20 ] ; then break ; fi ;  done ; echo last one: $$A  ; for A in `seq $$A 15` ; do rm $$A/*;done
	

test.pdf: test.tex test.usfm $(DIR)/*.tex *.sty 

bisect:
	-mkdir ../bisect || rm -f ../bisect/* 
	cp *.tex *.usfm *.sty *.piclist Makefile image.jpg tiger.pdf ../bisect

map.jpg:?/test.pdf Makefile
	for  A in `seq 1 8` ; do test -f $$A/test.pdf && gs -q -dNOPAUSE -dSAFER -sDEVICE=jpeg -dFirstPage=1 -dLastPage=1 -dBATCH -r144x144 -dTextAlphaBits=4 -dDownScaleFactor=2 -sOutputFile=$$A/test.jpg $$A/test.pdf   || true ; done
	montage [0-9]/test.jpg -tile 4x3 -geometry +0+0 maps.jpg

auto:
	echo Source code in $(DIR)
	while inotifywait -e close_write . $(DIR) ; do sleep 0.5 ; make test.pdf ; done < /dev/null

1:
	rename -f 's/\./.1./' test.pdf test.parlocs test.delayed
