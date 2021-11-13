import tkinter as tk
import os
import sys
import shutil
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from tkinter import *

in_filename = os.path.join(sys.path[0], "./scripts/00_user_settings.txt")
strLeagueTXTin = os.path.join(sys.path[0], "./scripts/00_league_list.txt")
league_list = []

def initialize():
    print("called")
    # Set defaults
    with open(in_filename, 'w') as f:
        f.write("patch_number: 3.16\n")         # We're setting defaults here. We can't use a variable. User will have to change or update.
        f.write("league_name: 1 Standard\n")
        f.write("t1value: 100\n")
        f.write("t2value: 50\n")
        f.write("t3value: 25\n")
        f.write("t4value: 20\n")
        f.write("t5value: 10\n")
        f.write("t6value: 5\n")
        f.write("t7value: 1\n")
        f.write("t8value: .14\n")
        f.write("t9value: .1\n")
        f.write("t1font: 45\n")
        f.write("t2font: 45\n")
        f.write("t3font: 42\n")
        f.write("t4font: 42\n")
        f.write("t5font: 39\n")
        f.write("t6font: 39\n")
        f.write("t7font: 36\n")
        f.write("t8font: 36\n")
        f.write("t9font: 32\n")
        f.write("t10font: 32\n")
        f.write("t11font: 39\n")
        f.write("Overall Strictness: 10\n")
        f.write("Rare Strictness: 10\n")
        f.write("Non-special Rare cutoff: 0\n")
        f.write("Gray item cutoff: 0\n")
        f.write("Show gray items: True\n")
        f.write("Show Normal/Magic 6-socket items: True\n")
        f.write("Show Normal/Magic 5-link items: True\n")
        f.write("Boost Button (+4 all tiers for league start): False\n")
        f.write("Invert colors: False\n")
        f.write("Chaos Recipe: True\n")
        f.write("Exalt Recipe: True\n")
        f.write("Chromium Recipe: True\n")
        f.write("Misc Recipes: True\n")
        f.write("Hide Corrupted: False\n")
        f.write("Enforce 3L/4L: False\n")
        f.write("Confidence: 2\n")
        f.write("Junk Gem Quality: 0\n")

def load_values():
    global patch_number, league_name, t1font, t1value, t2font, t2value, t3font, t3value, t4font, t4value, t5font, t5value, t6font, t6value, t7font, t7value, t8font, t8value, t9font, t9value, t10font, t11font
    global e12, e13, e22, e23, e32, e33, e42, e43, e52, e53, e62, e63, e72, e73, e82, e83, e92, e93, e102, e112
    global strOverallStrictness, strRareStrictness, strRareCutoff, booShowT11, strGrayCutoff, booShowNM6S, booShowNM5S, boobuttonBB, booInvert, booChaosRec, booExaltRec, booChromRec, booMiscRec, booHideCorr, booEnforce34, strConfidence, strGemQual

    # Get settings in settings file
    with open(in_filename, 'r') as f:
        for line in f:
            if "patch_number: " in line:
                patch_number = (line.split("patch_number: ")[1])
                patch_number = patch_number.strip()
                #print ("patch_number is " + str(patch_number)
            if "league_name: " in line:
                league_name = (line.split("league_name: ")[1])
                league_name = league_name.strip()
                #print ("league_name is " + str(league_name)

            if "t1value: " in line:
                t1value = (line.split("t1value: ")[1])
                t1value = t1value.strip()
                #print ("t1value is " + str(t1value)
            if "t2value: " in line:
                t2value = (line.split("t2value: ")[1])
                t2value = t2value.strip()
                #print ("t2value is " + str(t2value)
            if "t3value: " in line:
                t3value = (line.split("t3value: ")[1])
                t3value = t3value.strip()
                #print ("t3value is " + str(t3value)
            if "t4value: " in line:
                t4value = (line.split("t4value: ")[1])
                t4value = t4value.strip()
                #print ("t4value is " + str(t4value)
            if "t5value: " in line:
                t5value = (line.split("t5value: ")[1])
                t5value = t5value.strip()
                #print ("t5value is " + str(t5value)
            if "t6value: " in line:
                t6value = (line.split("t6value: ")[1])
                t6value = t6value.strip()
                #print ("t6value is " + str(t6value)
            if "t7value: " in line:
                t7value = (line.split("t7value: ")[1])
                t7value = t7value.strip()
                #print ("t7value is " + str(t7value)
            if "t8value: " in line:
                t8value = (line.split("t8value: ")[1])
                t8value = t8value.strip()
                #print ("t8value is " + str(t8value)
            if "t9value: " in line:
                t9value = (line.split("t9value: ")[1])
                t9value = t9value.strip()
                #print ("t9value is " + str(t9value)
            # Get fonts Get fonts Get fonts Get fonts Get fonts Get fonts Get fonts Get fonts Get fonts
            if "t1font: " in line:
                t1font = (line.split("t1font: ")[1])
                t1font = t1font.strip()
                #print ("t1font is " + str(t1font)
            if "t2font: " in line:
                t2font = (line.split("t2font: ")[1])
                t2font = t2font.strip()
                #print ("t2font is " + str(t2font)
            if "t3font: " in line:
                t3font = (line.split("t3font: ")[1])
                t3font = t3font.strip()
                #print ("t3font is " + str(t3font)
            if "t4font: " in line:
                t4font = (line.split("t4font: ")[1])
                t4font = t4font.strip()
                #print ("t4font is " + str(t4font)
            if "t5font: " in line:
                t5font = (line.split("t5font: ")[1])
                t5font = t5font.strip()
                #print ("t5font is " + str(t5font)
            if "t6font: " in line:
                t6font = (line.split("t6font: ")[1])
                t6font = t6font.strip()
                #print ("t6font is " + str(t6font)
            if "t7font: " in line:
                t7font = (line.split("t7font: ")[1])
                t7font = t7font.strip()
                #print ("t7font is " + str(t7font)
            if "t8font: " in line:
                t8font = (line.split("t8font: ")[1])
                t8font = t8font.strip()
                #print ("t8font is " + str(t8font)
            if "t9font: " in line:
                t9font = (line.split("t9font: ")[1])
                t9font = t9font.strip()
                #print ("t9font is " + str(t9font)
            if "t10font: " in line:
                t10font = (line.split("t10font: ")[1])
                t10font = t10font.strip()
                #print ("t10font is " + str(t10font)
            if "t11font: " in line:
                t11font = (line.split("t11font: ")[1])
                t11font = t11font.strip()
                #print ("t11font is " + str(t11font)
            if "Overall Strictness: " in line:
                strOverallStrictness = (line.split("Overall Strictness: ")[1])
                strOverallStrictness = strOverallStrictness.strip()
                #print ("strOverallStrictness is " + strOverallStrictness)
            if "Rare Strictness: " in line:
                strRareStrictness = (line.split("Rare Strictness: ")[1])
                strRareStrictness = strRareStrictness.strip()
                #print ("strRareStrictness is " + strRareStrictness)
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
            if "Show Normal/Magic 5-link items: " in line:
                booShowNM5S = (line.split("Show Normal/Magic 5-link items: ")[1])
                booShowNM5S = booShowNM5S.strip()
                #print ("booShowNM5S is " + booShowNM5S)
            #if "Boost Button (+4 all tiers for league start): " in line:
            #    boobuttonBB = (line.split("Boost Button (+4 all tiers for league start): ")[1])
            #    boobuttonBB = boobuttonBB.strip()
            #    #print ("boobuttonBB is " + boobuttonBB)
            if "Invert colors: " in line:
                booInvert = (line.split("Invert colors: ")[1])
                booInvert = booInvert.strip()
                #print ("booInvert is " + booInvert)
            if "Chaos Recipe: " in line:
                booChaosRec = (line.split("Chaos Recipe: ")[1])
                booChaosRec = booChaosRec.strip()
                #print ("booChaosRec is " + booChaosRec)
            if "Exalt Recipe: " in line:
                booExaltRec = (line.split("Exalt Recipe: ")[1])
                booExaltRec = booExaltRec.strip()
                #print ("booExaltRec is " + booExaltRec)
            if "Chromium Recipe: " in line:
                booChromRec = (line.split("Chromium Recipe: ")[1])
                booChromRec = booChromRec.strip()
                #print ("booChromRec is " + booChromRec)
            if "Misc Recipes: " in line:
                booMiscRec = (line.split("Misc Recipes: ")[1])
                booMiscRec = booMiscRec.strip()
                #print ("booMiscRec is " + booMiscRec)
            if "Hide Corrupted: " in line:
                booHideCorr = (line.split("Hide Corrupted: ")[1])
                booHideCorr = booHideCorr.strip()
                #print ("booHideCorr is " + booHideCorr)
            if "Enforce 3L/4L: " in line:
                booEnforce34 = (line.split("Enforce 3L/4L: ")[1])
                booEnforce34 = booEnforce34.strip()
                #print ("booEnforce34 is " + booEnforce34)
            if "Confidence: " in line:
                strConfidence = (line.split("Confidence: ")[1])
                strConfidence = strConfidence.strip()
                #print ("strConfidence is " + strConfidence)
            if "Junk Gem Quality: " in line:
                strGemQual = (line.split("Junk Gem Quality: ")[1])
                strGemQual = strGemQual.strip()
                #print ("strGemQual is " + strGemQual)

    # Swap 0/1 Boolean values for True/False
    # I probably shouldn't do this but I like seeing True/False in the settings txt file.
    if booShowT11 == "True":
        booShowT11 = "1"
    if booShowT11 == "False":
        booShowT11 = "0"

    if booShowNM6S == "True":
        booShowNM6S = "1"
    if booShowNM6S == "False":
        booShowNM6S = "0"

    if booShowNM5S == "True":
        booShowNM5S = "1"
    if booShowNM5S == "False":
        booShowNM5S = "0"

    #if boobuttonBB == "True":
    #    boobuttonBB = "1"
    #if boobuttonBB == "False":
    #    boobuttonBB = "0"

    if booInvert == "True":
        booInvert = "1"
    if booInvert == "False":
        booInvert = "0"

    if booChaosRec == "True":
        booChaosRec = "1"
    if booChaosRec == "False":
        booChaosRec = "0"

    if booExaltRec == "True":
        booExaltRec = "1"
    if booExaltRec == "False":
        booExaltRec = "0"

    if booChromRec == "True":
        booChromRec = "1"
    if booChromRec == "False":
        booChromRec = "0"

    if booMiscRec == "True":
        booMiscRec = "1"
    if booMiscRec == "False":
        booMiscRec = "0"

    if booHideCorr == "True":
        booHideCorr = "1"
    if booHideCorr == "False":
        booHideCorr = "0"

    if booEnforce34 == "True":
        booEnforce34 = "1"
    if booEnforce34 == "False":
        booEnforce34 = "0"

