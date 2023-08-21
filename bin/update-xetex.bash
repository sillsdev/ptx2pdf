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

# save current location
repo=$PWD/xetex

# versioned files
versioned_files="icudt*.dll msvcr*.dll"   # kpathsea*.dll

# handle versioned files
pushd xetex
pushd bin/windows
git rm $versioned_files

# record existing files
popd
find -type f > $tmpdir/../old.txt
popd

# update files
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
