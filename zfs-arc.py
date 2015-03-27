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
parser.add_argument(
    "-e",
    "--efficiency", action="store_true",
    help="Display efficiency statistics from the SLAB stores")
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


if args.efficiency:
    """Efficiency statistics for the SPLs internal slab implementation. Note
    that in ZoL 0.6.3 and onward objects smaller than the
    spl_kmem_cache_slab_limit parameter use the Linux kernel SLAB
    allocator and will not show up in these numbers.
    """
    print("============")
    slab_file = open('/proc/spl/kmem/slab')

    # The first two lines descibe the rest of the file, skip them and get to
    # the information this loop needs.
    slab_file.readline()
    slab_file.readline()

    size = 0
    alloc = 0

    for line in slab_file:
        splitline = str.split(line)
        # Column 2 is described as:
        # The total amount of memory allocated for this slab
        size += int(splitline[2])
        # Column 3 is described as:
        # The total amount of memory *in use* by users of this cache
        alloc += int(splitline[3])

    print("size:".ljust(13) + bytes_to_gibibytes(size).rjust(9) + "\tGB\t" +
          "Current size of all slabs allocated by SPLs slab allocator")
    print("alloc:".ljust(13) + bytes_to_gibibytes(alloc).rjust(9) + "\tGB\t" +
          "Current space used in the above slabs")
    percent_efficency = percent(alloc, size)
    print("efficiency:".ljust(13) + percent_efficency.rjust(9) + "\t%\t" +
          "The efficiency of the SPL slab allocator")
