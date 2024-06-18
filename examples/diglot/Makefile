.SUFFIXES: .dvi .pdf
all: Galatians.pdf
DIR:=$(shell dirname `find ../..  -name paratext2.tex`)
SCRIPTDIR:=$(shell dirname `find ../..  -name diglot_merge.pl | grep -v bisect`)

.tex.pdf:
	TEXINPUTS=.:../../src xetex $<
	TEXINPUTS=.:../../src xetex $<

Galatians.pdf: Galatians.tex Galatians-setup.tex intro.usfm mergedGal.usfm mergedGalV.usfm ../../src/*.tex *.sty
Galatians2.pdf: Galatians2.tex Galatians-setup.tex intro.usfm mergedGal.usfm mergedGalV.usfm ../../src/*.tex *.sty
Galatians3.pdf: Galatians3.tex Galatians-setup.tex intro.usfm mergedGal.usfm mergedGalV.usfm ../../src/*.tex *.sty
history.pdf: history.tex history.usfm $(DIR)/*.tex

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

Gal_wyc.usfm 54-GALengwyc2018.usfm: engwyc2018_usfm.zip
	unzip $< 54-GALengwyc2018.usfm
	perl -CSD -pe 's/\\sls/\\+sls/og' 54-GALengwyc2018.usfm > $@

Gal_web.usfm: engwebp_usfm.zip
	unzip $< 78-GALengwebp.usfm
	perl -CSD -pe 's/\\w ([^|]+?)\|[^\\]*?\\w\*/\1/og; s/\\sls/\\+sls/og' 78-GALengwebp.usfm > $@
eg1.usfm: Gal_web.usfm
	cp $< $@
eg2.usfm: Gal_wyc.usfm
	cp $< $@
	
mergedGal.usfm: Gal_wyc.usfm Gal_web.usfm Makefile $(SCRIPTDIR)/diglot_merge.pl 
	$(SCRIPTDIR)/diglot_merge.pl -s -l -C -L merge.log -o merged.out Gal_web.usfm Gal_wyc.usfm 
	cat merged.out | grep -Ev '\\sts|\\rem' > $@
	rm merged.out

mergedGalV.usfm: Gal_wyc.usfm Gal_web.usfm Makefile $(SCRIPTDIR)/diglot_merge.pl 
	$(SCRIPTDIR)/diglot_merge.pl -s -v -C -L merge.log -o merged.out Gal_web.usfm Gal_wyc.usfm 
	cat merged.out | grep -Ev '\\sts|\\rem' > $@

egmerged.usfm:$(DIR)/ptx2pdf.sty  eg1.usfm eg2.usfm $(SCRIPTDIR)/usfmerge $(DIR)/ptx2pdf.sty $(DIR)/../python/lib/ptxprint/usfmerge.py 
	$(SCRIPTDIR)/usfmerge --debug -s $(DIR)/ptx2pdf.sty  -m scores eg1.usfm eg2.usfm -o egmerged.usfm 2> egmerge.log
eg.pdf: eg.tex egmerged.usfm 
autoeg:
	while inotifywait -e close_write  . $(DIR)/../python/lib/ptxprint ; do sleep 1 ;  make egmerged.usfm eg.pdf ; done

midVmerged.usfm:$(DIR)/ptx2pdf.sty  midV1.usfm midV2.usfm $(SCRIPTDIR)/usfmerge $(DIR)/ptx2pdf.sty $(DIR)/../python/lib/ptxprint/usfmerge.py 
	$(SCRIPTDIR)/usfmerge --debug -s $(DIR)/ptx2pdf.sty  -m scores midV1.usfm midV2.usfm -o midVmerged.usfm 2> midVmerge.log
automidV:
	while inotifywait -e close_write  . $(DIR)/../python/lib/ptxprint ; do sleep 0.5 ;  make midVmerged.usfm midV.pdf ; done
midV.pdf: midV.tex midVmerged.usfm 
noV.pdf: noV.tex noVmerged.usfm 

noVmerged.usfm:$(DIR)/ptx2pdf.sty  noV1.usfm noV2.usfm $(SCRIPTDIR)/usfmerge $(DIR)/ptx2pdf.sty $(DIR)/../python/lib/ptxprint/usfmerge.py 
	$(SCRIPTDIR)/usfmerge --debug -s $(DIR)/ptx2pdf.sty  noV1.usfm noV2.usfm -o noVmerged.usfm 2> noVmerge.log

autonoV:
	while inotifywait -e close_write  . $(DIR)/../python/lib/ptxprint ; do sleep 0.5 ;  make noVmerged.usfm ; done
autohist:	
	while inotifywait -e close_write . $(DIR) ; do sleep 1 ; make history.pdf ; done </dev/null
autogal:	
	while inotifywait -e close_write . $(DIR) ; do sleep 1 ; make Galatians.pdf ; done </dev/null
autogal2:	
	while inotifywait -e close_write . $(DIR) ; do sleep 1 ; make Galatians2.pdf ; cp Galatians2.pdf Galatians2`git branch --show-current`.pdf; done </dev/null
