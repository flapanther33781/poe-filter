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
# Use the Tier (or Override) field to assign the correct values for play sounds, background colors, etc.

strCSVin = r'E:\PoE Stuff\Filters\1\exp\030_assigned.csv'
strCSVout = r'E:\PoE Stuff\Filters\1\exp\038_assigned.csv'

def func_init():

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

def assign_color(blahblah):
    print("Recieved "+str(blahblah))
    if blahblah == 1:
        str_SetFontSize = "45"
        str_PlayAlertSound = "2-300"
        str_SetBackgroundColor = "White"
        str_PlayEffect = "White"
    if blahblah == 2:
        str_SetFontSize = "45"
        str_PlayAlertSound = "16-300"
        str_SetBackgroundColor = "Pink"
        str_PlayEffect = "Pink"
    if blahblah == 3:
        str_SetFontSize = "45"
        str_PlayAlertSound = "6-300"
        str_SetBackgroundColor = "Cyan"
        str_PlayEffect = "Cyan"
    if blahblah == 4:
        str_SetFontSize = "45"
        str_PlayAlertSound = "7-300"
        str_SetBackgroundColor = "Purple"
        str_PlayEffect = "Purple"
    if blahblah == 5:
        str_SetFontSize = "42"
        str_PlayAlertSound = "8-300"
        str_SetBackgroundColor = "Blue"
        str_PlayEffect = "Blue"
    if blahblah == 6:
        str_SetFontSize = "42"
        str_PlayAlertSound = "9-300"
        str_SetBackgroundColor = "Green"
        str_PlayEffect = "None"
    if blahblah == 7:
        str_SetFontSize = "42"
        str_PlayAlertSound = "'9-1"
        str_SetBackgroundColor = "Yellow"
        str_PlayEffect = "None"
    if blahblah == 8:
        str_SetFontSize = "42"
        str_PlayAlertSound = "'9-1"
        str_SetBackgroundColor = "Orange"
        str_PlayEffect = "None"
    if blahblah == 9:
        str_SetFontSize = "39"
        str_PlayAlertSound = "'9-1"
        str_SetBackgroundColor = "Red"
        str_PlayEffect = "None"
    if blahblah == 10:
        str_SetFontSize = "39"
        str_PlayAlertSound = "'9-1"
        str_SetBackgroundColor = "Brown"
        str_PlayEffect = "None"
    if blahblah == 11:
        str_SetFontSize = "39"
        str_PlayAlertSound = ""
        str_SetBackgroundColor = "Grey"
        str_PlayEffect = "None"
    return str_SetFontSize, str_PlayAlertSound, str_SetBackgroundColor, str_PlayEffect

def assign_icon(str_itemType, str_strTier):
    #print (str_itemType)
    #print(str_Tier)
    # Currency
    if str_itemType == "curr" or str_itemType == "frag":
        str_MinimapIcon = "Hexagon"
    # Maps
    if str_itemType == "map" or str_itemType == "umap":
        str_MinimapIcon = "Pentagon"
    # T2 Uniques
    if str_itemType == "uacc" and str_strTier == 2:
        str_MinimapIcon = "Star"
    if str_itemType == "uarm" and str_strTier == 2:
        str_MinimapIcon = "Star"
    if str_itemType == "ufla" and str_strTier == 2:
        str_MinimapIcon = "Star"
    if str_itemType == "ujew" and str_strTier == 2:
        str_MinimapIcon = "Star"
    if str_itemType == "umap" and str_strTier == 2:
        str_MinimapIcon = "Star"
    if str_itemType == "uwea" and str_strTier == 2:
        str_MinimapIcon = "Star"
    # T3 Uniques
    if str_itemType == "uacc" and str_strTier == 3:
        str_MinimapIcon = "Star"
    if str_itemType == "uarm" and str_strTier == 3:
        str_MinimapIcon = "Star"
    if str_itemType == "ufla" and str_strTier == 3:
        str_MinimapIcon = "Star"
    if str_itemType == "ujew" and str_strTier == 3:
        str_MinimapIcon = "Star"
    if str_itemType == "umap" and str_strTier == 3:
        str_MinimapIcon = "Star"
    if str_itemType == "uweap" and str_strTier == 3:
        str_MinimapIcon = "Star"
    # All other Uniques
    if str_itemType == "uacc":
        str_MinimapIcon = "Cross"
    if str_itemType == "uarm":
        str_MinimapIcon = "Cross"
    if str_itemType == "ufla":
        str_MinimapIcon = "Cross"
    if str_itemType == "ujew":
        str_MinimapIcon = "Cross"
    if str_itemType == "umap":
        str_MinimapIcon = "Cross"
    if str_itemType == "uweap":
        str_MinimapIcon = "Cross"
    # Not sure what to put for beasts
    if str_itemType == "beast":
        str_MinimapIcon = ""
    # Div cards, Essences, Fossils, Prophecies, Oils, Inubators
    if str_itemType == "oil":
        str_MinimapIcon = "Square"
    if str_itemType == "div":
        str_MinimapIcon = "Square"
    if str_itemType == "ess":
        str_MinimapIcon = "Square"
    if str_itemType == "foss":
        str_MinimapIcon = "Square"
    if str_itemType == "inc":
        str_MinimapIcon = "Square"
    if str_itemType == "scar":
        str_MinimapIcon = "Square"
    if str_itemType == "prop":
        str_MinimapIcon = "Square"
    if str_itemType == "res":
        str_MinimapIcon = "Square"
    if str_itemType == "beast":
        str_MinimapIcon = "Square"
    # Gems
    if str_itemType == "gem" or "divergent" or "anomalous" or "phantasmal":
        str_MinimapIcon = "Circle"
    # Rare gear
    if str_itemType == "base" and str_variant == "":
        str_MinimapIcon = "Triangle"
    if str_itemType == "base" and str_variant != "":
        str_MinimapIcon = "Kite"
    if str_itemType == "ench":
        str_MinimapIcon = "Triangle"
    # All Tier 1 - Have to do last to overwrite anything above.
    if str_strTier == 1:
        str_MinimapIcon = "Diamond"
    return str_MinimapIcon

