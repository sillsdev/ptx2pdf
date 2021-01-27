#!/bin/bash

# save current location
repo=$PWD/xetex

# create download location
tmpdir=$(mktemp -d -p /tmp)

# record existing files
pushd xetex
find -type f > $tmpdir/old.txt
popd

# possible servers
ring1=http://ring.shibaura-it.ac.jp/archives/text/TeX/ptex-win32/current/

# server to use
server=$ring1

# download and unpack TeX Live
packages="dvipdfm-w32 web2c-lib web2c-w32 xetex-w32"
suffix=tar.xz

pushd $tmpdir
for package in $packages
do
    tarball=$package.$suffix
    command="wget $server/$tarball"
    echo
    echo Download $tarball
    echo $command
    $command
    echo Unpack $tarball
    tar -Jxf $tarball
done

# show timestamps of downloaded files
ls -lh *.$suffix

# update TeX tree
mkdir xetex
mv -v bin share xetex

pushd xetex
find -type f > ../new.txt
sort ../old.txt ../new.txt | uniq -d | rsync -a -v --files-from - ./ $repo
popd

# cleanup
popd
rm -rf $tmpdir
echo
echo "Review changes and commit"
echo
