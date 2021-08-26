# Fla_Panther's Super Simple Loot Filter

### Desktop tool for generating Path of Exile filters using current poe.ninja prices.

#### NOTE: THIS TOOL IS IN AN --ALPHA-- STAGE, NOT EVEN BETA. THE CODE & GUI ARE UGLY BUT THEY WILL CHANGE.
#### GETTING EVERYTHING WORKING RIGHT IS THE FIRST PRIORITY, MAKING THE CODE/GUI LOOK NICE WILL COME LATER.

A quick thank you to StupidFatHobbit and the guys over at FilterBlade, you all taught me a lot. This filter isn't meant to replace theirs. This filter is for VERY new players who aren't ready for racing, crafting, hardcore, SSF, or build-specific highlighting - seriously, just THE MOST BASIC filter possible.

Due to not showing those items this filter will be more strict than theirs, and does NOT use combinations of background color, text color, or border color when displaying an item.  This filter displays all items with black text, no border, and the background color is based on softcore market prices obtained from poe.ninja.  (Yes, experienced players know poe.ninja's pricing isn't perfect, but for a completely new player it's good enough to start with. Anyway, this tool also allows you to do manual overrides.)

I may add other schemes later, but for now this is what it looks like:

![ss01](https://user-images.githubusercontent.com/26362032/130993851-52d7c04e-4535-44ba-9d69-7b0ca024d615.PNG)

The second goal for this filter is to configure tiers universally, across all item types.  If you see a color you know what its value is, regardless of what kind of item it is. No need to memorize multiple tier profiles, nor combinations of background and border colors.  By default these are the tiers and map icon assignments:

![ss02](https://user-images.githubusercontent.com/26362032/130992017-5944432a-754c-4639-9ba9-fc7a3c7b344c.PNG)

On the second tab are some additional settings (scroll down for a FAQ with more info on what these do/mean):

![ss03](https://user-images.githubusercontent.com/26362032/130992040-8c31b422-bf04-4517-abf1-016377544d39.PNG)

## FAQ

#### What are T11/Gray/Grey items?

There are many items in Path of Exile that share common base types, when you have one of these you will not know which item you have until you look at it.  Some are more valuable than others, but the loot filter cannot tell these items apart because of the limitations of PoE's filtering system. Since we don't know what value these items have we put them into "Tier 11" and the tool gives these items a gray background. If you see gray, you may want to either look at it, or pick it up and look at it later.

#### How does the Unique Item Breakpoint feature work?

The poe.ninja website tracks market values of many items in a much more granular fashion than the PoE filter system allows, so we might be able to get more info from poe.ninja than we can from the game. How does this help us?  It gives us three possibilities:

- If poe.ninja tells us that some variants of a particular basetype are above our Unique Item Breakpoint and some are below, then we can continue to highlight those items with a gray background.
- If poe.ninja tells us that EVERY variant of a particular basetype is ABOVE our Unique Item Breakpoint then we can highlight those items based on the lowest common denominator (meaning if the item can be 10c or 20c and my breakpoint is 5c I know I can highlight both items as being worth at least 10c).
- If poe.ninja tells us that every variant of a particular basetype is BELOW our Unique Item Breakpoint then we know we can hide all of those items without missing anything important.

NOTE: In reality, this Unique Item Breakpoint feature is not 100% foolproof.  Experienced players know that there are 'price-fixers' out there who intentionally list expensive items below their real value to trick newer players into selling that item more cheaply - BUT - experienced players ALSO know that expensive items rarely drop in low-tier areas of the game.  To work around this we have included an Override feature with this tool.

#### How does the Override feature work?

I need to add this info.
