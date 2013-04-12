import subprocess


output = subprocess.check_output(["free", "-g"])

lines = str.splitlines(output)

memoryline = lines[1]

splitLine = str.split(memoryline)

totalSystemRamInGb = splitLine[1]

usedSystemRamInGb = splitLine[2]

freeSystemRamInGb = splitLine[3]

print "Total System Memory\t" + totalSystemRamInGb + "\tGB"
print "Used System Memory\t" + usedSystemRamInGb + "\tGB"
print "Free System Memory\t" + freeSystemRamInGb + "\tGB"

print "============"

arcFile = open('/proc/spl/kstat/zfs/arcstats','r')

allLines = arcFile.readlines();

importantValues = {
'size' : 'Current Arc Size',
'c_min' : 'Minimum Arc Size',
'c_max' : 'Maximum Arc Size',
'c' : 'Target Arc Size',
'arc_meta_used' : 'Current Arc Meta Size',
'arc_meta_limit' : 'The Largest Arc Meta Can Be',
'arc_meta_max' : 'The Largest Arc Meta Has Been(?)',
'l2_size' : 'Size of L2 cache'
}
contentDictionary = {}
for line in allLines:
        splitLine = str.split(line)
        contentDictionary[splitLine[0]] = splitLine[2]

for value, description in importantValues.iteritems():
        sizeInBytes = contentDictionary[value]
        sizeInGb = (int(sizeInBytes)/(1024*1024*1024));
        print value + "\t\t" + str(sizeInGb) + "\tGB\t" + description

