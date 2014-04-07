import subprocess
import os
import re

#there are a few options inside of /dev/disk/by-id,
#I choose ata-
prefixOfChoice = 'ata-'

#a list containing all the disks connected to this machine
allDisks = dict()

devDir = os.listdir('/dev/disk/by-id/')
for diskID in devDir:
	#exclude partition entries
	if 'part' in diskID:
		continue
	#only include entries with our prefix in them
	if prefixOfChoice in diskID:
		#get what it point to, should be /dev/sd*
		devName = os.path.realpath('/dev/disk/by-id/'+diskID)
		#create a dictionary for the current disk
		currentDisk = {'id':diskID , 'dev':devName}
		allDisks[diskID] = currentDisk

#a list of all the disks being used by ZFS
zfsDisks = []

#a list that will only contain disks not used by ZFS in the end
nonZfsDisks = list(allDisks)

#pre compile a regular expression that matches a word starting with your chosen
#prefix, and ending on any whitespace character
patern = re.compile(prefixOfChoice + '\\S+')

#collect the output of a zpool status
zpoolStatus = subprocess.check_output(['zpool', 'status'], universal_newlines=True)
#for each line in the zpool status
for zpoolLine in zpoolStatus.split('\n'):
	result = patern.search(zpoolLine)
	#if it matches the regular expression
	if result != None:
		#get its name from the regular expression group
		diskID = result.group()
		#since it was in a zpool status, add it to the list of disks
		#zfs is using, and remove it from the list of disks zfs is
		#not using
		zfsDisks.append(diskID)
		nonZfsDisks.remove(diskID)

#this is the number of spaces to pad the ID number.  It should be a few
#characters longer than the longest disk ID.
padNumber = 45

print("Disks used by ZFS:")
for disk in zfsDisks:
	diskID = allDisks[disk]['id']
	diskName = allDisks[disk]['dev']
	print(diskID.ljust(padNumber) + diskName.rjust(6))

print('###############')
print("Disks not used by ZFS:")
for disk in nonZfsDisks:
	diskID = allDisks[disk]['id']
	diskName = allDisks[disk]['dev']
	print(diskID.ljust(padNumber) + diskName.rjust(6))
