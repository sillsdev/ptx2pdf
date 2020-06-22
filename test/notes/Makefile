.SUFFIXES: .dvi .pdf
all: Galatians.pdf

DIR:=$(shell dirname `find ../../..  -name paratext2.tex`)
.tex.pdf:
	TEXINPUTS=.:$(DIR) xetex $<

Galatians.pdf: Galatians.tex Galatians-setup.tex $(DIR)/*.tex *.sty Gal_web.usfm

bisect:
	mkdir ../bisect || rm -f ../bisect/*
	cp *.tex *.usfm *.sty Makefile ../bisect

engwebp_usfm.zip:
	test -f $@ || wget https://ebible.org/Scriptures/engwebp_usfm.zip

Gal_web.usfm: engwebp_usfm.zip
	unzip $< 78-GALengwebp.usfm
	awk '/\\c 2/{exit;}{print}' < 78-GALengwebp.usfm > $@
	
mergedGal.usfm: Gal_wyc.usfm Gal_web.usfm Makefile ./diglot_merge.pl 
	./diglot_merge.pl -s -l -C -L merge.log -o merged.out Gal_web.usfm Gal_wyc.usfm 
	cat merged.out | grep -Ev '\\sts|\\rem' > $@
	rm merged.out

