.SUFFIXES: .dvi .pdf
all: Galatians.pdf

.tex.pdf:
	TEXINPUTS=.:../../src xetex $<
	TEXINPUTS=.:../../src xetex $<

Galatians.pdf: Galatians.tex Galatians-setup.tex intro.usfm mergedGal.usfm mergedGalV.usfm ../../src/*.tex *.sty
history.pdf: history.tex history.usfm

history.png: history.pdf Makefile
	gs -dNOPAUSE -q -sOutputFile=history.png -dBATCH -r150 -sDEVICE=png16 history.pdf 
	mogrify -trim history.png

bisect:
	mkdir ../bisect || rm -f ../bisect/*
	cp *.tex *.usfm *.sty Makefile ../bisect

engwyc2018_usfm.zip:
	test -f $@ || wget https://ebible.org/Scriptures/engwyc2018_usfm.zip
engwebp_usfm.zip:
	test -f $@ || wget https://ebible.org/Scriptures/engwebp_usfm.zip

Gal_wyc.usfm: engwyc2018_usfm.zip
	unzip $< 78-GALengwyc2018.usfm
	sed 's/+//g;' <  78-GALengwyc2018.usfm > $@
	touch $@
Gal_web.usfm: engwebp_usfm.zip
	unzip $< 78-GALengwebp.usfm
	mv 78-GALengwebp.usfm $@
	touch $@
	
mergedGal.usfm: Gal_wyc.usfm Gal_web.usfm Makefile ./diglot_merge.pl 
	./diglot_merge.pl -s -l -C -L merge.log -o merged.out Gal_web.usfm Gal_wyc.usfm 
	cat merged.out | grep -Ev '\\sts|\\rem' > $@
	rm merged.out

mergedGalV.usfm: Gal_wyc.usfm Gal_web.usfm Makefile ./diglot_merge.pl 
	./diglot_merge.pl -s -v -C -L merge.log -o merged.out Gal_web.usfm Gal_wyc.usfm 
	cat merged.out | grep -Ev '\\sts|\\rem' > $@
