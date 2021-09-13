import csv
import re
import os
import sys
import time
from csv import writer
from csv import reader
from datetime import datetime
  
# Python
# I know these are all a non-factored mess right now, by design. There are so many
# variations that need to be handled diff ways that it's actually easier to not
# factorize yet. Make sure it all works, then factorize what we can.

# This script:
# Create text filter file. Multiple notes below in Main section.
# My filters are in "C:\Users\<user>\Documents\My Games\Path of Exile"

strUserSettings = os.path.join(sys.path[0], "00_user_settings.txt")
strCSVin = os.path.join(sys.path[0], "z038_assigned-colors.csv")
strCSVinOther = os.path.join(sys.path[0], "00_other.csv")
#strTXTout = os.path.join(sys.path[0], "z030_filter.filter")

current_time = datetime.now()
arrInfluences = ["Crusader","Elder","Hunter","Redeemer","Shaper","Warlord"]
arrDoubleInfluences = ["Crusader/Hunter","Crusader/Redeemer","Crusader/Warlord","Elder/Crusader","Elder/Hunter","Elder/Redeemer","Elder/Warlord","Redeemer/Hunter","Redeemer/Warlord","Shaper/Crusader","Shaper/Elder","Shaper/Elder/Crusader/Redeemer/Warlord/Hunter","Shaper/Hunter","Shaper/Redeemer","Shaper/Warlord","Warlord/Hunter"]

