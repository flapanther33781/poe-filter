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
# Look for an output csv from a prior run of this script, which may have Override fields filled in.
# If there is one, back it up.  Create a new file.

strUserSettings = os.path.join(sys.path[0], "00_user_settings.txt")
strCSVin = os.path.join(sys.path[0], "z025_dups_removed.csv")
strCSVout = os.path.join(sys.path[0], "z030_assigned-values.temp.csv")
strCSVbak = os.path.join(sys.path[0], "z030_assigned-values.bak.csv")
strCSVexisting = os.path.join(sys.path[0], "z030_assigned-values.csv")

def func_init():
    global strGrayCutoff, strUserSettings, strBoostButton
    # Check for existence of a previous .bak file and delete it if it's found.
    if os.path.isfile(strCSVbak):
        os.remove(strCSVbak)

    # Set strGrayCutoff default, then look for it in settings file
    strGrayCutoff = "0"
    with open(strUserSettings) as f:
        for line in f:
            if "Gray item cutoff: " in line:
                strGrayCutoff = (line.split("Gray item cutoff: ")[1])
                strGrayCutoff = strGrayCutoff.strip()
                #print ("strGrayCutoff is " + strGrayCutoff)
                #time.sleep(10)
            if "Boost Button" in line:
                strBoostButton = (line.split(": ")[1])
                strBoostButton = strBoostButton.strip()
                #print ("strBoostButton is " + strBoostButton)
                #time.sleep(10)

    # If the output file already exists we back it up and create a new one.
    # The next script will look to see if that .bak file is present. If it is,
    # it will scan it for lines where the Override field was set, and update
    # the new file this script will have just created.
    # The next time we run these scripts the old .bak will be deleted just above.
    if os.path.isfile(strCSVexisting):
        os.rename(strCSVexisting, strCSVbak)
    if os.path.isfile(strCSVout):
        os.remove(strCSVout)

    global csv_writer
    # Initialize the new document
    with open(strCSVout, 'w', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        csv_writer = writer(write_obj)
        output_row = ["category"]
        
        # Append new column headers to the first row
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
        output_row.append("Override")
        output_row.append("count")
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

def assign_tier(str_chaosEquivalent, minval, str_maxval):
    global strGrayCutoff, strBoostButton, str_name

#    if str_name == "Astragali":
#        print ("Astragali")
#        print ("str_chaosEquivalent: ", str_chaosEquivalent)
#        print (type(str_chaosEquivalent))
#        print ("minval: ", minval)
#        print (type(minval))
#        print ("str_maxval: ", str_maxval)
#        print (type(str_maxval))

    # Set default of temp_val = str_chaosEquivalent
    if ("." not in str_chaosEquivalent):
        temp_val = int(str_chaosEquivalent)
    if ("." in str_chaosEquivalent):
        temp_val = float(str_chaosEquivalent)
    
#    if str_name == "Astragali":
#        print ("temp_val: ", temp_val)
#        print (type(temp_val))

    # No matter what the item is, if minval != "" we need to Tier the item based on minvalue.
    # This is because the chaosEquivalent of the line that gets put into the CSV may not be the
    # lowest valued item, but the minval field should be tracking the minval either way.
    if (minval != ""):
#        print ("minval is not empty")
        if (("." not in minval)):
            temp_val = int(minval)
        if (("." in minval)):
            temp_val = float(minval)

#    if str_name == "Astragali":
#        print ("minval should be empty for Astragali.  temp_val should stay the same.")
#        print ("temp_val: ", temp_val)
#        print (type(temp_val))

    # Also need to do this for maxval because reasons
    if (str_maxval != ""):
#        print ("minval is not empty")
        if (("." not in str_maxval)):
            temp_maxval = int(str_maxval)
        if (("." in str_maxval)):
            temp_maxval = float(str_maxval)
    else:
        temp_maxval = ""

#    if str_name == "Astragali":
#        print ("temp_maxval should be empty for Astragali.")
#        print ("temp_maxval: ", temp_maxval)
#        print (type(temp_maxval))

    # Start with T10 and work our way up.
    temp_tier = 10
    if temp_val >= 0.1:
        temp_tier = 9
    if temp_val >= 0.15:
        temp_tier = 8
    if temp_val >= 1:
        temp_tier = 7
    if temp_val >= 5:
        temp_tier = 6
    if temp_val >= 10:
        temp_tier = 5
    if temp_val >= 20:
        temp_tier = 4
    if temp_val >= 25:
        temp_tier = 3
    if temp_val >= 50:
        temp_tier = 2
    if temp_val >= 100:
        temp_tier = 1

#    if str_name == "Astragali":
#        print ("temp_tier should be 7 for Astragali.")
#        print ("temp_tier: ", temp_tier)

    # League Start Boost Button boosts tiers 10-5 up 4 levels
    # Brown items will become yellow, red will become orange, etc.
    #if strBoostButton == "True" and temp_tier > 4 and temp_tier < 11:
        #print ("strBoostButton == ""True"" and temp_tier = ", temp_tier)
        #temp_tier = temp_tier - 4
        #print (temp_tier)
        #time.sleep(1)

    # Now, only mark the item as gray if temp_val < strGrayCutoff
    # if temp_val >= strGrayCutoff we want it to retain the tier set above.
    if (minval != ""):
        #print("found minval")
        #print("temp_val is ", temp_val)
        #print("temp_val is ", type(temp_val))
        #print("temp_maxval is ", temp_maxval)
        #print("temp_maxval is ", type(temp_maxval))
        #print("strGrayCutoff is ", strGrayCutoff)
        #print("strGrayCutoff is ", type(strGrayCutoff))
        #print(temp_val < int(strGrayCutoff))
        #print(temp_maxval > int(strGrayCutoff))
        #time.sleep(10)
        if temp_maxval > int(strGrayCutoff):
            temp_tier = 11

#    if str_name == "Astragali":
#        print ("temp_val should be empty for Astragali, so this should never be triggered.")
#        print ("temp_val: ", temp_val)
#        print ("strGrayCutoff: ", strGrayCutoff)
#        print ("temp_tier: ", temp_tier)
#        time.sleep(30)

    # Now, if str_maxval < strGrayCutoff we can hide the item completely by setting it to T12
    # which will never be shown because the function that creates the filters only goes up to T11
    # But we'll have to add a sepcial HIDE section at the bottom of that function to explicitly hide all T12.
    if (temp_maxval != "") and (temp_maxval < int(strGrayCutoff)):
        temp_tier = 12
        #print (str_maxval)
        #print (strGrayCutoff)
        #print (float(str_maxval) < float(strGrayCutoff))
        #print ()
        #time.sleep(2)
        #print((str_maxval != "") and (str_maxval < strGrayCutoff))
        #time.sleep(10)

    if temp_tier > 12:
        print ("PROBLEM !!!!!!!!!")
        time.sleep(5)

    #if (str_maxval != ""):
    #    print (temp_tier)
    #    time.sleep(10)
    return temp_tier

# Main starts here
# Main starts here
# Main starts here

func_init()

# Open the input_file in read mode and output_file in write mode
with open(strCSVin, 'r') as read_obj, \
    open(strCSVout, 'a', newline='') as write_obj:

    # Create a csv.reader object from the input file object
    csv_reader = reader(read_obj)
    # Create a csv.writer object from the output file object
    csv_writer = writer(write_obj)
    # Read each row of the input csv file as list

    for row in csv_reader:
        if row[10] != "chaosEquivalent":
            #if "Caer" in row[1]:
            #    print (row)

            print (row)
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
            str_Count = row[13]
            str_SetFontSize = row[14]
            str_PlayAlertSound = row[15]
            str_SetBackgroundColor = row[16]
            str_PlayEffect = row[17]
            str_MinimapIcon = row[18]
            str_hasdup = row[19]
            minval = row[20]
            str_maxval = row[21]

            # Assign the tier
            #if str_name == "Regal Shard":
                #print("Found Regal shard")
                #time.sleep(10)
            str_Tier = assign_tier(str_chaosEquivalent, minval, str_maxval)
            #if str_name == "Regal Shard":
                #print("Found Regal shard")
                #print(str_Tier)
                #time.sleep(10)

            # Create output row
            output_row = [str_category]
            output_row.append(str_name)
            output_row.append(str_baseType)
            output_row.append(str_variant)
            output_row.append(str_levelRequired)
            output_row.append(str_links)
            output_row.append(str_corrupted)
            output_row.append(str_mapTier)
            output_row.append(str_gemLevel)
            output_row.append(str_gemQuality)
            output_row.append(str_chaosEquivalent)
            output_row.append(str_Tier)
            output_row.append(str_Override)
            output_row.append(str_Count)
            output_row.append(str_SetFontSize)
            output_row.append(str_PlayAlertSound)
            output_row.append(str_SetBackgroundColor)
            output_row.append(str_PlayEffect)
            output_row.append(str_MinimapIcon)
            output_row.append(str_hasdup)
            output_row.append(minval)
            output_row.append(str_maxval)
    
            # Add the updated row / list to the output file
            #print(output_row)
            #if str_category == "clus" and str_baseType == "Small Cluster Jewel" and minval != "":
                #print("minval is " + str(minval))
                #print("strGrayCutoff is " + str(strGrayCutoff))
                #time.sleep(10)
            #if "Caer" in row[1]:
            #    print (row)
            #    time.sleep(10)
            csv_writer.writerow(output_row)
 
print('Done!')