def save_values():
    global patch_number, league_name, t1font, t1value, t2font, t2value, t3font, t3value, t4font, t4value, t5font, t5value, t6font, t6value, t7font, t7value, t8font, t8value, t9font, t9value, t10font, t11font
    global e12, e13, e22, e23, e32, e33, e42, e43, e52, e53, e62, e63, e72, e73, e82, e83, e92, e93, e102, e112
    global strOverallStrictness, strRareStrictness, strRareCutoff, booShowT11, strGrayCutoff, booShowNM6S, booShowNM5S, boobuttonBB, booInvert, booChaosRec, booExaltRec, booChromRec, booMiscRec, booHideCorr, booEnforce34, strConfidence, strGemQual

    # Get entererd values
    t1value = e13.get()
    t2value = e23.get()
    t3value = e33.get()
    t4value = e43.get()
    t5value = e53.get()
    t6value = e63.get()
    t7value = e73.get()
    t8value = e83.get()
    t9value = e93.get()

    t1font = e12.get()
    t2font = e22.get()
    t3font = e32.get()
    t4font = e42.get()
    t5font = e52.get()
    t6font = e62.get()
    t7font = e72.get()
    t8font = e82.get()
    t9font = e92.get()
    t10font = e102.get()
    t11font = e112.get()

    patch_number = e200b.get()
    selected_league = league_selection.get()

    strOverallStrictness = str(slider1.get())
    strRareStrictness = str(slider6.get())
    strRareCutoff = str(slider2.get())
    booShowT11 = str(buttont11.get())
    strGrayCutoff = str(slider3.get())
    booShowNM6S = str(buttonS6.get())
    booShowNM5S = str(buttonS5.get())
    #boobuttonBB = str(buttonBB.get())
    booInvert = str(InvertButton.get())
    booChaosRec = str(ChaosRecButton.get())
    booExaltRec = str(ExaltRecButton.get())
    booChromRec = str(ChromRecButton.get())
    booMiscRec = str(MiscRecButton.get())
    booHideCorr = str(HideCorrButton.get())
    booEnforce34 = str(Enforce34Button.get())
    strConfidence = str(ConSlider.get())
    strGemQual = str(LoadGemVal.get())

    print ("Patch Number is " + str(e200b.get()))
    print ("Selected League is " + str(league_selection.get()))
    print ("Overall Strictness is " + str(slider1.get()))
    print ("strRareCutoff is " + str(slider2.get()))
    print ("Gray item checkbox is " + str(buttont11.get()))
    print ("strGrayCutoff is " + str(slider3.get()))
    print ("booShowNM6S is " + str(buttonS6.get()))
    print ("booShowNM5S is " + str(buttonS5.get()))
    #print ("boobuttonBB is " + str(buttonBB.get()))
    print ("booInvert is " + str(InvertButton.get()))
    print ("booChaosRec is " + str(ChaosRecButton.get()))
    print ("booExaltRec is " + str(ExaltRecButton.get()))
    print ("booChromRec is " + str(ChromRecButton.get()))
    print ("booMiscRec is " + str(MiscRecButton.get()))
    print ("booHideCorr is " + str(HideCorrButton.get()))
    print ("booEnforce34 is " + str(Enforce34Button.get()))
    print ("strConfidence is " + str(ConSlider.get()))
    print ("strGemQual is " + str(LoadGemVal.get()))

    print ("t1value is " + str(t1value))
    print ("t2value is " + str(t2value))
    print ("t3value is " + str(t3value))
    print ("t4value is " + str(t4value))
    print ("t5value is " + str(t5value))
    print ("t6value is " + str(t6value))
    print ("t7value is " + str(t7value))
    print ("t8value is " + str(t8value))
    print ("t9value is " + str(t9value))

    print ("t1font is " + str(t1font))
    print ("t2font is " + str(t2font))
    print ("t3font is " + str(t3font))
    print ("t4font is " + str(t4font))
    print ("t5font is " + str(t5font))
    print ("t6font is " + str(t6font))
    print ("t7font is " + str(t7font))
    print ("t8font is " + str(t8font))
    print ("t9font is " + str(t9font))
    print ("t10font is " + str(t10font))
    print ("t11font is " + str(t11font))

    # I'll need to move the user settings to a .bak
    # Read in the .bak, do replace() to update certain lines
    # Then write a new user settings file, and delete the .bak

    # Swap 0/1 Boolean values for True/False
    # I probably shouldn't do this but I like seeing True/False in the settings txt file.
    if booShowT11 == "1":
        booShowT11 = "True"
    if booShowT11 == "0":
        booShowT11 = "False"

    if booShowNM6S == "1":
        booShowNM6S = "True"
    if booShowNM6S == "0":
        booShowNM6S = "False"

    if booShowNM5S == "1":
        booShowNM5S = "True"
    if booShowNM5S == "0":
        booShowNM5S = "False"

    #if boobuttonBB == "1":
    #    boobuttonBB = "True"
    #if boobuttonBB == "0":
    #    boobuttonBB = "False"

    if booInvert == "1":
        booInvert = "True"
    if booInvert == "0":
        booInvert = "False"

    if booChaosRec == "1":
        booChaosRec = "True"
    if booChaosRec == "0":
        booChaosRec = "False"

    if booExaltRec == "1":
        booExaltRec = "True"
    if booExaltRec == "0":
        booExaltRec = "False"

    if booChromRec == "1":
        booChromRec = "True"
    if booChromRec == "0":
        booChromRec = "False"

    if booMiscRec == "1":
        booMiscRec = "True"
    if booMiscRec == "0":
        booMiscRec = "False"

    if booHideCorr == "1":
        booHideCorr = "True"
    if booHideCorr == "0":
        booHideCorr = "False"

    if booEnforce34 == "1":
        booEnforce34 = "True"
    if booEnforce34 == "0":
        booEnforce34 = "False"

    with open(in_filename, 'w') as f:
        f.write("patch_number: " + patch_number + "\n")
        f.write("league_name: " + selected_league + "\n")
        f.write("t1value: " + str(t1value) + "\n")
        f.write("t2value: " + str(t2value) + "\n")
        f.write("t3value: " + str(t3value) + "\n")
        f.write("t4value: " + str(t4value) + "\n")
        f.write("t5value: " + str(t5value) + "\n")
        f.write("t6value: " + str(t6value) + "\n")
        f.write("t7value: " + str(t7value) + "\n")
        f.write("t8value: " + str(t8value) + "\n")
        f.write("t9value: " + str(t9value) + "\n")
        f.write("t1font: " + str(t1font) + "\n")
        f.write("t2font: " + str(t2font) + "\n")
        f.write("t3font: " + str(t3font) + "\n")
        f.write("t4font: " + str(t4font) + "\n")
        f.write("t5font: " + str(t5font) + "\n")
        f.write("t6font: " + str(t6font) + "\n")
        f.write("t7font: " + str(t7font) + "\n")
        f.write("t8font: " + str(t8font) + "\n")
        f.write("t9font: " + str(t9font) + "\n")
        f.write("t10font: " + str(t10font) + "\n")
        f.write("t11font: " + str(t11font) + "\n")
        f.write("Overall Strictness: " + strOverallStrictness + "\n")
        f.write("Rare Strictness: " + strRareStrictness + "\n")
        f.write("Non-special Rare cutoff: " + strRareCutoff + "\n")
        f.write("Gray item cutoff: " + strGrayCutoff + "\n")
        f.write("Show gray items: " + booShowT11 + "\n")
        f.write("Show Normal/Magic 6-socket items: " + booShowNM6S + "\n")
        f.write("Show Normal/Magic 5-link items: " + booShowNM5S + "\n")
        #f.write("Boost Button (+4 all tiers for league start): " + boobuttonBB + "\n")
        f.write("Boost Button (+4 all tiers for league start): False\n")
        f.write("Invert colors: " + booInvert + "\n")
        f.write("Chaos Recipe: " + booChaosRec + "\n")
        f.write("Exalt Recipe: " + booExaltRec + "\n")
        f.write("Chromium Recipe: " + booChromRec + "\n")
        f.write("Misc Recipes: " + booMiscRec + "\n")
        f.write("Hide Corrupted: " + booHideCorr + "\n")
        f.write("Enforce 3L/4L: " + booEnforce34 + "\n")
        f.write("Confidence: " + strConfidence + "\n")
        f.write("Junk Gem Quality: " + strGemQual + "\n")

