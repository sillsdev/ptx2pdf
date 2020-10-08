
ptx2pdf.pdf : ptx2pdf.mdt layout.tex
	@- echo "Generating pdf"
	pandoc -o ptx2pdf.tex -H layout.tex --toc --latex-engine=xelatex $<
	xelatex ptx2pdf
	xelatex ptx2pdf

ptx2pdf.mdt : *.md ../../src/*.tex
	../../python/scripts/src2md -o $@ -t main $^

clean:
	rm -f ptx2pdf.mdt
