
all: *.pdf
DIR:=../../../../src
ptxprint-Default-GEN_JHNminitests.pdf: $(DIR)/*.tex *.tex 
	TEXINPUTS=$(DIR):. xetex ptxprint-Default-GEN_JHNminitests
auto:
	echo Source code in $(DIR)
	while inotifywait -e close_write . $(DIR) ; do make  ; done < /dev/null