def func_init():
    global strOverallStrictness, strRareCutoff, booShowT11, strGrayCutoff, booShowNM6S, booShowNM5S, strTXTout, strBoostButton

    # Overwrite defaults if found in settings file
    with open(strUserSettings, 'r') as f:
        for line in f:
            if "league_number: " in line:
                league_number = (line.split("league_number: ")[1])
                league_number = league_number.strip()
                #print ("league_number is " + league_number)
            if "league_name: " in line:
                league_name = (line.split("league_name: ")[1])
                league_name = league_name.strip()
                #print ("league_name is " + league_name)

            if "Overall Strictness: " in line:
                strOverallStrictness = (line.split("Overall Strictness: ")[1])
                strOverallStrictness = int(strOverallStrictness.strip())
                #print ("strOverallStrictness is " + strOverallStrictness)
            if "Non-special Rare cutoff: " in line:
                strRareCutoff = (line.split("Non-special Rare cutoff: ")[1])
                strRareCutoff = int(strRareCutoff.strip())
                #print ("strRareCutoff is " + strRareCutoff)
            if "Gray item cutoff: " in line:
                strGrayCutoff = (line.split("Gray item cutoff: ")[1])
                strGrayCutoff = int(strGrayCutoff.strip())
                #print ("strGrayCutoff is " + strGrayCutoff)
            if "Show gray items: " in line:
                booShowT11 = (line.split("Show gray items: ")[1])
                #print ("booShowT11 is " + booShowT11)
                #time.sleep(5)
                if "True" in booShowT11:
                    booShowT11 = True
                else:
                    booShowT11 = False
                #print (booShowT11)
                #time.sleep(5)
            if "Show Normal/Magic 6-socket items: " in line:
                booShowNM6S = (line.split("Show Normal/Magic 6-socket items: ")[1])
                #print ("booShowNM6S is " + booShowNM6S)
                if "True" in booShowNM6S:
                    booShowNM6S = True
                else:
                    booShowNM6S = False
                #print (booShowNM6S)
                #time.sleep(5)
            if "Show Normal/Magic 5-socket items: " in line:
                booShowNM5S = (line.split("Show Normal/Magic 5-socket items: ")[1])
                #print ("booShowNM5S is " + booShowNM5S)
                if "True" in booShowNM5S:
                    booShowNM5S = True
                else:
                    booShowNM5S = False
                #print (booShowNM5S)
                #time.sleep(5)
            if "Boost Button" in line:
                strBoostButton = (line.split(": ")[1])
                #print ("strBoostButton is " + strBoostButton)
                #time.sleep(5)
                if "True" in strBoostButton:
                    strBoostButton = True
                else:
                    strBoostButton = False
                #print (strBoostButton)
                #time.sleep(5)

    # Hard setting these right now so I can play with the GUI without screwing up my filters
    #strLeague = "3.15 (Expedition)"
    #strOverallStrictness = 9
    #strRareCutoff = 76
    #strGrayCutoff = 5
    #booShowNM6S = False
    #booShowNM5S = False
    #strBoostButton = False

    header00 = str("##### Super Simple Loot Filter for League: "+league_number+" ("+league_name+"), updated: "+str(current_time)+"\n")
    header01 = str("##### Standard? : False\n")
    header02 = str("##### strOverallStrictness :" + str(strOverallStrictness)+"\n")
    header03 = str("##### booShowT11 :" + str(booShowT11)+"\n")
    header04 = str("##### booShowNM6S :" + str(booShowNM6S)+"\n")
    header05 = str("##### booShowNM5S :" + str(booShowNM5S)+"\n")
    header06 = str("##### strBoostButton :" + str(strBoostButton)+"\n")
    header07 = str("##### strRareCutoff :" + str(strRareCutoff)+"\n")
    header08 = str("##### strGrayCutoff :" + str(strGrayCutoff)+"\n")

    # Have ot do this stupid bullshit bceause swapping between types in Python is an absolute PAIN IN THE DICK.
    strTXTout = league_number+"-1-"+str(strOverallStrictness)+"-"
    if booShowT11 == True:
        strTXTout = strTXTout + "1-"
    else:
        strTXTout = strTXTout + "0-"
    if booShowNM6S == True:
        strTXTout = strTXTout + "1-"
    else:
        strTXTout = strTXTout + "0-"
    if booShowNM5S == True:
        strTXTout = strTXTout + "1-"
    else:
        strTXTout = strTXTout + "0-"
    if strBoostButton == True:
        strTXTout = strTXTout + "1-"
    else:
        strTXTout = strTXTout + "0-"
    strTXTout = strTXTout + str(strRareCutoff)+"-"+str(strGrayCutoff)+".filter"

    header09 = ("##### Suggested filter name: "+strTXTout+"\n")

    # Open the output file in write mode
    with open(strTXTout, 'w', newline='') as write_obj:
        write_obj.write("#===============================================================================================================\n")
        write_obj.write(header00)
        write_obj.write("#####\n")
        write_obj.write("##### Settings:\n")
        write_obj.write(header01)
        write_obj.write(header02)
        write_obj.write(header03)
        write_obj.write(header04)
        write_obj.write(header05)
        write_obj.write(header06)
        write_obj.write(header07)
        write_obj.write(header08)
        write_obj.write("#####\n")
        write_obj.write(header09)
        write_obj.write("#===============================================================================================================\n")
        write_obj.write("##### LINKS TO LATEST VERSION AND FILTER EDITOR\n")
        write_obj.write("##### \n")
        write_obj.write("##### GET THE LATEST VERSION:                        https://github.com/flapanther33781/poe-filter\n")
        write_obj.write("##### POE FORUM THREAD:                                (TBD)\n")
        write_obj.write("#===============================================================================================================\n")
        write_obj.write("##### SUPPORT THE DEVELOPMENT:\n")
        write_obj.write("##### \n")
        write_obj.write("##### BUY ME A COFFEE:                                https://www.buymeacoffee.com/HMUH\n")
        write_obj.write("##### SUPPORT ME ON PATREON:                        https://www.patreon.com/HorrorMakesUsHappy\n")
        write_obj.write("##### IF YOU LOVE HORROR PLEASE CHECK OUT:            https://www.HorrorMakesUsHappy.com\n")
        write_obj.write("#===============================================================================================================\n")
        write_obj.write("##### CONTACT:\n")
        write_obj.write("##### \n")
        write_obj.write("##### PLEASE READ THE FAQ BEFORE ASKING QUESTIONS:    https://github.com/flapanther33781/poe-filter/wiki/FAQ\n")
        write_obj.write("##### GGG FORUMS:                                    https://www.pathofexile.com/account/view-profile/Fla_Panther\n")
        write_obj.write("##### GITHUB:                                        https://github.com/flapanther33781\n")
        write_obj.write("#===============================================================================================================\n")
        write_obj.write("##### INSTALLATION / UPDATE :\n")
        write_obj.write("##### \n")
        write_obj.write("##### If you have Python installed on your PC you can download the code for the scripts, run it on your own PC,\n")
        write_obj.write("##### and create filters with up-to-date pricing whenever you want!  Just download the zip file from the Github\n")
        write_obj.write("##### page linked above, and double-click the file titled \"00-super-simple-loot-filter.py\".\n")
        write_obj.write("##### \n")
        write_obj.write("##### If you don't want to run the files yourself you can download the text-based filters from my Github page linked above.\n")
        write_obj.write("##### Check for updates once a month or at least before new leagues to get the latest update.\n")
        write_obj.write("##### \n")
        write_obj.write("##### Once you have the filter file, put it into the following folder: %userprofile%/Documents/My Games/Path of Exile\n")
        write_obj.write("#####    (If you're not sure where your folder is, in the game, go to Options -> Game -> and click the folder icon.)\n")
        write_obj.write("##### Then, in the game, go to Options -> Game -> and select the filter from the Dropdown box.\n")
        write_obj.write("#===============================================================================================================\n")
        write_obj.write("##### Thank you to StupidFatHobbit and the guys over at FilterBlade, you all taught me a lot. This filter\n")
        write_obj.write("##### isn't meant to replace theirs. This filter is for new players who aren't ready for racing, crafting,\n")
        write_obj.write("##### hardcore, SSF, or build-specific highlighting - seriously, just THE MOST BASIC filter possible.\n")
        write_obj.write("##### \n")
        write_obj.write("##### Due to not showing those items this filter will be more strict than theirs, and does NOT use combinations of\n")
        write_obj.write("##### background color, text color, or border color when displaying an item.  This filter displays ALL items with\n")
        write_obj.write("##### black text, no border, and the background color is based on softcore market prices obtained from poe.ninja.\n")
        write_obj.write("##### \n")
        write_obj.write("##### (Yes, experienced players know poe.ninja's pricing isn't perfect, but for a completely new player it's good\n")
        write_obj.write("##### enough to start with. Anyway, this tool also allows you to do manual overrides.)\n")
        write_obj.write("##### \n")
        write_obj.write("##### The second goal for this filter is to configure tiers universally, across all item types.  If you see\n")
        write_obj.write("##### a color you know what its value is, regardless of what kind of item it is. No need to memorize multiple\n")
        write_obj.write("##### tier profiles, nor combinations of background and border colors.\n")
        write_obj.write("#===============================================================================================================\n")
        write_obj.write("##### Color order: Brown > Red > Orange > Yellow > Green > Blue > Purple > Cyan > Pink > White\n")
        write_obj.write("##### \n")
        write_obj.write("##### Unique items that share a common base will be gray.\n")
        write_obj.write("##### \n")
        write_obj.write("##### Minimap Icons:\n")
        write_obj.write("##### Diamond ---- All T1 drops\n")
        write_obj.write("##### Hexagon ---- Currency, Splinters\n")
        write_obj.write("##### Pentagon --- League Items, Maps, Scarabs\n")
        write_obj.write("##### Star ------- T2 & T3 Uniques\n")
        write_obj.write("##### Cross ------ All other Uniques\n")
        write_obj.write("##### Kite ------- Veiled, Enchanted, Synthesized, Fractured, Influenced items\n")
        write_obj.write("##### Square ----- Prophecies, Cards, Oils, Essences, Fossils, Incubators, etc.\n")
        write_obj.write("##### Triangle --- Rare Gear, Rare Jewels\n")
        write_obj.write("##### Circle ----- Gems, Flasks\n")
        write_obj.write("##### Rain ------- Use this for user overrides (crafting, recepies, etc)\n")
        write_obj.write("##### \n")
        write_obj.write("##### Aside from Diamond and Rain, more sides = more important, but color's still more important than the icon.\n")
        write_obj.write("##### An item with a Green Circle is worth more than one with a Red Pentagon. Colors follow the rainbow, but brown\n")
        write_obj.write("##### is below, and Cyan, Pink, and White above.\n")
        write_obj.write("#===============================================================================================================\n")
        write_obj.write("##### The tool I created to generate these filters does have a few other abilities, please check out my Github\n")
        write_obj.write("##### page for more info (linked above). If there's something you'd like to see added please message me there.\n")
        write_obj.write("#===============================================================================================================\n")
        write_obj.write("##### Note: This tool includes a function to preserve your manually-set overrides, but (a) it only works\n")
        write_obj.write("##### if the lines it's looking for don't change drastically, and (b) right now this tool is an an ALPHA\n")
        write_obj.write("##### stage, so it may change without notice, which may overwrite your manual overrides. As this\n")
        write_obj.write("##### progresses towards a BETA release this should stabilize, but for now please understand this is what\n")
        write_obj.write("##### needs to happen to get the tool to where it needs to be.\n")
        write_obj.write("##### \n")
        write_obj.write("##### Also, because it's in an ALPHA stage, the tool's actually creating a much longer filter file than\n")
        write_obj.write("##### it may need to. It was impossible to tell how long the text output was going to be until I built the\n")
        write_obj.write("##### tool, but now that I understand the output I'll be looking for ways to summarize and scale back the\n")
        write_obj.write("##### length of the filter. But even if I don't, even as it is now this filter isn't substantially longer\n")
        write_obj.write("##### than either FilterBlade's or StupidFatHobbit's.\n")
        write_obj.write("#===============================================================================================================\n")
        write_obj.write("##### Table of Contents\n")
        write_obj.write("#===============================================================================================================\n")
        write_obj.write("##### 10100 Manual Override Section\n")
        write_obj.write("##### 10200 6L\n")
        write_obj.write("##### 10300 6S\n")
        write_obj.write("##### 10400 5L\n")
        write_obj.write("##### 10500 4L and 2x2\n")
        write_obj.write("##### 10600 3L and 1x3\n")
        write_obj.write("##### 10700 Items with fewer than max links\n")
        write_obj.write("##### 10800 Rare Rings/Amulet/Belts/Jewels\n")
        write_obj.write("##### 10900 White and Abyss Sockets\n")
        write_obj.write("##### 11000 Flasks - Unique and Magic\n")
        write_obj.write("##### 11100 Map Fragments & Scarabs\n")
        write_obj.write("##### 11200 Oils\n")
        write_obj.write("##### 11300 Incubators\n")
        write_obj.write("##### 11400 Fossils & Resonators\n")
        write_obj.write("##### 11500 Essences\n")
        write_obj.write("##### 11600 Div Cards\n")
        write_obj.write("##### 11700 Prophecies\n")
        write_obj.write("##### 11800 Delirium Orbs\n")
        write_obj.write("##### 11900 Invitations\n")
        write_obj.write("##### 12000 Perandus coins\n")
        write_obj.write("##### 12100 Expedition items\n")
        write_obj.write("##### 12200 Currency\n")
        write_obj.write("##### 12300 Vials\n")
        write_obj.write("##### 12400 Heist\n")
        write_obj.write("##### 12500 Watchstones\n")
        write_obj.write("##### 12600 Cluster Jewels\n")
        write_obj.write("##### 12700 Other\n")
        write_obj.write("##### 12800 Quest/veiled/enchanted/synthesized items\n")
        write_obj.write("##### 12900 Fractured items\n")
        write_obj.write("##### 13000 Replica Jewels\n")
        write_obj.write("##### 13100 Replica Flasks\n")
        write_obj.write("##### 13200 Replica Accessories\n")
        write_obj.write("##### 13300 Replica Maps\n")
        write_obj.write("##### 13400 Unique Maps\n")
        write_obj.write("##### 13500 Blight Maps\n")
        write_obj.write("##### 13600 Influenced Maps\n")
        write_obj.write("##### 13700 Normal Maps\n")
        write_obj.write("##### 13800 Unique Jewels\n")
        write_obj.write("##### 13900 Unique Flasks\n")
        write_obj.write("##### 14000 All Other Replica Armor (5L and 6L caught at the top of the filter)\n")
        write_obj.write("##### 14100 All Other Unique Armor (5L and 6L caught at the top of the filter)\n")
        write_obj.write("##### 14200 All Other Replica Weapons (5L and 6L caught at the top of the filter)\n")
        write_obj.write("##### 14300 All Other Unique Weapons (5L and 6L caught at the top of the filter)\n")
        write_obj.write("##### 14400 Non-influenced bases\n")
        write_obj.write("##### 14500 Divergent Gems\n")
        write_obj.write("##### 14600 Anomalous Gems\n")
        write_obj.write("##### 14700 Phantasmal Gems\n")
        write_obj.write("##### 14800 Normal Gems (new GemQualityType Superior means normal)\n")
        write_obj.write("##### 14900 Hide specific normal/magic/rare items. Interesting rares caught at top of filter.\n")
        write_obj.write("##### 15000 Safety Net section - catch anything not caught above\n")
        write_obj.write("##### 15100 Special thanks!\n")
        write_obj.write("#===============================================================================================================\n")

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
        str_SetBackgroundColor = "150 50 150 255 # Purple"
        # str_SetBackgroundColor = "163 52 235 255 # Purple" # Alternate
        # str_SetBackgroundColor = "125 30 176 255 # Purple" # Alternate
    if str_SetBackgroundColor == "Blue":
        str_SetBackgroundColor = "50 50 255 255 # Blue"
        # str_SetBackgroundColor = "4 115 220 255 # Blue" # Alternate
        # str_SetBackgroundColor = "12 124 224 255 # Blue" # Alternate
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
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 10100 Manual Override Section - place whatever you want here.\n")
        write_obj.write("#####\n")
        write_obj.write("#####\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 10200 6L\n")
        write_obj.write("\n")
        write_obj.write("Show\n")
        write_obj.write("    LinkedSockets = 6\n")
        write_obj.write("    SetFontSize 45\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 255 255 255 255     # BACKGROUNDCOLOR WHITE\n")
        write_obj.write("    PlayAlertSound 10 300\n")
        write_obj.write("    PlayEffect White\n")
        write_obj.write("    MinimapIcon 0 White Diamond\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 10300 6S\n")
        write_obj.write("##### Unique items might be worth something.\n")
        write_obj.write("##### Rare items are almost definitely worth grabbing if ItemLevel >= 84\n")
        write_obj.write("##### Rare items ItemLevel < 84 might be worth something, we'll make that adjustable.\n")
        write_obj.write("##### Normal/magic are only worth grabbing in Acts 1-5 when you need the\n")
        write_obj.write("##### Jeweller's. Past that taking up 8 inventory slots for .1c is a waste.\n")
        write_obj.write("\n")
        write_obj.write("Show\n")
        write_obj.write("    Sockets = 6\n")
        write_obj.write("    Rarity Unique ######################## NOTE: This also catches 6S items not caught elsewhere!\n")
        write_obj.write("    SetFontSize 45\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 102 0 102 255     # BACKGROUNDCOLOR PURPLE\n")
        write_obj.write("    PlayAlertSound 10 300\n")
        write_obj.write("    PlayEffect Purple\n")
        write_obj.write("    MinimapIcon 0 Purple Cross\n")
        write_obj.write("Show\n")
        write_obj.write("    Sockets = 6\n")
        write_obj.write("    ItemLevel >= 84\n")
        write_obj.write("    Rarity Rare\n")
        write_obj.write("    SetFontSize 45\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 102 0 102 255     # BACKGROUNDCOLOR PURPLE\n")
        write_obj.write("    PlayAlertSound 10 300\n")
        write_obj.write("    PlayEffect Purple\n")
        write_obj.write("    MinimapIcon 0 Purple Triangle\n")
        write_obj.write("Show                                    # This ilvl is adjustable in User Settings.\n")
        write_obj.write("    Sockets = 6\n")
        write_obj.write("    ItemLevel >= "+str(strRareCutoff)+"\n")
        write_obj.write("    Rarity Rare\n")
        write_obj.write("    SetFontSize 42\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 102 0 102 255     # BACKGROUNDCOLOR PURPLE\n")
        write_obj.write("    PlayAlertSound 10 300\n")
        write_obj.write("    PlayEffect Purple\n")
        write_obj.write("    MinimapIcon 0 Purple Triangle\n")
        if booShowNM6S == 1:
            write_obj.write("Show # Normal & Magic 6S, or Rare and below the ilvl mentioned above\n")
            write_obj.write("    Sockets = 6\n")
            write_obj.write("    SetFontSize 42\n")
            write_obj.write("    SetTextColor 0 0 0 255\n")
            write_obj.write("    SetBackgroundColor 26 26 255 255     # BACKGROUNDCOLOR BLUE\n")
            write_obj.write("    PlayAlertSound 8 300\n")
            write_obj.write("    MinimapIcon 0 Blue Triangle\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 10400 5L\n")
        write_obj.write("##### Grab if Unique. Rare might be worth something.\n")
        write_obj.write("##### Normal/magic are super cheap. Past early maps they're not worth selling,\n")
        write_obj.write("##### and crafting in this game's so bad they're not worth wasting orbs on.\n")
        write_obj.write("\n")
        write_obj.write("Show\n")
        write_obj.write("    LinkedSockets = 5\n")
        write_obj.write("    Rarity Unique ######################## NOTE: This also catches 5S items not caught elsewhere!\n")
        write_obj.write("    SetFontSize 45\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 102 0 102 255     # BACKGROUNDCOLOR PURPLE\n")
        write_obj.write("    PlayAlertSound 10 300\n")
        write_obj.write("    PlayEffect Purple\n")
        write_obj.write("    MinimapIcon 0 Purple Cross\n")
        write_obj.write("Show                                    # This ilvl is adjustable in User Settings.\n")
        write_obj.write("    LinkedSockets = 5\n")
        write_obj.write("    ItemLevel >= "+str(strRareCutoff)+"\n")
        write_obj.write("    Rarity Rare\n")
        write_obj.write("    SetFontSize 42\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 102 0 102 255     # BACKGROUNDCOLOR PURPLE\n")
        write_obj.write("    PlayAlertSound 10 300\n")
        write_obj.write("    PlayEffect Purple\n")
        write_obj.write("    MinimapIcon 0 Blue Triangle\n")
        if booShowNM5S == 1:
            write_obj.write("Show # Normal & Magic 5L, or Rare and below the ilvl mentioned above\n")
            write_obj.write("    LinkedSockets = 5\n")
            write_obj.write("    SetFontSize 42\n")
            write_obj.write("    SetTextColor 0 0 0 255\n")
            write_obj.write("    SetBackgroundColor 28 236 4 255     # BACKGROUNDCOLOR GREEN\n")
            write_obj.write("    PlayAlertSound 8 300\n")
            write_obj.write("    PlayEffect Green\n")
            write_obj.write("    MinimapIcon 0 Green Triangle\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 10500 4L and 2x2\n")
        write_obj.write("##### I only want LinkedSockets = 4 if Unique, or Rare and 2x2.\n")
        write_obj.write("##### For mapping the ilvl is adjustable for Rares.\n")
        write_obj.write("##### I know 4L doesn't add much to the value, but 99.9999% are trash anyway,\n")
        write_obj.write("##### so using ANY method to filter them is better than picking up and\n")
        write_obj.write("##### identifying all of them.\n")
        write_obj.write("\n")
        write_obj.write("Show                                    # This ilvl is adjustable in User Settings.\n")
        write_obj.write("    Rarity Rare\n")
        write_obj.write("    ItemLevel >= "+str(strRareCutoff)+"\n")
        write_obj.write("    LinkedSockets = 4\n")
        write_obj.write("    Width = 2\n")
        write_obj.write("    Height = 2\n")
        write_obj.write("    SetFontSize 40\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 28 236 4 255     # BACKGROUNDCOLOR GREEN\n")
        write_obj.write("    PlayAlertSound 8 300\n")
        write_obj.write("    MinimapIcon 0 Green Triangle\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 10600 3L and 1x3\n")
        write_obj.write("##### I only want Rare 3L items if 1x3.\n")
        write_obj.write("##### For mapping the ilvl is adjustable for Rares.\n")
        write_obj.write("##### I know 3L doesn't add much to the value, but 99.9999% are trash anyway,\n")
        write_obj.write("##### so using ANY method to filter them is better than picking up and\n")
        write_obj.write("##### identifying all of them.\n")
        write_obj.write("##### This ilvl is adjustable in User Settings.\n")
        write_obj.write("\n")
        write_obj.write("Show                                    # This ilvl is adjustable in User Settings.\n")
        write_obj.write("    Rarity Rare\n")
        write_obj.write("    ItemLevel >= "+str(strRareCutoff)+"\n")
        write_obj.write("    LinkedSockets = 3\n")
        write_obj.write("    Width = 1\n")
        write_obj.write("    Height = 3\n")
        write_obj.write("    SetFontSize 40\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 28 236 4 255     # BACKGROUNDCOLOR GREEN\n")
        write_obj.write("    PlayAlertSound 8 300\n")
        write_obj.write("    MinimapIcon 0 Green Triangle\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 10700 Items with fewer than max links\n")
        write_obj.write("##### I'm going to have a higher level requirement for these.\n")
        write_obj.write("\n")
        write_obj.write("Show\n")
        write_obj.write("    Rarity Rare\n")
        write_obj.write("    ItemLevel >= 81\n")
        write_obj.write("    LinkedSockets = 3\n")
        write_obj.write("    Width = 1\n")
        write_obj.write("    Height = 3\n")
        write_obj.write("    SetFontSize 40\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 28 236 4 255     # BACKGROUNDCOLOR GREEN\n")
        write_obj.write("    PlayAlertSound 8 300\n")
        write_obj.write("    MinimapIcon 0 Green Triangle\n")
        write_obj.write("Show\n")
        write_obj.write("    Rarity Rare\n")
        write_obj.write("    ItemLevel >= 81\n")
        write_obj.write("    LinkedSockets = 3\n")
        write_obj.write("    Width = 2\n")
        write_obj.write("    Height = 2\n")
        write_obj.write("    SetFontSize 40\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 28 236 4 255     # BACKGROUNDCOLOR GREEN\n")
        write_obj.write("    PlayAlertSound 8 300\n")
        write_obj.write("    MinimapIcon 0 Green Triangle\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 10800 Rare Rings/Amulet/Belts/Jewels\n")
        write_obj.write("##### I only want Rare Rings/Amulet/Belts/Jewels if Unique if ilvl is met\n")
        write_obj.write("##### This ilvl is adjustable in User Settings.\n")
        write_obj.write("\n")
        write_obj.write("Show                                    # This ilvl is adjustable in User Settings.\n")
        write_obj.write("    Rarity Rare\n")
        write_obj.write("    ItemLevel >= "+str(strRareCutoff)+"\n")
        write_obj.write("    Class Rings Amulet Belts Jewel\n")
        write_obj.write("    SetFontSize 40\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 28 236 4 255     # BACKGROUNDCOLOR GREEN\n")
        write_obj.write("    PlayAlertSound 8 300\n")
        write_obj.write("    MinimapIcon 0 Green Triangle\n")
        write_obj.write("Hide                                    # Have to hide here or else Abyss will get flagged as Purple below.\n")
        write_obj.write("    Rarity Normal Magic\n")
        write_obj.write("    Class Jewel\n")
        write_obj.write("    DisableDropSound True\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 10900 White and Abyss Sockets\n")
        write_obj.write("##### Can't upgrade Normal/Magic corrupted items, only useful if Rare.\n")
        write_obj.write("##### Maybe make # of White or Abyss sockets adjustable later for strictness.\n")
        write_obj.write("\n")
        write_obj.write("Show\n")
        write_obj.write("    SocketGroup W\n")
        write_obj.write("    Rarity Rare\n")
        write_obj.write("    SetFontSize 40\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 26 26 255 255     # BACKGROUNDCOLOR BLUE\n")
        write_obj.write("    PlayAlertSound 8 300\n")
        write_obj.write("    PlayEffect Blue\n")
        write_obj.write("    MinimapIcon 0 Blue Triangle\n")
        write_obj.write("Show\n")
        write_obj.write("    SocketGroup A\n")
        write_obj.write("    Rarity Rare\n")
        write_obj.write("    SetFontSize 40\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 26 26 255 255     # BACKGROUNDCOLOR BLUE\n")
        write_obj.write("    PlayAlertSound 8 300\n")
        write_obj.write("    PlayEffect Blue\n")
        write_obj.write("    MinimapIcon 0 Blue Triangle\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 11000 Flasks - Unique and Magic\n")
        write_obj.write("##### Maybe make this adjustable later.\n")
        write_obj.write("Show\n")
        write_obj.write("    Rarity Magic\n")
        write_obj.write("    BaseType \"Divine Life\" \"Divine Mana\" \"Eternal Life\" \"Eternal Mana\"\n")
        write_obj.write("    SetFontSize 40\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 28 236 4 215 # Green\n")
        write_obj.write("    PlayAlertSound 9 300\n")
        write_obj.write("    PlayEffect None\n")
        write_obj.write("    MinimapIcon 2 Green Circle\n")
        write_obj.write("Show\n")
        write_obj.write("    Rarity Normal Magic\n")
        write_obj.write("    Class \"Utility\"\n")
        write_obj.write("    SetFontSize 40\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 28 236 4 215 # Green\n")
        write_obj.write("    PlayAlertSound 9 300\n")
        write_obj.write("    PlayEffect None\n")
        write_obj.write("    MinimapIcon 2 Green Circle\n")

    print ("Static Intro complete.")

