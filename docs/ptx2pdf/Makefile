
ptx2pdf.pdf : ptx2pdf.mdt layout.tex
	@- echo "Generating pdf"
	pandoc -o $@ -H layout.tex --pdf-engine=xelatex $<

ptx2pdf.mdt : *.md ../../src/*.tex
	../../python/scripts/TeX2md -o $@ -t main $?

clean:
	rm -f ptx2pdf.mdt