def on_tab_selected(event):
    selected_tab = event.widget.select()
    tab_text = event.widget.tab(selected_tab, "text")

    if tab_text == "TAB-1":
        print("TAB-1 tab selected")
    if tab_text == "TAB-2":
        print("TAB-2 tab selected")
    if tab_text == "TAB-3":
        print("TAB-3 tab selected")

def generate_filter():
    save_values()
    os.system('python ./scripts/010-main.py')

def reset_settings():
    initialize()
    load_values()

##### Need to fix: use float for tier values below 1.0
##### Need to fix: use float for tier values below 1.0
##### Need to fix: use float for tier values below 1.0

# If strLeagueTXTin exists, get the league list. Otherwise call initialize().
if os.path.isfile(strLeagueTXTin):
    with open(strLeagueTXTin, 'r') as f:
        for line in f:
            #print(line)
            league_list = line.split("|")
else:
    os.system('python ./scripts/005-get-leagues.py')
    with open(strLeagueTXTin, 'r') as f:
        for line in f:
            #print(line)
            league_list = line.split("|")

# If in_filename exists load values, otherwise call initialize().
if os.path.isfile(in_filename):
    load_values()
else:
    initialize()
    load_values()

form = tk.Tk()
form.title("Fla_Panther's Super Simple Loot Filter")
form.geometry("750x750")

tab_parent = ttk.Notebook(form)

tab1 = ttk.Frame(tab_parent)
tab2 = ttk.Frame(tab_parent)
tab3 = ttk.Frame(tab_parent)

tab_parent.bind("<<NotebookTabChanged>>", on_tab_selected)
tab_parent.add(tab1, text="Tiers")
tab_parent.add(tab2, text="Settings")
tab_parent.add(tab3, text="Options")

# === WIDGETS FOR TAB ONE === WIDGETS FOR TAB ONE === WIDGETS FOR TAB ONE === WIDGETS FOR TAB ONE
# === WIDGETS FOR TAB ONE === WIDGETS FOR TAB ONE === WIDGETS FOR TAB ONE === WIDGETS FOR TAB ONE
# === WIDGETS FOR TAB ONE === WIDGETS FOR TAB ONE === WIDGETS FOR TAB ONE === WIDGETS FOR TAB ONE

frame0 = tk.Frame(tab1, relief=GROOVE, borderwidth=5)
frame0.grid(row=0, column=0, padx=5, pady=1, sticky = W)