def func_frag():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 11100 Map Fragments & Scarabs\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_category = row[0]
                        str_name = row[1]
                        if "&&" in str_name:
                            str_name = str_name.replace("&&", ", ")
                        if row[12] != "":
                            str_Tier = row[12]
                        else:
                            str_Tier = row[11]
                        str_SetFontSize = row[13]
                        str_PlayAlertSound = row[14]
                        str_SetBackgroundColor = row[15]
                        str_PlayEffect = row[16]
                        str_MinimapIcon = row[17]

                        if int(str_Tier) == i and (str_category == "frag" or str_category == "scar"):
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
                if booHIDE == False:
                    print("Showing Tier "+str(i))
                    write_obj.write("Show\n")
                if booHIDE == True:
                    print("Hiding Tier "+str(i))
                    write_obj.write("Hide\n")
                    write_obj.write("DisableDropSound True\n")
                write_obj.write("    Class Map\n")
                write_obj.write("    BaseType =="+LineToWrite+"\n")
                write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("    SetTextColor 0 0 0 255\n")
                write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("    MinimapIcon "+IconToWrite+"\n")
    print ("Fragments and Sacarabs section complete.")

def func_curr():

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 12200 Currency\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_category = row[0]
                        str_name = row[1]
                        if "&&" in str_name:
                            str_name = str_name.replace("&&", ", ")
                        if row[12] != "":
                            str_Tier = row[12]
                        else:
                            str_Tier = row[11]
                        str_SetFontSize = row[13]
                        str_PlayAlertSound = row[14]
                        str_SetBackgroundColor = row[15]
                        str_PlayEffect = row[16]
                        str_MinimapIcon = row[17]

                        if int(str_Tier) == i and str_category == "curr":
                            LineToWrite = LineToWrite + ' "' + str_name + '"'
                            FontSizeToWrite = str_SetFontSize
                            BackgroundColorToWrite = str_SetBackgroundColor
                            AlertSoundToWrite = str_PlayAlertSound
                            EffectToWrite = str_PlayEffect
                            IconToWrite = str_MinimapIcon

            if (LineToWrite != ""):
                str_SetBackgroundColor = ChangeColors (BackgroundColorToWrite)
                str_PlayAlertSound = AlertSoundToWrite.replace("'", "")
                str_PlayAlertSound = str_PlayAlertSound.replace("-", " ")
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                if booHIDE == False:
                    print("Showing Tier "+str(i))
                    write_obj.write("Show\n")
                if booHIDE == True:
                    print("Hiding Tier "+str(i))
                    write_obj.write("Hide\n")
                    write_obj.write("DisableDropSound True\n")
                write_obj.write("    Class Currency\n")
                write_obj.write("    BaseType =="+LineToWrite+"\n")
                write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("    SetTextColor 0 0 0 255\n")
                write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("    MinimapIcon "+IconToWrite+"\n")
    print ("Currency section complete.")

def func_oil():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 11200 Oils\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_category = row[0]
                        str_name = row[1]
                        if "&&" in str_name:
                            str_name = str_name.replace("&&", ", ")
                        if row[12] != "":
                            str_Tier = row[12]
                        else:
                            str_Tier = row[11]
                        str_SetFontSize = row[13]
                        str_PlayAlertSound = row[14]
                        str_SetBackgroundColor = row[15]
                        str_PlayEffect = row[16]
                        str_MinimapIcon = row[17]

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
                if booHIDE == False:
                    print("Showing Tier "+str(i))
                    write_obj.write("Show\n")
                if booHIDE == True:
                    print("Hiding Tier "+str(i))
                    write_obj.write("Hide\n")
                    write_obj.write("DisableDropSound True\n")
                write_obj.write("    Class Currency\n")
                write_obj.write("    BaseType =="+LineToWrite+"\n")
                write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("    SetTextColor 0 0 0 255\n")
                write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("    MinimapIcon "+IconToWrite+"\n")
    print ("Oil section complete.")

