.SUFFIXES: .dvi .pdf
all: test.pdf
DIR:=$(shell dirname `find ../../..  -name paratext2.tex`)

mergedAB.usfm: SampleA.usfm SampleB.usfm
	usfmerge SampleA.usfm SampleB.usfm > $@
mergedBC.usfm: SampleC.usfm SampleB.usfm
	usfmerge SampleB.usfm SampleC.usfm > $@
mergedCB.usfm: SampleC.usfm SampleB.usfm
	usfmerge SampleC.usfm SampleB.usfm > $@

test.pdf:test.tex mergedAB.usfm mergedBC.usfm mergedCB.usfm ${DIR}/*.tex
	-rm test.delayed
	TEXINPUTS=.:$(DIR) xetex $< && cp test.pdf test.parlocs test.delayed test.log 1
	A=1 ; while grep Rerun test.log ; do TEXINPUTS=.:$(DIR) xetex $<  && mkdir $$A ; cp test.pdf test.parlocs test.delayed test.log $$A; A=$$((A+1)) ;  done ; echo last one: $$A  ; for A in `seq $$A 15` ; do rm $$A/*;done

