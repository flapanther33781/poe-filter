import csv
import os.path
import time
from csv import writer
from csv import reader

# Python
# I know these are all a non-factored mess right now, by design. There are so many
# variations that need to be handled diff ways that it's actually easier to not
# factorize yet. Make sure it all works, then factorize what we can.

# This script:
# Look for 030_assigned.bak. If we find it, compare it to 030_assigned.csv,
# specifically looking for items whose Override field had been set, and update the csv.
# If 030_assigned.bak doesn't exist then it doesn't need to do anything and just exits.

in_filename = r'E:\PoE Stuff\Filters\3\z030_assigned.bak.csv'
out_filename = r'E:\PoE Stuff\Filters\3\z030_assigned.csv'
file3name = r'E:\PoE Stuff\Filters\3\z035_assigned.csv'

important_cols = ["category","name","baseType","variant","levelRequired","links","corrupted","mapTier","gemLevel","gemQuality"]
ignore_cols = ["chaosEquivalent","Tier","Override","SetFontSize","PlayAlertSound","SetBackgroundColor","PlayEffect","MinimapIcon","hasdup","minval","maxval"]

def func_init():
    if os.path.isfile(in_filename):
        filter_csv(in_filename, out_filename, important_cols, ignore_cols)
    else:
        print (".bak file not found, nothing for this script to do.")
        print ("Should terminate and move on to the next script now.")

def filter_duplicates(reader, important_cols, ignore_dict):
    class RowHash(dict):
        def __hash__(self):
            return hash(tuple(self[col] for col in important_cols))

        def __eq__(self, other):
            if any(self[col] in ignore_dict.get(col, []) for col in self):
                return False
            return tuple(self[col] for col in important_cols) == tuple(other[col] for col in important_cols)

    result_dict = {}
    for row in map(RowHash, reader):
        print (row)

        #if (row["name"] == "Regal Shard"):
            #print ("Regal Shard found.")
            #print ("Regal Shard found.")
            #print ("Regal Shard found.")
            #print ("Regal Shard found.")
            #print ("Regal Shard found.")
            #print ("Regal Shard found.")
            #print ("Regal Shard found.")
            #time.sleep(10)

        #print('Item found in result_dict.  Moving Override info.')
        if (row in result_dict):
            result_dict[row]["Override"] = row["Override"]
            #print (row)
            #if (row["name"] == "Regal Shard"):
            #    print('Item found in result_dict.  Moving Override info.')
            #    print (row)
            #    time.sleep(10)

        #print('Item not found in result_dict at all.  Adding it.')
        if (row not in result_dict):
            result_dict[row] = row
            #print (row)
            #if (row["name"] == "Regal Shard"):
            #    print('Item not found in result_dict at all.  Adding it.')
            #    print (row)
            #    time.sleep(10)

    return list(result_dict.values())

def filter_csv(in_filename, out_filename, important_cols, ignore_cols):
    with open(in_filename, newline='') as in_f, open(out_filename, "w", newline='') as out_f, open(file3name, "w", newline='') as out_3:

        reader = csv.DictReader(in_f)
        writer = csv.DictWriter(out_f, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer2 = csv.DictWriter(out_f, fieldnames=reader.fieldnames)
        writer2.writeheader()

        for row in filter_duplicates(reader, important_cols, ignore_cols):
            print (row)
            writer2.writerow(row)

func_init()
print('Looking for Overridden items.')
print('Done!')




