.SUFFIXES: .dvi .pdf
all: test.pdf
#DIR:=$(shell dirname `find ../../..  -name paratext2.tex`)
DIR=../../../src
FONTCONFIG_FILE=~/.config/ptxprint/fonts.conf
TPATH:=.:$(DIR)//

.tex.pdf:
	TEXINPUTS="$(TPATH)" FONTCONFIG_FILE=${FONTCONFIG_FILE} xetex --no-pdf $<
	TEXINPUTS="$(TPATH)" FONTCONFIG_FILE=${FONTCONFIG_FILE} xetex --no-pdf $<
	xdvipdfmx -o $@ $*.xdv
	

test.pdf: test.tex  test.usfm $(DIR)/*.tex *.sty $(DIR)/*.sty
calctest.pdf: calctest.tex  calctest.usfm $(DIR)/*.tex *.sty
test2.pdf: test2.tex  test2.usfm $(DIR)/*.tex *.sty
fontish.pdf: fontish.tex fontish.usfm  $(DIR)/*.tex *.sty $(DIR)/*.sty
ornimg.pdf: ornimg.tex  test.usfm $(DIR)/*.tex *.sty $(DIR)/*.sty

catalogue.pdf: catalogue.tex catalogue.usfm  $(DIR)/*.tex *.sty $(DIR)/*.sty
	extra_mem_bot=50000000 TEXINPUTS="$(TPATH)" xetex $<
	extra_mem_bot=50000000 TEXINPUTS="$(TPATH)" xetex $<

installcat: catalogue.pdf
	cp catalogue.pdf ../../../docs/documentation/OrnamentsCatalogue.pdf
	git add -f ../../../docs/documentation/OrnamentsCatalogue.pdf
bisect:
	mkdir ../bisect || rm -f ../bisect/*
	cp *.tex *.usfm *.sty Makefile inner_include.pdf rose.jpg Background.jpg ../bisect

auto:
	echo Source code in $(DIR)
	while inotifywait -e close_write . $(DIR) ; do sleep 0.5 ;make test.pdf ; done < /dev/null
auto2:
	echo Source code in $(DIR)
	while inotifywait -e close_write . $(DIR) ; do sleep 0.5 ;make fontish.pdf ; done < /dev/null
auto3:
	echo Source code in $(DIR)
	while inotifywait -e close_write . $(DIR) ; do sleep 0.5 ;make calctest.pdf ; done < /dev/null
auto4:
	echo Source code in $(DIR)
	while inotifywait -e close_write . $(DIR) ; do sleep 0.5 ;make catalogue.pdf ; done < /dev/null
