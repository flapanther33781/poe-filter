import csv
import requests
import time
import os
import sys
from csv import writer
from csv import reader

# Python
# I know these are all a non-factored mess right now, by design. There are so many
# variations that need to be handled diff ways that it's actually easier to not
# factorize yet. Make sure it all works, then factorize what we can.

# This script:
# 1. Connect to poe.ninja, download current prices for all items they track
# 2. Put all of that information into a spreadsheet.

strCSVout = os.path.join(sys.path[0], "z015_compiled.csv")

def func_get_league():
    strUserSettings = os.path.join(sys.path[0], "00_user_settings.txt")
    strLeagueList = os.path.join(sys.path[0], "00_league_list.txt")
    global league_name, maps_for_league

    # Overwrite defaults if found in settings file
    with open(strUserSettings, 'r') as f:
        for line in f:
            if "league_name: " in line:
                temp = (line.split("league_name: ")[1])
                if "1 " in temp:
                    league_name = temp.strip("1 ")
                    league_name = league_name.strip()
                if "2 " in temp:
                    league_name = temp.strip("2 ")
                    league_name = league_name.strip()
                if "3 " in temp:
                    league_name = temp.strip("3 ")
                    league_name = league_name.strip()
                if "4 " in temp:
                    league_name = temp.strip("4 ")
                    league_name = league_name.strip()
                print ("league_name is " + league_name)

    # We need to get the Softcore Challenge League to get pricing info on league maps
    # because poe.ninja only tracks maps from PAST legues in their "Standard" league data.
    with open(strLeagueList, 'r') as f2:
        maps_for_league = ""
        for line in f2:
            if "|3 " in line:
                maps_for_league = (line.split("|3 ")[1])
                maps_for_league = (maps_for_league.split("|4 ")[0])
                maps_for_league = maps_for_league.strip()
        if maps_for_league == "":
            maps_for_league = "Standard"
            print("00_league_list.txt was not filled properly. We're either between leagues or poe.ninja's having some error.")
            print("We'll move forward only getting maps for Standard league.  League maps will be error-pink but it's better than failing here.")

    #print(maps_for_league)
    #time.sleep(10)

def func_init():
    global csv_writer
    # Initialize the document
    with open(strCSVout, 'w', newline='') as write_obj:

        # Create a csv.writer object from the output file object
        csv_writer = writer(write_obj)
        row = ["category"]
        
        # Append new column headers to the first row
        row.append("name")
        row.append("baseType")
        row.append("variant")
        row.append("levelRequired")
        row.append("links")
        row.append("corrupted")
        row.append("mapTier")
        row.append("gemLevel")
        row.append("gemQuality")
        row.append("chaosEquivalent")
        row.append("Tier")
        row.append("Override")
        row.append("count")
        row.append("SetFontSize")
        row.append("PlayAlertSound")
        row.append("SetBackgroundColor")
        row.append("PlayEffect")
        row.append("MinimapIcon")
        # Add the updated row / list to the output file
        csv_writer.writerow(row)

