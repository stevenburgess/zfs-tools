import subprocess
import argparse


def bytes_to_gibibytes(size_in_bytes):
    """Takes in a number of bytes and returns it as a formated string. The
    string is formated to be the amount of gibibytes to three decimal places of
    precision.
    """
    size_in_gb = round(((float)(size_in_bytes))/(1024*1024*1024), 3)
    proper_string = '%.3f' % size_in_gb
    return proper_string


def percent(numerator, denom):
    """There are quite a few statistics that are simple percentages, not bytes,
    this method makes working with them slightly easier.
    """
    percent = float(numerator) / float(denom)
    proper_string = '%.1f' % (100 * percent)
    return proper_string

"""
The argument parsing section of the script. It is done higher up so users
get feedback on bad args sooner rather than later.
"""
parser = argparse.ArgumentParser()
parser.add_argument(
    "-p",
    "--parts", action="store_true",
    help="Show stats about the different parts of the ARC")
args = parser.parse_args()

"""
system memory portion
"""
output = subprocess.check_output(["free", "-g"], universal_newlines=True)
lines = output.splitlines()
memoryline = lines[1]
splitline = memoryline.split()
total_system_ram_gb = splitline[1]
used_system_ram_gb = splitline[2]
free_system_ram_gb = splitline[3]

print("All values are in Gibibytes")

print("Total System Memory\t" + total_system_ram_gb + "\tGB")
print("Used System Memory\t" + used_system_ram_gb + "\tGB")
print("Free System Memory\t" + free_system_ram_gb + "\tGB")
#a seperator
print("============")

"""
zfs adaptive replacment cache stats are posted via kstat
to a file in proc, read in that file
"""
arc_file = open('/proc/spl/kstat/zfs/arcstats', 'r')

arc_file_lines = arc_file.readlines()
#fill the content_dictionary with key/value pairs
content_dictionary = {}
for line in arc_file_lines:
        splitline = str.split(line)
        content_dictionary[splitline[0]] = splitline[2]

# Dictionaries of arc stats to display. The three values are:
################################
# Actual name of stat in arcstats
# A short name to place before the stat
# A longer explanation of the stat

# The basic values we always display.
basic_values = [
    ['size', 'size', 'Current Arc Size'],
    ['c_min', 'minimum', 'Minimum Arc Size'],
    ['c_max', 'maximum', 'Maximum Arc Size'],
    ['c', 'target', 'Target Arc Size'],
    ['arc_meta_used', 'meta size', 'Current Arc Meta Size'],
    ['arc_meta_limit', 'meta maximum', 'The Largest Arc Meta Can Be'],
]

# This dictionary contains values important to the MRU and MFU.
size_values = [
    ['mru_size', 'MRU', 'Current MRU size'],
    ['mfu_size', 'MFU', 'Current MFU size']
]

# Display the values we always care about
for entry in basic_values:
        value_name = entry[0]
        useful_name = entry[1]
        value_description = entry[2]
        size_in_bytes = content_dictionary[value_name]
        formated_size_string = bytes_to_gibibytes(size_in_bytes)
        print(useful_name.ljust(13) + formated_size_string.rjust(9) +
              "\tGB\t" + value_description)

if args.parts:
    print("============")
    total_size = content_dictionary['size']
    for entry in size_values:
            value_name = entry[0]
            useful_name = entry[1]
            value_description = entry[2]
            size_in_bytes = content_dictionary[value_name]
            percent_of_arc = percent(size_in_bytes, total_size)
            formated_size_string = bytes_to_gibibytes(size_in_bytes)
            print(useful_name.ljust(13) + formated_size_string.rjust(9) +
                  "\tGB\t" + value_description + ' (' + percent_of_arc + '%)')
