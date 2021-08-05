import csv
import re
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

strUserSettings = r'E:\PoE Stuff\Filters\1\exp\00_user_settings.txt'
strCSVin = r'E:\PoE Stuff\Filters\1\exp\030_assigned.csv'
strCSVinOther = r'E:\PoE Stuff\Filters\1\exp\ZZ_other.csv'
strTXTout = r'E:\PoE Stuff\Filters\1\exp\030_filter.filter'
arrInfluences = ["Crusader","Elder","Hunter","Redeemer","Shaper","Warlord"]
arrDoubleInfluences = ["Crusader/Hunter","Crusader/Redeemer","Crusader/Warlord","Elder/Crusader","Elder/Hunter","Elder/Redeemer","Elder/Warlord","Redeemer/Hunter","Redeemer/Warlord","Shaper/Crusader","Shaper/Elder","Shaper/Elder/Crusader/Redeemer/Warlord/Hunter","Shaper/Hunter","Shaper/Redeemer","Shaper/Warlord","Warlord/Hunter"]

def func_init():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Set defaults
    strOverallStrictness = "10"
    strRareCutoff = "0"
    strGrayCutoff = "0"
    booShowT11 = 1
    booShowNM6S = 1
    booShowNM5S = 1

    # Overwrite defaults if found in settings file
    with open(r'E:\PoE Stuff\Filters\1\exp\00_user_settings.txt', 'r') as f:
        for line in f:
            if "Overall Strictness: " in line:
                strOverallStrictness = (line.split("Overall Strictness: ")[1])
                strOverallStrictness = strOverallStrictness.strip()
                #print ("strOverallStrictness is " + strOverallStrictness)
            if "Non-special Rare cutoff: " in line:
                strRareCutoff = (line.split("Non-special Rare cutoff: ")[1])
                strRareCutoff = strRareCutoff.strip()
                #print ("strRareCutoff is " + strRareCutoff)
            if "Gray item cutoff: " in line:
                strGrayCutoff = (line.split("Gray item cutoff: ")[1])
                strGrayCutoff = strGrayCutoff.strip()
                #print ("strGrayCutoff is " + strGrayCutoff)
            if "Show gray items: " in line:
                booShowT11 = (line.split("Show gray items: ")[1])
                booShowT11 = booShowT11.strip()
                #print ("booShowT11 is " + booShowT11)
            if "Show Normal/Magic 6-socket items: " in line:
                booShowNM6S = (line.split("Show Normal/Magic 6-socket items: ")[1])
                booShowNM6S = booShowNM6S.strip()
                #print ("booShowNM6S is " + booShowNM6S)
            if "Show Normal/Magic 5-socket items: " in line:
                booShowNM5S = (line.split("Show Normal/Magic 5-socket items: ")[1])
                booShowNM5S = booShowNM5S.strip()
                #print ("booShowNM5S is " + booShowNM5S)

    # Hard setting this right now so I can play with the GUI without screwing up my filters
    strRareCutoff = "76"

    # Open the output file in write mode
    with open(strTXTout, 'w', newline='') as write_obj:
        pass

    print ("User Settings read in, new filter initialized.")

def ChangeColors (str_SetBackgroundColor):
    #print("Got called for " + str_SetBackgroundColor)
    if str_SetBackgroundColor == "White":
        str_SetBackgroundColor = "255 255 255 255 # White"
    if str_SetBackgroundColor == "Pink":
        str_SetBackgroundColor = "242 146 234 255 # Pink"
        # str_SetBackgroundColor = "234 84 219 255 # Pink" # Alternate
        # str_SetBackgroundColor = "236 164 252 255 # Pink" # Alternate
        # str_SetBackgroundColor = "236 164 252 255 # Pink" # Alternate
    if str_SetBackgroundColor == "Cyan":
        str_SetBackgroundColor = "132 211 250 255 # Cyan"
        # str_SetBackgroundColor = "100 200 255 255 # Cyan" # Alternate
        # str_SetBackgroundColor = "92 156 188 255 # Cyan" # Alternate
    if str_SetBackgroundColor == "Purple":
        str_SetBackgroundColor = "100 0 100 235 # Purple"
        # str_SetBackgroundColor = "163 52 235 235 # Purple" # Alternate
        # str_SetBackgroundColor = "125 30 176 235 # Purple" # Alternate
    if str_SetBackgroundColor == "Blue":
        str_SetBackgroundColor = "25 25 255 235 # Blue"
        # str_SetBackgroundColor = "4 115 220 235 # Blue" # Alternate
        # str_SetBackgroundColor = "12 124 224 235 # Blue" # Alternate
    if str_SetBackgroundColor == "Green":
        str_SetBackgroundColor = "28 236 4 215 # Green"
        # str_SetBackgroundColor = "30 125 30 215 # Green" # Alternate
        # str_SetBackgroundColor = "100 192 56 215 # Green" # Alternate
        # str_SetBackgroundColor = "42 169 109 215 # Green" # Alternate
        # str_SetBackgroundColor = "36 132 92 215 # Green" # Alternate
    if str_SetBackgroundColor == "Yellow":
        str_SetBackgroundColor = "255 255 0 215 # Yellow"
        # str_SetBackgroundColor = "211 155 4 215 # Yellow" # Alternate
        # str_SetBackgroundColor = "196 140 4 215 # Yellow" # Alternate
        # str_SetBackgroundColor = "211 211 4 215 # Yellow" # Alternate
    if str_SetBackgroundColor == "Orange":
        #str_SetBackgroundColor = "223 132 20 230 # Orange"
        # str_SetBackgroundColor = "255 100 25 230 # Orange" # Alternate
        # str_SetBackgroundColor = "251 147 28 230 # Orange" # Alternate
        # str_SetBackgroundColor = "256 132 4 230 # Orange" # Alternate
         str_SetBackgroundColor = "244 92 36 230 # Orange" # Alternate
    if str_SetBackgroundColor == "Red":
        #str_SetBackgroundColor = "188 29 29 210 # Red"
        # str_SetBackgroundColor = "255 0 0 210 # Red" # Alternate
        # str_SetBackgroundColor = "212 32 48 210 # Red" # Alternate
        # str_SetBackgroundColor = "148 25 31 210 # Red" # Alternate
        str_SetBackgroundColor = "187 28 28 210 # Red" # Alternate
    if str_SetBackgroundColor == "Brown":
        str_SetBackgroundColor = "82 51 7 220 # Brown"
        # str_SetBackgroundColor = "116 52 4 220 # Brown" # Alternate
        # str_SetBackgroundColor = "160 98 18 220 # Brown" # Alternate
        # str_SetBackgroundColor = "125 76 12 220 # Brown" # Alternate
        # str_SetBackgroundColor = "102 61 12 220 # Brown" # Alternate
        # str_SetBackgroundColor = "38 24 4 220 # Brown" # Alternate
    if str_SetBackgroundColor == "Grey":
        str_SetBackgroundColor = "100 100 100 255 # Grey"
        # str_SetBackgroundColor = "108 108 108 255 # Grey" # Alternate
        # str_SetBackgroundColor = "156 156 156 255 # Grey" # Alternate
        # str_SetBackgroundColor = "164 164 164 255 # Grey" # Alternate
    return str_SetBackgroundColor

