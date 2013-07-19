import subprocess

#there are a few options inside of /dev/disk/by-id,
#I choose ata-
prefixOfChoice = 'ata-'

diskList = subprocess.check_output(['ls', '-l', '/dev/disk/by-id/']);
for line in diskList.split('\n'):
	#exclude partition lines
	if 'part' in line:
		continue	
	if prefixOfChoice in line:
		brokenLine = line.split(' ')
		for part in brokenLine:
			if prefixOfChoice in part:
				print part

