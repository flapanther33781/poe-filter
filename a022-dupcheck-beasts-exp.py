import csv
import time
from csv import writer
from csv import reader

in_filename = r'E:\PoE Stuff\Filters\1\exp\020_replica_dups_removed.csv'
out_filename = r'E:\PoE Stuff\Filters\1\exp\022_beast_dups_removed.csv'

all_categories = ["anomalous","base","beast","blight","clus","curr","deli","div","divergent","ess","foss","frag","gem","inc","inv","map","oil","phantasmal","prop","res","scar","uacc","uarm","ufla","ujew","umap","uweap","vial","watch"]

#basetype only
search_in = ["beast","clus","uacc","ufla","ujew"]
important_cols = ["category","baseType"]
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

        #if (row["baseType"] == "Crimson Jewel"):
        #    print ("Found Crimson Jewel:")
        #    if ("Replica" in row["name"]):
        #        print ("Item is also a Replica:")
        #        print ()
        #        print (row)
        #        print ()
        #        #time.sleep(20)

        if (row["category"] != "beast" and row["category"] != "clus" and row["category"] != "uacc" and row["category"] != "ufla" and row["category"] != "ujew"):
            #print ("Row does not contain one of the categories we're searching for.  We'll write it to result_dict.")
            result_dict[row] = row
            result_dict[row]["hasdup"] = False
        else:
            #print ("Row does contain one of the categories we're searching for.  Will we find it in result_dict?")
            if row in result_dict:
                #print ("Item IS in result_dict.  No need to write it to result_dict.")
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
                #print ("Item is NOT in result_dict.  We've written it to result_dict.")
                result_dict[row] = row
                result_dict[row]["hasdup"] = False

        #if (row["baseType"] == "Crimson Jewel"):
        #    print ("Found Crimson Jewel:")
        #    if ("Replica" in row["name"]):
        #        print ("Item is also a Replica.  What happened?")
        #        print ()
        #        print (row)
        #        print ()
        #        #time.sleep(20)

    return list(result_dict.values())

def filter_csv(in_filename, out_filename, important_cols, ignore_dict):
    with open(in_filename, newline='') as in_f, open(out_filename, "w", newline='') as out_f:
        reader = csv.DictReader(in_f)
        writer = csv.DictWriter(out_f, fieldnames=reader.fieldnames + ["hasdup"] + ["minval"] + ["maxval"])
        writer.writeheader()
        for row in filter_duplicates(reader, important_cols, ignore_dict):
            print (row)
            writer.writerow(row)   

print('Checking beast duplicates. Usually takes 30-60 seconds on my PC.')
filter_csv(in_filename, out_filename, important_cols, ignore_dict)
print('Done!')
