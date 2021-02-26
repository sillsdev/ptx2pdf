texts = TopNBottom.pdf Markers.pdf 

$(texts): %.pdf : %.md
	pandoc -f gfm --wrap=auto --pdf-engine=xelatex  -H ../listings-setup.tex  --listings -V geometry="hmargin=2cm,vmargin=2.5cm,nohead" -V papersize=A4 -V 'mainfont:GenBasR.ttf' -V 'mainfontoptions:BoldFont=GenBasB.ttf, ItalicFont=GenBasI.ttf, BoldItalicFont=GenBasBI.ttf' $< -o $@

%.svg:%.dia
	dia -t dia-svg $*.dia
