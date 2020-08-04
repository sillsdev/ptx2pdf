diglot.pdf: diglot.md Makefile Xrefs0.png Xrefs1.png Xrefs2.png Xrefs4.png
	pandoc -f markdown_github --wrap=auto --latex-engine=xelatex  -H listings-setup.tex  --listings -V geometry="hmargin=2cm,vmargin=2.5cm,nohead" -V papersize=A4 diglot.md -o diglot.pdf

ptx2pdf-faq.pdf: ptx2pdf-faq.md
	pandoc -f markdown_github --wrap=auto --latex-engine=xelatex  -H listings-setup.tex  --listings -V geometry="hmargin=2cm,vmargin=2.5cm,nohead" -V papersize=A4 ptx2pdf-faq.md  -o ptx2pdf-faq.pdf
