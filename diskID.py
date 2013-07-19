import subprocess

diskList = subprocess.check_output(['ls', '-l', '/dev/disk/by-id/']);
#print diskList.split('\n')
for line in diskList.split('\n'):
	if 'part' in line:
		continue	
	if 'scsi-' in line:
		brokenLine = line.split(' ')
		for part in brokenLine:
			if 'scsi-' in part:
				print part

