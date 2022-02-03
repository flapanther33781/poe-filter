# Fla_Panther's Super Simple Loot Filter

## This tool is on hiatus.

Unfortunately poe.ninja doesn't work the way I thought it did.
- They do not keep a database of all items, they only gather data from items if they're listed on the trade site.  If an item is not on the trade site there is no baseline, it will simply not exist in the filter.  So I'll need to create a baseline and incorporate it into the tool.
- I'd thought base really meant base, but it does not.  Their pricing mechanism for non-special bases includes all Normal/Magic/Rares of that base, which throws off the pricing for the items.  Rare items with good mods skew the items high, so we cannot assume that Normal/Magic items will fetch that price.  As a possible workaround I've asked the person who runs poe.ninja to create a new `variant` field in his output that tracks only Normal & Magic items but he has not yet agreed to this.
- Having used this filter for a league or two now I've learned of what I call the 1c/5c wastelands (which I describe in the FAQ below).  Because of these a good filter needs to be manually curated more than I thought.  That's not impossible, but it's depressing because that defeats the purpose of having a tool to automate filter building.  I may be able to create a mechanism that allows an item's price to rise in the filter if and only if poe.ninja shows the item as being higher than 1c or something, but I will need to code that and test it.

Unfortunately my father's cancer has also returned, and I have other personal matters that are more pressing.  So I have to set this aside for now.  I'll try to work on it a bit here and there but I'll probably not be ready in time for league start, and if I play at all it'll probably only be to test a few things.  I can't give PoE much time right now.

#### Current Features:

