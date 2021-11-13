import csv
import os
import sys
import time
from csv import writer
from csv import reader

# Python
# I know these are all a non-factored mess right now, by design. There are so many
# variations that need to be handled diff ways that it's actually easier to not
# factorize yet. Make sure it all works, then factorize what we can.

# This script:
# If items share a similar BaseType: condense them into 1 record, flag it, and track minval and maxval of the items.

in_filename = os.path.join(sys.path[0], "z020_fix_shit.csv")
out_filename = os.path.join(sys.path[0], "z025_dups_removed.csv")

all_cats = ["anomalous","base","beast","blight","clus","curr","deli","div","divergent","ess","foss","frag","gem","inc","inv","map","oil","phantasmal","prop","res","scar","uacc","uarm","ufla","ujew","umap","uweap","vial","watch"]

all_cols = ["category","name","baseType","variant","levelRequired","links","corrupted","mapTier","gemLevel","gemQuality","chaosEquivalent","Tier","Override","count","SetFontSize","PlayAlertSound","SetBackgroundColor","PlayEffect","MinimapIcon","hasdup","minval","maxval"]

col_dict = {
    "anomalous" : ["category","name","variant","gemLevel","gemQuality"],
    "arts" : ["category","name"],
    "base" : ["category","baseType","variant","levelRequired","links"],
    "beast" : ["category","baseType"],
    "blight" : ["category","baseType","mapTier"],
    "clus" : ["category","baseType"],
    "curr" : ["category","name"],
    "deli" : ["category","baseType"],
    "div" : ["category","name"],
    "divergent" : ["category","name","variant","gemLevel","gemQuality"],
    "ess" : ["category","name"],
    "foss" : ["category","name"],
    "frag" : ["category","name"],
    "gem" : ["category","name","variant","gemLevel","gemQuality"],
    "inc" : ["category","name"],
    "inv" : ["category","name"],
    "map" : ["category","baseType","mapTier"],
    "oil" : ["category","baseType"],
    "prop" : ["category","name"],
    "res" : ["category","name"],
    "repacc" : ["category","baseType"],
    "reparm" : ["category","baseType","links"],
    "repfla" : ["category","baseType"],
    "repjew" : ["category","baseType"],
    "repmap" : ["category","baseType","mapTier"],
    "repweap" : ["category","baseType","links"],
    "phantasmal" : ["category","name","variant","gemLevel","gemQuality"],
    "scar" : ["category","name"],
    "scourgemap" : ["category","baseType","mapTier"],
    "uacc" : ["category","baseType"],
    "uarm" : ["category","baseType","links"],
    "ubermap" : ["category","baseType","mapTier"],
    "ufla" : ["category","baseType"],
    "ujew" : ["category","baseType"],
    "umap" : ["category","baseType","mapTier"],
    "uweap" : ["category","baseType","links"],
    "vial" : ["category","name"],
    "watch" : ["category","mapTier"],
}

def filter_duplicates(reader):
    class RowHash(dict):
        def __hash__(self):
            return hash(tuple(self[col] for col in col_dict[self["category"]]))

        def __eq__(self, other):
            return tuple(self[col] for col in col_dict[self["category"]]) == tuple(other[col] for col in col_dict[self["category"]])

    result_dict = {}
    for row in map(RowHash, reader):

        if row in result_dict:
            result_dict[row]["hasdup"] = True

            #if result_dict[row]["category"] == "uacc" and result_dict[row]["baseType"] == "Studded Belt":
            #    print ("1")
            #    print ()
            #    print (row)
            #    print ()
            #    print (result_dict[row])
            #    print ()
            #    time.sleep(5)

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

        #if result_dict[row]["category"] == "uacc" and result_dict[row]["baseType"] == "Studded Belt":
        #    print ("2")
        #    print ()
        #    print (row)
        #    print ()
        #    print (result_dict[row])
        #    print ()
        #    time.sleep(10)

    return list(result_dict.values())

def filter_csv(in_filename, out_filename):
    with open(in_filename, newline='') as in_f, open(out_filename, "w", newline='') as out_f:
        reader = csv.DictReader(in_f)
        writer = csv.DictWriter(out_f, fieldnames=reader.fieldnames + ["hasdup"] + ["minval"] + ["maxval"])
        writer.writeheader()
        for row in filter_duplicates(reader):
            print (row)
            writer.writerow(row)   

print('Checking.')
filter_csv(in_filename, out_filename)
print('Done!')