frame000 = tk.Frame(frame0, relief=GROOVE, borderwidth=5)
frame000.grid(row=0, column=0, padx=5, pady=1, sticky = W)

# === ROW 0 === ROW 0 === ROW 0 === ROW 0
row00 = tk.Label(frame000, justify='left', text="Tier  ")
row01 = tk.Label(frame000, justify='left', text="Color  ")
row02 = tk.Label(frame000, justify='left', text="Font Size  ")
row03 = tk.Label(frame000, justify='left', text="Chaos  ")
row04 = tk.Label(frame000, justify='left', text="Map Icon Size  ")

row00.grid(row=0, column=0, padx=5, pady=1, sticky = W)
row01.grid(row=0, column=1, padx=5, pady=1, sticky = W)
row02.grid(row=0, column=2, padx=5, pady=1, sticky = W)
row03.grid(row=0, column=3, padx=5, pady=1, sticky = W)
row04.grid(row=0, column=4, padx=5, pady=1, sticky = W)

# === ROW 1 === ROW 1 === ROW 1 === ROW 1
row10 = tk.Label(frame000, justify='left', text="1")
row11 = tk.Label(frame000, justify='left', text="White")
row12 = tk.Label(frame000, justify='left')
row13 = tk.Label(frame000, justify='left')
row14 = tk.Label(frame000, justify='left', text="0")

e12 = StringVar(value=t1font)
e13 = StringVar(value=t1value)
entry1 = Entry(row12, width=5, textvariable=e12)
entry2 = Entry(row13, width=5, textvariable=e13)

row10.grid(row=1, column=0, padx=5, pady=1, sticky = W)
row11.grid(row=1, column=1, padx=5, pady=1, sticky = W)
row12.grid(row=1, column=2, padx=5, pady=1, sticky = W)
row13.grid(row=1, column=3, padx=5, pady=1, sticky = W)
row14.grid(row=1, column=4, padx=5, pady=1, sticky = W)
entry1.grid(row=1, column=2, padx=5, pady=1, sticky = W)
entry2.grid(row=1, column=3, padx=5, pady=1, sticky = W)

# === ROW 2 === ROW 2 === ROW 2 === ROW 2
row20 = tk.Label(frame000, justify='left', text="2")
row21 = tk.Label(frame000, justify='left', text="Pink")
row22 = tk.Label(frame000, justify='left')
row23 = tk.Label(frame000, justify='left')
row24 = tk.Label(frame000, justify='left', text="0")

e22 = StringVar(value=t2font)
e23 = StringVar(value=t2value)
entry3 = Entry(row22, width=5, textvariable=e22)
entry4 = Entry(row23, width=5, textvariable=e23)

row20.grid(row=2, column=0, padx=5, pady=1, sticky = W)
row21.grid(row=2, column=1, padx=5, pady=1, sticky = W)
row22.grid(row=2, column=2, padx=5, pady=1, sticky = W)
row23.grid(row=2, column=3, padx=5, pady=1, sticky = W)
row24.grid(row=2, column=4, padx=5, pady=1, sticky = W)
entry3.grid(row=2, column=2, padx=5, pady=1, sticky = W)
entry4.grid(row=2, column=3, padx=5, pady=1, sticky = W)

# === ROW 3 === ROW 3 === ROW 3 === ROW 3
row30 = tk.Label(frame000, justify='left', text="3")
row31 = tk.Label(frame000, justify='left', text="Cyan")
row32 = tk.Label(frame000, justify='left')
row33 = tk.Label(frame000, justify='left')
row34 = tk.Label(frame000, justify='left', text="1")

e32 = StringVar(value=t3font)
e33 = StringVar(value=t3value)
entry5 = Entry(row32, width=5, textvariable=e32)
entry6 = Entry(row33, width=5, textvariable=e33)

row30.grid(row=3, column=0, padx=5, pady=1, sticky = W)
row31.grid(row=3, column=1, padx=5, pady=1, sticky = W)
row32.grid(row=3, column=2, padx=5, pady=1, sticky = W)
row33.grid(row=3, column=3, padx=5, pady=1, sticky = W)
row34.grid(row=3, column=4, padx=5, pady=1, sticky = W)
entry5.grid(row=3, column=2, padx=5, pady=1, sticky = W)
entry6.grid(row=3, column=3, padx=5, pady=1, sticky = W)

# === ROW 4 === ROW 4 === ROW 4 === ROW 4
row40 = tk.Label(frame000, justify='left', text="4")
row41 = tk.Label(frame000, justify='left', text="Purple")
row42 = tk.Label(frame000, justify='left')
row43 = tk.Label(frame000, justify='left')
row44 = tk.Label(frame000, justify='left', text="1")

e42 = StringVar(value=t4font)
e43 = StringVar(value=t4value)
entry7 = Entry(row42, width=5, textvariable=e42)
entry8 = Entry(row43, width=5, textvariable=e43)

row40.grid(row=4, column=0, padx=5, pady=1, sticky = W)
row41.grid(row=4, column=1, padx=5, pady=1, sticky = W)
row42.grid(row=4, column=2, padx=5, pady=1, sticky = W)
row43.grid(row=4, column=3, padx=5, pady=1, sticky = W)
row44.grid(row=4, column=4, padx=5, pady=1, sticky = W)
entry7.grid(row=4, column=2, padx=5, pady=1, sticky = W)
entry8.grid(row=4, column=3, padx=5, pady=1, sticky = W)

# === ROW 5 === ROW 5 === ROW 5 === ROW 5
row50 = tk.Label(frame000, justify='left', text="5")
row51 = tk.Label(frame000, justify='left', text="Blue")
row52 = tk.Label(frame000, justify='left')
row53 = tk.Label(frame000, justify='left')
row54 = tk.Label(frame000, justify='left', text="2")

e52 = StringVar(value=t5font)
e53 = StringVar(value=t5value)
entry9 = Entry(row52, width=5, textvariable=e52)
entry10 = Entry(row53, width=5, textvariable=e53)

row50.grid(row=5, column=0, padx=5, pady=1, sticky = W)
row51.grid(row=5, column=1, padx=5, pady=1, sticky = W)
row52.grid(row=5, column=2, padx=5, pady=1, sticky = W)
row53.grid(row=5, column=3, padx=5, pady=1, sticky = W)
row54.grid(row=5, column=4, padx=5, pady=1, sticky = W)
entry9.grid(row=5, column=2, padx=5, pady=1, sticky = W)
entry10.grid(row=5, column=3, padx=5, pady=1, sticky = W)

# === ROW 6 === ROW 6 === ROW 6 === ROW 6
row60 = tk.Label(frame000, justify='left', text="6")
row61 = tk.Label(frame000, justify='left', text="Green")
row62 = tk.Label(frame000, justify='left')
row63 = tk.Label(frame000, justify='left')
row64 = tk.Label(frame000, justify='left', text="2")

e62 = StringVar(value=t6font)
e63 = StringVar(value=t6value)
entry11 = Entry(row62, width=5, textvariable=e62)
entry12 = Entry(row63, width=5, textvariable=e63)

