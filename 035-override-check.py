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

str30bak = os.path.join(sys.path[0], "z030_assigned.bak.csv")
str30temp = os.path.join(sys.path[0], "z030_assigned.temp.csv")
str30new = os.path.join(sys.path[0], "z030_assigned.csv")

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

def compare(searchstring1, searchstring2, str_Override):

    with open(str30temp, 'r') as read_obj:

        # Create a reader object from the input file object
        reader = csv.DictReader(read_obj)

        # Read each row of the input csv file as list
        for row in reader:
            #print (row)
            #print ()

            returnval = ""
            if row["category"] != "category":
                #print (row)
                #print (searchstring1)
                #print (searchstring2)
                #print ()
                #time.sleep(1)

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
                # row["SetFontSize"]
                # row["PlayAlertSound"]
                # row["SetBackgroundColor"]
                # row["PlayEffect"]
                # row["MinimapIcon"]
                # row["hasdup"]
                # row["minval"]
                # row["maxval"]

                if searchstring1 in row:
                    #print ("Found searchstring1.")
                    #print (row)
                    #print ()
                    # replace
                    row["Override"] = str_Override
                    #print (row)
                    #print ()
                    #time.sleep(2)
                    return row

                elif searchstring2 != "":
                    #print ("searchstring2 is not empty.")
                    # Prepare a searchstring to compare against
                    searchstringnewrow = row["category"] + "," + row["baseType"] + "," + row["levelRequired"] + "," + row["links"] + "," + row["corrupted"] + "," + row["mapTier"] + "," + row["gemLevel"] + "," + row["gemQuality"]

                    if searchstring2 in searchstringnewrow:
                        #print ("Found searchstring2.")
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
    with open(str30bak, 'r') as read_obj:

        # Create a csv.reader object from the input file object
        # We need skipinitialspace=False because some of the item names have commas in them.
        csv_reader = reader(read_obj, skipinitialspace=False)

        # Read each row of the input csv file as list
        for row in csv_reader:
            print (row)
            print ()

            # If we see the header line initialize the new output file.
            if row[0] == "category":
                print ("Initializing new file.")
                # Create a csv.writer object from the output file object
                with open(str30new, 'w', newline='') as write_obj:
                    csv_writer = csv.writer(write_obj)

                    # Create the header row and apply it.
                    output_row = ["category"]
                    output_row.append("name")
                    output_row.append("baseType")
                    output_row.append("variant")
                    output_row.append("levelRequired")
                    output_row.append("links")
                    output_row.append("corrupted")
                    output_row.append("mapTier")
                    output_row.append("gemLevel")
                    output_row.append("gemQuality")
                    output_row.append("chaosEquivalent")
                    output_row.append("Tier")
                    output_row.append("str_Override")
                    output_row.append("SetFontSize")
                    output_row.append("PlayAlertSound")
                    output_row.append("SetBackgroundColor")
                    output_row.append("PlayEffect")
                    output_row.append("MinimapIcon")
                    output_row.append("hasdup")
                    output_row.append("minval")
                    output_row.append("maxval")
                    # Add the updated row / list to the output file
                    csv_writer.writerow(output_row)

            # Otherwise continue
            # Create a csv.writer object from the output file object
            with open(str30new, 'a', newline='') as write_obj:
                csv_writer = csv.writer(write_obj)
                str_category = row[0]
                str_name = row[1]
                str_baseType = row[2]
                str_variant = row[3]
                str_levelRequired = row[4]
                str_links = row[5]
                str_corrupted = row[6]
                str_mapTier = row[7]
                str_gemLevel = row[8]
                str_gemQuality = row[9]
                str_chaosEquivalent = row[10]
                str_Tier = row[11]
                str_Override = row[12]
                str_SetFontSize = row[13]
                str_PlayAlertSound = row[14]
                str_SetBackgroundColor = row[15]
                str_PlayEffect = row[16]
                str_MinimapIcon = row[17]
                str_hasdup = row[18]
                str_minval = row[19]
                str_maxval = row[20]

                if str_category != "category":
                    if str_Override != "":
                        searchstring1 = ""
                        searchstring2 = ""
                        # If str_hasdup == "TRUE" we may not find an exact match. Prepare two searches.
                        if str_hasdup == "TRUE":
                            #print ("Found str_Override "+str_Override+". str_hasdup = TRUE.")
                            #print ()
                            #time.sleep(1)
                            # searchstring1 = from category to gemQuality, NOT including item name
                            searchstring1 = str_category + "," + str_baseType + "," + str_variant + "," + str_levelRequired + "," + str_links + "," + str_corrupted + "," + str_mapTier + "," + str_gemLevel + "," + str_gemQuality
                            # searchstring2 from category to gemQuality, NOT including item name or variant
                            searchstring1 = str_category + "," + str_baseType + "," + str_levelRequired + "," + str_links + "," + str_corrupted + "," + str_mapTier + "," + str_gemLevel + "," + str_gemQuality
                        if str_hasdup == "FALSE":
                            #print ("Found str_Override "+str_Override+". str_hasdup = FALSE.")
                            #print ()
                            #time.sleep(1)
                            # searchstring1 = from category to gemQuality, including item name
                            searchstring1 = str_category + "," + str_name + "," + str_baseType + "," + str_variant + "," + str_levelRequired + "," + str_links + "," + str_corrupted + "," + str_mapTier + "," + str_gemLevel + "," + str_gemQuality
                            # searchstring2 = ""
                            searchstring2 = ""
                            #if "Fenumus" in str_name:
                            #    print ("Found 1")
                            #    print ()
                            #    print (row)
                            #    print ()
                            #    print (searchstring1)
                            #    print ()
                            #    time.sleep(10)

                        #print("I am sending:")
                        #print(searchstring1)
                        #print()
                        #print(searchstring2)
                        #print()
                        #time.sleep(1)
                        returnval = compare(searchstring1, searchstring2, str_Override)
                        if returnval == "":
                            #print("Override was true. returnval was empty, so it doesn't exist in str30temp. Honestly, we should never see this.")
                            #print("But if we did, this is what I'm about to save to str30new:")
                            # I don't know why I have to do this, but I do.
                            rowtoprint = str_category + "," + str_name + "," + str_baseType + "," + str_variant + "," + str_levelRequired + "," + str_links + "," + str_corrupted + "," + str_mapTier + "," + str_gemLevel + "," + str_gemQuality + "," + str_chaosEquivalent + "," + str_Tier + "," + str_Override + "," + str_SetFontSize + "," + str_PlayAlertSound + "," + str_SetBackgroundColor + "," + str_PlayEffect + "," + str_MinimapIcon + "," + str_hasdup + "," + str_minval + "," + str_maxval + "\r\n"
                            #print(rowtoprint)
                            #time.sleep(10)
                            #print(returnval)
                            #print()
                            #print("I am writing:")
                            #print()
                            # print row to output
                            #if "Fenumus" in str_name:
                            #    print ("Found 2")
                            #    print ()
                            #    print ()
                            #    time.sleep(10)
                            with open(str30new, 'a', newline='') as write_obj:
                                csv_writer = csv.writer(write_obj)
                                write_obj.write(rowtoprint)
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
                            #if "Fenumus" in str_name:
                            #    print ("Found 3")
                            #    print ()
                            #    print ()
                            #    time.sleep(10)
                            with open(str30new, 'a', newline='') as write_obj:
                                csv_writer = csv.writer(write_obj)
                                write_obj.writerow(returnval)

                            #with open(strTXTout, 'a', newline='') as write_obj:
                            #    txt_writer = writer(write_obj)
                            #    write_obj.write("#####\n")
                    else:
                        # print row to output
                        #print("Override field empty, so we never called the function.  Just write this row to str30new.")
                        #print("I am writing:")
                        # I don't know why I have to do this, but I do.
                        rowtoprint = str_category + "," + str_name + "," + str_baseType + "," + str_variant + "," + str_levelRequired + "," + str_links + "," + str_corrupted + "," + str_mapTier + "," + str_gemLevel + "," + str_gemQuality + "," + str_chaosEquivalent + "," + str_Tier + "," + str_Override + "," + str_SetFontSize + "," + str_PlayAlertSound + "," + str_SetBackgroundColor + "," + str_PlayEffect + "," + str_MinimapIcon + "," + str_hasdup + "," + str_minval + "," + str_maxval + "\r\n"
                        #print(rowtoprint)
                        #time.sleep(10)
                        #print()
                        with open(str30new, 'a', newline='') as write_obj:
                            csv_writer = csv.writer(write_obj)
                            csv_writer.writerow(row)
                        #if "Fenumus" in str_name:
                        #    print ("Found 4")
                        #    print ()
                        #    print ()
                        #    time.sleep(10)

func_init()
print('Looking for Overridden items.')