def func_currency(category, URL):
    global csv_writer
    # send get request and save response
    r = requests.get(url = URL)
      
    # extract data as json
    json_data = r.json()

    with open(strCSVout, 'a', newline='') as write_obj:
        # Create a csv.writer object from the output file object
        csv_writer = writer(write_obj)

        # iterate through each item and add name and values as row
        for item in json_data["lines"]:
            if item["currencyTypeName"] != "Scroll of Wisdom":
                row = [category]
                row.append(item["currencyTypeName"])
                row.append("")
                row.append("")
                row.append("")
                row.append("")
                row.append("")
                row.append("")
                row.append("")
                row.append("")
                row.append(item["chaosEquivalent"])
                row.append("")
                row.append("")
                row.append("99")
                row.append("")
                row.append("")
                row.append("")
                row.append("")
                print (row)
                # Add the updated row / list to the output file
                csv_writer.writerow(row)

        # Have to block out Scrolls of Wisdom above and add here
        # Because otherwise they'll be in the final file twice (under curr & frags), not sure why poe.ninja's doing that.
        if category == "curr":
            row = [category,"Scroll of Wisdom","","","","","","","","",".1","","","99","","","","",""]
            csv_writer.writerow(row)
            row = [category,"Portal Scroll","","","","","","","","",".1","","","99","","","","",""]
            csv_writer.writerow(row)

        # Have to manually add these orbs???
        if category == "curr":
            row = [category,"Chaos Orb","","","","","","","","","1","","","99","","","","",""]
            csv_writer.writerow(row)
            # These are now showing up
            #row = [category,"Instilling Orb","","","","","","","","","1","","","99","","","","",""]
            #csv_writer.writerow(row)
            #row = [category,"Enkindling Orb","","","","","","","","","1","","","99","","","","",""]
            #csv_writer.writerow(row)

        # Have to manually add these shards???
        if category == "curr":
            # More than .10
            row = [category,"Ancient Shard","","","","","","","","",".5","","","99","","","","",""]
            csv_writer.writerow(row)
            row = [category,"Rogue's Marker","","","","","","","","",".2","","","99","","","","",""]
            csv_writer.writerow(row)
            row = [category,"Ritual Splinter","","","","","","","","",".5","","","99","","","","",""]
            csv_writer.writerow(row)
            row = [category,"Harbinger's Shard","","","","","","","","",".15","","","99","","","","",""]
            csv_writer.writerow(row)

            # More than .01
            row = [category,"Alteration Shard","","","","","","","","",".05","","","99","","","","",""]
            csv_writer.writerow(row)
            row = [category,"Chaos Shard","","","","","","","","",".05","","","99","","","","",""]
            csv_writer.writerow(row)
            row = [category,"Engineer's Shard","","","","","","","","",".05","","","99","","","","",""]
            csv_writer.writerow(row)
            row = [category,"Regal Shard","","","","","","","","",".05","","","99","","","","",""]
            csv_writer.writerow(row)

            # Others
            row = [category,"Horizon Shard","","","","","","","","",".001","","","99","","","","",""]
            csv_writer.writerow(row)
            row = [category,"Alchemy Shard","","","","","","","","",".001","","","99","","","","",""]
            csv_writer.writerow(row)
            row = [category,"Binding Shard","","","","","","","","",".001","","","99","","","","",""]
            csv_writer.writerow(row)
            row = [category,"Transmutation Shard","","","","","","","","",".001","","","99","","","","",""]
            csv_writer.writerow(row)

        # Have to manually add stuff to frags category too.
        if category == "frag":
            row = [category,"Chronicle of Atzoatl","","","","","","","","","10","","","99","","","","",""]
            csv_writer.writerow(row)
            row = [category,"Inscribed Ultimatum","","","","","","","","","1","","","99","","","","",""]
            csv_writer.writerow(row)

        # Have to manually add stuff to arts category too.
        if category == "curr":
            row = [category,"Greater Broken Circle Artifact","","","","","","","","",".01","","","99","","","","",""]
            csv_writer.writerow(row)
            row = [category,"Inscribed Ultimatum","","","","","","","","","1","","","99","","","","",""]
            csv_writer.writerow(row)

def func_other(category, URL):
    global csv_writer
    # send get request and save response
    r = requests.get(url = URL)
      
    # extract data as json
    json_data = r.json()

    with open(strCSVout, 'a', newline='') as write_obj:
        # Create a csv.writer object from the output file object
        csv_writer = writer(write_obj)

        # iterate through each item and add name and values as row
        for item in json_data["lines"]:
            #if "Crack Mace" in item["name"]:
            #    print()
            #    print(item)
            #    print()
            #    #time.sleep(10)

            # We'll replace commas in item names with && for now, then put them back later.
            if ", " in item["name"]:
                item["name"] = item["name"].replace(", ", "&&")
            # PoE filter can't handle ö, must replace with o
            if "Maelström" in item["name"]:
                item["name"] = item["name"].replace("Maelström", "Maelstrom")
            if "baseType" in item:
                if item["baseType"] != "":
                    if "Maelström" in item["baseType"]:
                        item["baseType"] = item["baseType"].replace("Maelström", "Maelstrom")

            # Move UberBlightedMap and Scourged maps to their own categories
            if (category == "map" or category == "blight") and "Blight-ravaged" in item["name"]:
                #print()
                #print(item)
                #print()
                #time.sleep(5)
                row = ["ubermap"]
                item["name"] = item["name"].replace("Blight-ravaged ", "")
                item["baseType"] = item["baseType"].replace("Blight-ravaged ", "")
                #print()
                #print(item)
                #print()
                #time.sleep(5)
            elif (category == "map" or category == "blight") and "Scourged" in item["name"]:
                #print()
                #print(item)
                #print()
                #time.sleep(5)
                row = ["scourgemap"]
                item["name"] = item["name"].replace("Scourged ", "")
                item["baseType"] = item["baseType"].replace("Scourged ", "")
                #print()
                #print(item)
                #print()
                #time.sleep(5)
            else:
                row = [category]


            row.append(item["name"])
            if "baseType" in item: row.append(item["baseType"])
            else: row.append("")
            ############# If it has a variant, then append ' otherwise Excel converts to date when opened
            ############# EXCEPT if it's a map or blight map, in which case don't append the ` and remove the leading comma
            if "variant" in item:
                if category == "map" or category == "blight" or category == "scourgemap":
                    item["variant"] = item["variant"].replace(", ", "")
                    row.append(item["variant"])
                else:
                    row.append("'"+item["variant"])
            else: row.append("")

            if "levelRequired" in item: row.append(item["levelRequired"])
            else: row.append("")
            if "links" in item: row.append(item["links"])
            else: row.append("")
            if "corrupted" in item: row.append(item["corrupted"])
            else: row.append("")
            if "mapTier" in item: row.append(item["mapTier"])
            else: row.append("")
            if "gemLevel" in item: row.append(item["gemLevel"])
            else: row.append("")
            if "gemQuality" in item: row.append(item["gemQuality"])
            else: row.append("")
            if "chaosEquivalent" in item: row.append(item["chaosEquivalent"])
            elif "chaosValue" in item: row.append(item["chaosValue"])
            else: row.append("")
            row.append("")
            row.append("")
            if "count" in item: row.append(item["count"])
            else: row.append("")
            row.append("")
            row.append("")
            row.append("")
            row.append("")
            row.append("")
            #print (row)

            # Add the updated row / list to the output file
            csv_writer.writerow(row)