def assign_s_n_c(str_strTier):
    global str_MinimapIcon
    if str_strTier == 1:
        str_MinimapIcon = "0 White " + str_MinimapIcon
    if str_strTier == 2:
        str_MinimapIcon = "0 Pink " + str_MinimapIcon
    if str_strTier == 3:
        str_MinimapIcon = "1 Cyan " + str_MinimapIcon
    if str_strTier == 4:
        str_MinimapIcon = "1 Purple " + str_MinimapIcon
    if str_strTier == 5:
        str_MinimapIcon = "2 Blue " + str_MinimapIcon
    if str_strTier == 6:
        str_MinimapIcon = "2 Green " + str_MinimapIcon
    if str_strTier > 6:
        str_MinimapIcon = ""
    return str_MinimapIcon

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
            if row[13] == "":
                str_Tier = ""
            else:
                str_Tier = int(row[13])
            if row[14] == "":
                str_Override = ""
            else:
                str_Override = int(row[14])
            str_SetFontSize = row[15]
            str_PlayAlertSound = row[16]
            str_SetBackgroundColor = row[17]
            str_PlayEffect = row[18]
            str_MinimapIcon = row[19]
            str_hasdup = row[20]
            str_minval = row[21]
            str_maxval = row[22]

            #if str_name == "Regal Shard":
            #    print ("Regal Shard found.")
            #    print ("Regal Shard found.")
            #    print ("Regal Shard found.")
            #    print ("Regal Shard found.")
            #    print ("Regal Shard found.")
            #    print ("Regal Shard found.")
            #    print ("Regal Shard found.")
            #    time.sleep(10)

            # Assign Color, Icon, size, and color - based on strTier
            # return str_SetFontSize, str_PlayAlertSound, SetBackgroundColor, PlayEffect
            tempColor = assign_color(str_Tier)
            str_SetFontSize = tempColor[0]
            str_PlayAlertSound = tempColor[1]
            str_SetBackgroundColor = tempColor[2]
            str_PlayEffect = tempColor[3]
            str_MinimapIcon = assign_icon(str_category, str_Tier)
            str_MinimapIcon = assign_s_n_c(str_Tier)

            # Overwrite Color, Icon, size, and color - if str_Override != ""
            # return str_SetFontSize, str_PlayAlertSound, SetBackgroundColor, PlayEffect
            if str_Override != "":
                tempColor = assign_color(str_Override)
                str_SetFontSize = tempColor[0]
                str_PlayAlertSound = tempColor[1]
                str_SetBackgroundColor = tempColor[2]
                str_PlayEffect = tempColor[3]
                str_MinimapIcon = assign_icon(str_category, str_Override)
                str_MinimapIcon = assign_s_n_c(str_Override)

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
            csv_writer.writerow(output_row)
 
            #if str_name == "Regal Shard":
            #    print (output_row)
            #    time.sleep(10)

print('Done!')

