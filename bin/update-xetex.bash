#!/bin/bash

# Regular TeX Live, not w32tex
# choose Install, not Unpack only
# choose a mirror if needed
# unselect Install TeXworks front end
# click Advanced
# Portable setup: Yes
# Scheme: small scheme (basic + xetex, metapost, a few languages)
# N. of collections: 1/41 [uncheck everything except the collection XeTeX and packages]

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

# mapping (w32text - texlive/2023)
pushd xetex

# bin - bin/windows
git mv -v bin windows
mkdir bin
git mv -v windows bin

pushd share/texmf-dist
cp -a $tmpdir/texmf-dist/ls-R .

# Only in xetex/share/texmf-dist/dvipdfmx: config
git rm -r dvipdfmx
cp -a $tmpdir/texmf-dist/dvipdfmx .

pushd fonts

# Only in xetex/share/texmf-dist/fonts/tfm/public/cm: cmbcsc10.tfm
# Only in xetex/share/texmf-dist/fonts/tfm/public/cm: cmsa10.tfm
# Only in xetex/share/texmf-dist/fonts/tfm/public/cm: cmsytt10.tfm
git rm tfm/public/cm/cmbcsc10.tfm
git rm tfm/public/cm/cmsa10.tfm
git rm tfm/public/cm/cmsytt10.tfm

# Only in xetex/share/texmf-dist/fonts: conf
git rm -r conf

# Only in xetex/share/texmf-dist/fonts/map: agl
# Only in xetex/share/texmf-dist/fonts/map/dvipdfmx: base
# Only in xetex/share/texmf-dist/fonts/map/dvipdfmx: updmap
git rm -r map
mkdir map
pushd map
cp -a $tmpdir/texmf-dist/fonts/map/dvipdfmx .
cp -a $tmpdir/texmf-dist/fonts/map/glyphlist .
popd

popd

cp -a $tmpdir/texmf-dist/web2c/fmtutil-hdr.cnf web2c

# Only in xetex/share/texmf-dist/web2c: xetex
git rm -r web2c/xetex

popd

# xetex/share/texmf-dist - texmf-dist
git mv -v share/texmf-dist texmf-dist

# - texmf-var
mkdir -p texmf-var/web2c/xetex
pushd texmf-var
cp -a $tmpdir/texmf-var/web2c/xetex/xetex.fmt web2c/xetex
cp -a $tmpdir/texmf-var/ls-R .
popd

# might not be needed
# mkdir texmf-var/fonts
# cp -a $tmpdir/texmf-var/fonts/conf texmf-var/fonts

# - texmf-config
# cp -a $tmpdir/texmf-config .

git add texmf-*
rmdir share

popd
git commit -a -m "Move away from some W32TeX file locations"
exit 0

# save current location
repo=$PWD/xetex

# versioned files
versioned_files="icudt*.dll msvcr*.dll"   # kpathsea*.dll

# record existing files (and handle versioned files)
pushd xetex
pushd bin/windows
git rm $versioned_files
popd
find -type f > $tmpdir/../old.txt
popd

pushd $tmpdir
find -type f > ../new.txt
sort ../old.txt ../new.txt | uniq -d | rsync -a -v --files-from - ./ $repo
pushd bin/windows
cp -p $versioned_files $repo/bin/windows
popd

# cleanup (back in the repo directory)
popd
pushd xetex/bin/windows
git add $versioned_files
chmod 700 *.exe
popd
echo
echo "Review changes and commit"
echo
