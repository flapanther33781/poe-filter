import csv
import requests
import time
from csv import writer
from csv import reader

# Python
# I know these are all a non-factored mess right now, by design. There are so many
# variations that need to be handled diff ways that it's actually easier to not
# factorize yet. Make sure it all works, then factorize what we can.

# This script:
# 1. Connect to poe.ninja, download current prices for all items they track
# 2. Put all of that information into a spreadsheet.

dictURLS = {
    'arts' : 'https://poe.ninja/api/data/ItemOverview?league=Expedition&type=Artifact&language=en',
    'base' : 'https://poe.ninja/api/data/itemoverview?league=Expedition&type=BaseType',
    'beast' : 'https://poe.ninja/api/data/itemoverview?league=Expedition&type=Beast',
    'clus' : 'https://poe.ninja/api/data/ItemOverview?league=Expedition&type=ClusterJewel&language=en',
    'curr' : 'https://poe.ninja/api/data/currencyoverview?league=Expedition&type=Currency',
    'deli' : 'https://poe.ninja/api/data/ItemOverview?league=Expedition&type=DeliriumOrb&language=en',
    'div' : 'https://poe.ninja/api/data/itemoverview?league=Expedition&type=DivinationCard',
    'ess' : 'https://poe.ninja/api/data/itemoverview?league=Expedition&type=Essence',
    'foss' : 'https://poe.ninja/api/data/itemoverview?league=Expedition&type=Fossil',
    'frag' : 'https://poe.ninja/api/data/currencyoverview?league=Expedition&type=Fragment',
    'gem' : 'https://poe.ninja/api/data/itemoverview?league=Expedition&type=SkillGem',
    'inc' : 'https://poe.ninja/api/data/itemoverview?league=Expedition&type=Incubator',
    'inv' : 'https://poe.ninja/api/data/ItemOverview?league=Expedition&type=Invitation&language=en',
    'oil' : 'https://poe.ninja/api/data/itemoverview?league=Expedition&type=Oil',
    'prop' : 'https://poe.ninja/api/data/itemoverview?league=Expedition&type=Prophecy',
    'res' : 'https://poe.ninja/api/data/itemoverview?league=Expedition&type=Resonator',
    'scar' : 'https://poe.ninja/api/data/itemoverview?league=Expedition&type=Scarab',
    'uacc' : 'https://poe.ninja/api/data/itemoverview?league=Expedition&type=UniqueAccessory',
    'uarm' : 'https://poe.ninja/api/data/itemoverview?league=Expedition&type=UniqueArmour',
    'ufla' : 'https://poe.ninja/api/data/itemoverview?league=Expedition&type=UniqueFlask',
    'ujew' : 'https://poe.ninja/api/data/itemoverview?league=Expedition&type=UniqueJewel',
    'umap' : 'https://poe.ninja/api/data/itemoverview?league=Expedition&type=UniqueMap',
    'uweap' : 'https://poe.ninja/api/data/itemoverview?league=Expedition&type=UniqueWeapon',
    'vial' : 'https://poe.ninja/api/data/ItemOverview?league=Expedition&type=Vial&language=en',
    'watch' : 'https://poe.ninja/api/data/ItemOverview?league=Expedition&type=Watchstone&language=en',
    # Keeping these separate in the list because these must reference the latest league
    # If not then we get results of maps from all past leagues
    'map' : 'https://poe.ninja/api/data/ItemOverview?league=Expedition&type=Map',
    'blight' : 'https://poe.ninja/api/data/ItemOverview?league=Expedition&type=BlightedMap',

    # Can't do anything with this right now.
    # 'ench' : 'https://poe.ninja/api/data/itemoverview?league=Expedition&type=HelmetEnchant'
}

