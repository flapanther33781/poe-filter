# Fla_Panther's Super Simple Loot Filter

### Desktop tool for generating Path of Exile filters using current poe.ninja prices.

#### NOTE: THIS TOOL IS IN AN --ALPHA-- STAGE, NOT EVEN BETA. THE CODE & GUI ARE UGLY BUT THEY WILL CHANGE.
#### GETTING EVERYTHING WORKING RIGHT IS THE FIRST PRIORITY, MAKING THE CODE/GUI LOOK NICE WILL COME LATER.

## The first goal for this filter was to make it as simple as possible.

A quick thank you to StupidFatHobbit and the guys over at FilterBlade, you all taught me a lot. This filter isn't meant to replace theirs. This filter is for VERY new players who aren't ready for racing, crafting, hardcore, SSF, or build-specific highlighting - seriously, just THE MOST BASIC filter possible.

Due to not showing those items **this filter** will be more strict than theirs, and **does NOT use combinations of background color, text color, or border color when displaying an item (except for items that normally drop with borders - but you can ignore them).  The background color is based on softcore market prices obtained from poe.ninja.**  (Yes, experienced players know poe.ninja's pricing isn't perfect, but for a completely new player it's good enough to start with. Anyway, this tool also allows you to do manual overrides.)

I may add other schemes later, but for now this is what it looks like:

![ss01](https://user-images.githubusercontent.com/26362032/130993851-52d7c04e-4535-44ba-9d69-7b0ca024d615.PNG)

## The second goal for this filter is to configure tiers universally, across all item types.

#### If you see a color you know what its value is, regardless of what kind of item it is. No need to memorize multiple tier profiles, nor combinations of background and border colors. By default these are the tiers and map icon assignments:

![ss02](https://user-images.githubusercontent.com/26362032/130992017-5944432a-754c-4639-9ba9-fc7a3c7b344c.PNG)

On the second tab are some additional settings (scroll down for a FAQ with more info on what these do/mean):

![ss03](https://user-images.githubusercontent.com/26362032/130992040-8c31b422-bf04-4517-abf1-016377544d39.PNG)

## What is the status of this project?

I feel like I have the tool doing 98% of what it should. I'm sure there are some errors in the output file - there are limitations in the poe.ninja dataset, and also limitations of what the PoE filter can accept, and wrangling them both is a real hassle.  I think I've found most of the obvious issues, and I'm at the point where I've accomplished a lot of the little goals I'd set for achieving different functions.  Now is the time where I want to ask for help with two things:

- Playtesting: The more people willing to use this tool (or the filters it generates) the faster I can find and fix any remaining issues.
- Refactoring: There are _sooooo maaaany variations to handle!!!_ If you factorize too early you run the risk of running into edge cases that require you to rewrite what you had, and in the process you could break what you'd already written. There are so many variations to handle that I decided not to do ANY factorizing at all until I got closer to a Beta stage. I am getting closer to that, and would love it if I could find some people to assist with the factorization.  To be completely honest, I'd never written more than 50 lines of Python before taking on this project.  It was my exuse to learn Python at the same time as I wanted to tackle this idea I'd been wanting to do for years.

## FAQ

#### What does the slider for Strictness selector do?

As shown above, we put all items into tiers based on their value. This slider will allow you to modify your filter's strictness.  For example, if you set the slider to 5 then items in tiers 6 through 10 will be hidden.

#### What does the slider for non-influenced/veiled/etc Rare items do?

There are some classes (like flasks) where Magic items will be of interest, but for armor, weapons, and accessories we only care about Rare items.  By default this tool hides all Normal and Magic armor, weapons, and accessories.  As you progress through the game you're going to want to hide even Rare items below a certain item level.  This slider will let you do that.

#### What are T11/Gray/Grey items?

There are many items in Path of Exile that share common base types, when you have one of these you will not know which item you have until you look at it.  Some are more valuable than others, but the loot filter cannot tell these items apart because of the limitations of PoE's filtering system. Since we don't know what value these items have we put them into "Tier 11" and the tool gives these items a gray background. If you see gray, you may want to either look at it, or pick it up and look at it later.

#### How does the Unique Item Breakpoint feature work?

The poe.ninja website tracks market values of many items in a much more granular fashion than the PoE filter system allows, so we might be able to get more info from poe.ninja than we can from the game. How does this help us?  It gives us three possibilities:

- If poe.ninja tells us that some variants of a particular basetype are above our Unique Item Breakpoint and some are below, then we can continue to highlight those items with a gray background.
- If poe.ninja tells us that EVERY variant of a particular basetype is ABOVE our Unique Item Breakpoint then we can highlight those items based on the lowest common denominator. Say there are only two items in a particular basetype. One is worth 10c, and the other is 20c.  If my breakpoint is 5c I know I can highlight all occurrences of that basetype not with a gray background, but as being worth at least 10c.
- If poe.ninja tells us that every variant of a particular basetype is BELOW our Unique Item Breakpoint then we know we can hide all of those items without missing anything important.

NOTE 1: In reality, this Unique Item Breakpoint feature is not 100% foolproof.  Experienced players know that there are 'price-fixers' out there who intentionally list expensive items below their real value to trick newer players into selling that item more cheaply - BUT - experienced players ALSO know that expensive items rarely drop in low-tier areas of the game.  So you can kind of work with it in the low-tier areas.  To be safe we have included an Override feature with this tool.

NOTE 2: Keep in mind that certain basetypes will always be shown. Unique Leather Belts could be a HeadHunter. HeadHunters are so valueable you'd have to set the breakpoint above 50-150 Exalts to hide all Unique Leather Belts, but the slider only goes up to 200c, so that's not possible ... unless you manually edit the filter file, which you shouldn't do.

#### How does the Override feature work?

I'm going to make a video and post it here. Until this tool is more refined the process is a little complex.  Not too bad, but easier to show in a video.

#### Why does the tool have checkboxes for Normal/Magic 5-socket and 6-socket items?

These items can be relatively valuable early in the game, but as you get farther into the game they become less valuable. Also, these items take up a lot of inventory space. So at some point you'll want to hide them from your loot drops.  But note, these checkboxes are for 5/6 sockets, not links.  5L/6L items are handled differently.  6L items will always be shown.  5L items will always be shown if the item is a Unique item, or if it's a Rare item that's above your Rare item cutoff.

#### What does the "+4 tiers (league start)" checkbox do?

It's mainly a feel-good thing.  When you start a new character (or a new league) you'll be doing very low-tier areas where all the drops are very low in value.  By default most of them will be T9 or T10 (red or brown) items.  It might be nice to see some yellow or green highlighted drops, so if you want, check this box and it'll boost the tiers of lower-tier items.
