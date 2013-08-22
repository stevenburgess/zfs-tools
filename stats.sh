#!/bin/bash

if [ -z $1 ]
then
	echo "Please give a file name"
	exit 1
fi

fileName=$1

#%b     number of blocks allocated (see %B)
numberOfBlocks=$(stat -c "%b" $fileName)

#%B     the size in bytes of each block reported by %b
blockSize=$(stat -c "%B" $fileName)

#%s     total size, in bytes
#this is equal to du -b
totalSize=$(stat -c "%s" $fileName)

#the actual size would be numberOfBlocks * blockSize
realSize=$(($numberOfBlocks*$blockSize))

echo "$numberOfBlocks number of blocks consumed"
echo "$blockSize blockSize"
echo "$realSize real size consumed"
echo "$totalSize total (reported) size"
