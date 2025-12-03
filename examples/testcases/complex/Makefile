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

bisect:
	-mkdir ../bisect || rm -f ../bisect/*
	cp *.tex *.usfm *.sty *.lua Makefile ../bisect

auto:
	echo Source code in $(DIR)
	while inotifywait -e close_write . $(DIR) ; do sleep 0.5 ;make test.pdf ; done < /dev/null
averages.txt:
	awk 'function f(a){print a, r[a]/(n[a]>0?n[a]:1);}/#/{A=$$2;print A}/Splitting/{r[A] += $$2;n[A]++}END{f("Full");f("Minimal");f("Rerun");}' < timings.dat | tee averages.txt
