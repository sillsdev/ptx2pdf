.SUFFIXES: .dvi .pdf
all: test.pdf longtest.pdf
DIR:=$(shell dirname `find ../../..  \( -name test -prune \) -or -name paratext2.tex -print`)
.tex.pdf:
	TEXINPUTS=.:$(DIR) xetex $<
	TEXINPUTS=.:$(DIR) xetex $<
	

test.pdf: test.tex usfmTex-ext.tex usfmTex-settings.tex test.usfm table.usfm $(DIR)/*.tex *.sty 
longtest.pdf: longtest.tex usfmTex-ext.tex usfmTex-settings.tex longtest.usfm $(DIR)/*.tex *.sty

subtests:
	for A in ck-* ; do make -C $$A all ; done
auto:
	echo Source code in $(DIR)
	while inotifywait -e close_write . $(DIR) ; do make all ; done < /dev/null
autotest:
	echo Source code in $(DIR)
	while inotifywait -e close_write . $(DIR) ; do make test.pdf ; done < /dev/null
autolong:
	echo Source code in $(DIR)
	while inotifywait -e close_write . $(DIR) ; do make longtest.pdf ; done < /dev/null


bisect:
	mkdir ../bisect || rm -rf ../bisect/*
	cp *.tex *.usfm *.sty Makefile ../bisect
	for A in ck-* ; do mkdir ../bisect/$$A ; cp $$A/extra.tex $$A/Makefile ../bisect/$$A ; done


