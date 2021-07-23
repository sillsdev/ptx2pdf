.SUFFIXES:.pdf .md

diglot.pdf: diglot.md Makefile Xrefs0.png Xrefs1.png Xrefs2.png Xrefs4.png
ptx2pdf-faq.pdf: ptx2pdf-faq.md
styling.pdf:styling.md Makefile

%.pdf: %.md
	pandoc -f gfm --wrap=auto --pdf-engine=xelatex  -H listings-setup.tex  --listings -V geometry="hmargin=2cm,vmargin=2.5cm,nohead" -V papersize=A4 $*.md -o $*.pdf

