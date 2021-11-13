import csv
import os.path
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
# Create text filter file. Multiple notes below in Main section.
# My filters are in "C:\Users\<user>\Documents\My Games\Path of Exile"

# This script fucks up when we try to override the tier of a map, probably due to the comma in the variant name.
# Need to figure out a workaround.  For now, just don't override maps.

str30bak = os.path.join(sys.path[0], "z030_assigned-values.bak.csv")
str30temp = os.path.join(sys.path[0], "z030_assigned-values.temp.csv")
str30new = os.path.join(sys.path[0], "z030_assigned-values.csv")

def func_init():
    if os.path.isfile(str30bak):
        do_work()
        # Once the work is done, delete the temp file
        os.remove(str30temp)
    else:
        print (".bak file not found, all we can do is copy .temp to the active role.")
        # Cannot create a file if it already exists, so we have to delete an existing one first, if it exists.
        if os.path.isfile(str30new):
            os.remove(str30new)
        os.rename(str30temp, str30new)

def compare(cat_test, dict_searchstring1, dict_searchstring2, str_Override):

    with open(str30temp, 'r') as read_obj:

        # Create a reader object from the input file object
        reader = csv.DictReader(read_obj)

        # Read each row of the input csv file as list
        for row in reader:
            #print (row)
            #print ()

            returnval = ""
            if row["category"] == cat_test:
                if "Caer" in row["name"]:
                    print ("We're in compare(), we're in the right category, and these are the things we're about to compare:")
                    print ()
                    print (row)
                    print ()
                    print (dict_searchstring1)
                    print ()
                    print (dict_searchstring2)
                    print ()
                    time.sleep(10)

                # row["category"]
                # row["name"]
                # row["baseType"]
                # row["variant"]
                # row["levelRequired"]
                # row["links"]
                # row["corrupted"]
                # row["mapTier"]
                # row["gemLevel"]
                # row["gemQuality"]
                # row["chaosEquivalent"]
                # row["Tier"]
                # row["Override"]
                # row["count"]
                # row["SetFontSize"]
                # row["PlayAlertSound"]
                # row["SetBackgroundColor"]
                # row["PlayEffect"]
                # row["MinimapIcon"]
                # row["hasdup"]
                # row["minval"]
                # row["maxval"]

                if dict_searchstring1 in row:
                    #print ("Found dict_searchstring1.")
                    #print (row)
                    #print ()
                    # replace
                    row["Override"] = str_Override
                    #print (row)
                    #print ()
                    #time.sleep(2)
                    return row

                elif dict_searchstring2 != "":
                    #print ("dict_searchstring2 is not empty.")
                    # Prepare a searchstring to compare against
                    searchstringnewrow = row["category"] + "," + row["baseType"] + "," + row["levelRequired"] + "," + row["links"] + "," + row["corrupted"] + "," + row["mapTier"] + "," + row["gemLevel"] + "," + row["gemQuality"]

                    if dict_searchstring2 in searchstringnewrow:
                        #print ("Found dict_searchstring2.")
                        #print (row)
                        #print ()
                        # replace
                        row["Override"] = str_Override
                        #print (row)
                        #print ()
                        #time.sleep(2)
                        return row

                else:
                    pass
                    #print("We ain't found shit!")
                    # DON'T return here, as we want to continue searching str30tempfile
        # If we got here, we didn't find it.  Return nothing.
        return returnval

