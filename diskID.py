import subprocess

#there are a few options inside of /dev/disk/by-id,
#I choose ata-
prefixOfChoice = 'ata-'

#a list containing all the disks connected to this machine
allDisks = []

diskList = subprocess.check_output(['ls', '-l', '/dev/disk/by-id/'])
for line in diskList.split('\n'):
	#exclude partition lines
	if 'part' in line:
		continue	
	if prefixOfChoice in line:
		brokenLine = line.split(' ')
		for part in brokenLine:
			if prefixOfChoice in part:
				allDisks.append(part)

#a list of all the disks being used by ZFS
zfsDisks = []

#a list that will only contain disks not used by ZFS in the end
nonZfsDisks = list(allDisks)

zpoolStatus = subprocess.check_output(['zpool', 'status'])
for zpoolLine in zpoolStatus.split('\n'):
	if prefixOfChoice in zpoolLine:
		diskID = zpoolLine.split(' ')[4]
		zfsDisks.append(diskID)
		nonZfsDisks.remove(diskID)

print "Disks used by ZFS:"
for disk in zfsDisks:
	print disk

print '###############'
print "Disks not used by ZFS:"
for disk in nonZfsDisks:
	print disk
