import os
import pprint

stat = os.stat('/var/lib/libvirt/images/ubuntu13desktop/ubuntu13desktop.img')
blocksAllocated = stat.st_blocks
blockSize = stat.st_blksize
size = stat.st_size

print "bytes"
