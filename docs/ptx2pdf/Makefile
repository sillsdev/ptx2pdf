PANDOC_VER=$(sh pandoc -v| head -1 | cut -d' ' -f2 | cut -d'.' -f1 )
ifeq ($(PANDOC_VER),1) 
  PANDOC_ARG=--latex-engine=xelatex
else
  PANDOC_ARG=--pdf-engine=xelatex
endif
ptx2pdf.pdf : ptx2pdf.mdt layout.tex
	@- echo "Generating pdf"
	pandoc -o ptx2pdf.tex -H layout.tex --toc $(PANDOC_ARG) $<
	xelatex ptx2pdf
	xelatex ptx2pdf

ptx2pdf.mdt : *.md ../../src/*.tex
	../../python/scripts/src2md -o $@ -t main $^

clean:
	rm -f ptx2pdf.mdt