# Main starts here
# Main starts here
# Main starts here

func_init()
func_get_league()

print("League is: " + league_name)

dictURLS = {
    'arts' : 'https://poe.ninja/api/data/ItemOverview?league=' + league_name + '&type=Artifact&language=en',
    'base' : 'https://poe.ninja/api/data/itemoverview?league=' + league_name + '&type=BaseType',
    'beast' : 'https://poe.ninja/api/data/itemoverview?league=' + league_name + '&type=Beast',
    'clus' : 'https://poe.ninja/api/data/ItemOverview?league=' + league_name + '&type=ClusterJewel&language=en',
    'curr' : 'https://poe.ninja/api/data/currencyoverview?league=' + league_name + '&type=Currency',
    'deli' : 'https://poe.ninja/api/data/ItemOverview?league=' + league_name + '&type=DeliriumOrb&language=en',
    'div' : 'https://poe.ninja/api/data/itemoverview?league=' + league_name + '&type=DivinationCard',
    'ess' : 'https://poe.ninja/api/data/itemoverview?league=' + league_name + '&type=Essence',
    'foss' : 'https://poe.ninja/api/data/itemoverview?league=' + league_name + '&type=Fossil',
    'frag' : 'https://poe.ninja/api/data/currencyoverview?league=' + league_name + '&type=Fragment',
    'gem' : 'https://poe.ninja/api/data/itemoverview?league=' + league_name + '&type=SkillGem',
    'inc' : 'https://poe.ninja/api/data/itemoverview?league=' + league_name + '&type=Incubator',
    'inv' : 'https://poe.ninja/api/data/ItemOverview?league=' + league_name + '&type=Invitation&language=en',
    'oil' : 'https://poe.ninja/api/data/itemoverview?league=' + league_name + '&type=Oil',
    'prop' : 'https://poe.ninja/api/data/itemoverview?league=' + league_name + '&type=Prophecy',
    'res' : 'https://poe.ninja/api/data/itemoverview?league=' + league_name + '&type=Resonator',
    'scar' : 'https://poe.ninja/api/data/itemoverview?league=' + league_name + '&type=Scarab',
    'uacc' : 'https://poe.ninja/api/data/itemoverview?league=' + league_name + '&type=UniqueAccessory',
    'uarm' : 'https://poe.ninja/api/data/itemoverview?league=' + league_name + '&type=UniqueArmour',
    'ufla' : 'https://poe.ninja/api/data/itemoverview?league=' + league_name + '&type=UniqueFlask',
    'ujew' : 'https://poe.ninja/api/data/itemoverview?league=' + league_name + '&type=UniqueJewel',
    'umap' : 'https://poe.ninja/api/data/itemoverview?league=' + league_name + '&type=UniqueMap',
    'uweap' : 'https://poe.ninja/api/data/itemoverview?league=' + league_name + '&type=UniqueWeapon',
    'vial' : 'https://poe.ninja/api/data/ItemOverview?league=' + league_name + '&type=Vial&language=en',
    'watch' : 'https://poe.ninja/api/data/ItemOverview?league=' + league_name + '&type=Watchstone&language=en',
    # Keeping these separate in the list because these must reference the latest league
    # If not then we get results of maps from all past leagues
    'map' : 'https://poe.ninja/api/data/ItemOverview?league=' + maps_for_league + '&type=Map',
    'blight' : 'https://poe.ninja/api/data/ItemOverview?league=' + maps_for_league + '&type=BlightedMap',

    # Can't do anything with this right now.
    # 'ench' : 'https://poe.ninja/api/data/itemoverview?league=' + league_name + '&type=HelmetEnchant'
}

for urlpair in dictURLS.items():
    category = urlpair[0] ; URL = urlpair[1]
    print (category)
    print (URL)
    if category == "curr" or category == "frag":
        func_currency(category, URL)
    else:
        func_other(category, URL)
print('Done!')
