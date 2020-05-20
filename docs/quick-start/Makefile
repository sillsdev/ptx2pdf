diglot-quick.pdf: diglot-quick.md Makefile
	pandoc -f markdown_github --wrap=auto --latex-engine=xelatex  -H listings-setup.tex  --listings -V geometry="hmargin=2cm,vmargin=2.5cm,nohead" -V papersize=A4 diglot-quick.md -o diglot-quick.pdf