row60.grid(row=6, column=0, padx=5, pady=1, sticky = W)
row61.grid(row=6, column=1, padx=5, pady=1, sticky = W)
row62.grid(row=6, column=2, padx=5, pady=1, sticky = W)
row63.grid(row=6, column=3, padx=5, pady=1, sticky = W)
row64.grid(row=6, column=4, padx=5, pady=1, sticky = W)
entry11.grid(row=6, column=2, padx=5, pady=1, sticky = W)
entry12.grid(row=6, column=3, padx=5, pady=1, sticky = W)

# === ROW 7 === ROW 7 === ROW 7 === ROW 7
row70 = tk.Label(frame000, justify='left', text="7")
row71 = tk.Label(frame000, justify='left', text="Yellow")
row72 = tk.Label(frame000, justify='left')
row73 = tk.Label(frame000, justify='left')
row74 = tk.Label(frame000, justify='left', text="None")

e72 = StringVar(value=t7font)
e73 = StringVar(value=t7value)
entry13 = Entry(row72, width=5, textvariable=e72)
entry14 = Entry(row73, width=5, textvariable=e73)

row70.grid(row=7, column=0, padx=5, pady=1, sticky = W)
row71.grid(row=7, column=1, padx=5, pady=1, sticky = W)
row72.grid(row=7, column=2, padx=5, pady=1, sticky = W)
row73.grid(row=7, column=3, padx=5, pady=1, sticky = W)
row74.grid(row=7, column=4, padx=5, pady=1, sticky = W)
entry13.grid(row=7, column=2, padx=5, pady=1, sticky = W)
entry14.grid(row=7, column=3, padx=5, pady=1, sticky = W)

# === ROW 8 === ROW 8 === ROW 8 === ROW 8
row80 = tk.Label(frame000, justify='left', text="8")
row81 = tk.Label(frame000, justify='left', text="Orange")
row82 = tk.Label(frame000, justify='left')
row83 = tk.Label(frame000, justify='left')
row84 = tk.Label(frame000, justify='left', text="None")

e82 = StringVar(value=t8font)
e83 = StringVar(value=t8value)
entry15 = Entry(row82, width=5, textvariable=e82)
entry16 = Entry(row83, width=5, textvariable=e83)

row80.grid(row=8, column=0, padx=5, pady=1, sticky = W)
row81.grid(row=8, column=1, padx=5, pady=1, sticky = W)
row82.grid(row=8, column=2, padx=5, pady=1, sticky = W)
row83.grid(row=8, column=3, padx=5, pady=1, sticky = W)
row84.grid(row=8, column=4, padx=5, pady=1, sticky = W)
entry15.grid(row=8, column=2, padx=5, pady=1, sticky = W)
entry16.grid(row=8, column=3, padx=5, pady=1, sticky = W)

# === ROW 9 === ROW 9 === ROW 9 === ROW 9
row90 = tk.Label(frame000, justify='left', text="9")
row91 = tk.Label(frame000, justify='left', text="Red")
row92 = tk.Label(frame000, justify='left')
row93 = tk.Label(frame000, justify='left')
row94 = tk.Label(frame000, justify='left', text="None")

e92 = StringVar(value=t9font)
e93 = StringVar(value=t9value)
entry17 = Entry(row92, width=5, textvariable=e92)
entry18 = Entry(row93, width=5, textvariable=e93)

row90.grid(row=9, column=0, padx=5, pady=1, sticky = W)
row91.grid(row=9, column=1, padx=5, pady=1, sticky = W)
row92.grid(row=9, column=2, padx=5, pady=1, sticky = W)
row93.grid(row=9, column=3, padx=5, pady=1, sticky = W)
row94.grid(row=9, column=4, padx=5, pady=1, sticky = W)
entry17.grid(row=9, column=2, padx=5, pady=1, sticky = W)
entry18.grid(row=9, column=3, padx=5, pady=1, sticky = W)

# === ROW 10 === ROW 10 === ROW 10 === ROW 10
row100 = tk.Label(frame000, justify='left', text="10")
row101 = tk.Label(frame000, justify='left', text="Brown")
row102 = tk.Label(frame000, justify='left')
row103 = tk.Label(frame000, justify='left', text="0")
row104 = tk.Label(frame000, justify='left', text="None")

e102 = StringVar(value=t10font)
entry19 = Entry(row102, width=5, textvariable=e102)

row100.grid(row=10, column=0, padx=5, pady=1, sticky = W)
row101.grid(row=10, column=1, padx=5, pady=1, sticky = W)
row102.grid(row=10, column=2, padx=5, pady=1, sticky = W)
row103.grid(row=10, column=3, padx=5, pady=1, sticky = W)
row104.grid(row=10, column=4, padx=5, pady=1, sticky = W)
entry19.grid(row=10, column=2, padx=5, pady=1, sticky = W)

# === ROW 11 === ROW 11 === ROW 11 === ROW 11
row110 = tk.Label(frame000, justify='left', text="11")
row111 = tk.Label(frame000, justify='left', text="Gray")
row112 = tk.Label(frame000, justify='left')
row113 = tk.Label(frame000, justify='left', text="Unknown")
row114 = tk.Label(frame000, justify='left', text="None")

e112 = StringVar(value=t11font)
entry21 = Entry(row112, width=5, textvariable=e112)

row110.grid(row=11, column=0, padx=5, pady=1, sticky = W)
row111.grid(row=11, column=1, padx=5, pady=1, sticky = W)
row112.grid(row=11, column=2, padx=5, pady=1, sticky = W)
row113.grid(row=11, column=3, padx=5, pady=1, sticky = W)
row114.grid(row=11, column=4, padx=5, pady=1, sticky = W)
entry21.grid(row=11, column=2, padx=5, pady=1, sticky = W)

# === LEGEND === LEGEND === LEGEND === LEGEND === LEGEND === LEGEND === LEGEND
# === LEGEND === LEGEND === LEGEND === LEGEND === LEGEND === LEGEND === LEGEND
# === LEGEND === LEGEND === LEGEND === LEGEND === LEGEND === LEGEND === LEGEND
# === LEGEND === LEGEND === LEGEND === LEGEND === LEGEND === LEGEND === LEGEND

frame001 = tk.Frame(frame0, relief=GROOVE, borderwidth=5)
frame001.grid(row=0, column=1, padx=5, pady=1, sticky = W)

# === ROW 0 === ROW 0 === ROW 0 === ROW 0
row30 = tk.Label(frame001, justify='left', text="MiniMap Icon")
row31 = tk.Label(frame001, justify='left', text="Covers these items")

row30.grid(row=0, column=0, padx=5, pady=1, sticky = W)
row31.grid(row=0, column=1, padx=5, pady=1, sticky = W)

# === ROW 1 === ROW 1 === ROW 1 === ROW 1
row32 = tk.Label(frame001, justify='left', text="Diamond")
row33 = tk.Label(frame001, justify='left', text="All Tier 1 Drops")

row32.grid(row=1, column=0, padx=5, pady=1, sticky = W)
row33.grid(row=1, column=1, padx=5, pady=1, sticky = W)

# === ROW 2 === ROW 2 === ROW 2 === ROW 2
row34 = tk.Label(frame001, justify='left', text="Hexagon")
row35 = tk.Label(frame001, justify='left', text="Currencies, Splinters")

