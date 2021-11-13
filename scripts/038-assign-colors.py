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
# Use the Tier (or Override) field to assign the correct values for play sounds, background colors, etc.

strCSVin = os.path.join(sys.path[0], "z030_assigned-values.csv")
strCSVout = os.path.join(sys.path[0], "z038_assigned-colors.csv")

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

def assign_color(str_Tier):
    print("Recieved "+str(str_Tier))
    if str_Tier == 1:
        str_SetFontSize = "45"
        str_PlayAlertSound = "2-300"
        str_SetBackgroundColor = "White"
        str_PlayEffect = "White"
    if str_Tier == 2:
        str_SetFontSize = "45"
        str_PlayAlertSound = "16-300"
        str_SetBackgroundColor = "Pink"
        str_PlayEffect = "Pink"
    if str_Tier == 3:
        str_SetFontSize = "45"
        str_PlayAlertSound = "6-300"
        str_SetBackgroundColor = "Cyan"
        str_PlayEffect = "Cyan"
    if str_Tier == 4:
        str_SetFontSize = "45"
        str_PlayAlertSound = "7-300"
        str_SetBackgroundColor = "Purple"
        str_PlayEffect = "Purple"
    if str_Tier == 5:
        str_SetFontSize = "42"
        str_PlayAlertSound = "8-300"
        str_SetBackgroundColor = "Blue"
        str_PlayEffect = "Blue"
    if str_Tier == 6:
        str_SetFontSize = "42"
        str_PlayAlertSound = "9-300"
        str_SetBackgroundColor = "Green"
        str_PlayEffect = "None"
    if str_Tier == 7:
        str_SetFontSize = "42"
        str_PlayAlertSound = "'9-1"
        str_SetBackgroundColor = "Yellow"
        str_PlayEffect = "None"
    if str_Tier == 8:
        str_SetFontSize = "42"
        str_PlayAlertSound = "'9-1"
        str_SetBackgroundColor = "Orange"
        str_PlayEffect = "None"
    if str_Tier == 9:
        str_SetFontSize = "39"
        str_PlayAlertSound = "'9-1"
        str_SetBackgroundColor = "Red"
        str_PlayEffect = "None"
    if str_Tier == 10:
        str_SetFontSize = "39"
        str_PlayAlertSound = "'9-1"
        str_SetBackgroundColor = "Brown"
        str_PlayEffect = "None"
    if str_Tier == 11:
        str_SetFontSize = "39"
        str_PlayAlertSound = ""
        str_SetBackgroundColor = "Grey"
        str_PlayEffect = "None"
    if str_Tier == 12:
        str_SetFontSize = "39"
        str_PlayAlertSound = ""
        str_SetBackgroundColor = "Grey"
        str_PlayEffect = "None"
    return str_SetFontSize, str_PlayAlertSound, str_SetBackgroundColor, str_PlayEffect

def assign_icon(str_Category, str_variant, str_strTier):
    #print (str_Category)
    #print(str_Tier)
    # Currency
    if str_Category == "curr" or str_Category == "frag" or str_Category == "scar":
        str_MinimapIcon = "Hexagon"

    # Maps
    if str_Category == "map" or str_Category == "umap" or str_Category == "repmap" or str_Category == "clus" or str_Category == "arts" or str_Category == "deli" or str_Category == "blight" or str_Category == "inv" or str_Category == "vial" or str_Category == "watch" or str_Category == "ubermap" or str_Category == "scourgemap":
        str_MinimapIcon = "Pentagon"

    # Uniques
    if str_Category == "uacc" or str_Category == "uarm" or str_Category == "ufla" or str_Category == "ujew" or str_Category == "umap" or str_Category == "uweap":
        if str_strTier == 2 or str_strTier == 3:
            str_MinimapIcon = "Star"
        else:
            str_MinimapIcon = "Cross"

    # Replica Uniques
    if str_Category == "repacc" or str_Category == "reparm" or str_Category == "repfla" or str_Category == "repjew" or str_Category == "repmap" or str_Category == "repweap":
        if str_strTier == 2 or str_strTier == 3:
            str_MinimapIcon = "Star"
        else:
            str_MinimapIcon = "Cross"

    # Div cards, Essences, Fossils, Prophecies, Oils, Inubators
    if str_Category == "oil" or str_Category == "div" or str_Category == "ess" or str_Category == "foss" or str_Category == "inc" or str_Category == "prop" or str_Category == "res":
        str_MinimapIcon = "Square"

    # non-Influenced Bases
    if (str_Category == "base" or str_Category == "ench") and str_variant == "":
        str_MinimapIcon = "Triangle"

    # Influenced Bases
    if (str_Category == "base" or str_Category == "ench") and str_variant != "":
        str_MinimapIcon = "Kite"

    # Gems
    if str_Category == "gem" or str_Category == "divergent" or str_Category == "anomalous" or str_Category == "phantasmal":
        str_MinimapIcon = "Circle"

    # Not sure what to put for beasts
    if str_Category == "beast":
        str_MinimapIcon = ""

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

print("Starting to assign colors and stuff.")
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
        print (row)
        #print ()
        if row[10] != "chaosEquivalent":
            str_Category = row[0]
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
            str_Tier = int(row[11])
            if row[12] != "":
                str_Override = int(row[12])
            else:
                str_Override = ""
            str_Count = row[13]
            str_SetFontSize = row[14]
            str_PlayAlertSound = row[15]
            str_SetBackgroundColor = row[16]
            str_PlayEffect = row[17]
            str_MinimapIcon = row[18]
            str_hasdup = row[19]
            str_minval = row[20]
            str_maxval = row[21]

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
            str_MinimapIcon = assign_icon(str_Category, str_variant, str_Tier)
            str_MinimapIcon = assign_s_n_c(str_Tier)

            # Overwrite Color, Icon, size, and color - if str_Override != ""
            # return str_SetFontSize, str_PlayAlertSound, SetBackgroundColor, PlayEffect
            if str_Override != "":
                tempColor = assign_color(str_Override)
                str_SetFontSize = tempColor[0]
                str_PlayAlertSound = tempColor[1]
                str_SetBackgroundColor = tempColor[2]
                str_PlayEffect = tempColor[3]
                str_MinimapIcon = assign_icon(str_Category, str_variant, str_Override)
                str_MinimapIcon = assign_s_n_c(str_Override)

            # Create output row
            output_row = [str_Category]
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
            output_row.append(str_minval)
            output_row.append(str_maxval)
    
            # Add the updated row / list to the output file
            #print(output_row)
            csv_writer.writerow(output_row)
 
            #if str_name == "Regal Shard":
            #    print (output_row)
            #    time.sleep(10)

print('Done!')

