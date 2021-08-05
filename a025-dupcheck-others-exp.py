import csv
from csv import writer
from csv import reader

in_filename = r'E:\PoE Stuff\Filters\1\exp\020_dup_bases_removed.csv'
out_filename = r'E:\PoE Stuff\Filters\1\exp\020_dup_other_removed.csv'

important_cols = ["category","baseType","links"]
ignore_dict = {"category" : ["base","beast","curr","div","ench","ess","foss","frag","gem","inc","inv","map","prop","res","scar","uarm","vial","watch"]}

# Python
# I know these are all a non-factored mess right now, by design. There are so many
# variations that need to be handled diff ways that it's actually easier to not
# factorize yet. Make sure it all works, then factorize what we can.

# This script:
# Search for duplicates in certain categories.
#   Ignore rare bases (we'll sort later on ilvl) and relics (filter can recognize these).
#
# Someone helped me with this, but the conversation went in such a manner that they helped me
# find dups first, then exclude categories second. In retrospect it would be easier to only
# look for a match on specific categories but at this point I feel bad for wasting so much of the
# guy's time that I'll just deal with this as it is for now.

# For unique minval and maxval my plan is to have a slider where the user will dictate the
# behavior they want from the filter.  If there are 2 bases and one has a value of 5c and
# another has a value of 70c then we can say the following:
#
# If maxval < UserSetting: Tier = HIDE
# If minval > UserSetting: Tier = whatever the proper tier should be for that minval
# Else: Mark item T11 (grey) and show the items

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

        if "Replica" not in row["name"]:
            print (row)
            if row in result_dict:
                result_dict[row]["hasdup"] = True
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
                #if "Sledgehammer" in row["baseType"]:
                #    print ("Found a Sledgehammer that wasn't in the output file:")
                #    print ("")
                #    print (row)
                #    print ("")
                result_dict[row] = row
                result_dict[row]["hasdup"] = False

    return list(result_dict.values())

def filter_csv(in_filename, out_filename, important_cols, ignore_dict):
    with open(in_filename, newline='') as in_f, open(out_filename, "w", newline='') as out_f:
        reader = csv.DictReader(in_f)
        writer = csv.DictWriter(out_f, fieldnames=reader.fieldnames + ["hasdup"] + ["minval"] + ["maxval"])
        writer.writeheader()
        for row in filter_duplicates(reader, important_cols, ignore_dict):
            #print (row)
            writer.writerow(row)   

filter_csv(in_filename, out_filename, important_cols, ignore_dict)
print('Checking for all other duplicates')
print('Done!')
