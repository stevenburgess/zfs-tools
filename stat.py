import os
import pprint
import sys

#grab the first argument passed
fileName = sys.argv[1]

stat = os.stat(fileName)
blocksAllocated = stat.st_blocks
blockSize = stat.st_blksize
#the total amount consumed is the block size * blocks allocated
totalConsumed = blockSize * blocksAllocated
size = stat.st_size

print str(blocksAllocated) + " number of blocks consumed"
print str(blockSize) + " blockSize"
print str(totalConsumed) + " real size consumed"
print str(size) + " total (reported) size"
