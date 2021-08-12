import csv
import time
from csv import writer
from csv import reader

# Python
# I know these are all a non-factored mess right now, by design. There are so many
# variations that need to be handled diff ways that it's actually easier to not
# factorize yet. Make sure it all works, then factorize what we can.

# This script:
# Condense "uarm","uweap" items that share a similar BaseType into 1 record, and track minval and maxval of all of them.
# We can ignore items where row["links"] != "" because the PoE filter will be able to filter on links later.

in_filename = r'E:\PoE Stuff\Filters\1\exp\022_beast_dups_removed.csv'
out_filename = r'E:\PoE Stuff\Filters\1\exp\024_uarm_dups_removed.csv'

all_categories = ["anomalous","base","beast","blight","clus","curr","deli","div","divergent","ess","foss","frag","gem","inc","inv","map","oil","phantasmal","prop","res","scar","uacc","uarm","ufla","ujew","umap","uweap","vial","watch"]

#basetype, but ignore levelRequired and ones where links !=""
search_in = ["uarm","uweap"]  # this variable is not actually used, it's just for me to keep track of
important_cols = ["category","baseType","links"]
ignore_dict = {"category" : ["anomalous","arts","base","beast","blight","clus","curr","deli","div","divergent","ess","foss","frag","gem","inc","inv","map","oil","phantasmal","prop","res","scar","vial","watch"]}


def filter_duplicates(reader, important_cols, ignore_dict):
    class RowHash(dict):
        def __hash__(self):
            return hash(tuple(self[col] for col in important_cols))

        def __eq__(self, other):
            if any(self[col] in ignore_dict.get(col, []) for col in self):
                return False
            if self["name"].startswith("Replica") or other["name"].startswith("Replica"):
                return False
            return tuple(self[col] for col in important_cols) == tuple(other[col] for col in important_cols)

    result_dict = {}
    for row in map(RowHash, reader):

        if "Replica" not in row["name"]:
            if ((row["category"] == "uarm") or (row["category"] == "uweap")):
                #print (row)
                #time.sleep(5)
                if (row["links"] == ""):
                    if row in result_dict:
                        result_dict[row]["hasdup"] = True
                        #print ()
                        #print ("links == 0 and row IS in result_dict.  No need to write it to result_dict.")
                        #print ()
                        #time.sleep(5)

                        # Track minvalue
                        if float(row["chaosEquivalent"]) < float(result_dict[row]["chaosEquivalent"]):
                            result_dict[row]["minval"] = row["chaosEquivalent"]
                        else:
                            result_dict[row]["minval"] = result_dict[row]["chaosEquivalent"]

                        # Track maxvalue
                        if float(row["chaosEquivalent"]) > float(result_dict[row]["chaosEquivalent"]):
                            result_dict[row]["maxval"] = row["chaosEquivalent"]
                        else:
                            result_dict[row]["maxval"] = result_dict[row]["chaosEquivalent"]
                    else:
                        result_dict[row] = row
                        result_dict[row]["hasdup"] = False
                        #print ()
                        #print ("links == 0 and row is NOT in result_dict.  We've written it to result_dict.")
                        #print ()
                        #time.sleep(5)
                else:
                        result_dict[row] = row
                        result_dict[row]["hasdup"] = False
                        #print ()
                        #print ("links != 0 - we need to write it to the result_dict because there will be no duplicate.")
                        #print (row["links"])
                        #print ()
                        #print (result_dict[row])
                        #print ()
                        #time.sleep(5)
            else:
                result_dict[row] = row
                result_dict[row]["hasdup"] = False
                #print ("Row does not contain uarm or uweap.  We've written it to result_dict.")
        else:
            result_dict[row] = row
            result_dict[row]["hasdup"] = False
            #print ("Row contains Replica.  We've written it to result_dict.")

    return list(result_dict.values())

def filter_csv(in_filename, out_filename, important_cols, ignore_dict):
    with open(in_filename, newline='') as in_f, open(out_filename, "w", newline='') as out_f:
        reader = csv.DictReader(in_f)
        writer = csv.DictWriter(out_f, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in filter_duplicates(reader, important_cols, ignore_dict):
            print (row)
            writer.writerow(row)   

print('Checking uarm duplicates. Usually takes 30-60 seconds on my PC.')
filter_csv(in_filename, out_filename, important_cols, ignore_dict)
print('Done!')
