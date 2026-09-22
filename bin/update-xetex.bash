#!/bin/bash

## Download
# Regular TeX Live, not w32tex
# choose Install, not Unpack only
# choose a mirror if needed
# unselect Install TeXworks front end
# click Advanced
# Portable setup: Yes
# Scheme: small scheme (basic + xetex, metapost, a few languages)
# N. of collections: 1/41 [uncheck everything except the collection "XeTeX and packages"]

## Prepare (in TeX Live folder)
# mv bin/windows bin/win32_x86_64

## Update
# ./bin/update-xetex.bash ../texlive/<year>

tmpdir=$1
if [ -z "$tmpdir" ]
then
    echo "Need to specify the portable TeX Live installed folder"
    exit 1
fi

if [ ! -e "$tmpdir" ]
then
    echo "$tmpdir does not exist"
    exit 1
fi

if [ ! -d "$tmpdir" ]
then
    echo "$tmpdir is not a directory"
    exit 1
fi

# save current location
repo=$PWD/xetex

# versioned files
versioned_files="icudt*.dll msvcr*.dll"   # kpathsea*.dll

# handle versioned files
pushd xetex
pushd bin/win32_x86_64
git rm $versioned_files

# record existing files
popd
find -type f > $tmpdir/../old.txt
popd

# update files
pushd $tmpdir
find -type f > ../new.txt
sort ../old.txt ../new.txt | uniq -d | rsync -a -v --files-from - ./ $repo
cp -p texmf-var/web2c/xetex/xetex.fmt $repo/bin/win32_x86_64/web2c/xetex/xetex.fmt
pushd bin/win32_x86_64
cp -p $versioned_files $repo/bin/win32_x86_64
popd

# cleanup (back in the repo directory)
popd
pushd xetex/bin/win32_x86_64
git add $versioned_files
chmod 700 *.exe
popd
echo
echo "The following hand-coded commits will have been over-written by the import of TeX Live."
echo
echo "The hand-coded commits need to remain, so the changed lines (from the import) need to"
echo "be reverted with a git client"
echo
echo https://github.com/sillsdev/ptx2pdf/commit/238f1dd0560410deaffa0cacbee0ee6febf30f2e
echo https://github.com/sillsdev/ptx2pdf/commit/9ef3e930d404ec0db31dcddc433b1df01f134147
echo https://github.com/sillsdev/ptx2pdf/commit/1f981832f7c5daf5ea0a1b0c6e7b2d17ecf33f0e
echo
echo "Now review changes from the import (and the reversions) and commit."
echo
