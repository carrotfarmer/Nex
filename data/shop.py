import discord

COIN_EMOTE = "<:nexcoin:894136203836805131>"

shop = [
    {"name": "Laptop", "price": 15000, "description": "Post memes with a laptop and earn coins!!", "emote": "<:laptop:887573704203198495>", "sell_price": 5000, "id": "Laptop"},
    {"name": "Shovel", "price": 10000, "description": "Dig around to possibly earn some coins!", "emote": "<:shovel:889535564016156763>", "sell_price": 1000, "id": "Shovel"},
    {"name": "Drill", "price": 75000, "description": "Mine with the drill to find coins or some other stuff", "emote": "<:drill:887578635681271878>", "sell_price": 15000, "id": "Drill"},
    {"name": "Worm", "price": None, "description": "A small gross worm. Get this by using the dig command!", "emote": "<a:worm:889113123087331408>", "sell_price": 2000, "id": "Worm"},
    {"name": "Iron", "price": None, "description": "A strong metal. Get this by using the mine command!", "emote": "<:iron:889187538403745903>", "sell_price": 7500, "id": "Iron"},
    {"name": "Copper", "price": None, "description": "A copper ore. Get this by using the mine command!", "emote": "<a:copper:889183465940078633>", "sell_price": 5000, "id": "Copper"},
    {"name": "Gold", "price": None, "description": "Woww a shiny piece of gold! Get this by using the mine command!", "emote": "<a:gold:889183920770404413>", "sell_price": 25000, "id": "Gold"},
    {"name": "Silver", "price": None, "description": "A nice extract of silver. Get this by using the mine command!", "emote": "<a:silver:889184426918027274>", "sell_price": 25000, "id": "Silver"},
    {"name": "Platinum", "price": None, "description": "A really cool and really expensive metal! Get this by using the mine command!", "emote": "<:platinum:889185688816353300>", "sell_price": 50000, "id": "Platinum"},
    {"name": "Diamond", "price": None, "description": "A cool**er** and **more** expensive metal! Get this by using the mine command!", "emote": "<a:diamond:889186405329293363>", "sell_price": 85000, "id": "Diamond"},
    {"name": "Stick", "price": None, "description": "~~A stupid useless stick~~ A really cool stick! Get this by using the mine command!", "emote": "<:stick:889188243134881832>", "sell_price": 250, "id": "Stick"},
    {"name": "Pickaxe", "price": 1000, "description": "A default item you get for mining! Get this by using the mine command!", "emote": "<:pickaxe:889375720420286475>", "sell_price": 500, "id": "Pickaxe"},
    {"name": "Axe", "price": 1000, "description": "A default item you get for chopping trees! Get this by using the mine command!", "emote": "<:nex_axe:889376208876347422>", "sell_price": 500, "id": "Axe"},
    {"name": "Iron shovel", "price": None, "description": "High chance of digging more useful stuff! Get this by using the craft command!", "emote": "<:iron_shovel:889536586553884702>", "sell_price": 45000, "id": "Ironshovel"},
    {"name": "Gold shovel", "price": None, "description": "High**er** chance of digging more useful stuff! Get this by using the craft command!", "emote": "<:gold_shovel:889536971360329739>", "sell_price": 75000, "id": "Goldshovel"},
    {"name": "Diamond shovel", "price": None, "description": "High**est** chance of digging more useful stuff! Get this by using the craft command!", "emote": "<:diamond_shovel:887574931729170433>", "sell_price": 100000, "id": "Diamondshovel"},
    # {"name": "Rod", "price": 25000, "description": "(aka fishing rod) Go fishing!", "emote": "<:fishingrod:889531742518669312>", "sell_price": 5000},
    # ["iron", "copper", "gold", "silver", "platinum", "diamond", "stick", "petrol", "coal", "limestone", "emerald", "quartz", "rock"]
    # ["iron shovel", "gold shovel", "diamond shovel"]
]


pg1 = discord.Embed(title="The Nex Shop", color=discord.Color.blue())
ind = 0

for item in shop:
    ind += 1
    if ind == 6:
        break
    else:
        txt = ""
        if not item['price']:
            txt = f"{shop[ind]['name']} {shop[ind]['emote']} - `Not Buyable`"
        else:
            txt = f"{shop[ind]['name']} {shop[ind]['emote']} - `{shop[ind]['price']}` {COIN_EMOTE}"

    pg1.add_field(name=txt, value=f"{shop[ind]['description']}", inline=False)
pg1.set_footer(text="Page 1 of 4")

pg2 = discord.Embed(title="The Nex Shop", color=discord.Color.blue())
for item in shop:
    ind += 1
    if ind == 12:
        break
    else:
        txt = ""
        if not item['price'] or item['price'] == None:
            txt = f"{shop[ind]['name']} {shop[ind]['emote']} - `Not Buyable`"
        else:
            txt = f"{shop[ind]['name']} {shop[ind]['emote']} - `{shop[ind]['price']}` {COIN_EMOTE}"

        pg2.add_field(name=txt, value=f"{shop[ind]['description']}", inline=False)
pg2.set_footer(text="Page 2 of 4")

pg3 = discord.Embed(title="The Nex Shop", color=discord.Color.blue())
for item in shop:
    ind += 1
    if ind == 16:
        break
    else:
        txt = ""
        if not item['price']:
            txt = f"{shop[ind]['name']} {shop[ind]['emote']} - `Not Buyable`"
        else:
            txt = f"{shop[ind]['name']} {shop[ind]['emote']} - `{shop[ind]['price']}` {COIN_EMOTE}"

        pg3.add_field(name=txt, value=f"{shop[ind]['description']}", inline=False)
pg3.set_footer(text="Page 3 of 4")


