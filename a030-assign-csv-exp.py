import csv
import os.path
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

strCSVin = r'E:\PoE Stuff\Filters\1\exp\020_dup_other_removed.csv'
strCSVout = r'E:\PoE Stuff\Filters\1\exp\030_assigned.csv'
strCSVbak = r'E:\PoE Stuff\Filters\1\exp\030_assigned.bak.csv'

def func_init():

    # Check for existence of a previous .bak file and delete it if it's found.
    if os.path.isfile(strCSVbak):
        os.remove(strCSVbak)

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
    str_chaosEquivalent = float(str_chaosEquivalent)
    #print (str_chaosEquivalent)
    if str_chaosEquivalent < 0.1:
        str_strTier = 10
        str_SetFontSize = "32"
        str_PlayAlertSound = "'9-1"
    if str_chaosEquivalent >= 0.1:
        str_strTier = 9
        str_SetFontSize = "32"
        str_PlayAlertSound = "'9-1"
    if str_chaosEquivalent >= 0.15:
        str_strTier = 8
        str_SetFontSize = "36"
        str_PlayAlertSound = "'9-1"
#    if str_chaosEquivalent >= 0.99:
    if str_chaosEquivalent >= 1:
        str_strTier = 7
        str_SetFontSize = "36"
        str_PlayAlertSound = "'9-1"
    if str_chaosEquivalent >= 5:
        str_strTier = 6
        str_SetFontSize = "39"
        str_PlayAlertSound = "9-300"
    if str_chaosEquivalent >= 10:
        str_strTier = 5
        str_SetFontSize = "39"
        str_PlayAlertSound = "8-300"
    if str_chaosEquivalent >= 20:
        str_strTier = 4
        str_SetFontSize = "42"
        str_PlayAlertSound = "7-300"
    if str_chaosEquivalent >= 25:
        str_strTier = 3
        str_SetFontSize = "42"
        str_PlayAlertSound = "6-300"
    if str_chaosEquivalent >= 50:
        str_strTier = 2
        str_SetFontSize = "45"
        str_PlayAlertSound = "16-300"
    if str_chaosEquivalent >= 100:
        str_strTier = 1
        str_SetFontSize = "45"
        str_PlayAlertSound = "2-300"
    if str_minval != "":
        str_strTier = 11
        str_SetFontSize = "39"
        str_PlayAlertSound = ""
    # print(f'Value {str_chaosEquivalent} is str_strTier {tier}')
    return str_strTier, str_SetFontSize, str_PlayAlertSound

def assign_color(str_itemType, str_strTier):
    if str_strTier == 1:
        str_SetBackgroundColor = "White"
        str_PlayEffect = "White"
    if str_strTier == 2:
        str_SetBackgroundColor = "Pink"
        str_PlayEffect = "Pink"
    if str_strTier == 3:
        str_SetBackgroundColor = "Cyan"
        str_PlayEffect = "Cyan"
    if str_strTier == 4:
        str_SetBackgroundColor = "Purple"
        str_PlayEffect = "Purple"
    if str_strTier == 5:
        str_SetBackgroundColor = "Blue"
        str_PlayEffect = "Blue"
    if str_strTier == 6:
        str_SetBackgroundColor = "Green"
        str_PlayEffect = "None"
    if str_strTier == 7:
        str_SetBackgroundColor = "Yellow"
        str_PlayEffect = "None"
    if str_strTier == 8:
        str_SetBackgroundColor = "Orange"
        str_PlayEffect = "None"
    if str_strTier == 9:
        str_SetBackgroundColor = "Red"
        str_PlayEffect = "None"
    if str_strTier == 10:
        str_SetBackgroundColor = "Brown"
        str_PlayEffect = "None"
    if str_strTier == 11:
        str_SetBackgroundColor = "Grey"
        str_PlayEffect = "None"
    return str_SetBackgroundColor, str_PlayEffect

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

            # Fix category names and reassign items that poe.ninja have incorrectly categorized
            # may need to change more later (beasts, umap, etc)
            ####################################### beasts are Class Map Frags? No, only lures are.
            if (((str_category == "frag" in str_name) and ("Goddess" not in str_name)) or ("splinter" in str_name)):
                str_category = "curr"
            if str_category == "inv":
                str_category = "frag"
            if str_category == "scar":
                str_category = "Map Fragments"
            if str_category == "res":
                str_category = "Delve Stackable Socketable Currency"
            # Moving Divergent, Anomalous, & Phantasmal gems to their own categories in order to make them easier to deal with later.
            if "Divergent" in str_name:
                str_category = "divergent"
                str_itemType = "divergent"
                str_name = str_name.replace("Divergent ", "")
            if "Anomalous" in str_name:
                str_category = "anomalous"
                str_itemType = "anomalous"
                str_name = str_name.replace("Anomalous ", "")
            if "Phantasmal" in str_name:
                str_category = "phantasmal"
                str_itemType = "phantasmal"
                str_name = str_name.replace("Phantasmal ", "")

            # Assign Tier
            # return str_strTier, str_SetFontSize,  str_PlayAlertSound
            tempTier = assign_tier(str_chaosEquivalent, str_minval)
            str_Tier = tempTier[0]
            str_SetFontSize = tempTier[1]
            str_PlayAlertSound = tempTier[2]
            #
            # Assign Color
            # return SetBackgroundColor, PlayEffect
            tempColor = assign_color(str_category, str_Tier)
            str_SetBackgroundColor = tempColor[0]
            str_PlayEffect = tempColor[1]
            #
            # Assign Icon, then size and color
            str_MinimapIcon = assign_icon(str_category, str_Tier)
            str_MinimapIcon = assign_s_n_c(str_Tier)
    
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
            csv_writer.writerow(output_row)
 
print('Done!')