def do_work():
    with open(str30bak, 'r') as read_obj, \
        open(str30new, 'w', newline='') as write_obj:

        # Create a reader object from the input file object
        reader = csv.DictReader(read_obj)

        # Initialize the new output file.
        print ("Initializing new file.")
        writer = csv.DictWriter(write_obj, fieldnames=reader.fieldnames)
        writer.writeheader()

        # Read each row of the input csv file as list
        for row in reader:
            print (row)
            print ()

            # Reset this before checking each row.
            returnval = ""

            if row["Override"] != "Override":
                if row["Override"] != "":
                    dict_searchstring1 = ""
                    dict_searchstring2 = ""

                    # If str_hasdup == "TRUE" we may not find an exact match. Prepare two searches.
                    if row["hasdup"] == "TRUE":
                        #print ("Found Override "+row["Override"]+". hasdup = TRUE.")
                        #print ()
                        #time.sleep(1)
                        # dict_searchstring1 = from category to gemQuality, NOT including item name

                        # will need to send category separate in order to skip name.
                        category1 = row["category"]
                        dict_searchstring1 = {"baseType": [],"variant": [],"levelRequired": [],"links": [],"corrupted": [],"mapTier": [],"gemLevel": [],"gemQuality": []}
                        dict_searchstring1["baseType"].append(row["baseType"])
                        dict_searchstring1["variant"].append(row["variant"])
                        dict_searchstring1["levelRequired"].append(row["levelRequired"])
                        dict_searchstring1["links"].append(row["links"])
                        dict_searchstring1["corrupted"].append(row["corrupted"])
                        dict_searchstring1["mapTier"].append(row["mapTier"])
                        dict_searchstring1["gemLevel"].append(row["gemLevel"])
                        dict_searchstring1["gemQuality"].append(row["gemQuality"])

                        # dict_searchstring2 = from category to gemQuality, NOT including item name OR variant
                        dict_searchstring2 = row["category"] + "," + row["baseType"] + "," + row["levelRequired"] + "," + row["links"] + "," + row["corrupted"] + "," + row["mapTier"] + "," + row["gemLevel"] + "," + row["gemQuality"]

                        # will need to send category separate in order to skip name.
                        dict_searchstring1 = {"baseType": [],"levelRequired": [],"links": [],"corrupted": [],"mapTier": [],"gemLevel": [],"gemQuality": []}
                        dict_searchstring1["baseType"].append(row["baseType"])
                        dict_searchstring1["levelRequired"].append(row["levelRequired"])
                        dict_searchstring1["links"].append(row["links"])
                        dict_searchstring1["corrupted"].append(row["corrupted"])
                        dict_searchstring1["mapTier"].append(row["mapTier"])
                        dict_searchstring1["gemLevel"].append(row["gemLevel"])
                        dict_searchstring1["gemQuality"].append(row["gemQuality"])

                        if "Caer" in row["name"]:
                            print ("name is:")
                            print ()
                            print (row["name"])
                            print ()
                            print ("Found 0, means Override = True and hasdup = True")
                            print ()
                            print (row)
                            print ()
                            print (dict_searchstring1)
                            print ()
                            time.sleep(10)

                    if row["hasdup"] == "FALSE":
                        #print ("Found Override "+row["Override"]+". hasdup = FALSE.")
                        #print ()
                        #time.sleep(1)
                        # dict_searchstring1 = from category to gemQuality, including item name
                        # will need to send category separate in order to skip name.
                        dict_searchstring1 = {"baseType": [],"variant": [],"levelRequired": [],"links": [],"corrupted": [],"mapTier": [],"gemLevel": [],"gemQuality": []}
                        dict_searchstring1["baseType"].append(row["baseType"])
                        dict_searchstring1["variant"].append(row["variant"])
                        dict_searchstring1["levelRequired"].append(row["levelRequired"])
                        dict_searchstring1["links"].append(row["links"])
                        dict_searchstring1["corrupted"].append(row["corrupted"])
                        dict_searchstring1["mapTier"].append(row["mapTier"])
                        dict_searchstring1["gemLevel"].append(row["gemLevel"])
                        dict_searchstring1["gemQuality"].append(row["gemQuality"])

                        # dict_searchstring2 = ""
                        dict_searchstring2 = ""
                        if "Caer" in row["name"]:
                            print ("name is:")
                            print ()
                            print (row["name"])
                            print ()
                            print ("Found 1, means Override = True and hasdup = False")
                            print ()
                            print (row)
                            print ()
                            print (dict_searchstring1)
                            print ()
                            time.sleep(10)

                    print("I am preparing to send:")
                    print(dict_searchstring1)
                    print()
                    print(dict_searchstring2)
                    print()
                    #time.sleep(10)
                    returnval = compare(row["category"], dict_searchstring1, dict_searchstring2, row["Override"])
                    if returnval == "":
                        #print("Override was true. returnval was empty, so it doesn't exist in str30temp. Honestly, we should never see this.")
                        #print("But if we did, this is what I'm about to save to str30new:")
                        # I don't know why I have to do this, but I do.
                        #rowtoprint = row["category"] + "," + row["name"] + "," + row["baseType"] + "," + row["variant"] + "," + row["levelRequired"] + "," + row["links"] + "," + row["corrupted"] + "," + row["mapTier"] + "," + row["gemLevel"] + "," + row["gemQuality"] + "," + row["chaosEquivalent"] + "," + row["Tier"] + "," + row["Override"] + "," + row["count"] + "," + row["SetFontSize"] + "," + row["PlayAlertSound"] + "," + row["SetBackgroundColor"] + "," + row["PlayEffect"] + "," + row["MinimapIcon"] + "," + row["hasdup"] + "," + row["minval"] + "," + row["maxval"]
                        dict_rowtoprint = {"category": [],"name": [],"baseType": [],"variant": [],"levelRequired": [],"links": [],"corrupted": [],"mapTier": [],"gemLevel": [],"gemQuality": [],"chaosEquivalent": [],"Tier": [],"Override": [],"count": [],"SetFontSize": [],"PlayAlertSound": [],"SetBackgroundColor": [],"PlayEffect": [],"MinimapIcon": [],"hasdup": [],"minval": [],"maxval": []}

                        dict_rowtoprint["category"].append(row["category"])
                        dict_rowtoprint["name"].append(row["name"])
                        dict_rowtoprint["baseType"].append(row["baseType"])
                        dict_rowtoprint["variant"].append(row["variant"])
                        dict_rowtoprint["levelRequired"].append(row["levelRequired"])
                        dict_rowtoprint["links"].append(row["links"])
                        dict_rowtoprint["corrupted"].append(row["corrupted"])
                        dict_rowtoprint["mapTier"].append(row["mapTier"])
                        dict_rowtoprint["gemLevel"].append(row["gemLevel"])
                        dict_rowtoprint["gemQuality"].append(row["gemQuality"])
                        dict_rowtoprint["chaosEquivalent"].append(row["chaosEquivalent"])
                        dict_rowtoprint["Tier"].append(row["Tier"])
                        dict_rowtoprint["Override"].append(row["Override"])
                        dict_rowtoprint["count"].append(row["count"])
                        dict_rowtoprint["SetFontSize"].append(row["SetFontSize"])
                        dict_rowtoprint["PlayAlertSound"].append(row["PlayAlertSound"])
                        dict_rowtoprint["SetBackgroundColor"].append(row["SetBackgroundColor"])
                        dict_rowtoprint["PlayEffect"].append(row["PlayEffect"])
                        dict_rowtoprint["MinimapIcon"].append(row["MinimapIcon"])
                        dict_rowtoprint["hasdup"].append(row["hasdup"])
                        dict_rowtoprint["minval"].append(row["minval"])
                        dict_rowtoprint["maxval"].append(row["maxval"])
                        #print(dict_rowtoprint)
                        #time.sleep(10)
                        #print(returnval)
                        #print()
                        #print("I am writing:")
                        #print()
                        # print row to output
                        if "Caer" in row["name"]:
                            print ("Found 2, means Override was True and comparison completed, but returnval = "".")
                            print ("This is probably because we sent bad data to compare() such that it didn't find a match.")
                            print ("I will print to the new file:")
                            print ()
                            print(dict_rowtoprint)
                            print ()
                            time.sleep(10)
                        writer.writerow(dict_rowtoprint)
                    else:
                        #print("Override was true. returnval found something in str30temp. This is expected.")
                        #print("This is what I'm about to save to str30new:")
                        #print(row)
                        #print("returnval was:")
                        #print(returnval)
                        #print()
                        #print("I am writing:")
                        #print(returnval)
                        #print()
                        #time.sleep(1)
                        # print returnval to output
                        if "Caer" in row["name"]:
                            print ("Found 3")
                            print ()
                            print ()
                            time.sleep(10)
                        writer.writerow(returnval)

                        #with open(strTXTout, 'a', newline='') as write_obj:
                        #    txt_writer = writer(write_obj)
                        #    write_obj.write("#####\n")
                else:
                    # print row to output
                    #print("Override field empty, so we never called the function.  Just write this row to str30new.")
                    #print("I am writing:")
                    # I don't know why I have to do this, but I do.
                    dict_rowtoprint = {"category": [],"name": [],"baseType": [],"variant": [],"levelRequired": [],"links": [],"corrupted": [],"mapTier": [],"gemLevel": [],"gemQuality": [],"chaosEquivalent": [],"Tier": [],"Override": [],"count": [],"SetFontSize": [],"PlayAlertSound": [],"SetBackgroundColor": [],"PlayEffect": [],"MinimapIcon": [],"hasdup": [],"minval": [],"maxval": []}

                    dict_rowtoprint["category"].append(row["category"])
                    dict_rowtoprint["name"].append(row["name"])
                    dict_rowtoprint["baseType"].append(row["baseType"])
                    dict_rowtoprint["variant"].append(row["variant"])
                    dict_rowtoprint["levelRequired"].append(row["levelRequired"])
                    dict_rowtoprint["links"].append(row["links"])
                    dict_rowtoprint["corrupted"].append(row["corrupted"])
                    dict_rowtoprint["mapTier"].append(row["mapTier"])
                    dict_rowtoprint["gemLevel"].append(row["gemLevel"])
                    dict_rowtoprint["gemQuality"].append(row["gemQuality"])
                    dict_rowtoprint["chaosEquivalent"].append(row["chaosEquivalent"])
                    dict_rowtoprint["Tier"].append(row["Tier"])
                    dict_rowtoprint["Override"].append(row["Override"])
                    dict_rowtoprint["SetFontSize"].append(row["SetFontSize"])
                    dict_rowtoprint["PlayAlertSound"].append(row["PlayAlertSound"])
                    dict_rowtoprint["SetBackgroundColor"].append(row["SetBackgroundColor"])
                    dict_rowtoprint["PlayEffect"].append(row["PlayEffect"])
                    dict_rowtoprint["MinimapIcon"].append(row["MinimapIcon"])
                    dict_rowtoprint["hasdup"].append(row["hasdup"])
                    dict_rowtoprint["minval"].append(row["minval"])
                    dict_rowtoprint["maxval"].append(row["maxval"])
                    #rowtoprint = row["category"] + "," + row["name"] + "," + row["baseType"] + "," + row["variant"] + "," + row["levelRequired"] + "," + row["links"] + "," + row["corrupted"] + "," + row["mapTier"] + "," + row["gemLevel"] + "," + row["gemQuality"] + "," + row["chaosEquivalent"] + "," + row["Tier"] + "," + row["Override"] + "," + row["count"] + "," + row["SetFontSize"] + "," + row["PlayAlertSound"] + "," + row["SetBackgroundColor"] + "," + row["PlayEffect"] + "," + row["MinimapIcon"] + "," + row["hasdup"] + "," + row["minval"] + "," + row["maxval"]
                    #rowtoprint = str_category + "," + str_name + "," + str_baseType + "," + str_variant + "," + str_levelRequired + "," + str_links + "," + str_corrupted + "," + str_mapTier + "," + str_gemLevel + "," + str_gemQuality + "," + str_chaosEquivalent + "," + str_Tier + "," + str_Override + "," + str_Count + "," + str_SetFontSize + "," + str_PlayAlertSound + "," + str_SetBackgroundColor + "," + str_PlayEffect + "," + str_MinimapIcon + "," + str_hasdup + "," + str_minval + "," + str_maxval + "\r\n"
                    print(dict_rowtoprint)
                    print()
                    #time.sleep(10)
                    if ",," in row["name"]:
                        print ("Found two commas in row[\"name\"]")
                        print ()
                    if "Caer" in row["name"]:
                        print ("Found 4.  I will be writing row (not dict_rowtoprint?)")
                        print ()
                        print (row)
                        print ()
                        print (dict_rowtoprint)
                        print ()
                        time.sleep(10)
                    writer.writerow(dict_rowtoprint)

print('Looking for Overridden items.')
func_init()
print('Finished updating Overridden items.')
