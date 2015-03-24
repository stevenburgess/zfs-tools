import subprocess
import os
import re

#there are a few options inside of /dev/disk/by-id,
#I choose ata-
prefix_of_choice = 'ata-'

#a list containing all the disks connected to this machine
all_disks = dict()

devdir = os.listdir('/dev/disk/by-id/')
for disk_id in devdir:
        #exclude partition entries
        if 'part' in disk_id:
                continue
        #only include entries with our prefix in them
        if prefix_of_choice in disk_id:
                #get what it point to, should be /dev/sd*
                dev_name = os.path.realpath('/dev/disk/by-id/'+disk_id)
                #create a dictionary for the current disk
                current_disk = {'id': disk_id, 'dev': dev_name}
                all_disks[disk_id] = current_disk

#a list of all the disks being used by ZFS
zfs_disks = []

#a list that will only contain disks not used by ZFS in the end
nonzfs_disks = list(all_disks)

#pre compile a regular expression that matches a word starting with your chosen
#prefix, and ending on any whitespace character
patern = re.compile(prefix_of_choice + '\\S+')

#collect the output of a zpool status
zpoolstatus = subprocess.check_output(['zpool', 'status'],
                                      universal_newlines=True)
#for each line in the zpool status
for zpool_line in zpoolstatus.split('\n'):
        result = patern.search(zpool_line)
        #if it matches the regular expression
        if result is not None:
                #get its name from the regular expression group
                disk_id = result.group()
                #since it was in a zpool status, add it to the list of disks
                #zfs is using, and remove it from the list of disks zfs is
                #not using
                zfs_disks.append(disk_id)
                nonzfs_disks.remove(disk_id)

#this is the number of spaces to pad the ID number.  It should be a few
#characters longer than the longest disk ID.
padnumber = 45

print("Disks used by ZFS:")
for disk in zfs_disks:
        disk_id = all_disks[disk]['id']
        disk_name = all_disks[disk]['dev']
        print(disk_id.ljust(padnumber) + disk_name.rjust(6))

print('###############')
print("Disks not used by ZFS:")
for disk in nonzfs_disks:
        disk_id = all_disks[disk]['id']
        disk_name = all_disks[disk]['dev']
        print(disk_id.ljust(padnumber) + disk_name.rjust(6))