- Creates filters based on pricing from poe.ninja (now includes confidence!)
- Universal tiering (tiers set for all items in one place)
- Adjustable strictness - for all item classes, in one place!
- Borders indicate item size (# of inventory slots) to assist with loot choices
- Manual overrides possible, and tool respects overrides for later filters
- Filter non-special bases by value, ilvl, or both
- Further filter non-special 1x3 and 2x2 bases by enforcing max links
- Option to hide corrupted (other than 5L, 6L, or gems)
- Filter uniques differently based on the value of their basetypes
- Swap for colored font on black background
- A few recipes (chaos, exalt, chromium, etc)
- Semi-adjustable gem quality for GCP recipes
- Drop sounds: more expensive items use the heavier sounds!!!
- Possibly useable by Magic Find players as well (see FAQ).

#### Planned features:

- Filter currency based on stack sizes
- Allow custom color selections

#### Features I'm considering:

- Additional vendor recipies, with checkboxes (handy for challenges - some added)
- Separate sliders for gems/cards/prophs/etc.
- Include filtering identified items by # of T1 mods, T2 mods, etc

#### New League update: Please check the FAQ below for notes on my plans for adding the new items for this league.

#### My eventual goal is to make this an executable program anyone can run, but in its current stage you need to install Python and one dependency. There is a 6-minute video linked in the FAQ at the bottom of the page that shows how to do this.  If you don't want to install the program just download the .filter files shown above.  There's a legend at the bottom of the FAQ that explains what the filenames mean and what's in each filter.

#### Here is a quick video showing the filter in action (right-click and open in a new tab) - also, I did fix the black on black thing:

[![Quick Intro Video](https://user-images.githubusercontent.com/26362032/137053308-877ea63d-dff5-4b70-bc66-728936d0ee03.png)](https://youtu.be/3RdbGLjCu5g)

#### Here is a more in-depth introduction video (right-click and open in a new tab):

[![Introduction/Demo Video](https://user-images.githubusercontent.com/26362032/131201669-a51e130b-bd84-4dda-9e9c-52ba96e558f2.png)](https://youtu.be/-kXiwg55DLI)

#### NOTE: THIS TOOL IS IN AN --ALPHA-- STAGE, NOT EVEN BETA. THE CODE & GUI ARE UGLY BUT THEY WILL CHANGE.
#### GETTING EVERYTHING WORKING RIGHT IS THE FIRST PRIORITY, MAKING THE CODE/GUI LOOK NICE WILL COME LATER.

## The first goal for this filter was to make it as simple as possible.

A quick thank you to StupidFatHobbit and the guys over at FilterBlade, you all taught me a lot. This filter isn't meant to replace theirs. This filter is for VERY new players who aren't ready for racing, crafting, hardcore, SSF, or build-specific highlighting - seriously, just THE MOST BASIC filter possible.

Due to not showing those items **this filter** will be more strict than theirs, and **does NOT use combinations of background color, text color, or border color when displaying an item (except for items that normally drop with borders - but you can ignore them).  The background color is based on softcore market prices obtained from poe.ninja.**  (Yes, experienced players know poe.ninja's pricing isn't perfect, but for a completely new player it's good enough to start with. Anyway, this tool also allows you to do manual overrides.)

I may add other schemes later, but for now this is what it looks like:

![01](https://user-images.githubusercontent.com/26362032/136266615-a20e1eb2-4f98-46a3-953b-feea4f2acb2a.PNG)
![02](https://user-images.githubusercontent.com/26362032/136266626-6eef0b94-392c-4dee-8cd0-2d8d16a39755.PNG)

#### White border = item takes 1-2 inventory slots, Red border = item takes 3-4 slots, no border = item takes 5-6 slots

![04](https://user-images.githubusercontent.com/26362032/136266817-4e7e65e1-878e-490f-8c5d-618ccd978eaf.PNG)
![05](https://user-images.githubusercontent.com/26362032/136266824-89d5bc0e-d3f6-49fb-ab02-394f5bdbc178.PNG)

## The second goal for this filter is to configure tiers universally, across all item types.

#### If you see a color you know what its value is, regardless of what kind of item it is. No need to memorize multiple tier profiles, nor combinations of background and border colors. By default these are the tiers and map icon assignments:

![Tab1](https://user-images.githubusercontent.com/26362032/141643781-40b0ff9c-1be0-428a-a42d-a23f592b044a.png)

On the second tab are some additional settings (scroll down for a FAQ with more info on what these do/mean):

![Tab2](https://user-images.githubusercontent.com/26362032/138002094-0ae70546-fb3a-4686-84a2-62903a010bde.png)

On the third tab are more settings (scroll down for a FAQ with more info on what these do/mean):

![Tab3](https://user-images.githubusercontent.com/26362032/141643800-fab8eb7f-ceb7-4d48-b476-41e1b06ce64b.png)

## What is the status of this project?

I feel like I have the tool doing 98% of what it should. I'm sure there are some errors in the output file - there are limitations in the poe.ninja dataset, and also limitations of what the PoE filter can accept, and wrangling them both is a real hassle.  I think I've found most of the obvious issues, and I'm at the point where I've accomplished a lot of the little goals I'd set for achieving different functions.  Now is the time where I want to ask for help with two things:

- Playtesting: The more people willing to use this tool (or the filters it generates) the faster I can find and fix any remaining issues.
- Refactoring: There are _sooooo maaaany variations to handle!!!_ If you factorize too early you run the risk of running into edge cases that require you to rewrite what you had, and in the process you could break what you'd already written. There are so many variations to handle that I decided not to do ANY factorizing at all until I got closer to a Beta stage. I am getting closer to that, and would love it if I could find some people to assist with the factorization.  To be completely honest, I'd never written more than 50 lines of Python before taking on this project.  It was my exuse to learn Python and at the same time tackle this idea I'd been wanting to do for (literally) years.

## FAQ

#### How do we install/run this program?

Here's a short video (6 minute) that explains how to install the program and get it to run: https://youtu.be/07Te5tPNaWc

#### How do we interpret the colors and map icons of the items?

The order is: Brown > Red > Orange > Yellow > Green > Blue > Purple > Cyan > Pink > White

Just follow the the rainbow.  Red through Purple are in the same order as in the rainbow.  Then you just need to know that brown is below red, and above purple are cyan, pink, and white.

Regarding icons, aside from Diamond and Rain, more sides = more important, but color's still more important than the icon. (An item with a Green Circle is worth more than one with a Red Pentagon, etc.)

#### Is there anything important about the Patch # field?

This is used in the naming of the filter file (scroll down in the FAQ to see more info about that).  I thought it might be interesting in case you want to keep filters from previous leagues. There's no easy way to programatically download this patch # so I'll have to manually update it eacy league.  I decided to make it a user-editable field in case you want to use this tool before I've had a chance to update the tool yet.  The actual legue names (Epedition, Scourge) should update automatically, so no need for manual intervention there.

#### What do we need to know about the Save Settings/Reset Settings/Generate Filter buttons?

Clicking the `Generate Filter` button automatically saves the settings to `00_user_settings.txt`, then kicks off the filter generation scripts, which reads the settings from that file.  If you change the filter settings but close out of the program without Saving your settings or Generating a new file THEN YOUR CHANGES WILL NOT BE SAVED.

Also, the `Reset Settings` button will reset the `00_user_settings.txt` file but I don't yet know how to get Python to reset the checkboxes and sliders.  So for right now, if you want to reset the settings, click that button, then close the program and reopen it.  Then the checkboxes and sliders will be where they should be.

#### What does the poe.ninja confidence slider do?

poe.ninja has three confidence ratings: high (10+ of the items are listed for sale), medium (5-10 of the items are listed for sale), and low (fewer than 5 of the items are listed for sale).  If more of an item are listed the more confident you can be that the price listed is probably accurate. If only a few are listed then it's harder to be confident of the listed price because of things like overpriced dump tabs (which there's nothing wrong with), or people underpricing things to try to scam by price-fixing (which there is something wrong with).

#### What does the Overall Filter Strictness slider do?

As shown above, we put all items into tiers based on their value. This slider will allow you to modify your filter's strictness.  For example, if you set the slider to 5 then items in tiers 6 through 10 will be hidden.  The other sliders work in relation to this.  Read the other questions/answers for more info.

#### Why are there two sliders for non-influenced/veiled/etc Rare items?

There are like 3 things that all come into play here.

1. In the first few Acts Rare items might be usable upgrades for your own gear, but as you progress through the Acts on your way towards the Endgame the odds of them being usable start to drop, especially if you're using build guides (which is suggested).  You may still want to pick them up to trade to vendors for currency, but once you start getting to the point where you can do the Chaos Recipe you'll probably want to hide all rares below ilvl 65 because you can't use those for the Chaos Recipe.  These items will be pretty cheap, but using the Economy-Based slider for rares may not give you the granularity you need because the economy at the start of a league can be pretty weird for the first few days (assuming you're not playing in Standard).

2. On the other hand, by the time you get to red maps so many Rares are dropping that even setting the slider to ilvl 86 will still leave lots of items appearing on the screen.  That's when the Economy-Based slider will come into play.  If you were to use the Overall Filter Strictness slider then you might be hiding a bunch of other items that you are willing to view otherwise (currency, maps, oils, div cards, etc.), so having a separate slider for the Rares allows us to filter those without needing to go and set overrides for all other items.

3. You also need to understand price-fixing, Dump Tabs, default pricing, and how they affect pricing on poe.ninja.  I made a video about this (here: https://youtu.be/xGkBxN_aNAA) because it took about 7-8 minutes to discuss these things. Spoken word takes a lot of space to write out, so a video is faster.

#### What does the slider for non-influenced/veiled/etc Rare items do?

There are some classes (like flasks) where Magic items will be of interest, but for armor, weapons, and accessories we only care about Rare items.  By default this tool hides all Normal and Magic armor, weapons, and accessories.  As you progress through the game you're going to want to hide even Rare items below a certain item level.  This slider will let you do that.

#### What are T11/Gray/Grey items?

There are many items in Path of Exile that share common base types, when you have one of these you will not know which item you have until you look at it.  Some are more valuable than others, but the loot filter cannot tell these items apart because of the limitations of PoE's filtering system. Since we don't know what value these items have we put them into "Tier 11" and the tool gives these items a gray background. If you see gray, you may want to either look at it, or pick it up and look at it later.

#### How does the Unique Item Breakpoint feature work?

Here is a short video that explains it (right-click and open in a new tab).  If you don't want to watch the video I explain it in text below the video.

[![Unique Item Breakpoint](https://user-images.githubusercontent.com/26362032/131201767-df9055ef-dcc9-4286-b114-c3bf12a7781d.png)](https://youtu.be/vyq4zIIuO-w)

The poe.ninja website tracks market values of many items in a much more granular fashion than the PoE filter system allows, so we might be able to get more info from poe.ninja than we can from the game. How does this help us?  It gives us three possibilities:

- If poe.ninja tells us that some variants of a particular basetype are above our Unique Item Breakpoint and some are below, then we can continue to highlight those items with a gray background.
- If poe.ninja tells us that EVERY variant of a particular basetype is ABOVE our Unique Item Breakpoint then we can highlight those items based on the lowest common denominator. Say there are only two items in a particular basetype. One is worth 10c, and the other is 20c.  If my breakpoint is 5c I know I can highlight all occurrences of that basetype not with a gray background, but as being worth at least 10c.
- If poe.ninja tells us that every variant of a particular basetype is BELOW our Unique Item Breakpoint then we know we can hide all of those items without missing anything important.

NOTE 1: In reality, this Unique Item Breakpoint feature is not 100% foolproof.  Experienced players know that there are 'price-fixers' out there who intentionally list expensive items below their real value to trick newer players into selling that item more cheaply - BUT - experienced players ALSO know that expensive items rarely drop in low-tier areas of the game.  So you can kind of work with it in the low-tier areas.  To be safe we have included an Override feature with this tool.

NOTE 2: Keep in mind that certain basetypes will always be shown. Unique Leather Belts could be a HeadHunter. HeadHunters are so valueable you'd have to set the breakpoint above 50-150 Exalts to hide all Unique Leather Belts, but the slider only goes up to 200c, so that's not possible ... unless you manually edit the filter file, which you shouldn't do if you're a new player.

#### Why does the tool have checkboxes for Normal/Magic 5-link and 6-socket items?

These items can be relatively valuable early in the game, but as you get farther into the game they become less valuable. Also, these items take up a lot of inventory space. So at some point you'll want to hide them from your loot drops.  But 6L items will always be shown.  5L items will always be shown if the item is a Unique item, or if it's a Rare item that's above your Rare item ilvl cutoff.

#### What does the "+4 tiers (league start)" checkbox do?

This has been disabled for now.  It was mainly a feel-good thing, but may have been affecting normal functioning of the tool, so I disabled it.  When you start a new character (or a new league) you'll be doing very low-tier areas where all the drops are very low in value.  By default most of them will be T9 or T10 (red or brown) items.  It might be nice to see some yellow or green highlighted drops, so I created this checkbox.  When selected it'll boost the tiers of lower-tier items up by 4 levels.

#### What does the "Misc Recipes" checkbox do?

This is really only relevant for the challenge leagues, and specifically, only relelvant at league start, from Acts 1-10.  Checking this box will show all Flasks, Rings, Belts, Amulets, Jewels, Gems, and Magic or Rare items that are smaller than 6 or 8 inventory slots.  These can all be listed for 1 alt or 1 alch at league start.  People will need them for recipes.  Vendor anything that doesn't sell within an hour or two.  These items will have a red background and the minimap icon will be a Red Raindrop.  

#### What does the "Hide Corrupted" checkbox do?

This is really only relevant for the challenge leagues, and specifically, only relelvant at league start, from Acts 1-10.  At league start you'll have no currency, and one of the best ways to start getting some is to identify and then sell Rare gear to vendors (assuming it's not something you can use or sell).  Corrupted gear is good for this because it always drops identified, so you don't have to waste Scrolls of Wisdom on them.  Also, you also may want to put corrupted items into the Scourge cauldron rather than risk bricking otherwise good items.  As you get farther into the game you may want to hide corrupted items, however this checkbox will not hide corrupted gems, nor 5L or 6L items (which could be valuable).

#### What does the "Enforce 3L/4L" checkbox do?

This is really only relevant for the challenge leagues, and specifically, only relelvant at league start, from Acts 1-10.  At league start you'll have no currency, and one of the best ways to start getting some is to identify and then sell Rare gear to vendors (assuming it's not something you can use or sell).  As you get farther into the game you may want to limit how many Rare items the loot filter shows. The slider for ilvl may get you what you want, but it also may not.  Checking this checkbox will only show 1x3 items or 2x2 items if they have the maximum number of links possible (3 and 4, respectively) as another way to limit what the filter shows.  Typically 3L/4L on an item does not add much to its value, it's just an arbitrary thing we can do to limit what gets through the filter.

#### What do the radio buttons for Junk Gem Quality do?

The tool does a lot of filtering for gems because there are a lot of possible variations (level, quality, corruption, etc). If a gem doesn't meet any of those criteria it would normally be hidden, but gems with quality (that are otherwise not worth showing) can be traded in for Gemcutter's Prisms (check out Vendor Recipes).  Also, as a personal note ... I keep 1 tab where I list nothing but gems for 1c each.  These are gems I picked up off the ground, without leveling them at all.  Last league I made 200c-300c just from selling those.  Even if you only sell two or three a day, it adds up.

#### What if I want to manually override/edit the filter?

I explain how to do manual overrides in the video at the top of this page, please watch that.  Or, if you want a link to the exact timestamp: https://youtu.be/-kXiwg55DLI?t=479  If you feel like you can't do what you want with my tool (even with the CSV override method) then either open a feature request via Github, or maybe you're ready to graduate to using FilterBlade or StupidFatHobbit's filters.  I did say my tool's not meant to replace theirs.

#### How do we interpret the filter file names?

Here's the legend:

3.15-A-B-C-D-E-F-G-HH-II-INV.filter

3.15 - This is the current patch level. I'll use 3.15 as the default, but you can edit in the GUI in case I don't update it.    
A - Sub-league (Standard/HC/Challenge League/Challenge League HC): 1-4, will match the # shown next to the subleague name in the GUI.    
B - Overall Filter strictness (slider): 1-9 means 1-9, 0 means 10.    
C - Rare Filter strictness (slider): 1-9 means 1-9, 0 means 10.    
D - Show gray items: 1 = True, 0 = False    
E - Show Normal/Magic 6S items: 1 = True, 0 = False    
F - Show Normal/Magic 5S items: 1 = True, 0 = False    
G - Add +4 to all tiers: 1 = True, 0 = False    
HH - Non-influenced/synthesized/etc Rare ilvl cutoff    
II - Unique item breakpoint
INV - If the color inversion option is selected "-INV" will be added to the filter name.

So, for example, let's decipher a filter named: 3.15-1-8-8-1-0-0-0-76-10.filter ... this is a filter for 3.15, league, shows items down to Tier 8 (both Rare and otherwise), shows grey items, does not show 5S or 6S normal/magic items, does not add 4+ tiers, the cutoff for non-special rares is ilvl 76, and the Unique item breakpoint is 10c.

#### Why are you naming filter files so strangely?

Three reasons:

1. Naming the file based on its settings means the file name doesn't change when you update the filter with new pricing.  The next time you open the game you don't need to select a new filter in the options menu, it just loads automatically.  If PoE's already running you only need to click the refresh button in the options tab, not find and select a completely new filter.

2. Once you know the naming convention you can swap between filters quickly without trying to remember what the differences are between filters.  You'll know exactly just by looking at the file name.

3. Now I don't have to sit there trying to think of what to name the filter in order to differentiate it from the other filters I've made.

#### What are your plans for adding new items introduced in the new league?

I've looked at some of GGG's notes about what items they've added to the game, but from my perspective the first thing I need to do is find out is whether or not poe.ninja has added them to the list of items they're tracking.  If they have then I might only need to update my link to the items they've added, and after that they should automatically be included into the filters this tool generates.  But there will be some delay and process between getting their new items and then finding out if there are any they've left out.  If you know of some item that my tool is not handling, please open an issue in the Issues section at the top of the Github page to let me know to look at it.

#### Can this tool be used by Magic Find players?

With some tweaks, yes.  In the files section I've included a checklist of all the statically-assigned items in the fitler and given notes/instructions on how you can modify them to suit your needs.  One thing to note is that until I learn how to filter out low-confidence items from poe.ninja I am only showing non-special (non-veiled, influenced, etc) bases if they're rare.  So you could be missing some normal/magic bases that might be worth something, but if you're not targeting those you should be fine.  Once I learn how to filter out low-confidence items I will note that in the features section above and modify this note here.
