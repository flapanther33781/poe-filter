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
# Fix some catefody names to make later work easier. Can't do this earlier because if we do then the
# gems will be treated as duplicates in previous scripts, and we don't want that.

in_filename = os.path.join(sys.path[0], "z015_compiled.csv")
out_filename = os.path.join(sys.path[0], "z020_fix_shit.csv")

print('Fixing some stuff, moving some stuff.')

with open(in_filename, newline='') as in_f, open(out_filename, "w", newline='') as out_f:
    reader = csv.DictReader(in_f)
    writer = csv.DictWriter(out_f, fieldnames=reader.fieldnames)
    writer.writeheader()
    for row in reader:
        # Put splinters into Currency
        if ((row["category"] == "frag") and ("Splinter" in row["name"])):
            row["category"] = "curr"

        # Put Artifacts into Currency
        if (row["category"] == "arts"):
            row["category"] = "curr"

        # Moving Divergent, Anomalous, & Phantasmal gems to their own categories in order to make them easier to deal with later.
        if ("Divergent" in row["name"]):
            row["category"] = "divergent"
            row["name"] = row["name"].replace("Divergent ", "")
        if ("Anomalous" in row["name"]):
            row["category"] = "anomalous"
            row["name"] = row["name"].replace("Anomalous ", "")
        if ("Phantasmal" in row["name"]):
            row["category"] = "phantasmal"
            row["name"] = row["name"].replace("Phantasmal ", "")

        # Moving Replica items to their own categories in order to make them easier to deal with later.
        if (("Replica " in row["name"]) and ("ujew" in row["category"])):
            row["category"] = "repjew"
            row["name"] = row["name"].replace("Replica ", "")
        if (("Replica " in row["name"]) and ("ufla" in row["category"])):
            row["category"] = "repfla"
            row["name"] = row["name"].replace("Replica ", "")
        if (("Replica " in row["name"]) and ("uacc" in row["category"])):
            row["category"] = "repacc"
            row["name"] = row["name"].replace("Replica ", "")
        if (("Replica " in row["name"]) and ("uarm" in row["category"])):
            row["category"] = "reparm"
            row["name"] = row["name"].replace("Replica ", "")
        if (("Replica " in row["name"]) and ("uweap" in row["category"])):
            row["category"] = "repweap"
            row["name"] = row["name"].replace("Replica ", "")
        if (("Replica " in row["name"]) and ("umap" in row["category"])):
            row["category"] = "repmap"
            row["name"] = row["name"].replace("Replica ", "")

        # Renaming Blight Maps because the PoE filter requires it.
        if (("Blighted " in row["baseType"]) and ("inc" not in row["category"])):
            row["baseType"] = row["baseType"].replace("Blighted ", "")

        print (row)
        writer.writerow(row)

print('Done!')