def func_static_intro():
    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("###########################################################################\n")
        write_obj.write("##### The notes you'll find in this document are NOT intended for SSF, HC,\n")
        write_obj.write("##### or race leagues. If you're playing one of those this is NOT the right\n")
        write_obj.write("##### tool for you. You're going to want/need granularity that I don't, and I\n")
        write_obj.write("##### have no interest in building that into this tool. You can either go use\n")
        write_obj.write("##### FilterBlade or fork my project if you want that level of granularity.\n")
        write_obj.write("\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Static Intro - special highlighting\n")
        write_obj.write("##### Less-nice items not caught here may still be caught farther below.\n")
        write_obj.write("\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### 6L\n")
        write_obj.write("\n")
        write_obj.write("Show\n")
        write_obj.write("	LinkedSockets = 6\n")
        write_obj.write("	SetFontSize 45\n")
        write_obj.write("	SetBackgroundColor 0 0 0 255     # BACKGROUNDCOLOR WHITE\n")
        write_obj.write("	PlayAlertSound 10 300\n")
        write_obj.write("	PlayEffect White\n")
        write_obj.write("	MinimapIcon 0 White Diamond\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Sockets = 6\n")
        write_obj.write("##### Unique items might be worth something.\n")
        write_obj.write("##### Rare items are almost definitely worth grabbing if ItemLevel >= 84\n")
        write_obj.write("##### Rare items ItemLevel < 84 might be worth something, we'll make that adjustable.\n")
        write_obj.write("##### Normal/magic are only worth grabbing in Acts 1-5 when you need the\n")
        write_obj.write("##### Jeweller's. Past that taking up 8 inventory slots for .1c is a waste.\n")
        write_obj.write("\n")
        write_obj.write("Show\n")
        write_obj.write("	Sockets = 6\n")
        write_obj.write("	Rarity Unique\n")
        write_obj.write("	SetFontSize 45\n")
        write_obj.write("	SetBackgroundColor 102 0 102 255     # BACKGROUNDCOLOR PURPLE\n")
        write_obj.write("	PlayAlertSound 10 300\n")
        write_obj.write("	PlayEffect Purple\n")
        write_obj.write("	MinimapIcon 0 Purple Diamond\n")
        write_obj.write("Show\n")
        write_obj.write("	Sockets = 6\n")
        write_obj.write("	ItemLevel >= 84\n")
        write_obj.write("	Rarity Rare\n")
        write_obj.write("	SetFontSize 45\n")
        write_obj.write("	SetBackgroundColor 102 0 102 255     # BACKGROUNDCOLOR PURPLE\n")
        write_obj.write("	PlayAlertSound 10 300\n")
        write_obj.write("	PlayEffect Purple\n")
        write_obj.write("	MinimapIcon 0 Purple Diamond\n")
        write_obj.write("Show\n")
        write_obj.write("	Sockets = 6\n")
        write_obj.write("	ItemLevel >= "+strRareCutoff+"\n")
        write_obj.write("	Rarity Rare\n")
        write_obj.write("	SetFontSize 45\n")
        write_obj.write("	SetBackgroundColor 102 0 102 255     # BACKGROUNDCOLOR PURPLE\n")
        write_obj.write("	PlayAlertSound 10 300\n")
        write_obj.write("	PlayEffect Purple\n")
        write_obj.write("	MinimapIcon 0 Purple Diamond\n")
        if booShowNM6S == 1:
            write_obj.write("Show\n")
            write_obj.write("	Sockets = 6\n")
            write_obj.write("	SetFontSize 45\n")
            write_obj.write("	SetBackgroundColor 102 0 102 255     # BACKGROUNDCOLOR PURPLE\n")
            write_obj.write("	PlayAlertSound 10 300\n")
            write_obj.write("	PlayEffect Purple\n")
            write_obj.write("	MinimapIcon 0 Purple Diamond\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### 5L\n")
        write_obj.write("##### Grab if Unique. Rare might be worth something.\n")
        write_obj.write("##### Normal/magic are super cheap. Past early maps they're not worth selling,\n")
        write_obj.write("##### and crafting in this game's so bad they're not worth wasting orbs on.\n")
        write_obj.write("\n")
        write_obj.write("Show\n")
        write_obj.write("	LinkedSockets = 5\n")
        write_obj.write("	Rarity Unique\n")
        write_obj.write("	SetFontSize 40\n")
        write_obj.write("	SetBackgroundColor 26 26 255 255     # BACKGROUNDCOLOR BLUE\n")
        write_obj.write("	PlayAlertSound 8 300\n")
        write_obj.write("	PlayEffect Blue\n")
        write_obj.write("	MinimapIcon 0 Blue Cross\n")
        write_obj.write("Show\n")
        write_obj.write("	Sockets = 5\n")
        write_obj.write("	ItemLevel >= "+strRareCutoff+"\n")
        write_obj.write("	Rarity Rare\n")
        write_obj.write("	SetFontSize 45\n")
        write_obj.write("	SetBackgroundColor 102 0 102 255     # BACKGROUNDCOLOR PURPLE\n")
        write_obj.write("	PlayAlertSound 10 300\n")
        write_obj.write("	PlayEffect Purple\n")
        write_obj.write("	MinimapIcon 0 Purple Diamond\n")
        if booShowNM5S == 1:
            write_obj.write("Show\n")
            write_obj.write("	LinkedSockets = 5\n")
            write_obj.write("	SetFontSize 40\n")
            write_obj.write("	SetBackgroundColor 31 122 31 255     # BACKGROUNDCOLOR GREEN\n")
            write_obj.write("	PlayAlertSound 8 300\n")
            write_obj.write("	PlayEffect Green\n")
            write_obj.write("	MinimapIcon 0 Green Triangle\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### 4L\n")
        write_obj.write("##### I only want LinkedSockets = 4 if Unique, or Rare and 2x2.\n")
        write_obj.write("##### For mapping the ilvl is adjustable for the Rares.\n")
        write_obj.write("##### I know 4L doesn't add much to the value of the item, but 99.9999% of\n")
        write_obj.write("##### unidentified rares are trash so using ANY method to filter them out is\n")
        write_obj.write("##### better than picking up and identifying all of them.\n")
        write_obj.write("\n")
        write_obj.write("Show\n")
        write_obj.write("	Rarity Unique\n")
        write_obj.write("	LinkedSockets = 4\n")
        write_obj.write("	Width = 2\n")
        write_obj.write("	Height = 2\n")
        write_obj.write("	SetFontSize 35\n")
        write_obj.write("	SetBackgroundColor 26 26 255 255     # BACKGROUNDCOLOR BLUE\n")
        write_obj.write("	PlayAlertSound 8 300\n")
        write_obj.write("	MinimapIcon 0 Blue Cross\n")
        write_obj.write("Show\n")
        write_obj.write("	Rarity Rare\n")
        write_obj.write("	ItemLevel >= "+strRareCutoff+"\n")
        write_obj.write("	LinkedSockets = 4\n")
        write_obj.write("	Width = 2\n")
        write_obj.write("	Height = 2\n")
        write_obj.write("	SetFontSize 35\n")
        write_obj.write("	SetBackgroundColor 31 122 31 255     # BACKGROUNDCOLOR GREEN\n")
        write_obj.write("	PlayAlertSound 8 300\n")
        write_obj.write("	MinimapIcon 0 Green Triangle\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### 3L\n")
        write_obj.write("##### I only want LinkedSockets = 3 if Unique, or Rare and 1x3.\n")
        write_obj.write("##### For mapping the ilvl is adjustable for Rares.\n")
        write_obj.write("##### I know 3L doesn't add much to the value of the item, but 99.9999% of\n")
        write_obj.write("##### unidentified rares are trash so using ANY method to filter them out is\n")
        write_obj.write("##### better than picking up and identifying all of them.\n")
        write_obj.write("\n")
        write_obj.write("Show\n")
        write_obj.write("	Rarity Unique\n")
        write_obj.write("	LinkedSockets = 3\n")
        write_obj.write("	Width = 1\n")
        write_obj.write("	Height = 3\n")
        write_obj.write("	SetFontSize 35\n")
        write_obj.write("	SetBackgroundColor 26 26 255 255     # BACKGROUNDCOLOR BLUE\n")
        write_obj.write("	PlayAlertSound 8 300\n")
        write_obj.write("	MinimapIcon 0 Blue Cross\n")
        write_obj.write("Show\n")
        write_obj.write("	Rarity Rare\n")
        write_obj.write("	ItemLevel >= "+strRareCutoff+"\n")
        write_obj.write("	LinkedSockets = 3\n")
        write_obj.write("	Width = 1\n")
        write_obj.write("	Height = 3\n")
        write_obj.write("	SetFontSize 35\n")
        write_obj.write("	SetBackgroundColor 31 122 31 255     # BACKGROUNDCOLOR GREEN\n")
        write_obj.write("	PlayAlertSound 8 300\n")
        write_obj.write("	MinimapIcon 0 Green Triangle\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### I only want Rings/Amulet/Belts/Jewels if Unique or Rare.\n")
        write_obj.write("##### For mapping the ilvl is adjustable for Rares.\n")
        write_obj.write("\n")
        write_obj.write("Show\n")
        write_obj.write("	Rarity Unique\n")
        write_obj.write("	Class Rings Amulet Belts Jewel\n")
        write_obj.write("	Sockets > 0\n")
        write_obj.write("	SetFontSize 35\n")
        write_obj.write("	SetBackgroundColor 26 26 255 255     # BACKGROUNDCOLOR BLUE\n")
        write_obj.write("	PlayAlertSound 8 300\n")
        write_obj.write("	MinimapIcon 0 Blue Cross\n")
        write_obj.write("Show\n")
        write_obj.write("	Rarity Rare\n")
        write_obj.write("	ItemLevel >= "+strRareCutoff+"\n")
        write_obj.write("	Class Rings Amulet Belts Jewel\n")
        write_obj.write("	Sockets > 0\n")
        write_obj.write("	SetFontSize 35\n")
        write_obj.write("	SetBackgroundColor 31 122 31 255     # BACKGROUNDCOLOR GREEN\n")
        write_obj.write("	PlayAlertSound 8 300\n")
        write_obj.write("	MinimapIcon 0 Green Triangle\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### White Sockets\n")
        write_obj.write("##### Can't upgrade Rare/Magic, only useful if item is Rare.\n")
        write_obj.write("##### Maybe make # of White sockets adjustable later for strictness.\n")
        write_obj.write("\n")
        write_obj.write("Show\n")
        write_obj.write("	SocketGroup W\n")
        write_obj.write("	Rarity Rare\n")
        write_obj.write("	SetFontSize 40\n")
        write_obj.write("	SetBackgroundColor 26 26 255 255     # BACKGROUNDCOLOR BLUE\n")
        write_obj.write("	PlayAlertSound 8 300\n")
        write_obj.write("	PlayEffect Blue\n")
        write_obj.write("	MinimapIcon 0 Blue Triangle\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Flasks - Unique and Magic\n")
        write_obj.write("##### Maybe make this adjustable later.\n")
        write_obj.write("\n")
        write_obj.write("Show\n")
        write_obj.write("	Class Flasks\n")
        write_obj.write("	Rarity Unique\n")
        write_obj.write("	SetFontSize 39\n")
        write_obj.write("	SetTextColor 0 0 0 255\n")
        write_obj.write("	SetBackgroundColor 25 25 255 235 # Blue\n")
        write_obj.write("	PlayAlertSound 8 300\n")
        write_obj.write("	PlayEffect Blue\n")
        write_obj.write("	MinimapIcon 2 Blue Circle\n")
        write_obj.write("Show\n")
        write_obj.write("	Rarity Magic\n")
        write_obj.write("	BaseType \"Divine Life\" \"Divine Mana\" \"Eternal Life\" \"Eternal Mana\"\n")
        write_obj.write("	SetFontSize 39\n")
        write_obj.write("	SetTextColor 0 0 0 255\n")
        write_obj.write("	SetBackgroundColor 28 236 4 215 # Green\n")
        write_obj.write("	PlayAlertSound 9 300\n")
        write_obj.write("	PlayEffect None\n")
        write_obj.write("	MinimapIcon 2 Green Circle\n")
        write_obj.write("Show\n")
        write_obj.write("	Rarity Normal Magic\n")
        write_obj.write("	Class \"Utility\"\n")
        write_obj.write("	SetFontSize 39\n")
        write_obj.write("	SetTextColor 0 0 0 255\n")
        write_obj.write("	SetBackgroundColor 28 236 4 215 # Green\n")
        write_obj.write("	PlayAlertSound 9 300\n")
        write_obj.write("	PlayEffect None\n")
        write_obj.write("	MinimapIcon 2 Green Circle\n")

    print ("Static Intro complete.")

def func_curr():
    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Currency\n")
        write_obj.write("#####\n")

        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i) + ".")
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_category = row[0]
                        str_name = row[1]
                        if row[14] != "":
                            str_Tier = row[14]
                        else:
                            str_Tier = row[13]
                        str_SetFontSize = row[15]
                        str_PlayAlertSound = row[16]
                        str_SetBackgroundColor = row[17]
                        str_PlayEffect = row[18]
                        str_MinimapIcon = row[19]

                        if int(str_Tier) == i and str_category == "curr":
                            LineToWrite = LineToWrite + ' "' + str_name + '"'
                            FontSizeToWrite = str_SetFontSize
                            BackgroundColorToWrite = str_SetBackgroundColor
                            AlertSoundToWrite = str_PlayAlertSound
                            EffectToWrite = str_PlayEffect
                            IconToWrite = str_MinimapIcon

            if LineToWrite != "":
                str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                write_obj.write("Show\n")
                write_obj.write("	Class Currency\n")
                write_obj.write("	BaseType =="+LineToWrite+"\n")
                write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("	SetTextColor 0 0 0 255\n")
                write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("	MinimapIcon "+IconToWrite+"\n")
    print ("Currency section complete.")

def func_frag():

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Map Fragments & Scarabs\n")
        write_obj.write("#####\n")

        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_category = row[0]
                        str_name = row[1]
                        if row[14] != "":
                            str_Tier = row[14]
                        else:
                            str_Tier = row[13]
                        str_SetFontSize = row[15]
                        str_PlayAlertSound = row[16]
                        str_SetBackgroundColor = row[17]
                        str_PlayEffect = row[18]
                        str_MinimapIcon = row[19]

                        if int(str_Tier) == i and (str_category == "frag" or str_category == "Map Fragments"):
                            LineToWrite = LineToWrite + ' "' + str_name + '"'
                            FontSizeToWrite = str_SetFontSize
                            BackgroundColorToWrite = str_SetBackgroundColor
                            AlertSoundToWrite = str_PlayAlertSound
                            EffectToWrite = str_PlayEffect
                            IconToWrite = str_MinimapIcon

            if LineToWrite != "":
                str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                write_obj.write("Show\n")
                write_obj.write("	Class Map\n")
                write_obj.write("	BaseType =="+LineToWrite+"\n")
                write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("	SetTextColor 0 0 0 255\n")
                write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("	MinimapIcon "+IconToWrite+"\n")
    print ("Fragments and Sacarabs section complete.")

def func_oil():

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Oil\n")
        write_obj.write("#####\n")

        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_category = row[0]
                        str_name = row[1]
                        if row[14] != "":
                            str_Tier = row[14]
                        else:
                            str_Tier = row[13]
                        str_SetFontSize = row[15]
                        str_PlayAlertSound = row[16]
                        str_SetBackgroundColor = row[17]
                        str_PlayEffect = row[18]
                        str_MinimapIcon = row[19]

                        if int(str_Tier) == i and str_category == "oil":
                            LineToWrite = LineToWrite + ' "' + str_name + '"'
                            FontSizeToWrite = str_SetFontSize
                            BackgroundColorToWrite = str_SetBackgroundColor
                            AlertSoundToWrite = str_PlayAlertSound
                            EffectToWrite = str_PlayEffect
                            IconToWrite = str_MinimapIcon

            if LineToWrite != "":
                str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                write_obj.write("Show\n")
                write_obj.write("	Class Currency\n")
                write_obj.write("	BaseType =="+LineToWrite+"\n")
                write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("	SetTextColor 0 0 0 255\n")
                write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("	MinimapIcon "+IconToWrite+"\n")
    print ("Oil section complete.")

