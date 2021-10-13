# Fla_Panther's Super Simple Loot Filter

### Desktop tool for generating Path of Exile filters using current poe.ninja prices.

#### Note: It's been brought to my attention that I included one dependency that needs to be installed with this. See the FAQ for more info if you're okay with that, if not then you can just download the .filter files here and test with those.

#### Here is a quick video showing the filter in action (right-click and open in a new tab):

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

![Tab1](https://user-images.githubusercontent.com/26362032/136266861-f8254bcc-0bb4-4e4d-8b91-c5139b1aa25c.PNG)

On the second tab are some additional settings (scroll down for a FAQ with more info on what these do/mean):

![Tab2](https://user-images.githubusercontent.com/26362032/136266872-bf13b783-981c-42e7-aa57-38f9e3f7790a.PNG)

## What is the status of this project?

I feel like I have the tool doing 98% of what it should. I'm sure there are some errors in the output file - there are limitations in the poe.ninja dataset, and also limitations of what the PoE filter can accept, and wrangling them both is a real hassle.  I think I've found most of the obvious issues, and I'm at the point where I've accomplished a lot of the little goals I'd set for achieving different functions.  Now is the time where I want to ask for help with two things:

- Playtesting: The more people willing to use this tool (or the filters it generates) the faster I can find and fix any remaining issues.
- Refactoring: There are _sooooo maaaany variations to handle!!!_ If you factorize too early you run the risk of running into edge cases that require you to rewrite what you had, and in the process you could break what you'd already written. There are so many variations to handle that I decided not to do ANY factorizing at all until I got closer to a Beta stage. I am getting closer to that, and would love it if I could find some people to assist with the factorization.  To be completely honest, I'd never written more than 50 lines of Python before taking on this project.  It was my exuse to learn Python and at the same time tackle this idea I'd been wanting to do for (literally) years.

## FAQ

#### How do we install/run this program?

I wanted to make this something that wouldn't need anything to be installed other than the base Python library, but it looks like I included one additional dependency without realizing it.  So in order to run the program you'll need to install Python, and then from a command propmt, issue the command `pip install requests`.  This will install the `requests` library, which you can read about here: https://docs.python-requests.org/en/latest/

#### How do we interpret the colors and map icons of the items?

The color order is: Brown > Red > Orange > Yellow > Green > Blue > Purple > Cyan > Pink > White

Basically it goes from darkest to lightest, but the easiest way to remember it is to just follow the the rainbow.  Red through Purple are in the same order as in the rainbow.  Then you just need to know that brown is below red, and above purple are cyan, pink, and white.

Regarding icons, aside from Diamond and Rain, more sides = more important, but color's still more important than the icon.    
(An item with a Green Circle is worth more than one with a Red Pentagon, etc.)

#### Is there anything important about the Path # field?

This is used in the naming of the fiolter file this tool exports (scroll down in the FAQ to see more info about the naming convention I use for the filter file names).  I thought it might be interesting in case you want to keep filters from previous leagues. But there is no easy way to programatically download this patch # so I'll have to manually update it eacy league.  I decided to make it a user-editable field in case you want to use this tool for a new league and I haven't had a chance to update the tool yet.

#### What do we need to know about the Save Settings/Reset Settings/Generate Filter buttons?

You can save your filter settings two ways: either by clicking the `Save Settings` button, or by clicking the `Generate Filter` button.  Clicking the `Generate Filter` button automatically saves the settings to `00_user_settings.txt`, then kicks off the filter generation scripts which reads the settings from that file.  If you change the filter settings but close out of the program without doing one of those two things your changes will not be saved.

The `Reset Settings` button will reset the `00_user_settings.txt` file but I don't yet know how to get Python to reset the checkboxes and sliders.  So for right now if you want to reset the program, click that button, then close the program and reopen it.

#### What does the Overall Filter Strictness slider do?

As shown above, we put all items into tiers based on their value. This slider will allow you to modify your filter's strictness.  For example, if you set the slider to 5 then items in tiers 6 through 10 will be hidden.

#### Why are there two sliders for non-influenced/veiled/etc Rare items?

There are like 3 things that all come into play here.

1. In the first few Acts Rare items might be usable upgrades for your own gear, but as you progress through the Acts on your way towards the Endgame the odds of them being usable start to drop, especially if you're using build guides (which is suggested).  You may still want to pick them up to trade to vendors for currency, but once you start getting to the point where you can do the Chaos Recipe you'll probably want to hide all rares below ilvl 65 because you can't use those for the Chaos Recipe.  These items will be pretty cheap, so using the Economy-Based slider for rares may not give you the granularity you need.

2. On the other hand, by the time you get to red maps so many Rares are dropping that even setting the slider to ilvl 86 will still leave lots of items appearing on the screen.  That's when the Economy-Based slider will come into play.  If you were to use the Overall Filter Strictness slider then you might be hiding a bunch of other items that you are willing to view otherwise (currency, maps, oils, div cards, etc.), so having a separate slider for the Rares allows us to filter them without then needing to go and set overrides for all those other items.

3. Price-fixing, Dump Tabs, default pricing, and how they affect pricing on poe.ninja.  I made a video to talk about this (here: https://youtu.be/xGkBxN_aNAA) because it took about 7-8 minutes to discuss these things. Spoke word takes a lot of space to write out, so a video is just faster.

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

#### What if I want to manually edit the filter?

I've included a way to override certain settings by editing a CSV file (see below), and there is a Manual Override section at the top of the filter, but if you're a new player I'd suggest you not try to edit the filter settngs below that section.  Let's put it this way: if you feel like you can't do what you want with my tool, the CSV override method, or the manual override section, then either open a feature request via Github, or maybe you're ready to graduate to using FilterBlade or StupidFatHobbit's filters.  I did say my tool's not meant to replace theirs.

#### How does the Override feature work?

I explain how to do manual overrides in the video at the top of this page, please watch that.  Or, if you want a link to the exact timestamp: https://youtu.be/-kXiwg55DLI?t=479

#### Why does the tool have checkboxes for Normal/Magic 5-socket and 6-socket items?

These items can be relatively valuable early in the game, but as you get farther into the game they become less valuable. Also, these items take up a lot of inventory space. So at some point you'll want to hide them from your loot drops.  But note, these checkboxes are for 5/6 sockets, not links.  5L/6L items are handled differently.  6L items will always be shown.  5L items will always be shown if the item is a Unique item, or if it's a Rare item that's above your Rare item cutoff.

#### What does the "+4 tiers (league start)" checkbox do?

It's mainly a feel-good thing.  When you start a new character (or a new league) you'll be doing very low-tier areas where all the drops are very low in value.  By default most of them will be T9 or T10 (red or brown) items.  It might be nice to see some yellow or green highlighted drops, so if you want, check this box and it'll boost the tiers of lower-tier items.

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

#### What additional features will you be adding to this tool?

I'm open to suggestions, but right now on my list I have:

- A white border to indicate items 1x1/1x2/2x1 items, and red border for 1x3 and 2x2. (ADDED - Testing now.)
- A way to select which league you want pricing for. (ADDED - Testing now.)
- Create auto-override for Fated Unique items (Uniques that have an itemized prophecy) (ADDED - Testing now.)
- All vendor recipies, with checkboxes (handy for challenges)
- Separate sliders for gems/cards/prophs/etc?
- Additional color themes (suggestions welcome)
- Find a way to include poe.ninja confidence ratings to filter out overpriced items with low-confidence
- Include filtering identified items by # of T1 mods, T2 mods, etc
