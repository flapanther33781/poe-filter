import os
import requests
import sys
from csv import writer

league_list = ""
strTXTout = os.path.join(sys.path[0], "00_league_list.txt")
url = 'https://www.pathofexile.com/api/leagues'
my_headers = {'user-agent': 'my-app/0.0.1'}
response = requests.get(url, headers = my_headers)

# If request was successful
if (response.status_code == 200):
    json_data = response.json()

    # and if league is not a special league
    for item in json_data:
        if "SSF" not in item["id"] and "Gauntlet" not in item["id"] and "Royale" not in item["id"]:
            #print(item["id"])
            # then add it to league_list and use a pipe as a delimiter
            if league_list == "":
                league_list = item["id"]
            else:
                league_list = league_list + "|" + item["id"]

    #print(league_list)
    # Check for the correct/expected number of leagues
    if len(league_list) - len(league_list.replace("|", "")) == 3:
        print("Found correct/expected # of leagues. Writing to file.")

        # Open the input_file in read mode and output_file in write mode
        with open(strTXTout, 'w', newline='') as write_obj:
            # Create a writer object from the output file object
            txt_writer = writer(write_obj)
            write_obj.write(league_list)
    else:
        # If we find an unexpected # of leagues overwrite the .txt, forcing the program to break.
        print("Found an unexpected # of leagues.  Please alert the developer.")
        # Open the input_file in read mode and output_file in write mode
        with open(strTXTout, 'w', newline='') as write_obj:
            # Create a writer object from the output file object
            txt_writer = writer(write_obj)
            write_obj.write("Error")
