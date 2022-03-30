.SUFFIXES: .dvi .pdf
all: test.pdf
DIR:=$(shell dirname `find ../../..  -name paratext2.tex`)
TPATH:=.:$(DIR)//

.tex.pdf:
	TEXINPUTS="$(TPATH)" xetex $<
	TEXINPUTS="$(TPATH)" xetex $<
	

test.pdf: test.tex  test.usfm $(DIR)/*.tex *.sty
calctest.pdf: calctest.tex  calctest.usfm $(DIR)/*.tex *.sty
test2.pdf: test2.tex  test2.usfm $(DIR)/*.tex *.sty

bisect:
	mkdir ../bisect || rm -f ../bisect/*
	cp *.tex *.usfm *.sty Makefile ../bisect

auto:
	echo Source code in $(DIR)
	while inotifywait -e close_write . $(DIR) ; do make test.pdf ; done < /dev/null
auto2:
	echo Source code in $(DIR)
	while inotifywait -e close_write . $(DIR) ; do make test2.pdf ; done < /dev/null
auto3:
	echo Source code in $(DIR)
	while inotifywait -e close_write . $(DIR) ; do make calctest.pdf ; done < /dev/null
