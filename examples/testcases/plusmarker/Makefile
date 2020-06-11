.SUFFIXES: .dvi .pdf
all: Galatians.pdf
DIR:=$(shell dirname `find ../../..  -name paratext2.tex`)
SCRIPTDIR:=$(shell dirname `find ../../..  -name diglot_merge.pl | grep -v bisect`)

.tex.pdf:
	TEXINPUTS=.:$(DIR) xetex $<
	TEXINPUTS=.:$(DIR) xetex $<


../../diglot/78-GALengwyc2018.usfm: 
	make -C ../../diglot 78-GALengwyc2018.usfm
Gal_web.usfm: ../../diglot/78-GALengwyc2018.usfm
	ln -s ../../diglot/78-GALengwyc2018.usfm  $@

mini_web.usfm: Gal_web.usfm Makefile
	 awk 'BEGIN{e=0;}(e==3){exit;}/mt/{print ; print "\\mt1 \\+it or\\+it*: the true Gospel of the \\+nd Lord\\+nd* ";next;}{print;}/\\\+/{e++;}' < $< > $@	
Galatians.pdf: Galatians.tex Galatians-setup.tex mini_web.usfm $(DIR)/*.tex *.sty

auto:
	while inotifywait -e close_write . $(DIR) ; do make Galatians.pdf ; evince Galatians.pdf ; done < /dev/null
