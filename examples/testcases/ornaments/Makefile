.SUFFIXES: .dvi .pdf
all: test.pdf
DIR:=$(shell dirname `find ../../..  -name paratext2.tex`)
TPATH:=.:$(DIR)//

.tex.pdf:
	TEXINPUTS="$(TPATH)" xetex $<
	TEXINPUTS="$(TPATH)" xetex $<
	

test.pdf: test.tex  test.usfm $(DIR)/*.tex *.sty $(DIR)/*.sty
calctest.pdf: calctest.tex  calctest.usfm $(DIR)/*.tex *.sty
test2.pdf: test2.tex  test2.usfm $(DIR)/*.tex *.sty
fontish.pdf: fontish.tex fontish.usfm  $(DIR)/*.tex *.sty $(DIR)/*.sty
catalogue.pdf: catalogue.tex catalogue.usfm  $(DIR)/*.tex *.sty $(DIR)/*.sty

installcat: catalogue.pdf
	cp catalogue.pdf ../../../docs/documentation/OrnamentsCatalogue.pdf
	git add -f ../../../docs/documentation/OrnamentsCatalogue.pdf
bisect:
	mkdir ../bisect || rm -f ../bisect/*
	cp *.tex *.usfm *.sty Makefile ../bisect

auto:
	echo Source code in $(DIR)
	while inotifywait -e close_write . $(DIR) ; do make test.pdf ; done < /dev/null
auto2:
	echo Source code in $(DIR)
	while inotifywait -e close_write . $(DIR) ; do make fontish.pdf ; done < /dev/null
auto3:
	echo Source code in $(DIR)
	while inotifywait -e close_write . $(DIR) ; do make calctest.pdf ; done < /dev/null
auto4:
	echo Source code in $(DIR)
	while inotifywait -e close_write . $(DIR) ; do make catalogue.pdf ; done < /dev/null