row34.grid(row=2, column=0, padx=5, pady=1, sticky = W)
row35.grid(row=2, column=1, padx=5, pady=1, sticky = W)

# === ROW 3 === ROW 3 === ROW 3 === ROW 3
row36 = tk.Label(frame001, justify='left', text="Pentagon")
row37 = tk.Label(frame001, justify='left', text="League Items, Maps")

row36.grid(row=3, column=0, padx=5, pady=1, sticky = W)
row37.grid(row=3, column=1, padx=5, pady=1, sticky = W)

# === ROW 4 === ROW 4 === ROW 4 === ROW 4
row38 = tk.Label(frame001, justify='left', text="Star")
row39 = tk.Label(frame001, justify='left', text="Tier 2-3 Unique items")

row38.grid(row=4, column=0, padx=5, pady=1, sticky = W)
row39.grid(row=4, column=1, padx=5, pady=1, sticky = W)

# === ROW 5 === ROW 5 === ROW 5 === ROW 5
row310 = tk.Label(frame001, justify='left', text="Cross")
row311 = tk.Label(frame001, justify='left', text="All other Unique items")

row310.grid(row=5, column=0, padx=5, pady=1, sticky = W)
row311.grid(row=5, column=1, padx=5, pady=1, sticky = W)

# === ROW 6 === ROW 6 === ROW 6 === ROW 6
row312 = tk.Label(frame001, justify='left', text="Kite")
row313 = tk.Label(frame001, justify='left', text="Veil/Synth/Fract, Influenced, Enchanted Rares")

row312.grid(row=6, column=0, padx=5, pady=1, sticky = W)
row313.grid(row=6, column=1, padx=5, pady=1, sticky = W)

# === ROW 7 === ROW 7 === ROW 7 === ROW 7
row314 = tk.Label(frame001, justify='left', text="Square")
row315 = tk.Label(frame001, justify='left', text="Prophecies, Cards, Oils, Essences, Fossils")

row314.grid(row=7, column=0, padx=5, pady=1, sticky = W)
row315.grid(row=7, column=1, padx=5, pady=1, sticky = W)

# === ROW 8 === ROW 8 === ROW 8 === ROW 8
row316 = tk.Label(frame001, justify='left', text="Triangle")
row317 = tk.Label(frame001, justify='left', text="Jewels, Accessories, all other Rare gear")

row316.grid(row=8, column=0, padx=5, pady=1, sticky = W)
row317.grid(row=8, column=1, padx=5, pady=1, sticky = W)

# === ROW 9 === ROW 9 === ROW 9 === ROW 9
row318 = tk.Label(frame001, justify='left', text="Circle")
row319 = tk.Label(frame001, justify='left', text="Gems, Flasks")

row318.grid(row=9, column=0, padx=5, pady=1, sticky = W)
row319.grid(row=9, column=1, padx=5, pady=1, sticky = W)

# === ROW 10 === ROW 10 === ROW 10 === ROW 10
row320 = tk.Label(frame001, justify='left', text="Raindrop")
row321 = tk.Label(frame001, justify='left', text="User Override Items (recipes, etc)")

row320.grid(row=10, column=0, padx=5, pady=1, sticky = W)
row321.grid(row=10, column=1, padx=5, pady=1, sticky = W)

# === FILLER === FILLER === FILLER === FILLER === FILLER === FILLER
# === FILLER === FILLER === FILLER === FILLER === FILLER === FILLER
row320 = tk.Label(frame001, justify='left')
row321 = tk.Label(frame001, justify='left')
row322 = tk.Label(frame001, justify='left')

row320.grid(row=11, column=0, padx=5, pady=1, sticky = W)
row321.grid(row=12, column=1, padx=5, pady=1, sticky = W)
row322.grid(row=13, column=2, padx=5, pady=1, sticky = W)

# === NOTES === NOTES === NOTES === NOTES === NOTES === NOTES === NOTES
# === NOTES === NOTES === NOTES === NOTES === NOTES === NOTES === NOTES
# === NOTES === NOTES === NOTES === NOTES === NOTES === NOTES === NOTES
# === NOTES === NOTES === NOTES === NOTES === NOTES === NOTES === NOTES

# === ROW 12 === ROW 12 === ROW 12 === ROW 12

frame1 = tk.Frame(tab1, width=700, relief=GROOVE, borderwidth=5)
frame1.grid(row=30, column=0, padx=5, pady=1, sticky = W)

row40 = Frame(frame1)
row40.grid(row=0, column=0, padx=5, pady=1, sticky = W)
Label(row40, justify='left', text='I STRONGLY advise you to NOT change the tiers shown above! Instead, watch the video on my Github page that explains how to\rcreate override settings.\r\rPoE has 11 colors for PlayEffects and MiniMapIcons. My background colors roughly map to theirs. In the future I may add themes like\rFilterBlade has, but I want to try to maintain rough alignment with PoE\'s PlayEffects and MiniMapIcons.\r\rI\'ve ordered the colors to generally follow the rainbow: Red = bad, yellow = maybe, green = good, purple = even better.\rCyan, Pink, and White are above that, and Brown is below Red.\r\rSimilarly, other than Diamond and Raindrop, Minimap Icons go in order from fewest number of sides to highest,\rbut Tier Color will always be the more important indicator.   (Purple Circle > Red Hexagon)\r\rThe settings you see here will be applied across all item types, except T11/Gray/Grey which will only be used for Unique items that share\ra common BaseType. I plan to integrate a feature that will treat these items in a creative way, but it\'s too complex to explain here.\rPlease check my Github for a better description on that.\r\rNOTE: The Reset Settings button below does reset the settings, but you have to close the program and reopen it to see the changes.').pack()

frame2 = tk.Frame(tab1, relief=GROOVE, borderwidth=5)
frame2.grid(row=40, column=0, padx=5, pady=1, sticky = W)

frame200 = tk.Frame(frame2, relief=GROOVE, borderwidth=5)
frame200.grid(row=0, column=0, padx=5, pady=1, sticky = W)

row200a = tk.Label(frame200, justify='left', text="Patch #:")
row200b = tk.Label(frame200, justify='left')

e200b = StringVar(value=patch_number)
entry200b = Entry(row200b, width=5, textvariable=e200b)

row200a.grid(row=0, column=0, padx=5, pady=1, sticky = W)
row200b.grid(row=0, column=1, padx=5, pady=1, sticky = W)
entry200b.grid(row=0, column=1, padx=5, pady=1, sticky = W)

row200c = tk.Label(frame200, justify='left', text="Select League: ")
row200c.grid(row=0, column=2, padx=5, pady=1, sticky = W)

league_selection = StringVar(row200c)
league_selection.set(league_name) # default value
row200d = OptionMenu(frame200, league_selection, *league_list)
row200d.grid(row=0, column=3, padx=5, pady=1, sticky = W)

row201 = Frame(frame200)
row201.grid(row=1, column=0, padx=5, pady=1, sticky = W)
Button(row201, text='Save Settings', command=save_values).pack()

row202 = Frame(frame200)
row202.grid(row=1, column=1, padx=5, pady=1, sticky = W)
Button(row202, text='Reset Settings', command=reset_settings).pack()

