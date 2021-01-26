#!/bin/bash

ring1=http://ring.shibaura-it.ac.jp/archives/text/TeX/ptex-win32/current/
server=$ring1

packages="dvipdfm-w32 latex mftools pdftex-w32 platex ptex-w32 web2c-lib web2c-w32 xetex-w32"
suffix=tar.xz
for package in $packages
do
    echo Download $package.$suffix
    echo wget $ring1/$package.$suffix
    wget $ring1/$package.$suffix
done
