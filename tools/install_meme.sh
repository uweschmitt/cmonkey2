#!/bin/sh

#sudo apt-get install build-essential csh

memeVersion="4.10.0"
memePatch="_2"
url="http://ebi.edu.au/ftp/software/MEME/${memeVersion}/meme_${memeVersion}${memePatch}.tar.gz"
mkdir progs
cd progs
wget "$url"
tar -xvzf "meme_${memeVersion}${memePatch}.tar.gz"
cd "meme_${memeVersion}"
mkdir local
./configure --prefix=`pwd`/local/ --enable-dependency-tracking --enable-opt --disable-shared --disable-fast-install \
    --enable-serial --enable-build-libxml2 --enable-build-libxslt --disable-shared --enable-static --with-gnu-ld
make -j 4
make install
cd ..
ln -s "meme_${memeVersion}/local/bin/meme"
ln -s "meme_${memeVersion}/local/bin/mast"
ln -s "meme_${memeVersion}/local/bin/dust"
ln -s "meme_${memeVersion}/local/bin/tomtom"
ln -s "meme_${memeVersion}/local/bin/fimo"
cd ..
ln -s progs/meme
ln -s progs/mast
ln -s progs/dust
ln -s progs/tomtom