row203 = Frame(frame200)
row203.grid(row=1, column=2, padx=5, pady=1, sticky = W)
Button(row203, text='Generate Filter', command=generate_filter).pack()

row204 = tk.Label(frame200, justify='left', text="See FAQ for important notes about these buttons.")
row204.grid(row=2, column=0, padx=5, pady=1, sticky = W, columnspan = 4)

# === POE.NINJA CONFIDENCE === POE.NINJA CONFIDENCE === POE.NINJA CONFIDENCE

frame401 = tk.Frame(frame2, relief=GROOVE, borderwidth=5)
frame401.grid(row=0, column=1, padx=5, pady=1, sticky = W)

labe401 = Label(frame401, justify='left', text="poe.ninja confidence rating (2 is suggested):")
labe401.grid(row=0, column=0, padx=5, pady=1, sticky = W)

ConSlider = Scale(frame401, from_=3, to=1, length=200, tickinterval=1, orient=HORIZONTAL)
ConSlider.set(strConfidence)
ConSlider.grid(row=1, column=0, padx=5, pady=1, sticky = W)

# === WIDGETS FOR TAB TWO === WIDGETS FOR TAB TWO === WIDGETS FOR TAB TWO === WIDGETS FOR TAB TWO
# === WIDGETS FOR TAB TWO === WIDGETS FOR TAB TWO === WIDGETS FOR TAB TWO === WIDGETS FOR TAB TWO
# === WIDGETS FOR TAB TWO === WIDGETS FOR TAB TWO === WIDGETS FOR TAB TWO === WIDGETS FOR TAB TWO

frame0 = tk.Frame(tab2, width=100, height=40, relief=GROOVE, borderwidth=5)
frame0.grid(row=0, column=0, padx=5, pady=1, sticky = W)

# === ROW 0 === ROW 0 === ROW 0 === ROW 0

frame01 = Frame(frame0, relief=GROOVE, borderwidth=5)
frame01.grid(row=0, column=0, padx=5, pady=1, sticky = W)

label01 = Label(frame01, justify='left', text="Overall Filter Strictness - show tiers from 1 (highest) down to:\r(Set to 10 for league start.)")
label01.grid(row=0, column=0, padx=5, pady=1, sticky = W)

slider1 = Scale(frame01, from_=10, to=1, length=535, tickinterval=1, orient=HORIZONTAL)
slider1.set(strOverallStrictness)
slider1.grid(row=1, column=0, padx=5, pady=1, sticky = W)

# === ROW 6 === ROW 6 === ROW 6 === ROW 6

frame06 = Frame(frame0, relief=GROOVE, borderwidth=5)
frame06.grid(row=1, column=0, padx=5, pady=1, sticky = W)

label06 = Label(frame06, justify='left', text="Economy-Based Filter Strictness for non-influenced/synthesized/veiled/fractured Rares:\r(Set to 10 for league start.  See FAQ for some notes about this slider.)")
label06.grid(row=0, column=0, padx=5, pady=1, sticky = W)

slider6 = Scale(frame06, from_=10, to=1, length=535, tickinterval=1, orient=HORIZONTAL)
slider6.set(strRareStrictness)
slider6.grid(row=1, column=0, padx=5, pady=1, sticky = W)

# === ROW 2 === ROW 2 === ROW 2 === ROW 2

frame02 = Frame(frame0, relief=GROOVE, borderwidth=5)
frame02.grid(row=2, column=0, padx=5, pady=1, sticky = W)

label02 = Label(frame02, justify='left', text="ilvl-Based Filter Strictness for non-influenced/veiled/fractured/synthesized Rares not caught elsewhere:\r(Set to 0 for league start.  See FAQ for some notes about this slider.)")
label02.grid(row=0, column=0, padx=5, pady=1, sticky = W)

slider2 = Scale(frame02, from_=0, to=100, length=535, tickinterval=5, orient=HORIZONTAL)
slider2.set(strRareCutoff)
slider2.grid(row=1, column=0, padx=5, pady=1, sticky = W)

# === ROW 3 === ROW 3 === ROW 3 === ROW 3

frame03 = Frame(frame0, relief=GROOVE, borderwidth=5)
frame03.grid(row=3, column=0, padx=5, pady=1, sticky = W)

label03 = Label(frame03, justify='left', text="Set breakpoint for Unique items that share a common base (aka \"Tier 11\", or \"Gray items\"). Check the\rGithub FAQ, as this can have three different effects based on how you set it. Take care setting this\rabove 0, as it may hide Uniques that poe.ninja thinks aren't worth much. Rememeber, poe.ninja's\rpricing is usually for the lowest value, good rolls can fetch much more. Identify and use Awakened\rPoE Trade to price these until you get to know them.\r\rExample: I had this set to 3c, Overall Strictness to 6. The filter hid Unique Hallowed Hybrid flasks\rbecause poe.ninja thought all variants were were worth 2c max, but with good rolls it was worth 10c.")
label03.grid(row=0, column=0, padx=5, pady=1, sticky = W)

slider3 = Scale(frame03, from_=0, to=200, length=535, tickinterval=10, orient=HORIZONTAL)
slider3.set(strGrayCutoff)
slider3.grid(row=1, column=0, padx=5, pady=1, sticky = W)

# === ROW 4 === ROW 4 === ROW 4 === ROW 4
frame04 = Frame(frame0, width=100, relief=GROOVE, borderwidth=5)
frame04.grid(row=4, column=0, padx=5, pady=1, sticky = W)

# BUTTON T11
frame041 = Frame(frame04, width=100, height=50, borderwidth=5)
frame041.grid(row=0, column=0, padx=5, pady=1, sticky = W)

label041 = Label(frame041, justify='left', text="Show T11/Gray items?")
label041.grid(row=0, column=0, padx=5, pady=1, sticky = W)

buttont11 = StringVar(value=booShowT11)
buttonblah1 = Checkbutton(frame041, justify='left', text="Y/N", variable=buttont11)
buttonblah1.grid(row=1, column=0, padx=5, pady=1, sticky = W)

# BUTTON 6S
frame042 = Frame(frame04, width=100, height=50, borderwidth=5)
frame042.grid(row=0, column=1, padx=5, pady=1, sticky = W)

label042 = Label(frame042, justify='left', text="Normal/Magic 6-socket items?")
label042.grid(row=0, column=0, padx=5, pady=1, sticky = W)

buttonS6 = StringVar(value=booShowNM6S)
buttonblah2 = Checkbutton(frame042, justify='left', text="Y/N", variable=buttonS6)
buttonblah2.grid(row=1, column=0, padx=5, pady=1, sticky = W)

# BUTTON 5S
frame043 = Frame(frame04, width=100, height=50, borderwidth=5)
frame043.grid(row=0, column=2, padx=5, pady=1, sticky = W)

label043 = Label(frame043, justify='left', text="Normal/Magic 5-link items?")
label043.grid(row=0, column=0, padx=5, pady=1, sticky = W)

buttonS5 = StringVar(value=booShowNM5S)
buttonblah3 = Checkbutton(frame043, justify='left', text="Y/N", variable=buttonS5)
buttonblah3.grid(row=1, column=0, padx=5, pady=1, sticky = W)

