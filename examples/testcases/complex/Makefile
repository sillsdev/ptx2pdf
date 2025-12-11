.SUFFIXES: .dvi .pdf
all: test.pdf
DIR:=$(shell find ../../..  -name tmp -prune -or -name paratext2.tex -printf "%h")
TPATH=.:${DIR}//
.tex.pdf:
	TEXINPUTS="$(TPATH)"  xetex --no-pdf $<
	TEXINPUTS="$(TPATH)"  xetex --no-pdf $<
	xdvipdfmx -o $@ $*.xdv
	

pretest.pdf: pretest.tex  $(DIR)/*.tex *.sty $(DIR)/*.sty
test.pdf: test.tex  test.usfm $(DIR)/*.tex *.sty $(DIR)/*.sty
subtest.log: subtest.tex $(DIR)/*.tex  Makefile

bisect:
	-mkdir ../bisect || rm -f ../bisect/*
	cp *.tex *.usfm *.sty *.lua Makefile ../bisect

auto:
	echo Source code in $(DIR)
	while inotifywait -e close_write . $(DIR) ; do sleep 0.5 ;make pretest.pdf ; done < /dev/null

averages.txt: Makefile timings.dat
	awk 'function f(a){n=num[a]>0?num[a]:1; print a, 1000*r[a]/n "ms";}/#/{A=$$2;print A;N[names++]=$$2;}/Splitting/{r[A] += $$2;num[A]+=1;}END{while (names>0) {names-- ; f(N[names]);} ;}' < timings.dat | tee averages.txt

autosubtest:
	echo Source code in $(DIR)
	while inotifywait -e close_write . $(DIR) ; do sleep 0.5 ; make subtest.log ; done < /dev/null