strCSVout = r'E:\PoE Stuff\Filters\1\exp\015_compiled.csv'

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
        row.append("itemType")
        row.append("variant")
        row.append("detailsId")
        row.append("levelRequired")
        row.append("links")
        row.append("corrupted")
        row.append("mapTier")
        row.append("gemLevel")
        row.append("gemQuality")
        row.append("chaosEquivalent")
        row.append("Tier")
        row.append("Override")
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
                row.append("")
                row.append("")
                row.append(item["chaosEquivalent"])
                row.append("")
                row.append("")
                row.append("")
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
            row = [category,"Scroll of Wisdom","","","","","","","","","","",".1","","","","","","",""]
            csv_writer.writerow(row)

        # Have to manually add these orbs???
        if category == "curr":
            row = [category,"Chaos Orb","","","","","","","","","","","1","","","","","","",""]
            csv_writer.writerow(row)
            row = [category,"Instilling Orb","","","","","","","","","","","1","","","","","","",""]
            csv_writer.writerow(row)
            row = [category,"Enkindling Orb","","","","","","","","","","","1","","","","","","",""]
            csv_writer.writerow(row)

        # Have to manually add these shards???
        if category == "curr":
            # More than .10
            row = [category,"Ancient Shard","","","","","","","","","","",".5","","","","","","",""]
            csv_writer.writerow(row)
            row = [category,"Rogue's Marker","","","","","","","","","","",".2","","","","","","",""]
            csv_writer.writerow(row)
            row = [category,"Ritual Splinter","","","","","","","","","","",".5","","","","","","",""]
            csv_writer.writerow(row)
            row = [category,"Harbinger's Shard","","","","","","","","","","",".15","","","","","","",""]
            csv_writer.writerow(row)

            # More than .01
            row = [category,"Alteration Shard","","","","","","","","","","",".05","","","","","","",""]
            csv_writer.writerow(row)
            row = [category,"Chaos Shard","","","","","","","","","","",".05","","","","","","",""]
            csv_writer.writerow(row)
            row = [category,"Engineer's Shard","","","","","","","","","","",".05","","","","","","",""]
            csv_writer.writerow(row)
            row = [category,"Regal Shard","","","","","","","","","","",".05","","","","","","",""]
            csv_writer.writerow(row)

            # Others
            row = [category,"Horizon Shard","","","","","","","","","","",".001","","","","","","",""]
            csv_writer.writerow(row)
            row = [category,"Alchemy Shard","","","","","","","","","","",".001","","","","","","",""]
            csv_writer.writerow(row)
            row = [category,"Binding Shard","","","","","","","","","","",".001","","","","","","",""]
            csv_writer.writerow(row)
            row = [category,"Transmutation Shard","","","","","","","","","","",".001","","","","","","",""]
            csv_writer.writerow(row)

        # Have to manually add stuff to frags category too.
        if category == "frag":
            row = [category,"Chronicle of Atzoatl","","","","","","","","","","","10","","","","","","",""]
            csv_writer.writerow(row)
            row = [category,"Inscribed Ultimatum","","","","","","","","","","","1","","","","","","",""]
            csv_writer.writerow(row)

        # Have to manually add stuff to arts category too.
        if category == "curr":
            row = [category,"Greater Broken Circle Artifact","","","","","","","","","","",".01","","","","","","",""]
            csv_writer.writerow(row)
            row = [category,"Inscribed Ultimatum","","","","","","","","","","","1","","","","","","",""]
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
            if "Maelström" in item["name"]:
                item["name"] = item["name"].replace("Maelström", "Maelstrom")
            if "baseType" in item:
                if item["baseType"] != "":
                    if "Maelström" in item["baseType"]:
                        item["baseType"] = item["baseType"].replace("Maelström", "Maelstrom")

            row = [category]
            row.append(item["name"])
            if "baseType" in item: row.append(item["baseType"])
            else: row.append("")
            if "itemType" in item: row.append(item["itemType"])
            else: row.append("")
            if "variant" in item: row.append("'"+item["variant"]) ############# Must append ' otherwise Excel converts to date when opened
            else: row.append("")
            if "detailsId" in item: row.append(item["detailsId"])
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
            row.append("")
            row.append("")
            row.append("")
            row.append("")
            row.append("")
            print (row)

            # Add the updated row / list to the output file
            csv_writer.writerow(row)

# Main starts here
# Main starts here
# Main starts here

func_init()
for urlpair in dictURLS.items():
    category = urlpair[0] ; URL = urlpair[1]
    print (category)
    print (URL)
    if category == "curr" or category == "frag":
        func_currency(category, URL)
    else:
        func_other(category, URL)
print('Done!')