def func_heist():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 12400 Heist\n")
        write_obj.write("##### Added from ""other"" csv file, not tracked by poe.ninja at this time. \n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        # ilvl81 items
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            with open(strCSVinOther, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    print(row)
                    if row[10] != "chaosEquivalent":
                        str_category = row[0]
                        str_baseType = row[2]
                        str_levelRequired = row[4]
                        if row[12] != "":
                            str_Tier = row[12]
                        else:
                            str_Tier = row[11]
                        str_SetFontSize = row[13]
                        str_PlayAlertSound = row[14]
                        str_SetBackgroundColor = row[15]
                        str_PlayEffect = row[16]
                        str_MinimapIcon = row[17]

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
                if booHIDE == False:
                    print("Showing Tier "+str(i))
                    write_obj.write("Show\n")
                if booHIDE == True:
                    print("Hiding Tier "+str(i))
                    write_obj.write("Hide\n")
                    write_obj.write("DisableDropSound True\n")
                write_obj.write("    Class Heist\n")
                write_obj.write("    ItemLevel >= "+LevelToWrite+"\n")
                write_obj.write("    BaseType =="+LineToWrite+"\n")
                write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("    SetTextColor 0 0 0 255\n")
                write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("    MinimapIcon "+IconToWrite+"\n")

        # ilvl83 items
        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            with open(strCSVinOther, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_category = row[0]
                        str_baseType = row[2]
                        str_levelRequired = row[4]
                        if row[12] != "":
                            str_Tier = row[12]
                        else:
                            str_Tier = row[11]
                        str_SetFontSize = row[13]
                        str_PlayAlertSound = row[14]
                        str_SetBackgroundColor = row[15]
                        str_PlayEffect = row[16]
                        str_MinimapIcon = row[17]

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
                if booHIDE == False:
                    print("Showing Tier "+str(i))
                    write_obj.write("Show\n")
                if booHIDE == True:
                    print("Hiding Tier "+str(i))
                    write_obj.write("Hide\n")
                    write_obj.write("DisableDropSound True\n")
                write_obj.write("    Class Heist\n")
                write_obj.write("    ItemLevel >= "+LevelToWrite+"\n")
                write_obj.write("    BaseType =="+LineToWrite+"\n")
                write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("    SetTextColor 0 0 0 255\n")
                write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("    MinimapIcon "+IconToWrite+"\n")

        # ilvl84 items
        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            with open(strCSVinOther, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_category = row[0]
                        str_baseType = row[2]
                        str_levelRequired = row[4]
                        if row[12] != "":
                            str_Tier = row[12]
                        else:
                            str_Tier = row[11]
                        str_SetFontSize = row[13]
                        str_PlayAlertSound = row[14]
                        str_SetBackgroundColor = row[15]
                        str_PlayEffect = row[16]
                        str_MinimapIcon = row[17]

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
                if booHIDE == False:
                    print("Showing Tier "+str(i))
                    write_obj.write("Show\n")
                if booHIDE == True:
                    print("Hiding Tier "+str(i))
                    write_obj.write("Hide\n")
                    write_obj.write("DisableDropSound True\n")
                write_obj.write("    Class Heist\n")
                write_obj.write("    ItemLevel >= "+LevelToWrite+"\n")
                write_obj.write("    BaseType =="+LineToWrite+"\n")
                write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("    SetTextColor 0 0 0 255\n")
                write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("    MinimapIcon "+IconToWrite+"\n")

        # All other items
        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            with open(strCSVinOther, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_category = row[0]
                        str_baseType = row[2]
                        str_levelRequired = row[4]
                        if row[12] != "":
                            str_Tier = row[12]
                        else:
                            str_Tier = row[11]
                        str_SetFontSize = row[13]
                        str_PlayAlertSound = row[14]
                        str_SetBackgroundColor = row[15]
                        str_PlayEffect = row[16]
                        str_MinimapIcon = row[17]

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
                if booHIDE == False:
                    print("Showing Tier "+str(i))
                    write_obj.write("Show\n")
                if booHIDE == True:
                    print("Hiding Tier "+str(i))
                    write_obj.write("Hide\n")
                    write_obj.write("DisableDropSound True\n")
                write_obj.write("    Class Heist\n")
                write_obj.write("    BaseType =="+LineToWrite+"\n")
                write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("    SetTextColor 0 0 0 255\n")
                write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("    MinimapIcon "+IconToWrite+"\n")

        # Last few Heist items
        write_obj.write("\n")
        write_obj.write("##### Last few Heist classes not otherwise noted.  Marking these as Tier 4.\n")
        write_obj.write("Show\n")
        write_obj.write("    Class ""Heist Target"" Trinkets Contract Blueprint\n")
        write_obj.write("    SetFontSize 39\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 25 25 255 235 # Blue\n")
        write_obj.write("    PlayAlertSound 8 300\n")
        write_obj.write("    PlayEffect Blue\n")
        write_obj.write("    MinimapIcon 2 Blue Pentagon\n")

    print ("Heist section complete.")

def func_cluster():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 12600 Cluster Jewels\n")
        write_obj.write("##### Added from ""other"" csv file, too many variants for\n")
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

def func_stacks():
    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("#####################################################################################################################\n")
        write_obj.write("##### 12000 Perandus coins - not tracked by poe.ninja.\n")
        write_obj.write("\n")
        write_obj.write("#### Tier 1\n")
        write_obj.write("\n")
        write_obj.write("Show #5c\n")
        write_obj.write("    StackSize >= 5000\n")
        write_obj.write("    BaseType \"Perandus\"\n")
        write_obj.write("    SetFontSize 42\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 28 236 4 215 # Green\n")
        write_obj.write("    PlayAlertSound 9 300\n")
        write_obj.write("    PlayEffect None\n")
        write_obj.write("    MinimapIcon 2 Green Hexagon\n")
        write_obj.write("\n")
        write_obj.write("Show #1c\n")
        write_obj.write("    StackSize >= 1000\n")
        write_obj.write("    BaseType \"Perandus\"\n")
        write_obj.write("    SetFontSize 42\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 255 255 0 215 # Yellow\n")
        write_obj.write("    PlayAlertSound 9 1\n")
        write_obj.write("    PlayEffect None\n")
        write_obj.write("\n")
        write_obj.write("Show #.5c\n")
        write_obj.write("    StackSize >= 500\n")
        write_obj.write("    BaseType \"Perandus\"\n")
        write_obj.write("    SetFontSize 42\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 244 92 36 230 # Orange\n")
        write_obj.write("    PlayAlertSound 9 1\n")
        write_obj.write("    PlayEffect None\n")
        write_obj.write("\n")
        write_obj.write("Show #.2c\n")
        write_obj.write("    StackSize >= 200\n")
        write_obj.write("    BaseType \"Perandus\"\n")
        write_obj.write("    SetFontSize 39\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 187 28 28 210 # Red\n")
        write_obj.write("    PlayAlertSound 9 1\n")
        write_obj.write("    PlayEffect None\n")
        write_obj.write("\n")
        write_obj.write("Show #.1c\n")
        write_obj.write("    StackSize >= 1\n")
        write_obj.write("    BaseType \"Perandus\"\n")
        write_obj.write("    SetFontSize 39\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 82 51 7 220 # Brown\n")
        write_obj.write("    PlayAlertSound 9 1\n")
        write_obj.write("    PlayEffect None\n")

        # Create section
        write_obj.write("\n")
        write_obj.write("#####################################################################################################################\n")
        write_obj.write("##### 12100 Expedition items\n")
        write_obj.write("##### Stacksize 20+ first, then 10+. Singles handled under currency.\n")
        write_obj.write("##### Will try to automate stacksizes later.\n")
        write_obj.write("\n")
        write_obj.write("#### Tier 1\n")
        write_obj.write("\n")
        write_obj.write("Show\n")
        write_obj.write("    Class Currency\n")
        write_obj.write("    StackSize >= 20\n")
        write_obj.write("    BaseType \"Exotic Coinage\" \"Burial Medallion\"\n")
        write_obj.write("    SetFontSize 45\n")
        write_obj.write("    SetBackgroundColor 0 0 0 255 # White\n")
        write_obj.write("    PlayAlertSound 2 300\n")
        write_obj.write("    PlayEffect White\n")
        write_obj.write("    MinimapIcon 0 White Diamond\n")

        write_obj.write("#### Tier 6\n")
        write_obj.write("\n")
        write_obj.write("Show\n")
        write_obj.write("    Class Currency\n")
        write_obj.write("    StackSize >= 20\n")
        write_obj.write("    BaseType \"Grand Sun Artifact\" \"Grand Broken Circle Artifact\" \"Grand Order Artifact\" \"Grand Black Scythe Artifact\"\n")
        write_obj.write("    SetFontSize 39\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 28 236 4 215 # Green\n")
        write_obj.write("    PlayAlertSound 9 300\n")

        write_obj.write("#### Tier 7\n")
        write_obj.write("\n")
        write_obj.write("Show\n")
        write_obj.write("    Class Currency\n")
        write_obj.write("    StackSize >= 20\n")
        write_obj.write("    BaseType \"Greater Sun Artifact\"\n")
        write_obj.write("    SetFontSize 36\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 255 255 0 215 # Yellow\n")
        write_obj.write("    PlayAlertSound 9 1\n")
        write_obj.write("    PlayEffect None\n")

        write_obj.write("#### Tier 8\n")
        write_obj.write("\n")
        write_obj.write("Show\n")
        write_obj.write("    Class Currency\n")
        write_obj.write("    StackSize >= 20\n")
        write_obj.write("    BaseType \"Greater Broken Circle Artifact\" \"Greater Order Artifact\" \"Common Broken Circle Artifact\" \"Lesser Black Scythe Artifact\" \"Common Sun Artifact\" \"Lesser Sun Artifact\" \"Common Order Artifact\" \"Lesser Order Artifact\" \"Lesser Broken Circle Artifact\" \"Greater Black Scythe Artifact\" \"Common Black Scythe Artifact\"\n")
        write_obj.write("    SetFontSize 36\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 244 92 36 230 # Orange\n")
        write_obj.write("    PlayAlertSound 9 1\n")
        write_obj.write("    PlayEffect None\n")

        write_obj.write("#### Tier 1\n")
        write_obj.write("\n")
        write_obj.write("Show\n")
        write_obj.write("    Class Currency\n")
        write_obj.write("    StackSize >= 10\n")
        write_obj.write("    BaseType \"Exotic Coinage\" \"Burial Medallion\"\n")
        write_obj.write("    SetFontSize 45\n")
        write_obj.write("    SetBackgroundColor 0 0 0 255 # White\n")
        write_obj.write("    PlayAlertSound 2 300\n")
        write_obj.write("    PlayEffect White\n")
        write_obj.write("    MinimapIcon 0 White Diamond\n")

        write_obj.write("#### Tier 3\n")
        write_obj.write("\n")
        write_obj.write("Show\n")
        write_obj.write("    Class Currency\n")
        write_obj.write("    StackSize >= 10\n")
        write_obj.write("    BaseType \"Astragali\" \"Scrap Metal\"\n")
        write_obj.write("    SetFontSize 42\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 132 211 250 255 # Cyan\n")
        write_obj.write("    PlayAlertSound 6 300\n")
        write_obj.write("    PlayEffect Cyan\n")
        write_obj.write("    MinimapIcon 1 Cyan Pentagon\n")

        write_obj.write("#### Tier 5\n")
        write_obj.write("\n")
        write_obj.write("Show\n")
        write_obj.write("    Class Currency\n")
        write_obj.write("    StackSize >= 10\n")
        write_obj.write("    BaseType \"Scrap Metal\"\n")
        write_obj.write("    SetFontSize 39\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 25 25 255 235 # Blue\n")
        write_obj.write("    PlayAlertSound 8 300\n")
        write_obj.write("    PlayEffect Blue\n")
        write_obj.write("    MinimapIcon 2 Blue Pentagon\n")

        write_obj.write("#### Tier 7\n")
        write_obj.write("\n")
        write_obj.write("Show\n")
        write_obj.write("    Class Currency\n")
        write_obj.write("    StackSize >= 10\n")
        write_obj.write("    BaseType \"Grand Sun Artifact\" \"Grand Broken Circle Artifact\" \"Grand Order Artifact\" \"Grand Black Scythe Artifact\" \"Greater Sun Artifact\"\n")
        write_obj.write("    SetFontSize 36\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 255 255 0 215 # Yellow\n")
        write_obj.write("    PlayAlertSound 9 1\n")
        write_obj.write("    PlayEffect None\n")

        write_obj.write("#### Tier 8\n")
        write_obj.write("\n")
        write_obj.write("Show\n")
        write_obj.write("    Class Currency\n")
        write_obj.write("    StackSize >= 10\n")
        write_obj.write("    BaseType \"Greater Broken Circle Artifact\" \"Greater Order Artifact\" \"Common Broken Circle Artifact\" \"Lesser Black Scythe Artifact\" \"Common Sun Artifact\" \"Lesser Sun Artifact\" \"Common Order Artifact\" \"Lesser Order Artifact\" \"Lesser Broken Circle Artifact\" \"Greater Black Scythe Artifact\" \"Common Black Scythe Artifact\"\n")
        write_obj.write("    SetFontSize 36\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 244 92 36 230 # Orange\n")
        write_obj.write("    PlayAlertSound 9 1\n")
        write_obj.write("    PlayEffect None\n")
        write_obj.write("\n")
        write_obj.write("#####################################################################################################################\n")
        write_obj.write("##### Fucking GGG put the god damned Expedition Logbook into its own fucking class.\n")
        write_obj.write("\n")
        write_obj.write("Show\n")
        write_obj.write("    Class \"Expedition Logbook\"\n")
        write_obj.write("    SetFontSize 39\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 25 25 255 235 # Blue\n")
        write_obj.write("    PlayAlertSound 8 300\n")
        write_obj.write("    PlayEffect Blue\n")
        write_obj.write("    MinimapIcon 0 Blue Pentagon\n")

def func_other():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 12700 Other\n")
        write_obj.write("##### Added from ""other"" csv file, not tracked by poe.ninja at this time. \n")
        write_obj.write("#####\n")

        # ilvl81 items
        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            with open(strCSVinOther, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_category = row[0]
                        str_baseType = row[2]
                        str_levelRequired = row[4]
                        if row[12] != "":
                            str_Tier = row[12]
                        else:
                            str_Tier = row[11]
                        str_SetFontSize = row[13]
                        str_PlayAlertSound = row[14]
                        str_SetBackgroundColor = row[15]
                        str_PlayEffect = row[16]
                        str_MinimapIcon = row[17]

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
                if booHIDE == False:
                    print("Showing Tier "+str(i))
                    write_obj.write("Show\n")
                if booHIDE == True:
                    print("Hiding Tier "+str(i))
                    write_obj.write("Hide\n")
                    write_obj.write("DisableDropSound True\n")
                write_obj.write("    Class "+LineToWrite+"\n")
                write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("    SetTextColor 0 0 0 255\n")
                write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("    MinimapIcon "+IconToWrite+"\n")

        write_obj.write("#####################################################################################################################\n")
        write_obj.write("##### 12800 Quest/veiled/enchanted/synthesized items\n")
        write_obj.write("\n")
        write_obj.write("Show\n")
        write_obj.write("    Class Quest\n")
        write_obj.write("    SetFontSize 45\n")
        write_obj.write("    SetBackgroundColor 0 0 0 255 # White\n")
        write_obj.write("    PlayAlertSound 2 300\n")
        write_obj.write("    PlayEffect White\n")
        write_obj.write("    MinimapIcon 0 White Diamond\n")
        write_obj.write("Show\n")
        write_obj.write("    HasExplicitMod "" Veil""\n")
        write_obj.write("    SetFontSize 39\n")
        write_obj.write("    SetBackgroundColor 25 25 255 235 # Blue\n")
        write_obj.write("    PlayAlertSound 8 300\n")
        write_obj.write("    PlayEffect Blue\n")
        write_obj.write("    MinimapIcon 2 Blue Kite\n")
        write_obj.write("Show\n")
        write_obj.write("    AnyEnchantment True\n")
        write_obj.write("    SetFontSize 39\n")
        write_obj.write("    SetBackgroundColor 25 25 255 235 # Blue\n")
        write_obj.write("    PlayAlertSound 8 300\n")
        write_obj.write("    PlayEffect Blue\n")
        write_obj.write("    MinimapIcon 2 Blue Kite\n")
        write_obj.write("Show\n")
        write_obj.write("    SynthesisedItem True\n")
        write_obj.write("    SetFontSize 39\n")
        write_obj.write("    SetBackgroundColor 25 25 255 235 # Blue\n")
        write_obj.write("    PlayAlertSound 8 300\n")
        write_obj.write("    PlayEffect Blue\n")
        write_obj.write("    MinimapIcon 2 Blue Kite\n")
        write_obj.write("#####################################################################################################################\n")
        write_obj.write("##### 12900 Fractured items\n")
        write_obj.write("\n")
        write_obj.write("Show\n")
        write_obj.write("    FracturedItem True\n")
        write_obj.write("    Class Helmets\n")
        write_obj.write("    ItemLevel >= 86\n")
        write_obj.write("    SetFontSize 40\n")
        write_obj.write("    SetBackgroundColor 102 0 102 255     # BACKGROUNDCOLOR PURPLE\n")
        write_obj.write("    PlayAlertSound 10 300\n")
        write_obj.write("    PlayEffect Purple\n")
        write_obj.write("    MinimapIcon 0 Purple Kite\n")
        write_obj.write("\n")
        write_obj.write("Show\n")
        write_obj.write("    FracturedItem True\n")
        write_obj.write("    Class Wands\n")
        write_obj.write("    ItemLevel >= 55\n")
        write_obj.write("    SetFontSize 40\n")
        write_obj.write("    SetBackgroundColor 25 25 255 235 # Blue\n")
        write_obj.write("    PlayAlertSound 8 300\n")
        write_obj.write("    PlayEffect Blue\n")
        write_obj.write("    MinimapIcon 2 Blue Kite\n")
        write_obj.write("\n")
        write_obj.write("Hide\n")
        write_obj.write("    FracturedItem True\n")
        write_obj.write("    Class Gloves Boots Body Amulets Rings Shields Quivers\n")
        write_obj.write("    DisableDropSound True\n")
        write_obj.write("\n")
        write_obj.write("Show\n")
        write_obj.write("    FracturedItem True\n")
        write_obj.write("    SetFontSize 40\n")
        write_obj.write("    SetBackgroundColor 28 236 4 255     # BACKGROUNDCOLOR GREEN\n")
        write_obj.write("    PlayAlertSound 8 300\n")
        write_obj.write("    PlayEffect Green\n")
        write_obj.write("    MinimapIcon 0 Green Kite\n")

    print ("Other section complete.")

def func_watch():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 12500 Watchstones\n")
        write_obj.write("##### Added from ""other"" csv file. \n")
        write_obj.write("##### poe.ninja does not list the basetype names so we can't automate this.\n")
        write_obj.write("#####\n")

        # ilvl81 items
        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            with open(strCSVinOther, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_category = row[0]
                        str_baseType = row[2]
                        str_levelRequired = row[4]
                        if row[12] != "":
                            str_Tier = row[12]
                        else:
                            str_Tier = row[11]
                        str_SetFontSize = row[13]
                        str_PlayAlertSound = row[14]
                        str_SetBackgroundColor = row[15]
                        str_PlayEffect = row[16]
                        str_MinimapIcon = row[17]

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
                if booHIDE == False:
                    print("Showing Tier "+str(i))
                    write_obj.write("Show\n")
                if booHIDE == True:
                    print("Hiding Tier "+str(i))
                    write_obj.write("Hide\n")
                    write_obj.write("DisableDropSound True\n")
                write_obj.write("    BaseType "+LineToWrite+"\n")
                write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("    SetTextColor 0 0 0 255\n")
                write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("    MinimapIcon "+IconToWrite+"\n")

        # Last few Atlas items
        write_obj.write("\n")
        write_obj.write("##### Not sure if this class includes the items above or separate items.\n")
        write_obj.write("##### Adding here just to be sure.\n")
        write_obj.write("Show\n")
        write_obj.write("    Class \"Atlas Region Upgrade Item\"\n")
        write_obj.write("    SetFontSize 39\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 25 25 255 235 # Blue\n")
        write_obj.write("    PlayAlertSound 8 300\n")
        write_obj.write("    PlayEffect Blue\n")
        write_obj.write("    MinimapIcon 2 Blue Pentagon\n")

    print ("Watchstones section complete.")

def func_deli():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 11800 Delirium Orbs\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_category = row[0]
                        str_name = row[1]
                        if "&&" in str_name:
                            str_name = str_name.replace("&&", ", ")
                        if row[12] != "":
                            str_Tier = row[12]
                        else:
                            str_Tier = row[11]
                        str_SetFontSize = row[13]
                        str_PlayAlertSound = row[14]
                        str_SetBackgroundColor = row[15]
                        str_PlayEffect = row[16]
                        str_MinimapIcon = row[17]

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
                if booHIDE == False:
                    print("Showing Tier "+str(i))
                    write_obj.write("Show\n")
                if booHIDE == True:
                    print("Hiding Tier "+str(i))
                    write_obj.write("Hide\n")
                    write_obj.write("DisableDropSound True\n")
                write_obj.write("    Class Currency\n")
                write_obj.write("    BaseType =="+LineToWrite+"\n")
                write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("    SetTextColor 0 0 0 255\n")
                write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("    MinimapIcon "+IconToWrite+"\n")
    print ("Delirium Orb section complete.")

def func_inv():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 11900 Invitations\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_category = row[0]
                        str_name = row[1]
                        if "&&" in str_name:
                            str_name = str_name.replace("&&", ", ")
                        if row[12] != "":
                            str_Tier = row[12]
                        else:
                            str_Tier = row[11]
                        str_SetFontSize = row[13]
                        str_PlayAlertSound = row[14]
                        str_SetBackgroundColor = row[15]
                        str_PlayEffect = row[16]
                        str_MinimapIcon = row[17]

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
                if booHIDE == False:
                    print("Showing Tier "+str(i))
                    write_obj.write("Show\n")
                if booHIDE == True:
                    print("Hiding Tier "+str(i))
                    write_obj.write("Hide\n")
                    write_obj.write("DisableDropSound True\n")
                #write_obj.write("    Class Currency\n")
                write_obj.write("    BaseType =="+LineToWrite+"\n")
                write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("    SetTextColor 0 0 0 255\n")
                write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("    MinimapIcon "+IconToWrite+"\n")
    print ("Invitations section complete.")

def func_vial():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 12300 Vials\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_category = row[0]
                        str_name = row[1]
                        if "&&" in str_name:
                            str_name = str_name.replace("&&", ", ")
                        if row[12] != "":
                            str_Tier = row[12]
                        else:
                            str_Tier = row[11]
                        str_SetFontSize = row[13]
                        str_PlayAlertSound = row[14]
                        str_SetBackgroundColor = row[15]
                        str_PlayEffect = row[16]
                        str_MinimapIcon = row[17]

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
                if booHIDE == False:
                    print("Showing Tier "+str(i))
                    write_obj.write("Show\n")
                if booHIDE == True:
                    print("Hiding Tier "+str(i))
                    write_obj.write("Hide\n")
                    write_obj.write("DisableDropSound True\n")
                write_obj.write("    Class Currency\n")
                write_obj.write("    BaseType =="+LineToWrite+"\n")
                write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("    SetTextColor 0 0 0 255\n")
                write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("    MinimapIcon "+IconToWrite+"\n")
    print ("Vial section complete.")

def func_inc():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 11300 Incubators\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_category = row[0]
                        str_name = row[1]
                        if "&&" in str_name:
                            str_name = str_name.replace("&&", ", ")
                        if row[12] != "":
                            str_Tier = row[12]
                        else:
                            str_Tier = row[11]
                        str_SetFontSize = row[13]
                        str_PlayAlertSound = row[14]
                        str_SetBackgroundColor = row[15]
                        str_PlayEffect = row[16]
                        str_MinimapIcon = row[17]

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
                write_obj.write("\n")
                write_obj.write("##### Tier "+str(i)+"\n")
                if booHIDE == False:
                    print("Showing Tier "+str(i))
                    write_obj.write("Show\n")
                if booHIDE == True:
                    print("Hiding Tier "+str(i))
                    write_obj.write("Hide\n")
                    write_obj.write("DisableDropSound True\n")
                write_obj.write("    Class Incubator\n")
                write_obj.write("    BaseType =="+LineToWrite+"\n")
                write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("    SetTextColor 0 0 0 255\n")
                write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("    MinimapIcon "+IconToWrite+"\n")
    print ("Incubator section complete.")

def func_scar():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### Scarabs\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_category = row[0]
                        str_name = row[1]
                        if "&&" in str_name:
                            str_name = str_name.replace("&&", ", ")
                        if row[12] != "":
                            str_Tier = row[12]
                        else:
                            str_Tier = row[11]
                        str_SetFontSize = row[13]
                        str_PlayAlertSound = row[14]
                        str_SetBackgroundColor = row[15]
                        str_PlayEffect = row[16]
                        str_MinimapIcon = row[17]

                        if int(str_Tier) == i and str_category == "scar":
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
                if booHIDE == False:
                    print("Showing Tier "+str(i))
                    write_obj.write("Show\n")
                if booHIDE == True:
                    print("Hiding Tier "+str(i))
                    write_obj.write("Hide\n")
                    write_obj.write("DisableDropSound True\n")
                #write_obj.write("    Class ""Map Fragments""\n")
                write_obj.write("    BaseType =="+LineToWrite+"\n")
                write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("    SetTextColor 0 0 0 255\n")
                write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("    MinimapIcon "+IconToWrite+"\n")
    print ("Scarab section complete.")

def func_foss():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 11400 Fossils & Resonators\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_category = row[0]
                        str_name = row[1]
                        if "&&" in str_name:
                            str_name = str_name.replace("&&", ", ")
                        if row[12] != "":
                            str_Tier = row[12]
                        else:
                            str_Tier = row[11]
                        str_SetFontSize = row[13]
                        str_PlayAlertSound = row[14]
                        str_SetBackgroundColor = row[15]
                        str_PlayEffect = row[16]
                        str_MinimapIcon = row[17]

                        if int(str_Tier) == i and (str_category == "foss" or str_category == "res"):
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
                if booHIDE == False:
                    print("Showing Tier "+str(i))
                    write_obj.write("Show\n")
                if booHIDE == True:
                    print("Hiding Tier "+str(i))
                    write_obj.write("Hide\n")
                    write_obj.write("DisableDropSound True\n")
                write_obj.write("    Class Stackable\n")
                write_obj.write("    BaseType =="+LineToWrite+"\n")
                write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("    SetTextColor 0 0 0 255\n")
                write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("    MinimapIcon "+IconToWrite+"\n")
    print ("Fossil & Resonator section complete.")

def func_ess():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 11500 Essences\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_category = row[0]
                        str_name = row[1]
                        if "&&" in str_name:
                            str_name = str_name.replace("&&", ", ")
                        if row[12] != "":
                            str_Tier = row[12]
                        else:
                            str_Tier = row[11]
                        str_SetFontSize = row[13]
                        str_PlayAlertSound = row[14]
                        str_SetBackgroundColor = row[15]
                        str_PlayEffect = row[16]
                        str_MinimapIcon = row[17]

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
                if booHIDE == False:
                    print("Showing Tier "+str(i))
                    write_obj.write("Show\n")
                if booHIDE == True:
                    print("Hiding Tier "+str(i))
                    write_obj.write("Hide\n")
                    write_obj.write("DisableDropSound True\n")
                write_obj.write("    Class Currency\n")
                write_obj.write("    BaseType =="+LineToWrite+"\n")
                write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("    SetTextColor 0 0 0 255\n")
                write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("    MinimapIcon "+IconToWrite+"\n")
    print ("Essences section complete.")

def func_div():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 11600 Div Cards\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_category = row[0]
                        str_name = row[1]
                        if "&&" in str_name:
                            str_name = str_name.replace("&&", ", ")
                        if row[12] != "":
                            str_Tier = row[12]
                        else:
                            str_Tier = row[11]
                        str_SetFontSize = row[13]
                        str_PlayAlertSound = row[14]
                        str_SetBackgroundColor = row[15]
                        str_PlayEffect = row[16]
                        str_MinimapIcon = row[17]

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
                if booHIDE == False:
                    print("Showing Tier "+str(i))
                    write_obj.write("Show\n")
                if booHIDE == True:
                    print("Hiding Tier "+str(i))
                    write_obj.write("Hide\n")
                    write_obj.write("DisableDropSound True\n")
                write_obj.write("    Class Divination\n")
                write_obj.write("    BaseType =="+LineToWrite+"\n")
                write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("    SetTextColor 0 0 0 255\n")
                write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("    MinimapIcon "+IconToWrite+"\n")
    print ("Div Card section complete.")

def func_prop():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 11700 Prophecies\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_category = row[0]
                        str_name = row[1]
                        if "&&" in str_name:
                            str_name = str_name.replace("&&", ", ")
                        if row[12] != "":
                            str_Tier = row[12]
                        else:
                            str_Tier = row[11]
                        str_SetFontSize = row[13]
                        str_PlayAlertSound = row[14]
                        str_SetBackgroundColor = row[15]
                        str_PlayEffect = row[16]
                        str_MinimapIcon = row[17]

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
                if booHIDE == False:
                    print("Showing Tier "+str(i))
                    write_obj.write("Show\n")
                if booHIDE == True:
                    print("Hiding Tier "+str(i))
                    write_obj.write("Hide\n")
                    write_obj.write("DisableDropSound True\n")
                write_obj.write("    BaseType ""Prophecy""\n")
                write_obj.write("    Prophecy "+LineToWrite+"\n")
                write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("    SetTextColor 0 0 0 255\n")
                write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("    MinimapIcon "+IconToWrite+"\n")
    print ("Prophecies section complete.")

def func_beast():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### Beasts\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_category = row[0]
                        str_name = row[1]
                        if "&&" in str_name:
                            str_name = str_name.replace("&&", ", ")
                        if row[12] != "":
                            str_Tier = row[12]
                        else:
                            str_Tier = row[11]
                        str_SetFontSize = row[13]
                        str_PlayAlertSound = row[14]
                        str_SetBackgroundColor = row[15]
                        str_PlayEffect = row[16]
                        str_MinimapIcon = row[17]

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
                if booHIDE == False:
                    print("Showing Tier "+str(i))
                    write_obj.write("Show\n")
                if booHIDE == True:
                    print("Hiding Tier "+str(i))
                    write_obj.write("Hide\n")
                    write_obj.write("DisableDropSound True\n")
                write_obj.write("    BaseType =="+LineToWrite+"\n")
                write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("    SetTextColor 0 0 0 255\n")
                write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("    MinimapIcon "+IconToWrite+"\n")
    print ("Beasts section complete.")

def func_replica_umap():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

# Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 13300 Replica Maps\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        #print (row)
                        str_category = row[0]
                        str_baseType = row[2]
                        if row[12] != "":
                            str_Tier = row[12]
                        else:
                            str_Tier = row[11]
                        str_SetFontSize = row[13]
                        str_PlayAlertSound = row[14]
                        str_SetBackgroundColor = row[15]
                        str_PlayEffect = row[16]
                        str_MinimapIcon = row[17]

                        if str_category == "repmap" and int(str_Tier) == i:
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
                if booHIDE == False:
                    print("Showing Tier "+str(i))
                    write_obj.write("Show\n")
                if booHIDE == True:
                    print("Hiding Tier "+str(i))
                    write_obj.write("Hide\n")
                    write_obj.write("DisableDropSound True\n")
                #write_obj.write("    Class Maps\n")
                write_obj.write("    Replica True\n")
                write_obj.write("    BaseType =="+LineToWrite+"\n")
                write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("    SetTextColor 0 0 0 255\n")
                write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("    MinimapIcon "+IconToWrite+"\n")
    print ("Replica Maps section complete.")

def func_replica_ujew():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 13000 Replica Jewels\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        #print (row)
                        str_category = row[0]
                        str_baseType = row[2]
                        if row[12] != "":
                            str_Tier = row[12]
                        else:
                            str_Tier = row[11]
                        str_SetFontSize = row[13]
                        str_PlayAlertSound = row[14]
                        str_SetBackgroundColor = row[15]
                        str_PlayEffect = row[16]
                        str_MinimapIcon = row[17]

                        if str_category == "repjew" and int(str_Tier) == i:
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
                if booHIDE == False:
                    print("Showing Tier "+str(i))
                    write_obj.write("Show\n")
                if booHIDE == True:
                    print("Hiding Tier "+str(i))
                    write_obj.write("Hide\n")
                    write_obj.write("DisableDropSound True\n")
                #write_obj.write("    Class Jewel\n")
                write_obj.write("    Replica True\n")
                write_obj.write("    BaseType =="+LineToWrite+"\n")
                write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("    SetTextColor 0 0 0 255\n")
                write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("    MinimapIcon "+IconToWrite+"\n")
    print ("Replica Jewels section complete.")

def func_replica_ufla():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 13100 Replica Flasks\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        #print (row)
                        str_category = row[0]
                        str_baseType = row[2]
                        if row[12] != "":
                            str_Tier = row[12]
                        else:
                            str_Tier = row[11]
                        str_SetFontSize = row[13]
                        str_PlayAlertSound = row[14]
                        str_SetBackgroundColor = row[15]
                        str_PlayEffect = row[16]
                        str_MinimapIcon = row[17]

                        if str_category == "repfla" and int(str_Tier) == i:
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
                if booHIDE == False:
                    print("Showing Tier "+str(i))
                    write_obj.write("Show\n")
                if booHIDE == True:
                    print("Hiding Tier "+str(i))
                    write_obj.write("Hide\n")
                    write_obj.write("DisableDropSound True\n")
                #write_obj.write("    Class Flasks\n")
                write_obj.write("    Replica True\n")
                write_obj.write("    BaseType =="+LineToWrite+"\n")
                write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("    SetTextColor 0 0 0 255\n")
                write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("    MinimapIcon "+IconToWrite+"\n")
    print ("Replica Flasks section complete.")

def func_replica_uacc():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 13200 Replica Accessories\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        #print (row)
                        str_category = row[0]
                        str_baseType = row[2]
                        if row[12] != "":
                            str_Tier = row[12]
                        else:
                            str_Tier = row[11]
                        str_SetFontSize = row[13]
                        str_PlayAlertSound = row[14]
                        str_SetBackgroundColor = row[15]
                        str_PlayEffect = row[16]
                        str_MinimapIcon = row[17]

                        if str_category == "repacc" and int(str_Tier) == i:
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
                if booHIDE == False:
                    print("Showing Tier "+str(i))
                    write_obj.write("Show\n")
                if booHIDE == True:
                    print("Hiding Tier "+str(i))
                    write_obj.write("Hide\n")
                    write_obj.write("DisableDropSound True\n")
                #write_obj.write("    Class Belts Rings Amulet\n")
                write_obj.write("    Replica True\n")
                write_obj.write("    BaseType =="+LineToWrite+"\n")
                write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("    SetTextColor 0 0 0 255\n")
                write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("    MinimapIcon "+IconToWrite+"\n")
    print ("Replica Accessories section complete.")

def func_normal_maps():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

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
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 13700 Normal Maps\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

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
                        if row[10] != "chaosEquivalent":
                            str_category = row[0]
                            str_baseType = row[2]
                            str_variant = row[3]
                            str_mapTier = row[7]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]
                
                            if str_category == "map" and str_variant == "Gen-11" and int(str_mapTier) == k and int(str_Tier) == i:
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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Maps\n")
                    write_obj.write("    Rarity Normal Magic Rare\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    MapTier >= "+MapTierToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")
                    write_obj.write("\n")
    print ("Normal Map section complete.")

def func_blight_maps_2():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

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
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 13500 Blight Maps\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

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
                        if row[10] != "chaosEquivalent":
                            str_category = row[0]
                            str_baseType = row[2]
                            str_variant = row[3]
                            str_mapTier = row[7]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]
                
                            if str_category == "blight" and str_variant == "Gen-11" and int(str_mapTier) == k and int(str_Tier) == i:
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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Maps\n")
                    write_obj.write("    BlightedMap True\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    MapTier >= "+MapTierToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")
                    write_obj.write("\n")
    print ("Normal Map section complete.")

def func_influenced_maps():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

# Right now I don't think there's any way to get info fro poe.ninja about influenced maps.
# So we will hard-set these as Tier 4 for now.

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 13600 Influenced Maps\n")
        write_obj.write("#####\n")
        write_obj.write("\n")
        write_obj.write("Show\n")
        write_obj.write("    Class Maps\n")
        write_obj.write("    HasInfluence Shaper Elder\n")
        write_obj.write("    SetFontSize 39\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 25 25 255 235 # Blue\n")
        write_obj.write("    PlayAlertSound 8 300\n")
        write_obj.write("    PlayEffect Blue\n")
        write_obj.write("    MinimapIcon 2 Blue Pentagon\n")

    print ("Influenced Map section complete.")

def func_blight_maps():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

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
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### Blight Maps\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_category = row[0]
                        str_baseType = row[2]
                        if row[12] != "":
                            str_Tier = row[12]
                        else:
                            str_Tier = row[11]
                        str_SetFontSize = row[13]
                        str_PlayAlertSound = row[14]
                        str_SetBackgroundColor = row[15]
                        str_PlayEffect = row[16]
                        str_MinimapIcon = row[17]

                        if int(str_Tier) == i and str_category == "blight":
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
                if booHIDE == False:
                    print("Showing Tier "+str(i))
                    write_obj.write("Show\n")
                if booHIDE == True:
                    print("Hiding Tier "+str(i))
                    write_obj.write("Hide\n")
                    write_obj.write("DisableDropSound True\n")
                write_obj.write("    Class Maps\n")
                write_obj.write("    BlightedMap True\n")
                write_obj.write("    BaseType =="+LineToWrite+"\n")
                write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("    SetTextColor 0 0 0 255\n")
                write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("    MinimapIcon "+IconToWrite+"\n")
                write_obj.write("\n")
    print ("Blight Map section complete.")

def func_umaps():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

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
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 13400 Unique Maps\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_category = row[0]
                        str_baseType = row[2]
                        str_mapTier = row[7]
                        if row[12] != "":
                            str_Tier = row[12]
                        else:
                            str_Tier = row[11]
                        str_SetFontSize = row[13]
                        str_PlayAlertSound = row[14]
                        str_SetBackgroundColor = row[15]
                        str_PlayEffect = row[16]
                        str_MinimapIcon = row[17]

                        if int(str_Tier) == i and str_category == "umap":
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
                if booHIDE == False:
                    print("Showing Tier "+str(i))
                    write_obj.write("Show\n")
                if booHIDE == True:
                    print("Hiding Tier "+str(i))
                    write_obj.write("Hide\n")
                    write_obj.write("DisableDropSound True\n")
                write_obj.write("    Class Maps\n")
                write_obj.write("    Rarity Unique\n")
                write_obj.write("    BaseType =="+LineToWrite+"\n")
                write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("    SetTextColor 0 0 0 255\n")
                write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("    MinimapIcon "+IconToWrite+"\n")
                write_obj.write("\n")
    print ("Unique Map section complete.")

def func_ujew():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 13800 Unique Jewels\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_category = row[0]
                        str_baseType = row[2]
                        if row[12] != "":
                            str_Tier = row[12]
                        else:
                            str_Tier = row[11]
                        str_SetFontSize = row[13]
                        str_PlayAlertSound = row[14]
                        str_SetBackgroundColor = row[15]
                        str_PlayEffect = row[16]
                        str_MinimapIcon = row[17]

                        if int(str_Tier) == i and str_category == "ujew":
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
                if booHIDE == False:
                    print("Showing Tier "+str(i))
                    write_obj.write("Show\n")
                if booHIDE == True:
                    print("Hiding Tier "+str(i))
                    write_obj.write("Hide\n")
                    write_obj.write("DisableDropSound True\n")
                #write_obj.write("    Class Jewel\n")
                write_obj.write("    Rarity Unique\n")
                write_obj.write("    BaseType =="+LineToWrite+"\n")
                write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("    SetTextColor 0 0 0 255\n")
                write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("    MinimapIcon "+IconToWrite+"\n")
    print ("Unique Jewel section complete.")

def func_ufla():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 13900 Unique Flasks\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_category = row[0]
                        str_baseType = row[2]
                        if row[12] != "":
                            str_Tier = row[12]
                        else:
                            str_Tier = row[11]
                        str_SetFontSize = row[13]
                        str_PlayAlertSound = row[14]
                        str_SetBackgroundColor = row[15]
                        str_PlayEffect = row[16]
                        str_MinimapIcon = row[17]

                        if int(str_Tier) == i and str_category == "ufla":
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
                if booHIDE == False:
                    print("Showing Tier "+str(i))
                    write_obj.write("Show\n")
                if booHIDE == True:
                    print("Hiding Tier "+str(i))
                    write_obj.write("Hide\n")
                    write_obj.write("DisableDropSound True\n")
                #write_obj.write("    Class Flasks\n")
                write_obj.write("    Rarity Unique\n")
                write_obj.write("    BaseType =="+LineToWrite+"\n")
                write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("    SetTextColor 0 0 0 255\n")
                write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("    MinimapIcon "+IconToWrite+"\n")
    print ("Unique Flask section complete.")

def func_uacc():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### Unique Accessories\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_category = row[0]
                        str_baseType = row[2]
                        if row[12] != "":
                            str_Tier = row[12]
                        else:
                            str_Tier = row[11]
                        str_SetFontSize = row[13]
                        str_PlayAlertSound = row[14]
                        str_SetBackgroundColor = row[15]
                        str_PlayEffect = row[16]
                        str_MinimapIcon = row[17]

                        if int(str_Tier) == i and str_category == "uacc":
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
                if booHIDE == False:
                    print("Showing Tier "+str(i))
                    write_obj.write("Show\n")
                if booHIDE == True:
                    print("Hiding Tier "+str(i))
                    write_obj.write("Hide\n")
                    write_obj.write("DisableDropSound True\n")
                #write_obj.write("    Class Belts Rings Amulet\n")
                write_obj.write("    Rarity Unique\n")
                write_obj.write("    BaseType =="+LineToWrite+"\n")
                write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("    SetTextColor 0 0 0 255\n")
                write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("    MinimapIcon "+IconToWrite+"\n")
    print ("Unique Accessories section complete.")

def func_ench():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### Helment Enchants\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_category = row[0]
                        str_name = row[1]
                        if "&&" in str_name:
                            str_name = str_name.replace("&&", ", ")
                        if row[12] != "":
                            str_Tier = row[12]
                        else:
                            str_Tier = row[11]
                        str_SetFontSize = row[13]
                        str_PlayAlertSound = row[14]
                        str_SetBackgroundColor = row[15]
                        str_PlayEffect = row[16]
                        str_MinimapIcon = row[17]

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
                if booHIDE == False:
                    print("Showing Tier "+str(i))
                    write_obj.write("Show\n")
                if booHIDE == True:
                    print("Hiding Tier "+str(i))
                    write_obj.write("Hide\n")
                    write_obj.write("DisableDropSound True\n")
                #write_obj.write("    Class Helm\n")
                write_obj.write("    HasEnchantment =="+LineToWrite+"\n")
                write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("    SetTextColor 0 0 0 255\n")
                write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("    MinimapIcon "+IconToWrite+"\n")
    print ("Helmet Enchants section complete.")

def func_normal_gems():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 14800 Normal Gems (new GemQualityType Superior means normal)\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            write_obj.write("\n")
            write_obj.write("##### Tier "+str(i)+"\n")
            print ("Working on Normal Gems - Tier "+str(i))

            # 21/23c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'21/23c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("    GemLevel >= 21\n")
                    write_obj.write("    Quality >= 23\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 20/23c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'20/23c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("    GemLevel >= 20\n")
                    write_obj.write("    Quality >= 23\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 6/23c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'6/23c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("    GemLevel >= 6\n")
                    write_obj.write("    Quality >= 23\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 21/20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'21/20c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("    GemLevel >= 21\n")
                    write_obj.write("    Quality >= 20\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 20/20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'20/20c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("    GemLevel >= 20\n")
                    write_obj.write("    Quality >= 20\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 6/20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'6/20c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("    GemLevel >= 6\n")
                    write_obj.write("    Quality >= 20\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 5/20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'5/20c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("    GemLevel >= 5\n")
                    write_obj.write("    Quality >= 20\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 21c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'21c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("    GemLevel >= 21\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'20c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("    GemLevel >= 20\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 7c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'7c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("    GemLevel >= 7\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 6c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'6c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("    GemLevel >= 6\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 4c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'4c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("    GemLevel >= 4\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 3c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'3c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("    GemLevel >= 3\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 2c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'2c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("    GemLevel >= 2\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 1c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'1c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("    GemLevel >= 1\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 5/20
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'5/20":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    Corrupted False\n")
                    write_obj.write("    GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("    GemLevel >= 5\n")
                    write_obj.write("    Quality >= 20\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 1/20
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'1/20":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    Corrupted False\n")
                    write_obj.write("    GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("    GemLevel >= 1\n")
                    write_obj.write("    Quality >= 20\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 20
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'20":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    Corrupted False\n")
                    write_obj.write("    GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("    GemLevel >= 20\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 6
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'6":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]

                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    Corrupted False\n")
                    write_obj.write("    GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("    GemLevel >= 6\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 3
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'3":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    Corrupted False\n")
                    write_obj.write("    GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("    GemLevel >= 3\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 2
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'2":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    Corrupted False\n")
                    write_obj.write("    GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("    GemLevel >= 2\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 1
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'1":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    Corrupted False\n")
                    write_obj.write("    GemQualityType Superior\n") # "Superior" means normal.
                    write_obj.write("    GemLevel >= 1\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

    print ("Normal Gems section complete.")

def func_divergent_gems():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 14500 Divergent Gems\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            write_obj.write("\n")
            write_obj.write("##### Tier "+str(i)+"\n")
            print ("Working on Divergent Gems - Tier "+str(i))

            # 21/23c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'21/23c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Divergent\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 21\n")
                    write_obj.write("    Quality >= 23\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 20/23c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'20/23c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Divergent\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 20\n")
                    write_obj.write("    Quality >= 23\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 6/23c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'6/23c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Divergent\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 6\n")
                    write_obj.write("    Quality >= 23\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 21/20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'21/20c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Divergent\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 21\n")
                    write_obj.write("    Quality >= 20\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 20/20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'20/20c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Divergent\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 20\n")
                    write_obj.write("    Quality >= 20\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 6/20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'6/20c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Divergent\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 6\n")
                    write_obj.write("    Quality >= 20\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 5/20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'5/20c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Divergent\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 5\n")
                    write_obj.write("    Quality >= 20\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 21c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'21c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Divergent\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 21\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'20c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Divergent\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 20\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 7c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'7c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Divergent\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 7\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 6c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'6c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Divergent\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 6\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 4c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'4c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Divergent\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 4\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 3c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'3c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Divergent\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 3\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 2c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'2c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Divergent\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 2\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 1c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'1c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Divergent\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 1\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 5/20
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'5/20":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Divergent\n")
                    write_obj.write("    Corrupted False\n")
                    write_obj.write("    GemLevel >= 5\n")
                    write_obj.write("    Quality >= 20\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 1/20
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'1/20":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Divergent\n")
                    write_obj.write("    Corrupted False\n")
                    write_obj.write("    GemLevel >= 1\n")
                    write_obj.write("    Quality >= 20\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 20
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'20":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Divergent\n")
                    write_obj.write("    Corrupted False\n")
                    write_obj.write("    GemLevel >= 20\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 6
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'6":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Divergent\n")
                    write_obj.write("    Corrupted False\n")
                    write_obj.write("    GemLevel >= 6\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 3
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'3":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Divergent\n")
                    write_obj.write("    Corrupted False\n")
                    write_obj.write("    GemLevel >= 3\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 2
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'2":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Divergent\n")
                    write_obj.write("    Corrupted False\n")
                    write_obj.write("    GemLevel >= 2\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 1
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'1":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Divergent\n")
                    write_obj.write("    Corrupted False\n")
                    write_obj.write("    GemLevel >= 1\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

    print ("Divergent Gems section complete.")

def func_anomalous_gems():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 14600 Anomalous Gems\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            write_obj.write("\n")
            write_obj.write("##### Tier "+str(i)+"\n")
            print ("Working on Anomalous Gems - Tier "+str(i))

            # 21/23c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'21/23c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Anomalous\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 21\n")
                    write_obj.write("    Quality >= 23\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 20/23c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'20/23c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Anomalous\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 20\n")
                    write_obj.write("    Quality >= 23\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 6/23c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'6/23c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Anomalous\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 6\n")
                    write_obj.write("    Quality >= 23\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 21/20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'21/20c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Anomalous\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 21\n")
                    write_obj.write("    Quality >= 20\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 20/20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'20/20c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Anomalous\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 20\n")
                    write_obj.write("    Quality >= 20\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 6/20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'6/20c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Anomalous\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 6\n")
                    write_obj.write("    Quality >= 20\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 5/20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'5/20c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Anomalous\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 5\n")
                    write_obj.write("    Quality >= 20\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 21c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'21c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Anomalous\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 21\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'20c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Anomalous\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 20\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 7c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'7c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Anomalous\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 7\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 6c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'6c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Anomalous\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 6\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 4c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'4c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Anomalous\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 4\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 3c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'3c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Anomalous\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 3\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 2c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'2c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Anomalous\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 2\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 1c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'1c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Anomalous\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 1\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 5/20
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'5/20":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Anomalous\n")
                    write_obj.write("    Corrupted False\n")
                    write_obj.write("    GemLevel >= 5\n")
                    write_obj.write("    Quality >= 20\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 1/20
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'1/20":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Anomalous\n")
                    write_obj.write("    Corrupted False\n")
                    write_obj.write("    GemLevel >= 1\n")
                    write_obj.write("    Quality >= 20\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 20
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'20":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Anomalous\n")
                    write_obj.write("    Corrupted False\n")
                    write_obj.write("    GemLevel >= 20\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 6
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'6":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Anomalous\n")
                    write_obj.write("    Corrupted False\n")
                    write_obj.write("    GemLevel >= 6\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 3
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'3":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Anomalous\n")
                    write_obj.write("    Corrupted False\n")
                    write_obj.write("    GemLevel >= 3\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 2
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'2":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Anomalous\n")
                    write_obj.write("    Corrupted False\n")
                    write_obj.write("    GemLevel >= 2\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 1
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'1":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Anomalous\n")
                    write_obj.write("    Corrupted False\n")
                    write_obj.write("    GemLevel >= 1\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

    print ("Anomalous Gems section complete.")

def func_phantasmal_gems():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 14700 Phantasmal Gems\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            write_obj.write("\n")
            write_obj.write("##### Tier "+str(i)+"\n")
            print ("Working on Phantasmal Gems - Tier "+str(i))

            # 21/23c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'21/23c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Phantasmal\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 21\n")
                    write_obj.write("    Quality >= 23\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 20/23c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'20/23c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Phantasmal\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 20\n")
                    write_obj.write("    Quality >= 23\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 6/23c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'6/23c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Phantasmal\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 6\n")
                    write_obj.write("    Quality >= 23\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 21/20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'21/20c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Phantasmal\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 21\n")
                    write_obj.write("    Quality >= 20\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 20/20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'20/20c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Phantasmal\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 20\n")
                    write_obj.write("    Quality >= 20\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 6/20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'6/20c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Phantasmal\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 6\n")
                    write_obj.write("    Quality >= 20\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 5/20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'5/20c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Phantasmal\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 5\n")
                    write_obj.write("    Quality >= 20\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 21c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'21c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Phantasmal\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 21\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 20c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'20c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Phantasmal\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 20\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 7c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'7c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Phantasmal\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 7\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 6c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'6c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Phantasmal\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 6\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 4c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'4c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Phantasmal\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 4\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 3c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'3c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Phantasmal\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 3\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 2c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'2c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Phantasmal\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 2\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 1c
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'1c":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Phantasmal\n")
                    write_obj.write("    Corrupted True\n")
                    write_obj.write("    GemLevel >= 1\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 5/20
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'5/20":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Phantasmal\n")
                    write_obj.write("    Corrupted False\n")
                    write_obj.write("    GemLevel >= 5\n")
                    write_obj.write("    Quality >= 20\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 1/20
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'1/20":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Phantasmal\n")
                    write_obj.write("    Corrupted False\n")
                    write_obj.write("    GemLevel >= 1\n")
                    write_obj.write("    Quality >= 20\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 20
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'20":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Phantasmal\n")
                    write_obj.write("    Corrupted False\n")
                    write_obj.write("    GemLevel >= 20\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 6
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'6":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Phantasmal\n")
                    write_obj.write("    Corrupted False\n")
                    write_obj.write("    GemLevel >= 6\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 3
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'3":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Phantasmal\n")
                    write_obj.write("    Corrupted False\n")
                    write_obj.write("    GemLevel >= 3\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 2
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'2":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Phantasmal\n")
                    write_obj.write("    Corrupted False\n")
                    write_obj.write("    GemLevel >= 2\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

            # 1
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                LineToWrite = ""
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_variant = row[3]
                        if str_variant == "'1":
                            str_category = row[0]
                            str_name = row[1]
                            if "&&" in str_name:
                                str_name = str_name.replace("&&", ", ")
                            str_variant = row[3]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]

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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Class Gems\n")
                    write_obj.write("    GemQualityType Phantasmal\n")
                    write_obj.write("    Corrupted False\n")
                    write_obj.write("    GemLevel >= 1\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

    print ("Phantasmal Gems section complete.")

def func_uweap_6():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 6L Unique Weapons\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_category = row[0]
                        str_baseType = row[2]
                        str_links = row[5]
                        if row[12] != "":
                            str_Tier = row[12]
                        else:
                            str_Tier = row[11]
                        str_SetFontSize = row[13]
                        str_PlayAlertSound = row[14]
                        str_SetBackgroundColor = row[15]
                        str_PlayEffect = row[16]
                        str_MinimapIcon = row[17]

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
                if booHIDE == False:
                    print("Showing Tier "+str(i))
                    write_obj.write("Show\n")
                if booHIDE == True:
                    print("Hiding Tier "+str(i))
                    write_obj.write("Hide\n")
                    write_obj.write("DisableDropSound True\n")
                write_obj.write("    Rarity Unique\n")
                write_obj.write("    Sockets = 6\n")
                write_obj.write("    BaseType =="+LineToWrite+"\n")
                write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("    SetTextColor 0 0 0 255\n")
                write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("    MinimapIcon "+IconToWrite+"\n")
    print ("6L Unique Weapon section complete.")

def func_uweap_5():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 5L Unique Weapons\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_category = row[0]
                        str_baseType = row[2]
                        str_links = row[5]
                        if row[12] != "":
                            str_Tier = row[12]
                        else:
                            str_Tier = row[11]
                        str_SetFontSize = row[13]
                        str_PlayAlertSound = row[14]
                        str_SetBackgroundColor = row[15]
                        str_PlayEffect = row[16]
                        str_MinimapIcon = row[17]

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
                if booHIDE == False:
                    print("Showing Tier "+str(i))
                    write_obj.write("Show\n")
                if booHIDE == True:
                    print("Hiding Tier "+str(i))
                    write_obj.write("Hide\n")
                    write_obj.write("DisableDropSound True\n")
                write_obj.write("    Rarity Unique\n")
                write_obj.write("    Sockets = 5\n")
                write_obj.write("    BaseType =="+LineToWrite+"\n")
                write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("    SetTextColor 0 0 0 255\n")
                write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("    MinimapIcon "+IconToWrite+"\n")
    print ("5L Unique Weapon section complete.")

def func_repweap_0():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 14200 All Other Replica Weapons (5L and 6L caught at the top of the filter)\n")
        write_obj.write("##### NOTE: Unique items with multiple basetypes may show up as higher\n")
        write_obj.write("##### tiers than T11 if you have the Unique item breakpoint set > 0\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_category = row[0]
                        str_baseType = row[2]
                        str_links = row[5]
                        if row[12] != "":
                            str_Tier = row[12]
                        else:
                            str_Tier = row[11]
                        str_SetFontSize = row[13]
                        str_PlayAlertSound = row[14]
                        str_SetBackgroundColor = row[15]
                        str_PlayEffect = row[16]
                        str_MinimapIcon = row[17]

                        if int(str_Tier) == i and str_category == "repweap" and str_links == "":
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
                if booHIDE == False:
                    print("Showing Tier "+str(i))
                    write_obj.write("Show\n")
                if booHIDE == True:
                    print("Hiding Tier "+str(i))
                    write_obj.write("Hide\n")
                    write_obj.write("DisableDropSound True\n")
                write_obj.write("    Replica True\n")
                write_obj.write("    BaseType =="+LineToWrite+"\n")
                write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("    SetTextColor 0 0 0 255\n")
                write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("    MinimapIcon "+IconToWrite+"\n")
    print ("All Other Replica Weapon section complete.")

def func_uweap_0():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 14300 All Other Unique Weapons (5L and 6L caught at the top of the filter)\n")
        write_obj.write("##### NOTE: Unique items with multiple basetypes may show up as higher\n")
        write_obj.write("##### tiers than T11 if you have the Unique item breakpoint set > 0\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_category = row[0]
                        str_baseType = row[2]
                        str_links = row[5]
                        if row[12] != "":
                            str_Tier = row[12]
                        else:
                            str_Tier = row[11]
                        str_SetFontSize = row[13]
                        str_PlayAlertSound = row[14]
                        str_SetBackgroundColor = row[15]
                        str_PlayEffect = row[16]
                        str_MinimapIcon = row[17]

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
                if booHIDE == False:
                    print("Showing Tier "+str(i))
                    write_obj.write("Show\n")
                if booHIDE == True:
                    print("Hiding Tier "+str(i))
                    write_obj.write("Hide\n")
                    write_obj.write("DisableDropSound True\n")
                write_obj.write("    Rarity Unique\n")
                write_obj.write("    BaseType =="+LineToWrite+"\n")
                write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("    SetTextColor 0 0 0 255\n")
                write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("    MinimapIcon "+IconToWrite+"\n")
    print ("All Other Unique Weapon section complete.")

def func_uarm_6():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 6L Unique Armor\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_category = row[0]
                        str_baseType = row[2]
                        str_links = row[5]
                        if row[12] != "":
                            str_Tier = row[12]
                        else:
                            str_Tier = row[11]
                        str_SetFontSize = row[13]
                        str_PlayAlertSound = row[14]
                        str_SetBackgroundColor = row[15]
                        str_PlayEffect = row[16]
                        str_MinimapIcon = row[17]

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
                if booHIDE == False:
                    print("Showing Tier "+str(i))
                    write_obj.write("Show\n")
                if booHIDE == True:
                    print("Hiding Tier "+str(i))
                    write_obj.write("Hide\n")
                    write_obj.write("DisableDropSound True\n")
                write_obj.write("    Rarity Unique\n")
                write_obj.write("    Sockets = 6\n")
                write_obj.write("    BaseType =="+LineToWrite+"\n")
                write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("    SetTextColor 0 0 0 255\n")
                write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("    MinimapIcon "+IconToWrite+"\n")
    print ("6L Unique Armor section complete.")

def func_uarm_5():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 5L Unique Armor\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_category = row[0]
                        str_baseType = row[2]
                        str_links = row[5]
                        if row[12] != "":
                            str_Tier = row[12]
                        else:
                            str_Tier = row[11]
                        str_SetFontSize = row[13]
                        str_PlayAlertSound = row[14]
                        str_SetBackgroundColor = row[15]
                        str_PlayEffect = row[16]
                        str_MinimapIcon = row[17]

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
                if booHIDE == False:
                    print("Showing Tier "+str(i))
                    write_obj.write("Show\n")
                if booHIDE == True:
                    print("Hiding Tier "+str(i))
                    write_obj.write("Hide\n")
                    write_obj.write("DisableDropSound True\n")
                write_obj.write("    Rarity Unique\n")
                write_obj.write("    Sockets = 5\n")
                write_obj.write("    BaseType =="+LineToWrite+"\n")
                write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("    SetTextColor 0 0 0 255\n")
                write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("    MinimapIcon "+IconToWrite+"\n")

    print ("5L Unique Armor section complete.")

def func_reparm_0():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 14000 All Other Replica Armor (5L and 6L caught at the top of the filter)\n")
        write_obj.write("##### NOTE: Unique items with multiple basetypes may show up as higher\n")
        write_obj.write("##### tiers than T11 if you have the Unique item breakpoint set > 0\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_category = row[0]
                        str_baseType = row[2]
                        str_links = row[5]
                        if row[12] != "":
                            str_Tier = row[12]
                        else:
                            str_Tier = row[11]
                        str_SetFontSize = row[13]
                        str_PlayAlertSound = row[14]
                        str_SetBackgroundColor = row[15]
                        str_PlayEffect = row[16]
                        str_MinimapIcon = row[17]

                        if int(str_Tier) == i and str_category == "reparm" and str_links == "":
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
                if booHIDE == False:
                    print("Showing Tier "+str(i))
                    write_obj.write("Show\n")
                if booHIDE == True:
                    print("Hiding Tier "+str(i))
                    write_obj.write("Hide\n")
                    write_obj.write("DisableDropSound True\n")
                write_obj.write("    Replica True\n")
                write_obj.write("    BaseType =="+LineToWrite+"\n")
                write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("    SetTextColor 0 0 0 255\n")
                write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("    MinimapIcon "+IconToWrite+"\n")

    print ("All Other Replica Armor section complete.")

def func_uarm_0():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 14100 All Other Unique Armor (5L and 6L caught at the top of the filter)\n")
        write_obj.write("##### NOTE: Unique items with multiple basetypes may show up as higher\n")
        write_obj.write("##### tiers than T11 if you have the Unique item breakpoint set > 0\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for i in range (1,12):
            booHIDE = False
            if (booShowT11 == False) and (i > strOverallStrictness):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True
            if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                print ("Hiding tier " + str(i) + ".")
                booHIDE = True

            LineToWrite = ""
            with open(strCSVin, 'r') as read_obj:
                # Create a csv.reader object from the input file object
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if row[10] != "chaosEquivalent":
                        str_category = row[0]
                        str_baseType = row[2]
                        str_links = row[5]
                        if row[12] != "":
                            str_Tier = row[12]
                        else:
                            str_Tier = row[11]
                        str_SetFontSize = row[13]
                        str_PlayAlertSound = row[14]
                        str_SetBackgroundColor = row[15]
                        str_PlayEffect = row[16]
                        str_MinimapIcon = row[17]

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
                if booHIDE == False:
                    print("Showing Tier "+str(i))
                    write_obj.write("Show\n")
                if booHIDE == True:
                    print("Hiding Tier "+str(i))
                    write_obj.write("Hide\n")
                    write_obj.write("DisableDropSound True\n")
                write_obj.write("    Rarity Unique\n")
                write_obj.write("    BaseType =="+LineToWrite+"\n")
                write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                write_obj.write("    SetTextColor 0 0 0 255\n")
                write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                if str_PlayAlertSound != "":
                    write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                if EffectToWrite != "":
                    write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                if IconToWrite != "":
                    write_obj.write("    MinimapIcon "+IconToWrite+"\n")

    print ("All Other Unique Armor section complete.")

def func_influenced():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### Influenced items\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for k in range (86, 81, -1):
            print("Item level "+str(k))
            for strInfluence in arrInfluences:
                print("Influence "+strInfluence)
                for i in range (1,12):
                    booHIDE = False
                    if (booShowT11 == False) and (i > strOverallStrictness):
                        print ("Hiding tier " + str(i) + ".")
                        booHIDE = True
                    if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                        print ("Hiding tier " + str(i) + ".")
                        booHIDE = True

                    LineToWrite = ""
                    with open(strCSVin, 'r') as read_obj:
                        # Create a csv.reader object from the input file object
                        csv_reader = reader(read_obj)
                        for row in csv_reader:
                            if row[0] == "base":
                                #print(row)
                                str_category = row[0]
                                str_baseType = row[2]
                                str_variant = row[3]
                                str_variant = str_variant.replace("'", "")
                                str_levelRequired = row[4]
                                str_links = row[5]
                                if row[12] != "":
                                    str_Tier = row[12]
                                else:
                                    str_Tier = row[13]
                                str_SetFontSize = row[13]
                                str_PlayAlertSound = row[14]
                                str_SetBackgroundColor = row[15]
                                str_PlayEffect = row[16]
                                str_MinimapIcon = row[17]
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
                        if booHIDE == False:
                            print("Showing Tier "+str(i))
                            write_obj.write("Show\n")
                        if booHIDE == True:
                            print("Hiding Tier "+str(i))
                            write_obj.write("Hide\n")
                            write_obj.write("DisableDropSound True\n")
                        write_obj.write("    HasInfluence == "+strInfluence+"\n")
                        write_obj.write("    ItemLevel >= "+str(k)+"\n")
                        write_obj.write("    BaseType =="+LineToWrite+"\n")
                        write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                        write_obj.write("    SetTextColor 0 0 0 255\n")
                        write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                        if str_PlayAlertSound != "":
                            write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                        if EffectToWrite != "":
                            write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                        if IconToWrite != "":
                            write_obj.write("    MinimapIcon "+IconToWrite+"\n")

        # All other influenced items caught here
        write_obj.write("\n")
        write_obj.write("Show\n")
        write_obj.write("    HasInfluence Shaper Elder Crusader Redeemer Hunter Warlord\n")
        write_obj.write("    SetFontSize 39\n")
        write_obj.write("    SetTextColor 0 0 0 255\n")
        write_obj.write("    SetBackgroundColor 28 236 4 215 # Green\n")
        write_obj.write("    PlayAlertSound 9 300\n")
        write_obj.write("    MinimapIcon 2 Green Kite\n")

    print ("Influenced section complete.")

def func_non_influenced():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 14400 Non-influenced bases\n")
        write_obj.write("#####\n")

        print ("Strictness filter is " + str(strOverallStrictness) + " and booShowT11 is " + str(booShowT11))
        for k in range (86, 81, -1):
            LineToWrite = ""
            print("Item level "+str(k))
            for i in range (1,12):
                booHIDE = False
                if (booShowT11 == False) and (i > strOverallStrictness):
                    print ("Hiding tier " + str(i) + ".")
                    booHIDE = True
                if (booShowT11 == True) and (i < 11) and (i > int(strOverallStrictness)):
                    print ("Hiding tier " + str(i) + ".")
                    booHIDE = True

                LineToWrite = ""
                with open(strCSVin, 'r') as read_obj:
                    # Create a csv.reader object from the input file object
                    csv_reader = reader(read_obj)
                    for row in csv_reader:
                        if row[0] == "base":
                            #print(row)
                            str_category = row[0]
                            str_baseType = row[2]
                            str_variant = row[3]
                            str_levelRequired = row[4]
                            str_links = row[5]
                            if row[12] != "":
                                str_Tier = row[12]
                            else:
                                str_Tier = row[11]
                            str_SetFontSize = row[13]
                            str_PlayAlertSound = row[14]
                            str_SetBackgroundColor = row[15]
                            str_PlayEffect = row[16]
                            str_MinimapIcon = row[17]
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
                    if booHIDE == False:
                        print("Showing Tier "+str(i))
                        write_obj.write("Show\n")
                    if booHIDE == True:
                        print("Hiding Tier "+str(i))
                        write_obj.write("Hide\n")
                        write_obj.write("DisableDropSound True\n")
                    write_obj.write("    Rarity Rare\n")
                    write_obj.write("    ItemLevel >= "+str(k)+"\n")
                    write_obj.write("    BaseType =="+LineToWrite+"\n")
                    write_obj.write("    SetFontSize "+FontSizeToWrite+"\n")
                    write_obj.write("    SetTextColor 0 0 0 255\n")
                    write_obj.write("    SetBackgroundColor "+str_SetBackgroundColor+"\n")
                    if str_PlayAlertSound != "":
                        write_obj.write("    PlayAlertSound "+str_PlayAlertSound+"\n")
                    if EffectToWrite != "":
                        write_obj.write("    PlayEffect "+EffectToWrite+"\n")
                    if IconToWrite != "":
                        write_obj.write("    MinimapIcon "+IconToWrite+"\n")

    print ("Non-influenced bases section complete.")

def func_hide_norm():
    global strOverallStrictness
    global strRareCutoff
    global booShowT11
    global strGrayCutoff
    global booShowNM6S
    global booShowNM5S
    all_u_cats = ["uacc","uarm","ufla","ujew","umap","uweap"]

    # Open the input_file in read mode and output_file in write mode
    with open(strTXTout, 'a', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        txt_writer = writer(write_obj)

        # Create section
        write_obj.write("\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 14900 Hide specific normal/magic/rare items. Interesting rares caught at top of filter.\n")
        write_obj.write("##### Sections at top of filter are adjustable, so this section doesn't need to be.\n")
        write_obj.write("\n")
        write_obj.write("Hide\n")
        write_obj.write("    Rarity Normal Magic Rare\n")
        write_obj.write("    Class Abyss Amulets Axes Belts Body Boots Bows Claws Daggers Flasks Gems Gloves Helmets Jewel Maces Quivers Rings Sceptres Shields Staves Swords Wands Warstaves\n")
        write_obj.write("    SetFontSize 18\n")
        write_obj.write("    SetBorderColor 0 0 0 0\n")
        write_obj.write("    SetBackgroundColor 0 0 0 0\n")
        write_obj.write("    DisableDropSound True\n")
        write_obj.write("\n")

        with open(strCSVin, 'r') as read_obj:
            # Create a csv.reader object from the input file object
            csv_reader = reader(read_obj)
            LineToWrite = ""
            for row in csv_reader:
                for cat in all_u_cats:
                    if row[0] == cat and row[11] == "12":
                        str_baseType = row[2]
                        #print(str_baseType)
                        #time.sleep(1)
                        LineToWrite = LineToWrite + ' "' + str_baseType + '"'
        
        if LineToWrite != "":
            write_obj.write("Hide # Explicitly hide all ""Tier 12"" BaseTypes (maxvalue < strGrayCutoff)\n")
            write_obj.write("    Rarity Unique\n")
            write_obj.write("    BaseType =="+LineToWrite+"\n")
            write_obj.write("    SetFontSize 39\n")
            write_obj.write("    DisableDropSound True\n")

        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 15000 Safety Net section - catch anything not caught above\n")
        write_obj.write("##### Using the same settings as FilterBlade so people recognize what this means if they see it.\n")
        write_obj.write("##### NOTE: Known issue: When Perandus coins drop they may get flagged here, but if you pick them up and set\n")
        write_obj.write("##### them down again then the filter will recignize them properly.  Not sure why that happens.\n")
        write_obj.write("#####\n")
        write_obj.write("\n")
        write_obj.write("Show\n")
        write_obj.write("    SetFontSize 45\n")
        write_obj.write("    SetTextColor 255 0 255 255\n")
        write_obj.write("    SetBorderColor 255 0 255 255\n")
        write_obj.write("    SetBackgroundColor 150 50 150 255\n")
        write_obj.write("    PlayAlertSound 3 300\n")
        write_obj.write("    PlayEffect Pink\n")
        write_obj.write("    MinimapIcon 0 Pink Circle\n")
        write_obj.write("\n")
        write_obj.write("################################################################################################################\n")
        write_obj.write("##### 15100 Special thanks!\n")
        write_obj.write("#####\n")
        write_obj.write("##### This project is so new I don't have anyone specific to thank yet.\n")
        write_obj.write("##### If you want to help, you could be the first!\n")
        write_obj.write("\n")
        write_obj.write("\n")
    print ("Hide normal section complete.")

def func_cleanup():
    with open(strTXTout, "r+") as f:
        current_filter = f.read() # read everything in the file
        f.seek(0) # rewind

        # poe.ninja continues to track some items that have been removed from the drop pool
        # We'll remove them here.
        # Format for re.sub() is: re.sub(pattern, replace, string, count=0, flags=0)
        new_filter = re.sub(' "Poison Support"',"",current_filter)
        new_filter = re.sub(' "Lesser Poison Support"',"",new_filter)
        new_filter = re.sub(' ""Blessed Boots"',"",new_filter)

        new_filter = re.sub("\n\n##### Tier 1\n\n#####","\n\n#####",new_filter) # replace unused Tier lines followed by 2 newlines & #####
        new_filter = re.sub("\n\n##### Tier 2\n\n#####","\n\n#####",new_filter) # replace unused Tier lines followed by 2 newlines & #####
        new_filter = re.sub("\n\n##### Tier 3\n\n#####","\n\n#####",new_filter) # replace unused Tier lines followed by 2 newlines & #####
        new_filter = re.sub("\n\n##### Tier 4\n\n#####","\n\n#####",new_filter) # replace unused Tier lines followed by 2 newlines & #####
        new_filter = re.sub("\n\n##### Tier 5\n\n#####","\n\n#####",new_filter) # replace unused Tier lines followed by 2 newlines & #####
        new_filter = re.sub("\n\n##### Tier 6\n\n#####","\n\n#####",new_filter) # replace unused Tier lines followed by 2 newlines & #####
        new_filter = re.sub("\n\n##### Tier 7\n\n#####","\n\n#####",new_filter) # replace unused Tier lines followed by 2 newlines & #####
        new_filter = re.sub("\n\n##### Tier 8\n\n#####","\n\n#####",new_filter) # replace unused Tier lines followed by 2 newlines & #####
        new_filter = re.sub("\n\n##### Tier 9\n\n#####","\n\n#####",new_filter) # replace unused Tier lines followed by 2 newlines & #####
        new_filter = re.sub("\n\n##### Tier 10\n\n#####","\n\n#####",new_filter) # replace unused Tier lines followed by 2 newlines & #####
        new_filter = re.sub("\n\n##### Tier 11\n\n#####","\n\n#####",new_filter) # replace unused Tier lines followed by 2 newlines & #####

        f.write(new_filter) # write the new file

    print ("Cleanup of empty tier sections complete.")

# INITIALIZE NEW FILE - INITIALIZE NEW FILE - INITIALIZE NEW FILE
# INITIALIZE NEW FILE - INITIALIZE NEW FILE - INITIALIZE NEW FILE
# INITIALIZE NEW FILE - INITIALIZE NEW FILE - INITIALIZE NEW FILE
func_init()

# STATIC INTRO - STATIC INTRO - STATIC INTRO - STATIC INTRO - STATIC INTRO
# STATIC INTRO - STATIC INTRO - STATIC INTRO - STATIC INTRO - STATIC INTRO
func_static_intro()

# Want to put currency near the top, as it drops more often than other things. Less time to process the filter.
# But also need to put it below other stackable items that the game may consider currency.

# CONSUMABLES - CONSUMABLES - CONSUMABLES - CONSUMABLES - CONSUMABLES
# CONSUMABLES - CONSUMABLES - CONSUMABLES - CONSUMABLES - CONSUMABLES
# CONSUMABLES - CONSUMABLES - CONSUMABLES - CONSUMABLES - CONSUMABLES
func_frag() # now includes func_scar()
func_oil()
func_inc()
func_foss()
func_ess()
func_div()
func_prop()
func_deli()
func_inv() ####################################################################################################################### Is currently catching all kinds of weird stuff??
func_stacks() # Have to place this above currency for the stacks to work properly
func_curr()
func_vial()
func_heist()
func_watch() # what about unique watchstones?
func_cluster()
func_other()

# Replicas have their own section because they have their own prices
# Replicas have to go above uniques otherwise might match there
func_replica_ujew() # replicas only, can't recognize relics yet
func_replica_ufla() # replicas only, can't recognize relics yet
func_replica_uacc() # replicas only, can't recognize relics yet

# MAPS - MAPS - MAPS - MAPS - MAPS - MAPS - MAPS - MAPS - MAPS - MAPS - MAPS
# MAPS - MAPS - MAPS - MAPS - MAPS - MAPS - MAPS - MAPS - MAPS - MAPS - MAPS
# MAPS - MAPS - MAPS - MAPS - MAPS - MAPS - MAPS - MAPS - MAPS - MAPS - MAPS
# Replica maps are in the replica section, which must stay above this section.
# Unique maps above normal, blighted/influenced maps next
func_replica_umap() # replicas only, can't recognize relics yet
func_umaps()
func_blight_maps_2() ##################################################################### need to filter based on map tier like other maps
func_influenced_maps()
func_normal_maps() # there are no normal replicas

# UNIQUE JEWELS/FLASKS/ACCESSORIES - UNIQUE JEWELS/FLASKS/ACCESSORIES
# UNIQUE JEWELS/FLASKS/ACCESSORIES - UNIQUE JEWELS/FLASKS/ACCESSORIES
# UNIQUE JEWELS/FLASKS/ACCESSORIES - UNIQUE JEWELS/FLASKS/ACCESSORIES
func_ujew() # replicas are filtered out, can't recognize relics yet
func_ufla() # replicas are filtered out, can't recognize relics yet
func_uacc() # replicas are filtered out, can't recognize relics yet

# UNIQUE GEAR - UNIQUE GEAR - UNIQUE GEAR - UNIQUE GEAR - UNIQUE GEAR
# UNIQUE GEAR - UNIQUE GEAR - UNIQUE GEAR - UNIQUE GEAR - UNIQUE GEAR
# UNIQUE GEAR - UNIQUE GEAR - UNIQUE GEAR - UNIQUE GEAR - UNIQUE GEAR
#func_uarm_6() # Once I do catch all 6L and 5L intro I can skip this totally
#func_uarm_5() # Once I do catch all 6L and 5L intro I can skip this totally
func_reparm_0()
func_uarm_0()
#func_uweap_6() # Once I do catch all 6L and 5L intro I can skip this totally
#func_uweap_5() # Once I do catch all 6L and 5L intro I can skip this totally
func_repweap_0()
func_uweap_0()

# Online filter max 500,000 characters, but game can load much larger filter on hard drive.
func_influenced()
func_non_influenced() # Technically we don't need the 5L and 6L sections but this will improve highlighting if they're > Purple

# GEMS - GEMS - GEMS - GEMS - GEMS - GEMS - GEMS - GEMS - GEMS - GEMS - GEMS
# GEMS - GEMS - GEMS - GEMS - GEMS - GEMS - GEMS - GEMS - GEMS - GEMS - GEMS
# GEMS - GEMS - GEMS - GEMS - GEMS - GEMS - GEMS - GEMS - GEMS - GEMS - GEMS
# Have to do gems based on level, quality, & corruption
# Moved near to bottom because there's a lot to scroll through if you're looking for
# something on the other side of it.
func_divergent_gems()
func_anomalous_gems()
func_phantasmal_gems()
func_normal_gems()

# HIDE NORMAL AND MAGIC ITEMS - HIDE NORMAL AND MAGIC ITEMS
# HIDE NORMAL AND MAGIC ITEMS - HIDE NORMAL AND MAGIC ITEMS
# HIDE NORMAL AND MAGIC ITEMS - HIDE NORMAL AND MAGIC ITEMS
func_hide_norm()

# Always do the cleanup last.
func_cleanup()
print('Done!')

# NEEDS WORK - NEEDS WORK - NEEDS WORK - NEEDS WORK - NEEDS WORK
# NEEDS WORK - NEEDS WORK - NEEDS WORK - NEEDS WORK - NEEDS WORK
# NEEDS WORK - NEEDS WORK - NEEDS WORK - NEEDS WORK - NEEDS WORK

# Not sure if these can be used in a filter at all.
# func_beast()
# Might be able to use these for identified items.
# func_ench() 

# Work on GUI - allow reset button to apply changes onscreen
# Work on GUI - Add buttons to second tab
# Work on GUI - Select league
# Are talismans working correctly?

# Stretch goal: Crafting Recipes
# Stretch goal: include filtering identified items by # of T1 mods, T2 mods, etc.
# Stretch goal: hide items where maxvalue < strGrayCutoff

