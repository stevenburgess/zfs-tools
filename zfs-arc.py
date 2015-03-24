import subprocess
import argparse

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
There are quite a few statistics that are simple percentages, not bytes, this
method makes working with them slightly easier.
"""
def percent(numerator, denom):
    percent = float(numerator) / float(denom)
    properString = '%.1f' % (100 * percent)
    return properString

"""
The argument parsing section of the script. It is done higher up so users
get feedback on bad args sooner rather than later.
"""
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--parts", action="store_true",
        help="Show stats about the different parts of the ARC")
args = parser.parse_args()

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

# Dictionaries of arc stats to display. The three values are:
################################
# Actual name of stat in arcstats
# A short name to place before the stat
# A longer explanation of the stat

# The basic values we always display.
basicValues = [
['size' , 'size' , 'Current Arc Size'],
['c_min' , 'minimum' , 'Minimum Arc Size'],
['c_max' , 'maximum' , 'Maximum Arc Size'],
['c' , 'target' , 'Target Arc Size'],
['arc_meta_used' , 'meta size' , 'Current Arc Meta Size'],
['arc_meta_limit' , 'meta maximum' , 'The Largest Arc Meta Can Be'],
]

# This dictionary contains values important to the MRU and MFU.
sizeValues = [
['mru_size', 'MRU', 'Current MRU size'],
['mfu_size', 'MFU', 'Current MFU size']
]

# Display the values we always care about
for entry in basicValues:
	valueName = entry[0]
	usefulName = entry[1]
	valueDescription = entry[2]
	sizeInBytes = contentDictionary[valueName]
	formatedSizeString = bytesToGibibytes(sizeInBytes);
	print(usefulName.ljust(13)  + formatedSizeString.rjust(9) + "\tGB\t" + valueDescription)

if args.parts:
    print("============")
    totalSize = contentDictionary['size']
    for entry in sizeValues:
            valueName = entry[0]
            usefulName = entry[1]
            valueDescription = entry[2]
            sizeInBytes = contentDictionary[valueName]
            percentOfArc = percent(sizeInBytes, totalSize)
            formatedSizeString = bytesToGibibytes(sizeInBytes);
            print(usefulName.ljust(13)  + formatedSizeString.rjust(9) + "\tGB\t" + valueDescription + ' (' + percentOfArc + '%)')
