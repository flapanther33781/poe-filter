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
# Run dupcheck first to compile minval/maxval. Eventually we'll use a user-input breakpoint to
# determine whether or not to hide a unique basetype, give it a colored tier, or mark it grey.
# For now, just mark them grey if minval != ""

strUserSettings = r'E:\PoE Stuff\Filters\1\exp\00_user_settings.txt'
strCSVin = r'E:\PoE Stuff\Filters\1\exp\026_fix_shit.csv'
strCSVout = r'E:\PoE Stuff\Filters\1\exp\030_assigned.csv'
strCSVbak = r'E:\PoE Stuff\Filters\1\exp\030_assigned.bak.csv'

def func_init():
    global strGrayCutoff, strUserSettings
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

    # If the output file already exists we back it up and create a new one.
    # The next script will look to see if that .bak file is present. If it is,
    # it will scan it for lines where the Override field was set, and update
    # the new file this script will have just created.
    # The next time we run these scripts the old .bak will be deleted just above.
    if os.path.isfile(strCSVout):
        os.rename(strCSVout, strCSVbak)
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
        output_row.append("itemType")
        output_row.append("variant")
        output_row.append("detailsId")
        output_row.append("levelRequired")
        output_row.append("links")
        output_row.append("corrupted")
        output_row.append("mapTier")
        output_row.append("gemLevel")
        output_row.append("gemQuality")
        output_row.append("chaosEquivalent")
        output_row.append("Tier")
        output_row.append("Override")
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

def assign_tier(str_chaosEquivalent, str_minval):
    global strGrayCutoff

#    print ("str_chaosEquivalent")
#    print (str_chaosEquivalent)
#    print (type(str_chaosEquivalent))

#    print ("str_minval")
#    print (str_minval)
#    print (type(str_minval))

    # Set default of temp = str_chaosEquivalent
    if ("." not in str_chaosEquivalent):
        temp = int(str_chaosEquivalent)
    if ("." in str_chaosEquivalent):
        temp = float(str_chaosEquivalent)
    
#    print ("temp")
#    print (temp)
#    print (type(temp))

    # No matter what the item is, if str_minval != "" we need to Tier the item based on minvalue.
    # This is because the chaosEquivalent of the line that gets put into the CSV may not be the
    # lowest valued item, but the str_minval field should be tracking the minval either way.
    if (str_minval != ""):
#        print ("str_minval is not empty")
        if (("." not in str_minval)):
            temp = int(str_minval)
        if (("." in str_minval)):
            temp = float(str_minval)

#    print ("temp")
#    print (temp)

    # Start with T10 and work our way up.
    str_strTier = 10
    if temp >= 0.1:
        str_strTier = 9
    if temp >= 0.15:
        str_strTier = 8
    if temp >= 1:
        str_strTier = 7
    if temp >= 5:
        str_strTier = 6
    if temp >= 10:
        str_strTier = 5
    if temp >= 20:
        str_strTier = 4
    if temp >= 25:
        str_strTier = 3
    if temp >= 50:
        str_strTier = 2
    if temp >= 100:
        str_strTier = 1

    # Now, only mark the item as gray if str_minval < strGrayCutoff
    # if str_minval >= strGrayCutoff we want it to retain the tier set above.
    if ((str_minval != "") and (str_minval < strGrayCutoff)):
        str_strTier = 11

#    print (str_strTier)
    return str_strTier

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
        if row[12] != "chaosEquivalent":
            print (row)
            str_category = row[0]
            str_name = row[1]
            str_baseType = row[2]
            str_itemType = row[3]
            str_variant = row[4]
            str_detailsId = row[5]
            str_levelRequired = row[6]
            str_links = row[7]
            str_corrupted = row[8]
            str_mapTier = row[9]
            str_gemLevel = row[10]
            str_gemQuality = row[11]
            str_chaosEquivalent = row[12]
            str_Tier = row[13]
            str_Override = row[14]
            str_SetFontSize = row[15]
            str_PlayAlertSound = row[16]
            str_SetBackgroundColor = row[17]
            str_PlayEffect = row[18]
            str_MinimapIcon = row[19]
            str_hasdup = row[20]
            str_minval = row[21]
            str_maxval = row[22]

            # Assign the tier
            #if str_name == "Regal Shard":
                #print("Found Regal shard")
                #time.sleep(10)
            str_Tier = assign_tier(str_chaosEquivalent, str_minval)
            #if str_name == "Regal Shard":
                #print("Found Regal shard")
                #print(str_Tier)
                #time.sleep(10)

            # Create output row
            output_row = [str_category]
            output_row.append(str_name)
            output_row.append(str_baseType)
            output_row.append(str_itemType)
            output_row.append(str_variant)
            output_row.append(str_detailsId)
            output_row.append(str_levelRequired)
            output_row.append(str_links)
            output_row.append(str_corrupted)
            output_row.append(str_mapTier)
            output_row.append(str_gemLevel)
            output_row.append(str_gemQuality)
            output_row.append(str_chaosEquivalent)
            output_row.append(str_Tier)
            output_row.append(str_Override)
            output_row.append(str_SetFontSize)
            output_row.append(str_PlayAlertSound)
            output_row.append(str_SetBackgroundColor)
            output_row.append(str_PlayEffect)
            output_row.append(str_MinimapIcon)
            output_row.append(str_hasdup)
            output_row.append(str_minval)
            output_row.append(str_maxval)
    
            # Add the updated row / list to the output file
            print(output_row)
            #if str_category == "clus" and str_baseType == "Small Cluster Jewel" and str_minval != "":
                #print("str_minval is " + str(str_minval))
                #print("strGrayCutoff is " + str(strGrayCutoff))
                #time.sleep(10)
            csv_writer.writerow(output_row)
 
print('Done!')

