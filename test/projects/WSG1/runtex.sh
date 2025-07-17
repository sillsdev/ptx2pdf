#!/bin/sh
cd local/ptxprint/Default
hyph_size=32749 stack_size=32768 FONTCONFIG_FILE=`pwd`/../../../fonts.conf TEXINPUTS=../../../src:. xetex WSG_Default_GEN_ptxp.tex