# === ROW 5 === ROW 5 === ROW 5 === ROW 5
frame05 = Frame(frame0, width=1000, relief=GROOVE, borderwidth=5)
frame05.grid(row=5, column=0, padx=5, pady=1, sticky = W)

# BOOST BUTTON
#frame051 = Frame(frame05, width=100, height=50, borderwidth=5)
#frame051.grid(row=0, column=0, padx=5, pady=1, sticky = W)

#label051 = Label(frame051, justify='left', text="+4 all tiers (league start)?")
#label051.grid(row=0, column=0, padx=5, pady=1, sticky = W)

#buttonBB = StringVar(value=boobuttonBB)
#buttonblah4 = Checkbutton(frame051, justify='left', text="Y/N", variable=buttonBB)
#buttonblah4.grid(row=1, column=0, padx=5, pady=1, sticky = W)

# INVERT BUTTON
frame052 = Frame(frame05, width=100, height=50, borderwidth=5)
frame052.grid(row=0, column=1, padx=5, pady=1, sticky = W)

label052 = Label(frame052, justify='left', text="Invert Text & BG Colors?")
label052.grid(row=0, column=0, padx=5, pady=1, sticky = W)

InvertButton = StringVar(value=booInvert)
buttonblah5 = Checkbutton(frame052, justify='left', text="Y/N", variable=InvertButton)
buttonblah5.grid(row=1, column=0, padx=5, pady=1, sticky = W)

# === WIDGETS FOR TAB THREE === WIDGETS FOR TAB THREE === WIDGETS FOR TAB THREE
# === WIDGETS FOR TAB THREE === WIDGETS FOR TAB THREE === WIDGETS FOR TAB THREE
# === WIDGETS FOR TAB THREE === WIDGETS FOR TAB THREE === WIDGETS FOR TAB THREE
# === WIDGETS FOR TAB THREE === WIDGETS FOR TAB THREE === WIDGETS FOR TAB THREE
# === WIDGETS FOR TAB THREE === WIDGETS FOR TAB THREE === WIDGETS FOR TAB THREE

frame0 = tk.Frame(tab3, relief=GROOVE, borderwidth=5)
frame0.grid(row=0, column=0, padx=5, pady=1, sticky = W)

frame000 = tk.Frame(frame0, relief=GROOVE, borderwidth=5)
frame000.grid(row=0, column=0, padx=5, pady=1, sticky = W)

# === FRAME === FRAME === FRAME === FRAME

frame06 = Frame(frame0, width=1000, relief=GROOVE, borderwidth=5)
frame06.grid(row=5, column=0, padx=5, pady=1, sticky = W)

# === ROW 1 === ROW 1 === ROW 1 === ROW 1

# ChaosRec Checkbox
frame061 = Frame(frame06, width=100, height=50, borderwidth=5)
frame061.grid(row=0, column=0, padx=5, pady=1, sticky = W)

label061 = Label(frame061, justify='left', text="Chaos Recipe?")
label061.grid(row=0, column=0, padx=5, pady=1, sticky = W)

ChaosRecButton = StringVar(value=booChaosRec)
buttonblah6 = Checkbutton(frame061, justify='left', text="Y/N", variable=ChaosRecButton)
buttonblah6.grid(row=0, column=1, padx=5, pady=1, sticky = W)

# ExaltRec Checkbox
frame062 = Frame(frame06, width=100, height=50, borderwidth=5)
frame062.grid(row=0, column=1, padx=5, pady=1, sticky = W)

label062 = Label(frame062, justify='left', text="Exalt Recipe?")
label062.grid(row=0, column=0, padx=5, pady=1, sticky = W)

ExaltRecButton = StringVar(value=booExaltRec)
buttonblah7 = Checkbutton(frame062, justify='left', text="Y/N", variable=ExaltRecButton)
buttonblah7.grid(row=0, column=1, padx=5, pady=1, sticky = W)

# === ROW 2 === ROW 2 === ROW 2 === ROW 2

# ChromRec Checkbox
frame063 = Frame(frame06, width=100, height=50, borderwidth=5)
frame063.grid(row=1, column=0, padx=5, pady=1, sticky = W)

label063 = Label(frame063, justify='left', text="Chromium Recipe?")
label063.grid(row=0, column=0, padx=5, pady=1, sticky = W)

ChromRecButton = StringVar(value=booChromRec)
buttonblah8 = Checkbutton(frame063, justify='left', text="Y/N", variable=ChromRecButton)
buttonblah8.grid(row=0, column=1, padx=5, pady=1, sticky = W)

# MiscRec Checkbox
frame063 = Frame(frame06, width=100, height=50, borderwidth=5)
frame063.grid(row=1, column=1, padx=5, pady=1, sticky = W)

label063 = Label(frame063, justify='left', text="Misc Recipes?")
label063.grid(row=0, column=0, padx=5, pady=1, sticky = W)

MiscRecButton = StringVar(value=booMiscRec)
buttonblah9 = Checkbutton(frame063, justify='left', text="Y/N", variable=MiscRecButton)
buttonblah9.grid(row=0, column=1, padx=5, pady=1, sticky = W)

# === ROW 3 === ROW 3 === ROW 3 === ROW 3

# HideCorr Checkbox
frame064 = Frame(frame06, width=100, height=50, borderwidth=5)
frame064.grid(row=2, column=0, padx=5, pady=1, sticky = W)

label064 = Label(frame064, justify='left', text="Hide Corrupted?\r  (not 5L/6L or gems)")
label064.grid(row=0, column=0, padx=5, pady=1, sticky = W)

HideCorrButton = StringVar(value=booHideCorr)
buttonblah9 = Checkbutton(frame064, justify='left', text="Y/N", variable=HideCorrButton)
buttonblah9.grid(row=0, column=1, padx=5, pady=1, sticky = W)

# Enforce34 Checkbox
frame065 = Frame(frame06, width=100, height=50, borderwidth=5)
frame065.grid(row=2, column=1, padx=5, pady=1, sticky = W)

label065 = Label(frame065, justify='left', text="Enforce 3L/4L?\r  (non-special rares)")
label065.grid(row=0, column=0, padx=5, pady=1, sticky = W)

Enforce34Button = StringVar(value=booEnforce34)
buttonblah10 = Checkbutton(frame065, justify='left', text="Y/N", variable=Enforce34Button)
buttonblah10.grid(row=0, column=1, padx=5, pady=1, sticky = W)

# === ROW 4 === ROW 4 === ROW 4 === ROW 4

# Junk Gem Quality Radio buttons
frame070 = Frame(frame06, width=100, height=50, borderwidth=5)
frame070.grid(row=3, column=0, padx=5, pady=1, sticky = W)

LoadGemVal = StringVar(value=strGemQual)
GemRadio1 = Radiobutton(frame070, text="Gem Quality 0+ (league start)", variable=LoadGemVal, value=0)
GemRadio1.pack(anchor = W)
GemRadio2 = Radiobutton(frame070, text="Junk Gem Quality 10+", variable=LoadGemVal, value=10)
GemRadio2.pack(anchor = W)
GemRadio3 = Radiobutton(frame070, text="Junk Gem Quality 20+", variable=LoadGemVal, value=20)
GemRadio3.pack(anchor = W)



# End of tab stuff below this
tab_parent.pack(expand=1, fill='both')
form.mainloop()