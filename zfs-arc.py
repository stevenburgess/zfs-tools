import subprocess

"""
Takes in a number of bytes and returns it as a formated string. The string
is formated to be the amount of gibibytes to three decimal places of
precision.
"""
def bytesToGibibytes(sizeInBytes):
	sizeInGb = round(((float)(sizeInBytes))/(1024*1024*1024),3);
	properString = '%.3f' % sizeInGb
	return properString


"""
system memory portion
"""
output = subprocess.check_output(["free", "-g"], universal_newlines=True)
lines = output.splitlines()
memoryline = lines[1]
splitLine = memoryline.split()
totalSystemRamInGb = splitLine[1]
usedSystemRamInGb = splitLine[2]
freeSystemRamInGb = splitLine[3]

print("All values are in Gibibytes")

print("Total System Memory\t" + totalSystemRamInGb + "\tGB")
print("Used System Memory\t" + usedSystemRamInGb + "\tGB")
print("Free System Memory\t" + freeSystemRamInGb + "\tGB")
#a seperator
print("============")

"""
zfs adaptive replacment cache stats are posted via kstat
to a file in proc, read in that file
"""
arcFile = open('/proc/spl/kstat/zfs/arcstats','r')

arcFileLines = arcFile.readlines();
#fill the contentDictionary with key/value pairs
contentDictionary = {}
for line in arcFileLines:
        splitLine = str.split(line)
        contentDictionary[splitLine[0]] = splitLine[2]

#dictionary of the arc stats we care about for this program
#the key is a value we care about, the value is a description
#of what that value means
basicValues = [
['size' , 'size' , 'Current Arc Size'],
['c_min' , 'minimum' , 'Minimum Arc Size'],
['c_max' , 'maximum' , 'Maximum Arc Size'],
['c' , 'target' , 'Target Arc Size'],
['arc_meta_used' , 'meta size' , 'Current Arc Meta Size'],
['arc_meta_limit' , 'meta maximum' , 'The Largest Arc Meta Can Be'],
]

for entry in basicValues:
	valueName = entry[0]
	usefulName = entry[1]
	valueDescription = entry[2]
	sizeInBytes = contentDictionary[valueName]
	formatedSizeString = bytesToGibibytes(sizeInBytes);
	print(usefulName.ljust(13)  + formatedSizeString.rjust(9) + "\tGB\t" + valueDescription)

