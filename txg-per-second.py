import time
import argparse
import os
import sys
"""
There is a file in /proc/spl/kstat/zfs/txgs-POOLNAME that gets 
fully rewritten on each txg update.
"""

parser = argparse.ArgumentParser()
parser.add_argument('pool_name', metavar='poolName', type=str)
args = parser.parse_args()

txg_file = '/proc/spl/kstat/zfs/txgs-' + args.pool_name
# Check that the TXG file exists, if it does not, let
if not os.path.isfile(txg_file):
    print("Could not find the expected txg file, " + txg_file +
            " is your version of ZFS up to date? did you specify the pool " + 
            "correctly?")
    sys.exit(1)

def get_most_recent_txg():
    """Gets the most recent transaction group number. Since the txg file is
    only 62 lines long, reading through the whole thing seems
    acceptable."""
    txg_file_handle = open(txg_file, 'r')
    for line in txg_file_handle:
        last_line = line
    split_line = last_line.split(' ')
    current_txg = split_line[0]
    return int(current_txg)

start_time = time.time()
start_txg = get_most_recent_txg()
try:
    # Warm up the system for a few seconds, to let some txgs pass
    print("Warming up the txg counter for 10 seconds....")
    time.sleep(10)
    while True:
        txg = get_most_recent_txg()
        current_time = time.time()
        current_txg = get_most_recent_txg()

        elapsed_time = current_time - start_time
        elapsed_txgs = current_txg - start_txg

        txgs_per_second = elapsed_txgs / elapsed_time
        print(str(txgs_per_second))
        time.sleep(1)
except KeyboardInterrupt:
    # My expectation is that this will be cathing the "KeyboardInterrupt" when
    # the user kills this process via ctrl-c.
    end_time = time.time()
    end_txg = get_most_recent_txg()

    elapsed_time = end_time - start_time
    elapsed_txgs = end_txg - start_txg

    txgs_per_second = elapsed_txgs / elapsed_time
    # Print out the newline because python does not put a newline after the
    # ctrl-c character
    print("\n" + str(txgs_per_second) + " txgs/second")

