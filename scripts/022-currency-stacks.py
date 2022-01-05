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

existing_in_filename = os.path.join(sys.path[0], "z030_assigned-values.csv")
new_in_filename = os.path.join(sys.path[0], "z020_fix_shit.csv")
out_filename = os.path.join(sys.path[0], "00_currency_stacks.csv")

print()
print('Generating 00_currency_stacks.csv')
print()

def write_stack(str_BaseType, str_Variant, str_Tier):
    row = "curr,," + str_BaseType + "," + str_Variant + "," + "," + "," + "," + "," + "," + "," + "," + str_Tier + "," + ",99" + "\r\n"
    #print (row)

    with open(out_filename, "a", newline='') as out_f:
        if row != "":
            out_f.write(row)

def determine_variant(str_BaseType,str_Tier):

    if str_BaseType == "Rogue's Marker":
        str_Variant = "100"; str_Tier = "7"; write_stack(str_BaseType, str_Variant, str_Tier)
        str_Variant = "200"; str_Tier = "6"; write_stack(str_BaseType, str_Variant, str_Tier)
        str_Variant = "300"; str_Tier = "5"; write_stack(str_BaseType, str_Variant, str_Tier)
        return

    #T10
    if str_Tier == "10":
        str_Variant = "10"; str_Tier = "9"; write_stack(str_BaseType, str_Variant, str_Tier)
        str_Variant = "20"; str_Tier = "8"; write_stack(str_BaseType, str_Variant, str_Tier)
        str_Variant = "30"; str_Tier = "7"; write_stack(str_BaseType, str_Variant, str_Tier)
        return

    #T9
    if str_Tier == "9":
        str_Variant = "10"; str_Tier = "7"; write_stack(str_BaseType, str_Variant, str_Tier)
        str_Variant = "50"; str_Tier = "6"; write_stack(str_BaseType, str_Variant, str_Tier)
        return

    #T8
    if str_Tier == "8":
        str_Variant = "10"; str_Tier = "7"; write_stack(str_BaseType, str_Variant, str_Tier)
        str_Variant = "40"; str_Tier = "6"; write_stack(str_BaseType, str_Variant, str_Tier)
        return

    #T7
    if str_Tier == "7":
        str_Variant = "5"; str_Tier = "6"; write_stack(str_BaseType, str_Variant, str_Tier)
        str_Variant = "10"; str_Tier = "5"; write_stack(str_BaseType, str_Variant, str_Tier)
        str_Variant = "20"; str_Tier = "4"; write_stack(str_BaseType, str_Variant, str_Tier)
        return

    #T6
    if str_Tier == "6":
        str_Variant = "2"; str_Tier = "5"; write_stack(str_BaseType, str_Variant, str_Tier)
        str_Variant = "4"; str_Tier = "4"; write_stack(str_BaseType, str_Variant, str_Tier)
        str_Variant = "5"; str_Tier = "3"; write_stack(str_BaseType, str_Variant, str_Tier)
        str_Variant = "10"; str_Tier = "2"; write_stack(str_BaseType, str_Variant, str_Tier)
        str_Variant = "20"; str_Tier = "1"; write_stack(str_BaseType, str_Variant, str_Tier)
        return

    #T5
    if str_Tier == "5":
        str_Variant = "2"; str_Tier = "4"; write_stack(str_BaseType, str_Variant, str_Tier)
        str_Variant = "3"; str_Tier = "3"; write_stack(str_BaseType, str_Variant, str_Tier)
        str_Variant = "5"; str_Tier = "2"; write_stack(str_BaseType, str_Variant, str_Tier)
        str_Variant = "10"; str_Tier = "1"; write_stack(str_BaseType, str_Variant, str_Tier)
        return

    #T4
    if str_Tier == "4":
        str_Variant = "2"; str_Tier = "3"; write_stack(str_BaseType, str_Variant, str_Tier)
        str_Variant = "3"; str_Tier = "2"; write_stack(str_BaseType, str_Variant, str_Tier)
        str_Variant = "5"; str_Tier = "1"; write_stack(str_BaseType, str_Variant, str_Tier)
        return

    #T3
    if str_Tier == "3":
        str_Variant = "2"; str_Tier = "2"; write_stack(str_BaseType, str_Variant, str_Tier)
        str_Variant = "4"; str_Tier = "1"; write_stack(str_BaseType, str_Variant, str_Tier)
        return

    #T2
    if str_Tier == "2":
        str_Variant = "2"; str_Tier = "1"; write_stack(str_BaseType, str_Variant, str_Tier)
        return


def convert_chaos(str_Tier):
    if "." in str_Tier:
        str_Tier = float(str_Tier)
    else:
        str_Tier = int(str_Tier)

    if str_Tier >= 100:
        str_Tier = "1"; return str_Tier
    if str_Tier >= 50:
        str_Tier = "2"; return str_Tier
    if str_Tier >= 25:
        str_Tier = "3"; return str_Tier
    if str_Tier >= 20:
        str_Tier = "4"; return str_Tier
    if str_Tier >= 10:
        str_Tier = "5"; return str_Tier
    if str_Tier >= 5:
        str_Tier = "6"; return str_Tier
    if str_Tier >= 1:
        str_Tier = "7"; return str_Tier
    if str_Tier >= .14:
        str_Tier = "8"; return str_Tier
    if str_Tier >= .1:
        str_Tier = "9"; return str_Tier

    # If we're still here, then ...
    str_Tier = "10"; return str_Tier



def existing_in():
    print ("working with ", existing_in_filename)

    with open(existing_in_filename, newline='') as in_f:
        reader = csv.DictReader(in_f)
        for row in reader:
            str_Tier = ""; str_BaseType = ""
            str_BaseType = row["name"]
            if row["category"] == "curr" and row["Override"] != "":
                #str_Tier = row["Override"]
                str_Tier = row["Tier"]
                #print (str_Tier)
                determine_variant(str_BaseType,str_Tier)
            elif row["category"] == "curr" and row["Override"] == "":
                str_Tier = row["Tier"]
                #print (str_Tier)
                determine_variant(str_BaseType,str_Tier)

def new_in():
    print ("working with ", new_in_filename)

    with open(new_in_filename, newline='') as in_f:
        reader = csv.DictReader(in_f)
        for row in reader:
            #If we're here there won't be anything in the Overide or Tier fields.  We'll have to go by chaosEquivalent.
            str_Tier = ""
            if row["category"] == "curr":
                str_BaseType = row["name"]
                str_Tier = row["chaosEquivalent"]
                #print (row)
                str_Tier = convert_chaos(str_Tier)
                #print (str_Tier)
                determine_variant(str_BaseType,str_Tier)

# Main starts here
# Main starts here
# Main starts here

with open(out_filename, "w", newline='') as out_f:
    out_f.close

# Use existing_in_filename if it exists, otherwise use new_in_filename
if os.path.isfile(existing_in_filename):
    existing_in()
else:
    new_in()

print('Done!')