def func_heist():

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Heist - added from ""other"" csv file, not tracked by poe.ninja at this time. \n")
        write_obj.write("#####\n")

        # ilvl81 items
        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            with open(strCSVinOther, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_category = row[0]
                        str_baseType = row[2]
                        str_levelRequired = row[6]
                        if row[14] != "":
                            str_Tier = row[14]
                        else:
                            str_Tier = row[13]
                        str_SetFontSize = row[15]
                        str_PlayAlertSound = row[16]
                        str_SetBackgroundColor = row[17]
                        str_PlayEffect = row[18]
                        str_MinimapIcon = row[19]

                        if int(str_Tier) == i and str_category == "heist" and str_levelRequired == "84":
                            LineToWrite = LineToWrite + ' "' + str_baseType + '"'
                            LevelToWrite = str_levelRequired
                            FontSizeToWrite = str_SetFontSize
                            BackgroundColorToWrite = str_SetBackgroundColor
                            AlertSoundToWrite = str_PlayAlertSound
                            EffectToWrite = str_PlayEffect
                            IconToWrite = str_MinimapIcon

            if LineToWrite != "":
                #print(LevelToWrite)
                str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                write_obj.write("Show\n")
                write_obj.write("	Class Heist\n")
                write_obj.write("	ItemLevel >= "+LevelToWrite+"\n")
                write_obj.write("	BaseType =="+LineToWrite+"\n")
                write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("	SetTextColor 0 0 0 255\n")
                write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("	MinimapIcon "+IconToWrite+"\n")

        # ilvl83 items
        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            with open(strCSVinOther, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_category = row[0]
                        str_baseType = row[2]
                        str_levelRequired = row[6]
                        if row[14] != "":
                            str_Tier = row[14]
                        else:
                            str_Tier = row[13]
                        str_SetFontSize = row[15]
                        str_PlayAlertSound = row[16]
                        str_SetBackgroundColor = row[17]
                        str_PlayEffect = row[18]
                        str_MinimapIcon = row[19]

                        if int(str_Tier) == i and str_category == "heist" and str_levelRequired == "83":
                            LineToWrite = LineToWrite + ' "' + str_baseType + '"'
                            LevelToWrite = str_levelRequired
                            FontSizeToWrite = str_SetFontSize
                            BackgroundColorToWrite = str_SetBackgroundColor
                            AlertSoundToWrite = str_PlayAlertSound
                            EffectToWrite = str_PlayEffect
                            IconToWrite = str_MinimapIcon

            if LineToWrite != "":
                #print(LevelToWrite)
                str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                write_obj.write("Show\n")
                write_obj.write("	Class Heist\n")
                write_obj.write("	ItemLevel >= "+LevelToWrite+"\n")
                write_obj.write("	BaseType =="+LineToWrite+"\n")
                write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("	SetTextColor 0 0 0 255\n")
                write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("	MinimapIcon "+IconToWrite+"\n")

        # ilvl84 items
        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            with open(strCSVinOther, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_category = row[0]
                        str_baseType = row[2]
                        str_levelRequired = row[6]
                        if row[14] != "":
                            str_Tier = row[14]
                        else:
                            str_Tier = row[13]
                        str_SetFontSize = row[15]
                        str_PlayAlertSound = row[16]
                        str_SetBackgroundColor = row[17]
                        str_PlayEffect = row[18]
                        str_MinimapIcon = row[19]

                        if int(str_Tier) == i and str_category == "heist" and str_levelRequired == "81":
                            LineToWrite = LineToWrite + ' "' + str_baseType + '"'
                            LevelToWrite = str_levelRequired
                            FontSizeToWrite = str_SetFontSize
                            BackgroundColorToWrite = str_SetBackgroundColor
                            AlertSoundToWrite = str_PlayAlertSound
                            EffectToWrite = str_PlayEffect
                            IconToWrite = str_MinimapIcon

            if LineToWrite != "":
                #print(LevelToWrite)
                str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                write_obj.write("Show\n")
                write_obj.write("	Class Heist\n")
                write_obj.write("	ItemLevel >= "+LevelToWrite+"\n")
                write_obj.write("	BaseType =="+LineToWrite+"\n")
                write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("	SetTextColor 0 0 0 255\n")
                write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("	MinimapIcon "+IconToWrite+"\n")

        # All other items
        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            with open(strCSVinOther, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_category = row[0]
                        str_baseType = row[2]
                        str_levelRequired = row[6]
                        if row[14] != "":
                            str_Tier = row[14]
                        else:
                            str_Tier = row[13]
                        str_SetFontSize = row[15]
                        str_PlayAlertSound = row[16]
                        str_SetBackgroundColor = row[17]
                        str_PlayEffect = row[18]
                        str_MinimapIcon = row[19]

                        if int(str_Tier) == i and str_category == "heist" and str_levelRequired == "":
                            LineToWrite = LineToWrite + ' "' + str_baseType + '"'
                            FontSizeToWrite = str_SetFontSize
                            BackgroundColorToWrite = str_SetBackgroundColor
                            AlertSoundToWrite = str_PlayAlertSound
                            EffectToWrite = str_PlayEffect
                            IconToWrite = str_MinimapIcon

            if LineToWrite != "":
                str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                write_obj.write("Show\n")
                write_obj.write("	Class Heist\n")
                write_obj.write("	BaseType =="+LineToWrite+"\n")
                write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("	SetTextColor 0 0 0 255\n")
                write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("	MinimapIcon "+IconToWrite+"\n")

        # Last few Heist items
        write_obj.write("\n")
        write_obj.write("##### Last few Heist classes not otherwise noted.  Marking these as Tier 4.\n")
        write_obj.write("Show\n")
        write_obj.write("	Class ""Heist Target"" Trinkets Contract Blueprint\n")
        write_obj.write("	SetFontSize 39\n")
        write_obj.write("	SetTextColor 0 0 0 255\n")
        write_obj.write("	SetBackgroundColor 25 25 255 235 # Blue\n")
        write_obj.write("	PlayAlertSound 8 300\n")
        write_obj.write("	PlayEffect Blue\n")
        write_obj.write("	MinimapIcon 2 Blue Pentagon\n")

    print ("Heist section complete.")

def func_cluster():

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Cluster Jewels - added from ""other"" csv file, too many variants for\n")
        write_obj.write("##### poe.ninja data to be useful.\n")
        write_obj.write("#####\n")

        write_obj.write("Show # T3\n")
        write_obj.write("    BaseType \"Large Cluster Jewel\"\n")
        write_obj.write("    ItemLevel >= 82\n")
        write_obj.write("    EnchantmentPassiveNum = 8\n")
        write_obj.write("    SetFontSize 42\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 132 211 250 255 # Cyan\n")
        write_obj.write("    PlayAlertSound 6 300\n")
        write_obj.write("    PlayEffect Cyan\n")
        write_obj.write("    MinimapIcon 1 Cyan Pentagon\n")

        write_obj.write("Show # T3\n")
        write_obj.write("    BaseType \"Medium Cluster Jewel\"\n")
        write_obj.write("    ItemLevel = 84\n")
        write_obj.write("    EnchantmentPassiveNum 4\n")
        write_obj.write("    SetFontSize 42\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 132 211 250 255 # Cyan\n")
        write_obj.write("    PlayAlertSound 6 300\n")
        write_obj.write("    PlayEffect Cyan\n")
        write_obj.write("    MinimapIcon 1 Cyan Pentagon\n")

        write_obj.write("Show # T4\n")
        write_obj.write("    BaseType \"Large Cluster Jewel\"\n")
        write_obj.write("    EnchantmentPassiveNum 8\n")
        write_obj.write("    SetFontSize 42\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 100 0 100 235 # Purple\n")
        write_obj.write("    PlayAlertSound 7 300\n")
        write_obj.write("    PlayEffect Purple\n")
        write_obj.write("    MinimapIcon 1 Purple Pentagon\n")

        write_obj.write("Show # T4\n")
        write_obj.write("    BaseType \"Medium Cluster Jewel\"\n")
        write_obj.write("    EnchantmentPassiveNum 4\n")
        write_obj.write("    SetFontSize 42\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 100 0 100 235 # Purple\n")
        write_obj.write("    PlayAlertSound 7 300\n")
        write_obj.write("    PlayEffect Purple\n")
        write_obj.write("    MinimapIcon 1 Purple Pentagon\n")

        write_obj.write("Show # T5\n")
        write_obj.write("    BaseType \"Small Cluster Jewel\"\n")
        write_obj.write("    ItemLevel = 82\n")
        write_obj.write("    SetFontSize 39\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 25 25 255 235 # Blue\n")
        write_obj.write("    PlayAlertSound 8 300\n")
        write_obj.write("    PlayEffect Blue\n")
        write_obj.write("    MinimapIcon 2 Blue Pentagon\n")

        write_obj.write("Show # T6\n")
        write_obj.write("    BaseType \"Large Cluster Jewel\" \"Medium Cluster Jewel\" \"Small Cluster Jewel\"\n")
        write_obj.write("    SetFontSize 39\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 28 236 4 215 # Green\n")
        write_obj.write("    PlayAlertSound 9 300\n")

    print ("Cluster Jewel section complete.")

def func_other():

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Other - added from ""other"" csv file, not tracked by poe.ninja at this time. \n")
        write_obj.write("#####\n")

        # ilvl81 items
        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            with open(strCSVinOther, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_category = row[0]
                        str_baseType = row[2]
                        str_levelRequired = row[6]
                        if row[14] != "":
                            str_Tier = row[14]
                        else:
                            str_Tier = row[13]
                        str_SetFontSize = row[15]
                        str_PlayAlertSound = row[16]
                        str_SetBackgroundColor = row[17]
                        str_PlayEffect = row[18]
                        str_MinimapIcon = row[19]

                        if int(str_Tier) == i and str_category == "other":
                            LineToWrite = LineToWrite + ' "' + str_baseType + '"'
                            FontSizeToWrite = str_SetFontSize
                            BackgroundColorToWrite = str_SetBackgroundColor
                            AlertSoundToWrite = str_PlayAlertSound
                            EffectToWrite = str_PlayEffect
                            IconToWrite = str_MinimapIcon

            if LineToWrite != "":
                str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                write_obj.write("Show\n")
                write_obj.write("	Class "+LineToWrite+"\n")
                write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("	SetTextColor 0 0 0 255\n")
                write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("	MinimapIcon "+IconToWrite+"\n")

        # Create section
        write_obj.write("\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Expedition Currency \n")
        write_obj.write("#####\n")

        # Expedition Currency items
        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            with open(strCSVinOther, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_category = row[0]
                        str_Name = row[1]
                        str_BaseType = row[2]
                        str_levelRequired = row[6]
                        if row[14] != "":
                            str_Tier = row[14]
                        else:
                            str_Tier = row[13]
                        str_SetFontSize = row[15]
                        str_PlayAlertSound = row[16]
                        str_SetBackgroundColor = row[17]
                        str_PlayEffect = row[18]
                        str_MinimapIcon = row[19]

                        if int(str_Tier) == i and str_category == "exped":
                            LineToWrite = LineToWrite + ' "' + str_BaseType + '"'
                            FontSizeToWrite = str_SetFontSize
                            BackgroundColorToWrite = str_SetBackgroundColor
                            AlertSoundToWrite = str_PlayAlertSound
                            EffectToWrite = str_PlayEffect
                            IconToWrite = str_MinimapIcon

            if LineToWrite != "":
                str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                write_obj.write("Show\n")
                write_obj.write("	Class Currency\n")
                write_obj.write("	BaseType "+LineToWrite+"\n")
                write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("	SetTextColor 0 0 0 255\n")
                write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("	MinimapIcon "+IconToWrite+"\n")

        write_obj.write("################################################################################\n")
        write_obj.write("##### Fucking GGG put the god damned Expedition Logbook into its own fucking class.\n")
        write_obj.write("\n")
        write_obj.write("Show\n")
        write_obj.write("	Class \"Expedition Logbook\"\n")
        write_obj.write("	SetFontSize 39\n")
        write_obj.write("	SetTextColor 0 0 0 255\n")
        write_obj.write("	SetBackgroundColor 25 25 255 235 # Blue\n")
        write_obj.write("	PlayAlertSound 8 300\n")
        write_obj.write("	PlayEffect Blue\n")
        write_obj.write("	MinimapIcon 0 Blue Pentagon\n")
        write_obj.write("################################################################################\n")
        write_obj.write("##### Catch all quest/veiled/enchanted/synthesized/fractured items.\n")
        write_obj.write("\n")
        write_obj.write("Show\n")
        write_obj.write("	Class Quest\n")
        write_obj.write("	SetFontSize 45\n")
        write_obj.write("	SetBackgroundColor 0 0 0 255 # White\n")
        write_obj.write("	PlayAlertSound 2 300\n")
        write_obj.write("	PlayEffect White\n")
        write_obj.write("	MinimapIcon 0 White Diamond\n")
        write_obj.write("Show\n")
        write_obj.write("	HasExplicitMod "" Veil""\n")
        write_obj.write("	SetFontSize 39\n")
        write_obj.write("	SetBackgroundColor 25 25 255 235 # Blue\n")
        write_obj.write("	PlayAlertSound 8 300\n")
        write_obj.write("	PlayEffect Blue\n")
        write_obj.write("	MinimapIcon 2 Blue Kite\n")
        write_obj.write("Show\n")
        write_obj.write("	AnyEnchantment True\n")
        write_obj.write("	SetFontSize 39\n")
        write_obj.write("	SetBackgroundColor 25 25 255 235 # Blue\n")
        write_obj.write("	PlayAlertSound 8 300\n")
        write_obj.write("	PlayEffect Blue\n")
        write_obj.write("	MinimapIcon 2 Blue Kite\n")
        write_obj.write("Show\n")
        write_obj.write("	SynthesisedItem True\n")
        write_obj.write("	SetFontSize 39\n")
        write_obj.write("	SetBackgroundColor 25 25 255 235 # Blue\n")
        write_obj.write("	PlayAlertSound 8 300\n")
        write_obj.write("	PlayEffect Blue\n")
        write_obj.write("	MinimapIcon 2 Blue Kite\n")
        write_obj.write("Show\n")
        write_obj.write("	FracturedItem True\n")
        write_obj.write("	SetFontSize 39\n")
        write_obj.write("	SetBackgroundColor 25 25 255 235 # Blue\n")
        write_obj.write("	PlayAlertSound 8 300\n")
        write_obj.write("	PlayEffect Blue\n")
        write_obj.write("	MinimapIcon 2 Blue Kite\n")

    print ("Other section complete.")

def func_watch():

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Watchstones - added from ""other"" csv file. \n")
        write_obj.write("##### poe.ninja does not list the basetype names so we can't automate this.\n")
        write_obj.write("#####\n")

        # ilvl81 items
        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            with open(strCSVinOther, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_category = row[0]
                        str_baseType = row[2]
                        str_levelRequired = row[6]
                        if row[14] != "":
                            str_Tier = row[14]
                        else:
                            str_Tier = row[13]
                        str_SetFontSize = row[15]
                        str_PlayAlertSound = row[16]
                        str_SetBackgroundColor = row[17]
                        str_PlayEffect = row[18]
                        str_MinimapIcon = row[19]

                        if int(str_Tier) == i and str_category == "watch":
                            LineToWrite = LineToWrite + ' "' + str_baseType + '"'
                            FontSizeToWrite = str_SetFontSize
                            BackgroundColorToWrite = str_SetBackgroundColor
                            AlertSoundToWrite = str_PlayAlertSound
                            EffectToWrite = str_PlayEffect
                            IconToWrite = str_MinimapIcon

            if LineToWrite != "":
                str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                write_obj.write("Show\n")
                write_obj.write("	BaseType "+LineToWrite+"\n")
                write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("	SetTextColor 0 0 0 255\n")
                write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("	MinimapIcon "+IconToWrite+"\n")

        # Last few Heist items
        write_obj.write("\n")
        write_obj.write("##### Not sure if this class includes the items above or separate items.\n")
        write_obj.write("##### Adding here just to be sure.\n")
        write_obj.write("Show\n")
        write_obj.write("	Class \"Atlas Region Upgrade Item\"\n")
        write_obj.write("	SetFontSize 39\n")
        write_obj.write("	SetTextColor 0 0 0 255\n")
        write_obj.write("	SetBackgroundColor 25 25 255 235 # Blue\n")
        write_obj.write("	PlayAlertSound 8 300\n")
        write_obj.write("	PlayEffect Blue\n")
        write_obj.write("	MinimapIcon 2 Blue Pentagon\n")

    print ("Watchstones section complete.")

def func_deli():

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Delirium Orbs\n")
        write_obj.write("#####\n")

        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_category = row[0]
                        str_name = row[1]
                        if row[14] != "":
                            str_Tier = row[14]
                        else:
                            str_Tier = row[13]
                        str_SetFontSize = row[15]
                        str_PlayAlertSound = row[16]
                        str_SetBackgroundColor = row[17]
                        str_PlayEffect = row[18]
                        str_MinimapIcon = row[19]

                        if int(str_Tier) == i and str_category == "deli":
                            LineToWrite = LineToWrite + ' "' + str_name + '"'
                            FontSizeToWrite = str_SetFontSize
                            BackgroundColorToWrite = str_SetBackgroundColor
                            AlertSoundToWrite = str_PlayAlertSound
                            EffectToWrite = str_PlayEffect
                            IconToWrite = str_MinimapIcon

            if LineToWrite != "":
                str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                write_obj.write("Show\n")
                write_obj.write("	Class Currency\n")
                write_obj.write("	BaseType =="+LineToWrite+"\n")
                write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("	SetTextColor 0 0 0 255\n")
                write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("	MinimapIcon "+IconToWrite+"\n")
    print ("Delirium Orb section complete.")

def func_inv():

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Invitations\n")
        write_obj.write("#####\n")

        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_category = row[0]
                        str_name = row[1]
                        if row[14] != "":
                            str_Tier = row[14]
                        else:
                            str_Tier = row[13]
                        str_SetFontSize = row[15]
                        str_PlayAlertSound = row[16]
                        str_SetBackgroundColor = row[17]
                        str_PlayEffect = row[18]
                        str_MinimapIcon = row[19]

                        if int(str_Tier) == i and str_category == "frag":
                            LineToWrite = LineToWrite + ' "' + str_name + '"'
                            FontSizeToWrite = str_SetFontSize
                            BackgroundColorToWrite = str_SetBackgroundColor
                            AlertSoundToWrite = str_PlayAlertSound
                            EffectToWrite = str_PlayEffect
                            IconToWrite = str_MinimapIcon

            if LineToWrite != "":
                str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                write_obj.write("Show\n")
                #write_obj.write("	Class Currency\n")
                write_obj.write("	BaseType =="+LineToWrite+"\n")
                write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("	SetTextColor 0 0 0 255\n")
                write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("	MinimapIcon "+IconToWrite+"\n")
    print ("Invitations section complete.")

def func_vial():

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Vials\n")
        write_obj.write("#####\n")

        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_category = row[0]
                        str_name = row[1]
                        if row[14] != "":
                            str_Tier = row[14]
                        else:
                            str_Tier = row[13]
                        str_SetFontSize = row[15]
                        str_PlayAlertSound = row[16]
                        str_SetBackgroundColor = row[17]
                        str_PlayEffect = row[18]
                        str_MinimapIcon = row[19]

                        if int(str_Tier) == i and str_category == "vial":
                            LineToWrite = LineToWrite + ' "' + str_name + '"'
                            FontSizeToWrite = str_SetFontSize
                            BackgroundColorToWrite = str_SetBackgroundColor
                            AlertSoundToWrite = str_PlayAlertSound
                            EffectToWrite = str_PlayEffect
                            IconToWrite = str_MinimapIcon

            if LineToWrite != "":
                str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                write_obj.write("Show\n")
                write_obj.write("	Class Currency\n")
                write_obj.write("	BaseType =="+LineToWrite+"\n")
                write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("	SetTextColor 0 0 0 255\n")
                write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("	MinimapIcon "+IconToWrite+"\n")
    print ("Vial section complete.")

def func_inc():

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Incubators\n")
        write_obj.write("#####\n")

        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_category = row[0]
                        str_name = row[1]
                        if row[14] != "":
                            str_Tier = row[14]
                        else:
                            str_Tier = row[13]
                        str_SetFontSize = row[15]
                        str_PlayAlertSound = row[16]
                        str_SetBackgroundColor = row[17]
                        str_PlayEffect = row[18]
                        str_MinimapIcon = row[19]

                        if int(str_Tier) == i and str_category == "inc":
                            LineToWrite = LineToWrite + ' "' + str_name + '"'
                            FontSizeToWrite = str_SetFontSize
                            BackgroundColorToWrite = str_SetBackgroundColor
                            AlertSoundToWrite = str_PlayAlertSound
                            EffectToWrite = str_PlayEffect
                            IconToWrite = str_MinimapIcon

            if LineToWrite != "":
                str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                write_obj.write("Show\n")
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                write_obj.write("	Class Incubator\n")
                write_obj.write("	BaseType =="+LineToWrite+"\n")
                write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("	SetTextColor 0 0 0 255\n")
                write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("	MinimapIcon "+IconToWrite+"\n")
    print ("Incubator section complete.")

def func_scar():

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Scarabs\n")
        write_obj.write("#####\n")

        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_category = row[0]
                        str_name = row[1]
                        if row[14] != "":
                            str_Tier = row[14]
                        else:
                            str_Tier = row[13]
                        str_SetFontSize = row[15]
                        str_PlayAlertSound = row[16]
                        str_SetBackgroundColor = row[17]
                        str_PlayEffect = row[18]
                        str_MinimapIcon = row[19]

                        if int(str_Tier) == i and str_category == "Map Fragments":
                            LineToWrite = LineToWrite + ' "' + str_name + '"'
                            FontSizeToWrite = str_SetFontSize
                            BackgroundColorToWrite = str_SetBackgroundColor
                            AlertSoundToWrite = str_PlayAlertSound
                            EffectToWrite = str_PlayEffect
                            IconToWrite = str_MinimapIcon

            if LineToWrite != "":
                str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                write_obj.write("Show\n")
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                #write_obj.write("	Class ""Map Fragments""\n")
                write_obj.write("	BaseType =="+LineToWrite+"\n")
                write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("	SetTextColor 0 0 0 255\n")
                write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("	MinimapIcon "+IconToWrite+"\n")
    print ("Scarab section complete.")

def func_foss():

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Fossils & Resonators\n")
        write_obj.write("#####\n")

        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_category = row[0]
                        str_name = row[1]
                        if row[14] != "":
                            str_Tier = row[14]
                        else:
                            str_Tier = row[13]
                        str_SetFontSize = row[15]
                        str_PlayAlertSound = row[16]
                        str_SetBackgroundColor = row[17]
                        str_PlayEffect = row[18]
                        str_MinimapIcon = row[19]

                        if int(str_Tier) == i and (str_category == "foss" or str_category == "Delve Stackable Socketable Currency"):
                            LineToWrite = LineToWrite + ' "' + str_name + '"'
                            FontSizeToWrite = str_SetFontSize
                            BackgroundColorToWrite = str_SetBackgroundColor
                            AlertSoundToWrite = str_PlayAlertSound
                            EffectToWrite = str_PlayEffect
                            IconToWrite = str_MinimapIcon

            if LineToWrite != "":
                str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                write_obj.write("Show\n")
                write_obj.write("	Class Stackable\n")
                write_obj.write("	BaseType =="+LineToWrite+"\n")
                write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("	SetTextColor 0 0 0 255\n")
                write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("	MinimapIcon "+IconToWrite+"\n")
    print ("Fossil & Resonator section complete.")

def func_ess():

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Essences\n")
        write_obj.write("#####\n")

        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_category = row[0]
                        str_name = row[1]
                        if row[14] != "":
                            str_Tier = row[14]
                        else:
                            str_Tier = row[13]
                        str_SetFontSize = row[15]
                        str_PlayAlertSound = row[16]
                        str_SetBackgroundColor = row[17]
                        str_PlayEffect = row[18]
                        str_MinimapIcon = row[19]

                        if int(str_Tier) == i and str_category == "ess":
                            LineToWrite = LineToWrite + ' "' + str_name + '"'
                            FontSizeToWrite = str_SetFontSize
                            BackgroundColorToWrite = str_SetBackgroundColor
                            AlertSoundToWrite = str_PlayAlertSound
                            EffectToWrite = str_PlayEffect
                            IconToWrite = str_MinimapIcon

            if LineToWrite != "":
                str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                write_obj.write("Show\n")
                write_obj.write("	Class Currency\n")
                write_obj.write("	BaseType =="+LineToWrite+"\n")
                write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("	SetTextColor 0 0 0 255\n")
                write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("	MinimapIcon "+IconToWrite+"\n")
    print ("Essences section complete.")

def func_div():

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Div Cards\n")
        write_obj.write("#####\n")

        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_category = row[0]
                        str_name = row[1]
                        if row[14] != "":
                            str_Tier = row[14]
                        else:
                            str_Tier = row[13]
                        str_SetFontSize = row[15]
                        str_PlayAlertSound = row[16]
                        str_SetBackgroundColor = row[17]
                        str_PlayEffect = row[18]
                        str_MinimapIcon = row[19]

                        if int(str_Tier) == i and str_category == "div":
                            LineToWrite = LineToWrite + ' "' + str_name + '"'
                            FontSizeToWrite = str_SetFontSize
                            BackgroundColorToWrite = str_SetBackgroundColor
                            AlertSoundToWrite = str_PlayAlertSound
                            EffectToWrite = str_PlayEffect
                            IconToWrite = str_MinimapIcon

            if LineToWrite != "":
                str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                write_obj.write("Show\n")
                write_obj.write("	Class Divination\n")
                write_obj.write("	BaseType =="+LineToWrite+"\n")
                write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("	SetTextColor 0 0 0 255\n")
                write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("	MinimapIcon "+IconToWrite+"\n")
    print ("Div Card section complete.")

def func_prop():

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Prophecies\n")
        write_obj.write("#####\n")

        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_category = row[0]
                        str_name = row[1]
                        if row[14] != "":
                            str_Tier = row[14]
                        else:
                            str_Tier = row[13]
                        str_SetFontSize = row[15]
                        str_PlayAlertSound = row[16]
                        str_SetBackgroundColor = row[17]
                        str_PlayEffect = row[18]
                        str_MinimapIcon = row[19]

                        # These are now drop-disabled but poe.ninja still tracks them.
                        if int(str_Tier) == i and str_category == "prop":
                            if "The Emperor's Trove" in str_name:
                                LineToWrite = ""
                            elif "A Gracious Master" in str_name:
                                LineToWrite = ""
                            elif "Ancient Rivalries I" in str_name:
                                LineToWrite = ""
                            elif "Echoes of Lost Love" in str_name:
                                LineToWrite = ""
                            elif "The Blacksmith" in str_name:
                                LineToWrite = ""
                            else:
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
            if LineToWrite != "":
                str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                write_obj.write("Show\n")
                write_obj.write("	BaseType ""Prophecy""\n")
                write_obj.write("	Prophecy "+LineToWrite+"\n")
                write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("	SetTextColor 0 0 0 255\n")
                write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("	MinimapIcon "+IconToWrite+"\n")
    print ("Prophecies section complete.")

def func_beast():

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Beasts\n")
        write_obj.write("#####\n")

        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_category = row[0]
                        str_name = row[1]
                        if row[14] != "":
                            str_Tier = row[14]
                        else:
                            str_Tier = row[13]
                        str_SetFontSize = row[15]
                        str_PlayAlertSound = row[16]
                        str_SetBackgroundColor = row[17]
                        str_PlayEffect = row[18]
                        str_MinimapIcon = row[19]

                        if int(str_Tier) == i and str_category == "beast":
                            LineToWrite = LineToWrite + ' "' + str_name + '"'
                            FontSizeToWrite = str_SetFontSize
                            BackgroundColorToWrite = str_SetBackgroundColor
                            AlertSoundToWrite = str_PlayAlertSound
                            EffectToWrite = str_PlayEffect
                            IconToWrite = str_MinimapIcon

            if LineToWrite != "":
                str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                write_obj.write("Show\n")
                write_obj.write("	BaseType =="+LineToWrite+"\n")
                write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("	SetTextColor 0 0 0 255\n")
                write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("	MinimapIcon "+IconToWrite+"\n")
    print ("Beasts section complete.")

def func_replica_umap():
    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Replica Maps\n")
        write_obj.write("#####\n")

        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        #print (row)
                        str_category = row[0]
                        str_baseType = row[2]
                        str_detailsId = row[5]
                        if row[14] != "":
                            str_Tier = row[14]
                        else:
                            str_Tier = row[13]
                        str_SetFontSize = row[15]
                        str_PlayAlertSound = row[16]
                        str_SetBackgroundColor = row[17]
                        str_PlayEffect = row[18]
                        str_MinimapIcon = row[19]

                        if str_category == "umap" and int(str_Tier) == i and ("replica" in str_detailsId):
                            LineToWrite = LineToWrite + ' "' + str_baseType + '"'
                            FontSizeToWrite = str_SetFontSize
                            BackgroundColorToWrite = str_SetBackgroundColor
                            AlertSoundToWrite = str_PlayAlertSound
                            EffectToWrite = str_PlayEffect
                            IconToWrite = str_MinimapIcon

            if LineToWrite != "":
                str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                write_obj.write("Show\n")
                #write_obj.write("	Class Maps\n")
                write_obj.write("	Replica True\n")
                write_obj.write("	BaseType =="+LineToWrite+"\n")
                write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("	SetTextColor 0 0 0 255\n")
                write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("	MinimapIcon "+IconToWrite+"\n")
    print ("Replica Maps section complete.")

def func_replica_ujew():
    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Replica Jewels\n")
        write_obj.write("#####\n")

        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        #print (row)
                        str_category = row[0]
                        str_baseType = row[2]
                        str_detailsId = row[5]
                        if row[14] != "":
                            str_Tier = row[14]
                        else:
                            str_Tier = row[13]
                        str_SetFontSize = row[15]
                        str_PlayAlertSound = row[16]
                        str_SetBackgroundColor = row[17]
                        str_PlayEffect = row[18]
                        str_MinimapIcon = row[19]

                        if str_category == "ujew" and int(str_Tier) == i and ("replica" in str_detailsId):
                            LineToWrite = LineToWrite + ' "' + str_baseType + '"'
                            FontSizeToWrite = str_SetFontSize
                            BackgroundColorToWrite = str_SetBackgroundColor
                            AlertSoundToWrite = str_PlayAlertSound
                            EffectToWrite = str_PlayEffect
                            IconToWrite = str_MinimapIcon

            if LineToWrite != "":
                str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                write_obj.write("Show\n")
                #write_obj.write("	Class Jewel\n")
                write_obj.write("	Replica True\n")
                write_obj.write("	BaseType =="+LineToWrite+"\n")
                write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("	SetTextColor 0 0 0 255\n")
                write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("	MinimapIcon "+IconToWrite+"\n")
    print ("Replica Jewels section complete.")

def func_replica_ufla():
    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Replica Flasks\n")
        write_obj.write("#####\n")

        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        #print (row)
                        str_category = row[0]
                        str_baseType = row[2]
                        str_detailsId = row[5]
                        if row[14] != "":
                            str_Tier = row[14]
                        else:
                            str_Tier = row[13]
                        str_SetFontSize = row[15]
                        str_PlayAlertSound = row[16]
                        str_SetBackgroundColor = row[17]
                        str_PlayEffect = row[18]
                        str_MinimapIcon = row[19]

                        if str_category == "ufla" and int(str_Tier) == i and ("replica" in str_detailsId):
                            LineToWrite = LineToWrite + ' "' + str_baseType + '"'
                            FontSizeToWrite = str_SetFontSize
                            BackgroundColorToWrite = str_SetBackgroundColor
                            AlertSoundToWrite = str_PlayAlertSound
                            EffectToWrite = str_PlayEffect
                            IconToWrite = str_MinimapIcon

            if LineToWrite != "":
                str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                write_obj.write("Show\n")
                #write_obj.write("	Class Flasks\n")
                write_obj.write("	Replica True\n")
                write_obj.write("	BaseType =="+LineToWrite+"\n")
                write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("	SetTextColor 0 0 0 255\n")
                write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("	MinimapIcon "+IconToWrite+"\n")
    print ("Replica Flasks section complete.")

def func_replica_uacc():
    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Replica Accessories\n")
        write_obj.write("#####\n")

        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        #print (row)
                        str_category = row[0]
                        str_baseType = row[2]
                        str_detailsId = row[5]
                        if row[14] != "":
                            str_Tier = row[14]
                        else:
                            str_Tier = row[13]
                        str_SetFontSize = row[15]
                        str_PlayAlertSound = row[16]
                        str_SetBackgroundColor = row[17]
                        str_PlayEffect = row[18]
                        str_MinimapIcon = row[19]

                        if str_category == "uacc" and int(str_Tier) == i and ("replica" in str_detailsId):
                            LineToWrite = LineToWrite + ' "' + str_baseType + '"'
                            FontSizeToWrite = str_SetFontSize
                            BackgroundColorToWrite = str_SetBackgroundColor
                            AlertSoundToWrite = str_PlayAlertSound
                            EffectToWrite = str_PlayEffect
                            IconToWrite = str_MinimapIcon

            if LineToWrite != "":
                str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                write_obj.write("Show\n")
                #write_obj.write("	Class Belts Rings Amulet\n")
                write_obj.write("	Replica True\n")
                write_obj.write("	BaseType =="+LineToWrite+"\n")
                write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("	SetTextColor 0 0 0 255\n")
                write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("	MinimapIcon "+IconToWrite+"\n")
    print ("Replica Accessories section complete.")

def func_normal_maps():

# Right now I don't think there's any way to get info from poe.ninja about influenced maps or blighted maps.
# Have posted a question to the dev forum, we'll see what they say.

# But setting aside elder/shaper/blight, we can use variant and mapTier to determine everything else.
# For each variant, for each maptier, for each economy tier means there will be an assload of sections.

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Normal Maps\n")
        write_obj.write("#####\n")

        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            for j in range (16):
                k = 16-j
                LineToWrite = ""
                #write_obj.write("j is "+str(j)+" and k is "+str(k)+" and i is "+str(i)+"+\n")
                print("##### Economy Tier "+str(i)+ " Map Tier "+str(k))

                with open(strCSVin, 'r') as read_obj:
                    # Create a csv.reader object from the input file object
                    csv_reader = reader(read_obj)
                    for row in csv_reader:
                        if row[12] != "chaosEquivalent":
                            str_category = row[0]
                            str_baseType = row[2]
                            str_variant = row[4]
                            str_detailsId = row[5]
                            str_mapTier = row[9]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]
                
                            if str_category == "map" and str_variant == "', Gen-11" and int(str_mapTier) == k and int(str_Tier) == i and ("replica" not in str_detailsId):
                                LineToWrite = LineToWrite + ' "' + str_baseType + '"'
                                MapTierToWrite = str_mapTier
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("\n")
                    write_obj.write("##### Economy Tier "+str(i)+ " Map Tier "+str(k)+"\n")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Maps\n")
                    write_obj.write("	Rarity Normal Magic Rare\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	MapTier >= "+MapTierToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")
                    write_obj.write("\n")
    print ("Normal Map section complete.")

def func_influenced_maps():

# Right now I don't think there's any way to get info fro poe.ninja about influenced maps.
# So we will hard-set these as Tier 4 for now.

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Influenced Maps\n")
        write_obj.write("#####\n")
        write_obj.write("\n")
        write_obj.write("Show\n")
        write_obj.write("	Class Maps\n")
        write_obj.write("	HasInfluence Shaper Elder\n")
        write_obj.write("	SetFontSize 39\n")
        write_obj.write("	SetTextColor 0 0 0 255\n")
        write_obj.write("	SetBackgroundColor 25 25 255 235 # Blue\n")
        write_obj.write("	PlayAlertSound 8 300\n")
        write_obj.write("	PlayEffect Blue\n")
        write_obj.write("	MinimapIcon 2 Blue Pentagon\n")

    print ("Influenced Map section complete.")

def func_blight_maps():

# Right now I don't think there's any way to get info fro poe.ninja about influenced maps or blighted maps.
# Have posted a question to the dev forum, we'll see what they say.

# But setting aside elder/shaper/blight, we can use variant and mapTier to determine everything else.
# For each variant, for each maptier, for each economy tier means there will be 160 sections x number of leagues

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Blight Maps\n")
        write_obj.write("#####\n")

        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_category = row[0]
                        str_baseType = row[2]
                        str_detailsId = row[5]
                        if row[14] != "":
                            str_Tier = row[14]
                        else:
                            str_Tier = row[13]
                        str_SetFontSize = row[15]
                        str_PlayAlertSound = row[16]
                        str_SetBackgroundColor = row[17]
                        str_PlayEffect = row[18]
                        str_MinimapIcon = row[19]

                        if int(str_Tier) == i and (str_category == "blight" and "replica" not in str_detailsId):
                            str_baseType = str_baseType.replace("Blighted ", "")
                            LineToWrite = LineToWrite + ' "' + str_baseType + '"'
                            FontSizeToWrite = str_SetFontSize
                            BackgroundColorToWrite = str_SetBackgroundColor
                            AlertSoundToWrite = str_PlayAlertSound
                            EffectToWrite = str_PlayEffect
                            IconToWrite = str_MinimapIcon

            if LineToWrite != "":
                str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                write_obj.write("Show\n")
                write_obj.write("	Class Maps\n")
                write_obj.write("	BlightedMap True\n")
                write_obj.write("	BaseType =="+LineToWrite+"\n")
                write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("	SetTextColor 0 0 0 255\n")
                write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("	MinimapIcon "+IconToWrite+"\n")
                write_obj.write("\n")
    print ("Blight Map section complete.")

def func_umaps():

# Right now I don't think there's any way to get info fro poe.ninja about influenced maps or blighted maps.
# Have posted a question to the dev forum, we'll see what they say.

# But setting aside elder/shaper/blight, we can use variant and mapTier to determine everything else.
# For each variant, for each maptier, for each economy tier means there will be 160 sections x number of leagues

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Unique Maps\n")
        write_obj.write("#####\n")

        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_category = row[0]
                        str_baseType = row[2]
                        str_detailsId = row[5]
                        str_mapTier = row[9]
                        if row[14] != "":
                            str_Tier = row[14]
                        else:
                            str_Tier = row[13]
                        str_SetFontSize = row[15]
                        str_PlayAlertSound = row[16]
                        str_SetBackgroundColor = row[17]
                        str_PlayEffect = row[18]
                        str_MinimapIcon = row[19]

                        if int(str_Tier) == i and str_category == "umap" and "replica" not in str_detailsId:
                            LineToWrite = LineToWrite + ' "' + str_baseType + '"'
                            FontSizeToWrite = str_SetFontSize
                            BackgroundColorToWrite = str_SetBackgroundColor
                            AlertSoundToWrite = str_PlayAlertSound
                            EffectToWrite = str_PlayEffect
                            IconToWrite = str_MinimapIcon

            if LineToWrite != "":
                str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                write_obj.write("Show\n")
                write_obj.write("	Class Maps\n")
                write_obj.write("	Rarity Unique\n")
                write_obj.write("	BaseType =="+LineToWrite+"\n")
                write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("	SetTextColor 0 0 0 255\n")
                write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("	MinimapIcon "+IconToWrite+"\n")
                write_obj.write("\n")
    print ("Unique Map section complete.")

def func_ujew():

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Unique Jewels\n")
        write_obj.write("#####\n")

        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_category = row[0]
                        str_baseType = row[2]
                        str_detailsId = row[5]
                        if row[14] != "":
                            str_Tier = row[14]
                        else:
                            str_Tier = row[13]
                        str_SetFontSize = row[15]
                        str_PlayAlertSound = row[16]
                        str_SetBackgroundColor = row[17]
                        str_PlayEffect = row[18]
                        str_MinimapIcon = row[19]

                        if int(str_Tier) == i and str_category == "ujew" and ("replica" not in str_detailsId):
                            LineToWrite = LineToWrite + ' "' + str_baseType + '"'
                            FontSizeToWrite = str_SetFontSize
                            BackgroundColorToWrite = str_SetBackgroundColor
                            AlertSoundToWrite = str_PlayAlertSound
                            EffectToWrite = str_PlayEffect
                            IconToWrite = str_MinimapIcon

            if LineToWrite != "":
                str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                write_obj.write("Show\n")
                #write_obj.write("	Class Jewel\n")
                write_obj.write("	Rarity Unique\n")
                write_obj.write("	BaseType =="+LineToWrite+"\n")
                write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("	SetTextColor 0 0 0 255\n")
                write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("	MinimapIcon "+IconToWrite+"\n")
    print ("Unique Jewel section complete.")

def func_ufla():

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Unique Flasks\n")
        write_obj.write("#####\n")

        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_category = row[0]
                        str_baseType = row[2]
                        str_detailsId = row[5]
                        if row[14] != "":
                            str_Tier = row[14]
                        else:
                            str_Tier = row[13]
                        str_SetFontSize = row[15]
                        str_PlayAlertSound = row[16]
                        str_SetBackgroundColor = row[17]
                        str_PlayEffect = row[18]
                        str_MinimapIcon = row[19]

                        if int(str_Tier) == i and str_category == "ufla" and ("replica" not in str_detailsId):
                            LineToWrite = LineToWrite + ' "' + str_baseType + '"'
                            FontSizeToWrite = str_SetFontSize
                            BackgroundColorToWrite = str_SetBackgroundColor
                            AlertSoundToWrite = str_PlayAlertSound
                            EffectToWrite = str_PlayEffect
                            IconToWrite = str_MinimapIcon

            if LineToWrite != "":
                str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                write_obj.write("Show\n")
                #write_obj.write("	Class Flasks\n")
                write_obj.write("	Rarity Unique\n")
                write_obj.write("	BaseType =="+LineToWrite+"\n")
                write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("	SetTextColor 0 0 0 255\n")
                write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("	MinimapIcon "+IconToWrite+"\n")
    print ("Unique Flask section complete.")

def func_uacc():

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Unique Accessories\n")
        write_obj.write("#####\n")

        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_category = row[0]
                        str_baseType = row[2]
                        str_detailsId = row[5]
                        if row[14] != "":
                            str_Tier = row[14]
                        else:
                            str_Tier = row[13]
                        str_SetFontSize = row[15]
                        str_PlayAlertSound = row[16]
                        str_SetBackgroundColor = row[17]
                        str_PlayEffect = row[18]
                        str_MinimapIcon = row[19]

                        if int(str_Tier) == i and str_category == "uacc" and ("replica" not in str_detailsId):
                            LineToWrite = LineToWrite + ' "' + str_baseType + '"'
                            FontSizeToWrite = str_SetFontSize
                            BackgroundColorToWrite = str_SetBackgroundColor
                            AlertSoundToWrite = str_PlayAlertSound
                            EffectToWrite = str_PlayEffect
                            IconToWrite = str_MinimapIcon

            if LineToWrite != "":
                str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                write_obj.write("Show\n")
                #write_obj.write("	Class Belts Rings Amulet\n")
                write_obj.write("	Rarity Unique\n")
                write_obj.write("	BaseType =="+LineToWrite+"\n")
                write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("	SetTextColor 0 0 0 255\n")
                write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("	MinimapIcon "+IconToWrite+"\n")
    print ("Unique Accessories section complete.")

def func_ench():

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Helment Enchants\n")
        write_obj.write("#####\n")

        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_category = row[0]
                        str_name = row[1]
                        if row[14] != "":
                            str_Tier = row[14]
                        else:
                            str_Tier = row[13]
                        str_SetFontSize = row[15]
                        str_PlayAlertSound = row[16]
                        str_SetBackgroundColor = row[17]
                        str_PlayEffect = row[18]
                        str_MinimapIcon = row[19]

                        if int(str_Tier) == i and str_category == "ench":
                            LineToWrite = LineToWrite + ' "' + str_name + '"'
                            FontSizeToWrite = str_SetFontSize
                            BackgroundColorToWrite = str_SetBackgroundColor
                            AlertSoundToWrite = str_PlayAlertSound
                            EffectToWrite = str_PlayEffect
                            IconToWrite = str_MinimapIcon

            if LineToWrite != "":
                str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                write_obj.write("Show\n")
                #write_obj.write("	Class Helm\n")
                write_obj.write("	HasEnchantment =="+LineToWrite+"\n")
                write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("	SetTextColor 0 0 0 255\n")
                write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("	MinimapIcon "+IconToWrite+"\n")
    print ("Helmet Enchants section complete.")

def func_normal_gems():

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Normal Gems (new GemQualityType ""Superior"" means normal)\n")
        write_obj.write("#####\n")

        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            write_obj.write("\n")
            write_obj.write("##### Tier "+str(i)+"\n")
            print ("Working on Gems - Tier "+str(i))

            # 21/23c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'21/23c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "gem":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("	GemLevel >= 21\n")
                    write_obj.write("	Quality >= 23\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 20/23c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'20/23c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "gem":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("	GemLevel >= 20\n")
                    write_obj.write("	Quality >= 23\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 6/23c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'6/23c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "gem":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("	GemLevel >= 6\n")
                    write_obj.write("	Quality >= 23\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 21/20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'21/20c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "gem":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("	GemLevel >= 21\n")
                    write_obj.write("	Quality >= 20\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 20/20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'20/20c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "gem":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("	GemLevel >= 20\n")
                    write_obj.write("	Quality >= 20\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 6/20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'6/20c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "gem":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("	GemLevel >= 6\n")
                    write_obj.write("	Quality >= 20\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 5/20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'5/20c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "gem":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("	GemLevel >= 5\n")
                    write_obj.write("	Quality >= 20\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 21c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'21c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "gem":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("	GemLevel >= 21\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'20c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "gem":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("	GemLevel >= 20\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 7c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'7c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "gem":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("	GemLevel >= 7\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 6c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'6c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "gem":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("	GemLevel >= 6\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 4c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'4c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "gem":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("	GemLevel >= 4\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 3c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'3c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "gem":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("	GemLevel >= 3\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 2c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'2c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "gem":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("	GemLevel >= 2\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 1c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'1c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "gem":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("	GemLevel >= 1\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 5/20
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'5/20":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "gem":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	Corrupted False\n")
                    write_obj.write("	GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("	GemLevel >= 5\n")
                    write_obj.write("	Quality >= 20\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 1/20
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'1/20":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "gem":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	Corrupted False\n")
                    write_obj.write("	GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("	GemLevel >= 1\n")
                    write_obj.write("	Quality >= 20\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 20
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'20":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "gem":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	Corrupted False\n")
                    write_obj.write("	GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("	GemLevel >= 20\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 6
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'6":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "gem":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	Corrupted False\n")
                    write_obj.write("	GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("	GemLevel >= 6\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 3
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'3":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "gem":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	Corrupted False\n")
                    write_obj.write("	GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("	GemLevel >= 3\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 2
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'2":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "gem":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	Corrupted False\n")
                    write_obj.write("	GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("	GemLevel >= 2\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 1
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'1":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "gem":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	Corrupted False\n")
                    write_obj.write("	GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("	GemLevel >= 1\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

    print ("Normal Gems section complete.")

def func_divergent_gems():

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Divergent Gems\n")
        write_obj.write("#####\n")

        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            write_obj.write("\n")
            write_obj.write("##### Tier "+str(i)+"\n")
            print ("Working on Gems - Tier "+str(i))

            # 21/23c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'21/23c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "divergent":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Divergent\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 21\n")
                    write_obj.write("	Quality >= 23\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 20/23c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'20/23c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "divergent":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Divergent\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 20\n")
                    write_obj.write("	Quality >= 23\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 6/23c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'6/23c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "divergent":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Divergent\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 6\n")
                    write_obj.write("	Quality >= 23\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 21/20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'21/20c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "divergent":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Divergent\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 21\n")
                    write_obj.write("	Quality >= 20\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 20/20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'20/20c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "divergent":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Divergent\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 20\n")
                    write_obj.write("	Quality >= 20\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 6/20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'6/20c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "divergent":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Divergent\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 6\n")
                    write_obj.write("	Quality >= 20\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 5/20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'5/20c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "divergent":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Divergent\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 5\n")
                    write_obj.write("	Quality >= 20\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 21c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'21c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "divergent":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Divergent\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 21\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'20c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "divergent":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Divergent\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 20\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 7c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'7c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "divergent":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Divergent\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 7\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 6c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'6c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "divergent":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Divergent\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 6\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 4c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'4c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "divergent":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Divergent\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 4\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 3c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'3c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "divergent":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Divergent\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 3\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 2c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'2c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "divergent":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Divergent\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 2\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 1c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'1c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "divergent":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Divergent\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 1\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 5/20
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'5/20":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "divergent":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Divergent\n")
                    write_obj.write("	Corrupted False\n")
                    write_obj.write("	GemLevel >= 5\n")
                    write_obj.write("	Quality >= 20\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 1/20
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'1/20":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "divergent":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Divergent\n")
                    write_obj.write("	Corrupted False\n")
                    write_obj.write("	GemLevel >= 1\n")
                    write_obj.write("	Quality >= 20\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 20
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'20":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "divergent":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Divergent\n")
                    write_obj.write("	Corrupted False\n")
                    write_obj.write("	GemLevel >= 20\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 6
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'6":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "divergent":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Divergent\n")
                    write_obj.write("	Corrupted False\n")
                    write_obj.write("	GemLevel >= 6\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 3
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'3":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "divergent":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Divergent\n")
                    write_obj.write("	Corrupted False\n")
                    write_obj.write("	GemLevel >= 3\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 2
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'2":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "divergent":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Divergent\n")
                    write_obj.write("	Corrupted False\n")
                    write_obj.write("	GemLevel >= 2\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 1
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'1":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "divergent":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Divergent\n")
                    write_obj.write("	Corrupted False\n")
                    write_obj.write("	GemLevel >= 1\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

    print ("Divergent Gems section complete.")

def func_anomalous_gems():

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Anomalous Gems\n")
        write_obj.write("#####\n")

        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            write_obj.write("\n")
            write_obj.write("##### Tier "+str(i)+"\n")
            print ("Working on Gems - Tier "+str(i))

            # 21/23c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'21/23c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "anomalous":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Anomalous\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 21\n")
                    write_obj.write("	Quality >= 23\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 20/23c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'20/23c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "anomalous":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Anomalous\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 20\n")
                    write_obj.write("	Quality >= 23\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 6/23c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'6/23c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "anomalous":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Anomalous\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 6\n")
                    write_obj.write("	Quality >= 23\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 21/20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'21/20c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "anomalous":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Anomalous\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 21\n")
                    write_obj.write("	Quality >= 20\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 20/20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'20/20c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "anomalous":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Anomalous\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 20\n")
                    write_obj.write("	Quality >= 20\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 6/20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'6/20c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "anomalous":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Anomalous\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 6\n")
                    write_obj.write("	Quality >= 20\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 5/20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'5/20c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "anomalous":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Anomalous\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 5\n")
                    write_obj.write("	Quality >= 20\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 21c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'21c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "anomalous":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Anomalous\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 21\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'20c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "anomalous":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Anomalous\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 20\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 7c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'7c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "anomalous":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Anomalous\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 7\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 6c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'6c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "anomalous":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Anomalous\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 6\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 4c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'4c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "anomalous":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Anomalous\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 4\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 3c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'3c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "anomalous":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Anomalous\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 3\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 2c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'2c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "anomalous":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Anomalous\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 2\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 1c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'1c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "anomalous":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Anomalous\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 1\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 5/20
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'5/20":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "anomalous":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Anomalous\n")
                    write_obj.write("	Corrupted False\n")
                    write_obj.write("	GemLevel >= 5\n")
                    write_obj.write("	Quality >= 20\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 1/20
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'1/20":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "anomalous":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Anomalous\n")
                    write_obj.write("	Corrupted False\n")
                    write_obj.write("	GemLevel >= 1\n")
                    write_obj.write("	Quality >= 20\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 20
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'20":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "anomalous":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Anomalous\n")
                    write_obj.write("	Corrupted False\n")
                    write_obj.write("	GemLevel >= 20\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 6
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'6":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "anomalous":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Anomalous\n")
                    write_obj.write("	Corrupted False\n")
                    write_obj.write("	GemLevel >= 6\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 3
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'3":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "anomalous":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Anomalous\n")
                    write_obj.write("	Corrupted False\n")
                    write_obj.write("	GemLevel >= 3\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 2
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'2":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "anomalous":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Anomalous\n")
                    write_obj.write("	Corrupted False\n")
                    write_obj.write("	GemLevel >= 2\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 1
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'1":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "anomalous":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Anomalous\n")
                    write_obj.write("	Corrupted False\n")
                    write_obj.write("	GemLevel >= 1\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

    print ("Anomalous Gems section complete.")

def func_phantasmal_gems():

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Phantasmal Gems\n")
        write_obj.write("#####\n")

        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            write_obj.write("\n")
            write_obj.write("##### Tier "+str(i)+"\n")
            print ("Working on Gems - Tier "+str(i))

            # 21/23c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'21/23c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "phantasmal":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Phantasmal\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 21\n")
                    write_obj.write("	Quality >= 23\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 20/23c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'20/23c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "phantasmal":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Phantasmal\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 20\n")
                    write_obj.write("	Quality >= 23\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 6/23c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'6/23c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "phantasmal":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Phantasmal\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 6\n")
                    write_obj.write("	Quality >= 23\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 21/20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'21/20c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "phantasmal":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Phantasmal\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 21\n")
                    write_obj.write("	Quality >= 20\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 20/20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'20/20c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "phantasmal":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Phantasmal\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 20\n")
                    write_obj.write("	Quality >= 20\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 6/20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'6/20c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "phantasmal":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Phantasmal\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 6\n")
                    write_obj.write("	Quality >= 20\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 5/20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'5/20c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "phantasmal":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Phantasmal\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 5\n")
                    write_obj.write("	Quality >= 20\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 21c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'21c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "phantasmal":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Phantasmal\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 21\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'20c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "phantasmal":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Phantasmal\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 20\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 7c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'7c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "phantasmal":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Phantasmal\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 7\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 6c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'6c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "phantasmal":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Phantasmal\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 6\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 4c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'4c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "phantasmal":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Phantasmal\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 4\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 3c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'3c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "phantasmal":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Phantasmal\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 3\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 2c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'2c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "phantasmal":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Phantasmal\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 2\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 1c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'1c":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "phantasmal":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Phantasmal\n")
                    write_obj.write("	Corrupted True\n")
                    write_obj.write("	GemLevel >= 1\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 5/20
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'5/20":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "phantasmal":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Phantasmal\n")
                    write_obj.write("	Corrupted False\n")
                    write_obj.write("	GemLevel >= 5\n")
                    write_obj.write("	Quality >= 20\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 1/20
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'1/20":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "phantasmal":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Phantasmal\n")
                    write_obj.write("	Corrupted False\n")
                    write_obj.write("	GemLevel >= 1\n")
                    write_obj.write("	Quality >= 20\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 20
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'20":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "phantasmal":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Phantasmal\n")
                    write_obj.write("	Corrupted False\n")
                    write_obj.write("	GemLevel >= 20\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 6
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'6":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "phantasmal":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Phantasmal\n")
                    write_obj.write("	Corrupted False\n")
                    write_obj.write("	GemLevel >= 6\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 3
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'3":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "phantasmal":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Phantasmal\n")
                    write_obj.write("	Corrupted False\n")
                    write_obj.write("	GemLevel >= 3\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 2
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'2":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "phantasmal":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Phantasmal\n")
                    write_obj.write("	Corrupted False\n")
                    write_obj.write("	GemLevel >= 2\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

            # 1
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_variant = row[4]
                        if str_variant == "'1":
                            str_category = row[0]
                            str_name = row[1]
                            str_variant = row[4]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]

                            if int(str_Tier) == i and str_category == "phantasmal":
                                LineToWrite = LineToWrite + ' "' + str_name + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("Show\n")
                    write_obj.write("	Class Gems\n")
                    write_obj.write("	GemQualityType Phantasmal\n")
                    write_obj.write("	Corrupted False\n")
                    write_obj.write("	GemLevel >= 1\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

    print ("Phantasmal Gems section complete.")

def func_uweap_6():
    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("###########################################################################\n")
        write_obj.write("##### 6L Unique Weapons\n")
        write_obj.write("#####\n")

        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_category = row[0]
                        str_baseType = row[2]
                        str_links = row[7]
                        if row[14] != "":
                            str_Tier = row[14]
                        else:
                            str_Tier = row[13]
                        str_SetFontSize = row[15]
                        str_PlayAlertSound = row[16]
                        str_SetBackgroundColor = row[17]
                        str_PlayEffect = row[18]
                        str_MinimapIcon = row[19]

                        if int(str_Tier) == i and str_category == "uweap" and str_links == "6":
                            LineToWrite = LineToWrite + ' "' + str_baseType + '"'
                            FontSizeToWrite = str_SetFontSize
                            BackgroundColorToWrite = str_SetBackgroundColor
                            AlertSoundToWrite = str_PlayAlertSound
                            EffectToWrite = str_PlayEffect
                            IconToWrite = str_MinimapIcon

            if LineToWrite != "":
                str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                write_obj.write("Show\n")
                write_obj.write("	Rarity Unique\n")
                write_obj.write("	Sockets = 6\n")
                write_obj.write("	BaseType =="+LineToWrite+"\n")
                write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("	SetTextColor 0 0 0 255\n")
                write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("	MinimapIcon "+IconToWrite+"\n")
    print ("6L Unique Weapon section complete.")

def func_uweap_5():
    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("###########################################################################\n")
        write_obj.write("##### 5L Unique Weapons\n")
        write_obj.write("#####\n")

        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_category = row[0]
                        str_baseType = row[2]
                        str_links = row[7]
                        if row[14] != "":
                            str_Tier = row[14]
                        else:
                            str_Tier = row[13]
                        str_SetFontSize = row[15]
                        str_PlayAlertSound = row[16]
                        str_SetBackgroundColor = row[17]
                        str_PlayEffect = row[18]
                        str_MinimapIcon = row[19]

                        if int(str_Tier) == i and str_category == "uweap" and str_links == "5":
                            LineToWrite = LineToWrite + ' "' + str_baseType + '"'
                            FontSizeToWrite = str_SetFontSize
                            BackgroundColorToWrite = str_SetBackgroundColor
                            AlertSoundToWrite = str_PlayAlertSound
                            EffectToWrite = str_PlayEffect
                            IconToWrite = str_MinimapIcon

            if LineToWrite != "":
                str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                write_obj.write("Show\n")
                write_obj.write("	Rarity Unique\n")
                write_obj.write("	Sockets = 5\n")
                write_obj.write("	BaseType =="+LineToWrite+"\n")
                write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("	SetTextColor 0 0 0 255\n")
                write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("	MinimapIcon "+IconToWrite+"\n")
    print ("5L Unique Weapon section complete.")

def func_uweap_0():
    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("###########################################################################\n")
        write_obj.write("##### All Other Unique Weapons\n")
        write_obj.write("#####\n")

        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_category = row[0]
                        str_baseType = row[2]
                        str_links = row[7]
                        if row[14] != "":
                            str_Tier = row[14]
                        else:
                            str_Tier = row[13]
                        str_SetFontSize = row[15]
                        str_PlayAlertSound = row[16]
                        str_SetBackgroundColor = row[17]
                        str_PlayEffect = row[18]
                        str_MinimapIcon = row[19]

                        if int(str_Tier) == i and str_category == "uweap" and str_links == "":
                            LineToWrite = LineToWrite + ' "' + str_baseType + '"'
                            FontSizeToWrite = str_SetFontSize
                            BackgroundColorToWrite = str_SetBackgroundColor
                            AlertSoundToWrite = str_PlayAlertSound
                            EffectToWrite = str_PlayEffect
                            IconToWrite = str_MinimapIcon

            if LineToWrite != "":
                str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                write_obj.write("Show\n")
                write_obj.write("	Rarity Unique\n")
                write_obj.write("	BaseType =="+LineToWrite+"\n")
                write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("	SetTextColor 0 0 0 255\n")
                write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("	MinimapIcon "+IconToWrite+"\n")
    print ("All Other Unique Weapon section complete.")

def func_uarm_6():
    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("###########################################################################\n")
        write_obj.write("##### 6L Unique Armor\n")
        write_obj.write("#####\n")

        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_category = row[0]
                        str_baseType = row[2]
                        str_links = row[7]
                        if row[14] != "":
                            str_Tier = row[14]
                        else:
                            str_Tier = row[13]
                        str_SetFontSize = row[15]
                        str_PlayAlertSound = row[16]
                        str_SetBackgroundColor = row[17]
                        str_PlayEffect = row[18]
                        str_MinimapIcon = row[19]

                        if int(str_Tier) == i and str_category == "uarm" and str_links == "6":
                            LineToWrite = LineToWrite + ' "' + str_baseType + '"'
                            FontSizeToWrite = str_SetFontSize
                            BackgroundColorToWrite = str_SetBackgroundColor
                            AlertSoundToWrite = str_PlayAlertSound
                            EffectToWrite = str_PlayEffect
                            IconToWrite = str_MinimapIcon

            if LineToWrite != "":
                str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                write_obj.write("Show\n")
                write_obj.write("	Rarity Unique\n")
                write_obj.write("	Sockets = 6\n")
                write_obj.write("	BaseType =="+LineToWrite+"\n")
                write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("	SetTextColor 0 0 0 255\n")
                write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("	MinimapIcon "+IconToWrite+"\n")
    print ("6L Unique Armor section complete.")

def func_uarm_5():
    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("###########################################################################\n")
        write_obj.write("##### 5L Unique Armor\n")
        write_obj.write("#####\n")

        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_category = row[0]
                        str_baseType = row[2]
                        str_links = row[7]
                        if row[14] != "":
                            str_Tier = row[14]
                        else:
                            str_Tier = row[13]
                        str_SetFontSize = row[15]
                        str_PlayAlertSound = row[16]
                        str_SetBackgroundColor = row[17]
                        str_PlayEffect = row[18]
                        str_MinimapIcon = row[19]

                        if int(str_Tier) == i and str_category == "uarm" and str_links == "5":
                            LineToWrite = LineToWrite + ' "' + str_baseType + '"'
                            FontSizeToWrite = str_SetFontSize
                            BackgroundColorToWrite = str_SetBackgroundColor
                            AlertSoundToWrite = str_PlayAlertSound
                            EffectToWrite = str_PlayEffect
                            IconToWrite = str_MinimapIcon

            if LineToWrite != "":
                str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                write_obj.write("Show\n")
                write_obj.write("	Rarity Unique\n")
                write_obj.write("	Sockets = 5\n")
                write_obj.write("	BaseType =="+LineToWrite+"\n")
                write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("	SetTextColor 0 0 0 255\n")
                write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("	MinimapIcon "+IconToWrite+"\n")

    print ("5L Unique Armor section complete.")

def func_uarm_0():
    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("###########################################################################\n")
        write_obj.write("##### All Other Unique Armor\n")
        write_obj.write("#####\n")

        for i in range (1,12):
            print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
            if (booShowT11 == False) and (i > strOverallStrictness):
                continue
            if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                continue
            print ("Building data for tier " + str(i) + ".")

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[12] != "chaosEquivalent":
                        str_category = row[0]
                        str_baseType = row[2]
                        str_links = row[7]
                        if row[14] != "":
                            str_Tier = row[14]
                        else:
                            str_Tier = row[13]
                        str_SetFontSize = row[15]
                        str_PlayAlertSound = row[16]
                        str_SetBackgroundColor = row[17]
                        str_PlayEffect = row[18]
                        str_MinimapIcon = row[19]

                        if int(str_Tier) == i and str_category == "uarm" and str_links == "":
                            LineToWrite = LineToWrite + ' "' + str_baseType + '"'
                            FontSizeToWrite = str_SetFontSize
                            BackgroundColorToWrite = str_SetBackgroundColor
                            AlertSoundToWrite = str_PlayAlertSound
                            EffectToWrite = str_PlayEffect
                            IconToWrite = str_MinimapIcon

            if LineToWrite != "":
                str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                write_obj.write("Show\n")
                write_obj.write("	Rarity Unique\n")
                write_obj.write("	BaseType =="+LineToWrite+"\n")
                write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("	SetTextColor 0 0 0 255\n")
                write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("	MinimapIcon "+IconToWrite+"\n")

    print ("All Other Unique Armor section complete.")

def func_influenced():
    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Influenced items\n")
        write_obj.write("#####\n")

        for k in range (86, 81, -1):
            print("Item level "+str(k))
            for strInfluence in arrInfluences:
                print("Influence "+strInfluence)
                for i in range (1,12):
                    print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
                    if (booShowT11 == False) and (i > strOverallStrictness):
                        continue
                    if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                        continue
                    print ("Building data for tier " + str(i) + ".")

                    LineToWrite = ""
                    with open(strCSVin, 'r') as read_obj:
                        # Create a csv.reader object from the input file object
                        csv_reader = reader(read_obj)
                        for row in csv_reader:
                            if row[0] == "base":
                                #print(row)
                                str_category = row[0]
                                str_baseType = row[2]
                                str_variant = row[4]
                                str_variant = str_variant.replace("'", "")
                                str_levelRequired = row[6]
                                str_links = row[7]
                                if row[14] != "":
                                    str_Tier = row[14]
                                else:
                                    str_Tier = row[13]
                                str_SetFontSize = row[15]
                                str_PlayAlertSound = row[16]
                                str_SetBackgroundColor = row[17]
                                str_PlayEffect = row[18]
                                str_MinimapIcon = row[19]
                                #print(str(k)+" "+str_levelRequired+" "+str(i)+" "+str_Tier)
                                #write_obj.write("##### Item level "+str(k)+", Influence "+strInfluence+", Tier "+str(i)+"\n")
                                #write_obj.write(str_baseType+" "+str_chaosEquivalent+" "+str_Tier+"\n")

                                if int(str_levelRequired) == k and int(str_Tier) == i and str_variant == strInfluence:
                                    LineToWrite = LineToWrite + ' "' + str_baseType + '"'
                                    FontSizeToWrite = str_SetFontSize
                                    BackgroundColorToWrite = str_SetBackgroundColor
                                    AlertSoundToWrite = str_PlayAlertSound
                                    EffectToWrite = str_PlayEffect
                                    IconToWrite = str_MinimapIcon
        
                    if LineToWrite != "":
                        str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                        str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                        str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                        strInfluence = strInfluence.replace("'", "")
                        write_obj.write("\n")
                        write_obj.write("##### Item level "+str(k)+", Influence "+strInfluence+", Tier "+str(i)+"\n")
                        write_obj.write("Show\n")
                        write_obj.write("	HasInfluence == "+strInfluence+"\n")
                        write_obj.write("	ItemLevel >= "+str(k)+"\n")
                        write_obj.write("	BaseType =="+LineToWrite+"\n")
                        write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                        write_obj.write("	SetTextColor 0 0 0 255\n")
                        write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                        if str_PlayAlertSound != "":
                            write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                        if EffectToWrite != "":
                            write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                        if IconToWrite != "":
                            write_obj.write("	MinimapIcon "+IconToWrite+"\n")

        # All other influenced items caught here
        write_obj.write("\n")
        write_obj.write("	Show\n")
        write_obj.write("		HasInfluence Shaper Elder Crusader Redeemer Hunter Warlord\n")
        write_obj.write("		SetFontSize 39\n")
        write_obj.write("		SetBackgroundColor 28 236 4 215 # Green\n")
        write_obj.write("		PlayAlertSound 9 300\n")
        write_obj.write("		MinimapIcon 2 Green Kite\n")

    print ("Influenced section complete.")

def func_non_influenced():
    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Non-influenced bases\n")
        write_obj.write("#####\n")

        for k in range (86, 81, -1):
            LineToWrite = ""
            print("Item level "+str(k))
            for i in range (1,12):
                print ("Strictness filter is " + str(strOverallStrictness) + " and i is " + str(i))
                if (booShowT11 == False) and (i > strOverallStrictness):
                    continue
                if (booShowT11 == True) and (i < 11) and (i > strOverallStrictness):
                    continue
                print ("Building data for tier " + str(i) + ".")

                LineToWrite = ""
                with open(strCSVin, 'r') as read_obj:
                    # Create a csv.reader object from the input file object
                    csv_reader = reader(read_obj)
                    for row in csv_reader:
                        if row[0] == "base":
                            #print(row)
                            str_category = row[0]
                            str_baseType = row[2]
                            str_variant = row[4]
                            str_levelRequired = row[6]
                            str_links = row[7]
                            if row[14] != "":
                                str_Tier = row[14]
                            else:
                                str_Tier = row[13]
                            str_SetFontSize = row[15]
                            str_PlayAlertSound = row[16]
                            str_SetBackgroundColor = row[17]
                            str_PlayEffect = row[18]
                            str_MinimapIcon = row[19]
                            #print(str(k)+" "+str_levelRequired+" "+str(i)+" "+str_Tier)
                            #write_obj.write("##### Item level "+str(k)+", Influence "+strInfluence+", Tier "+str(i)+"\n")
                            #write_obj.write(str_baseType+" "+str_chaosEquivalent+" "+str_Tier+"\n")

                            if int(str_levelRequired) == k and int(str_Tier) == i and str_variant == "":
                                LineToWrite = LineToWrite + ' "' + str_baseType + '"'
                                FontSizeToWrite = str_SetFontSize
                                BackgroundColorToWrite = str_SetBackgroundColor
                                AlertSoundToWrite = str_PlayAlertSound
                                EffectToWrite = str_PlayEffect
                                IconToWrite = str_MinimapIcon
    
                if LineToWrite != "":
                    str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                    str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                    str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                    write_obj.write("\n")
                    write_obj.write("##### Item level "+str(k)+", Tier "+str(i)+"\n")
                    write_obj.write("Show\n")
                    write_obj.write("	Rarity Rare\n")
                    write_obj.write("	ItemLevel >= "+str(k)+"\n")
                    write_obj.write("	BaseType =="+LineToWrite+"\n")
                    write_obj.write("	SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("	SetTextColor 0 0 0 255\n")
                    write_obj.write("	SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("	PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("	PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("	MinimapIcon "+IconToWrite+"\n")

    print ("Non-influenced bases section complete.")

def func_hide_norm():

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Hide normal and magic items. Interesting rares caught at top of filter.\n")
        write_obj.write("##### Sections at top of filter are adjustable, so this section doesn't need to be.\n")
        write_obj.write("\n")
        write_obj.write("Hide\n")
        write_obj.write("	Rarity Normal Magic Rare\n")
        write_obj.write("	Class Abyss Amulets Axes Belts Body Boots Bows Claws Daggers Flasks Gems Gloves Helmets Jewel Maces Quivers Rings Sceptres Shields Staves Swords Wands Warstaves\n")
        write_obj.write("	SetFontSize 18\n")
        write_obj.write("	SetBorderColor 0 0 0 0\n")
        write_obj.write("	SetBackgroundColor 0 0 0 0\n")
        write_obj.write("	DisableDropSound True\n")
        write_obj.write("\n")
        write_obj.write("###########################################################################\n")
        write_obj.write("##### Using the same remaining unknown section as FilterBlade so people\n")
        write_obj.write("##### recognize what this means if they see it.\n")
        write_obj.write("#####\n")
        write_obj.write("\n")
        write_obj.write("Show\n")
        write_obj.write("	SetFontSize 45\n")
        write_obj.write("	SetTextColor 255 0 255 255\n")
        write_obj.write("	SetBorderColor 255 0 255 255\n")
        write_obj.write("	SetBackgroundColor 100 0 100 255\n")
        write_obj.write("	PlayAlertSound 3 300\n")
        write_obj.write("	PlayEffect Pink\n")
        write_obj.write("	MinimapIcon 0 Pink Circle\n")

    print ("Hide normal section complete.")

def func_cleanup():
    with open(strTXTout, "r+") as f:
        old = f.read() # read everything in the file
        f.seek(0) # rewind

        new = re.sub(' "Poison Support"',"",old)
        new = re.sub(' "Lesser Poison Support"',"",old)
        new = re.sub(' ""Blessed Boots"',"",old)

        #new1 = re.sub("\n\n#####.*\n\n","\n\n",new0) # delete unuesd Tier lines
        #new2 = re.sub("\n\n\n","\n\n",new1) # Delete extra newlines so they don't throw off later matches
        #new3 = re.sub("\n\n#####.*\n\n","\n\n",new2) # delete unuesd Tier lines
        #new4 = re.sub("\n\n\n","\n\n",new3) # Delete extra newlines so they don't throw off later matches
        f.write(new) # write the new file

    print ("Cleanup of empty tier sections complete.")

# INITIALIZE NEW FILE INITIALIZE NEW FILE INITIALIZE NEW FILE INITIALIZE NEW FILE
# INITIALIZE NEW FILE INITIALIZE NEW FILE INITIALIZE NEW FILE INITIALIZE NEW FILE
# INITIALIZE NEW FILE INITIALIZE NEW FILE INITIALIZE NEW FILE INITIALIZE NEW FILE
func_init()

# STATIC INTRO STATIC INTRO STATIC INTRO STATIC INTRO STATIC INTRO STATIC INTRO
# STATIC INTRO STATIC INTRO STATIC INTRO STATIC INTRO STATIC INTRO STATIC INTRO
# STATIC INTRO STATIC INTRO STATIC INTRO STATIC INTRO STATIC INTRO STATIC INTRO
func_static_intro()

# Want to put currency near the top, as it drops more often than other things. Less time to process the filter.
# But also need to put it below other stackable items that the game may consider currency.

# CONSUMABLES CONSUMABLES CONSUMABLES CONSUMABLES CONSUMABLES CONSUMABLES
# CONSUMABLES CONSUMABLES CONSUMABLES CONSUMABLES CONSUMABLES CONSUMABLES
# CONSUMABLES CONSUMABLES CONSUMABLES CONSUMABLES CONSUMABLES CONSUMABLES
func_frag() # now includes func_scar()
func_oil()
func_inc()
func_foss()
func_ess()
func_div()
func_prop()
func_deli()
# func_inv() # All invitations are now under frag section
func_curr()
func_vial()
func_heist()
func_watch() # what about unique watchstones?
func_cluster()
func_other()

# GEMS GEMS GEMS GEMS GEMS GEMS GEMS GEMS GEMS GEMS GEMS GEMS GEMS GEMS GEMS
# GEMS GEMS GEMS GEMS GEMS GEMS GEMS GEMS GEMS GEMS GEMS GEMS GEMS GEMS GEMS
# GEMS GEMS GEMS GEMS GEMS GEMS GEMS GEMS GEMS GEMS GEMS GEMS GEMS GEMS GEMS
# Have to do gems based on level, quality, & corruption
func_divergent_gems()
func_anomalous_gems()
func_phantasmal_gems()
func_normal_gems()

# Replicas have their own section because they have their own prices
# Replicas have to go above uniques otherwise might match there
func_replica_ujew() # replicas only, can't recognize relics yet
func_replica_ufla() # replicas only, can't recognize relics yet
func_replica_uacc() # replicas only, can't recognize relics yet
func_replica_umap() # replicas only, can't recognize relics yet

# UNIQUE GEAR UNIQUE GEAR UNIQUE GEAR UNIQUE GEAR UNIQUE GEAR UNIQUE GEAR
# UNIQUE GEAR UNIQUE GEAR UNIQUE GEAR UNIQUE GEAR UNIQUE GEAR UNIQUE GEAR
# UNIQUE GEAR UNIQUE GEAR UNIQUE GEAR UNIQUE GEAR UNIQUE GEAR UNIQUE GEAR
#func_uarm_6() # Once I do catch all 6L and 5L intro I can skip this totally
#func_uarm_5() # Once I do catch all 6L and 5L intro I can skip this totally
func_uarm_0()
#func_uweap_6() # Once I do catch all 6L and 5L intro I can skip this totally
#func_uweap_5() # Once I do catch all 6L and 5L intro I can skip this totally
func_uweap_0()

# UNIQUE JEWELS, FLASKS, ACCESSORIES UNIQUE JEWELS, FLASKS, ACCESSORIES
# UNIQUE JEWELS, FLASKS, ACCESSORIES UNIQUE JEWELS, FLASKS, ACCESSORIES
# UNIQUE JEWELS, FLASKS, ACCESSORIES UNIQUE JEWELS, FLASKS, ACCESSORIES
func_ujew() # replicas are filtered out, can't recognize relics yet
func_ufla() # replicas are filtered out, can't recognize relics yet
func_uacc() # replicas are filtered out, can't recognize relics yet

# MAPS MAPS MAPS MAPS MAPS MAPS MAPS MAPS MAPS MAPS MAPS MAPS MAPS MAPS MAPS
# MAPS MAPS MAPS MAPS MAPS MAPS MAPS MAPS MAPS MAPS MAPS MAPS MAPS MAPS MAPS
# MAPS MAPS MAPS MAPS MAPS MAPS MAPS MAPS MAPS MAPS MAPS MAPS MAPS MAPS MAPS
# Replica maps are in the replica section, which must stay above this section.
# Unique maps above normal, blighted/influenced maps next
func_umaps()
func_blight_maps()
func_influenced_maps()
func_normal_maps() # there are no normal replicas

# Online filter max 500,000 characters, but game can load much larger filter on hard drive. # 273,000 before this point.
func_influenced() # already at 568,000 here (!!!)
# The tiers on these seem pretty off.  I'll probably have to adjust these later.
func_non_influenced() # At 890,000 characters here (!!!)

# HIDE NORMAL AND MAGIC ITEMS HIDE NORMAL AND MAGIC ITEMS HIDE NORMAL AND MAGIC ITEMS
# HIDE NORMAL AND MAGIC ITEMS HIDE NORMAL AND MAGIC ITEMS HIDE NORMAL AND MAGIC ITEMS
# HIDE NORMAL AND MAGIC ITEMS HIDE NORMAL AND MAGIC ITEMS HIDE NORMAL AND MAGIC ITEMS
func_hide_norm()

# Always do the cleanup last.
func_cleanup()
print('Done!')

# NEEDS WORK NEEDS WORK NEEDS WORK NEEDS WORK NEEDS WORK NEEDS WORK NEEDS WORK
# NEEDS WORK NEEDS WORK NEEDS WORK NEEDS WORK NEEDS WORK NEEDS WORK NEEDS WORK
# NEEDS WORK NEEDS WORK NEEDS WORK NEEDS WORK NEEDS WORK NEEDS WORK NEEDS WORK

# func_uweap_0() # need to know how to ignore sockets in dupcheck
# func_uarm_0() # need to know how to ignore sockets in dupcheck

# Not sure if these can be used in a filter at all.
# func_beast()
# Might be able to use these for identified items.
# func_ench() 

# Rare weapons and armor by tier, sockets, variants, influence (and ilvl?)
# Rare weapons and armor by tier, sockets, variants, influence (and ilvl?)
# Rare weapons and armor by tier, sockets, variants, influence (and ilvl?)
# Rare ilvl >= 65 are economy T10 whether identified or not, based on chaos recipe

# Crafting Recipes

# When we get to hiding things, do explicit hide of currency and items first. Less time to process the filter since 99% is trash.
# Treat everything else as T1 to make sure we notice it and add it to our filters.

# Unique items go before Rare? MAYBE NORM > MAG > RARE > UN ? Filter out the more common stuff first?
# Identified items go before unidentified items? could be caught by the less-specific filters, or we could use HasExplicitMod?
# Stretch goal: include filtering identified items by # of T1 mods, T2 mods, etc.

# Is code for Maelström working properly??

# Create a header section to go at the top of the filters with info, Patreon, github, etc.

#Combine into one class = map but using maptier = None?
#Show
#    Class Map
# https://pathofexile.fandom.com/wiki/Map_fragment
# https://pathofexile.fandom.com/wiki/Misc_map_item



# also check:
# talismans

#Show # rare items with abyss sockets!
#	SocketGroup "A"		

# "Poison Support" "Lesser Poison Support" 
# Don't make any unique maps gray
# Don't make any blighted maps gray
