from replit import db
import discord
from discord.ext import commands
import json
import random
from utils.beg import people, messages, slow
from discord_components import Button

# shop
from data.shop import shop


def get_emote(item: str) -> str:
    for item_in_the_shop in shop:
        if item.capitalize() == item_in_the_shop["name"]:
            return item_in_the_shop["emote"]


def get_price(item: str, amount: int = 1) -> int:
    for item_in_the_shop in shop:
        if item.capitalize() == item_in_the_shop["name"]:
            return item_in_the_shop["sell_price"] * amount


class EconCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cogs extension \"Economy\" ready.")

    @commands.command(aliases=['bal'])
    async def balance(self, ctx, user: discord.Member = None):
        if not user:
            user = ctx.author
        await open_account(user)

        users = await get_bank_data()

        wallet_amt = users[str(user.id)]["wallet"]
        bank_amt = users[str(user.id)]["bank"]

        bal_emd = discord.Embed(
            title=f"{user.name}'s Balance",
            color=discord.Color.blurple(),
            description=f"**Wallet**: {wallet_amt:.0f}\n**Bank**: {bank_amt}")
        bal_emd.set_footer(text="what a loser", icon_url=user.avatar_url)

        await ctx.reply(embed=bal_emd)

    @commands.command()
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def beg(self, ctx):
        await open_account(ctx.author)

        users = await get_bank_data()
        user = ctx.author
        earnings = random.randrange(0, 1001)
        desc = ""

        if earnings == 0:
            desc = random.choice(messages)
        else:
            desc = f"wow nice lol you got {earnings} coins"

        beg_emd = discord.Embed(title=random.choice(people),
                                description=desc,
                                color=discord.Color.random())
        beg_emd.set_footer(icon_url=user.avatar_url,
                           text="why are you begging lol")
        await ctx.reply(embed=beg_emd)
        users[str(user.id)]["wallet"] += earnings

        with open("mainbank.json", "w") as f:
            json.dump(users, f)

    @beg.error
    async def begerror(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cool_emd = discord.Embed(
                title="omg calm down bro",
                description=
                f"{random.choice(slow)}. Try again in {error.retry_after:.0f}s.",
                color=discord.Color.dark_magenta())
            cool_emd.set_footer(text="imagine spamming lol")
            await ctx.send(embed=cool_emd)

    @commands.command(aliases=['with'])
    async def withdraw(self, ctx, amount=None):
        await open_account(ctx.author)
        if not amount:
            return await ctx.reply("enter the amount u dumb")

        bal = await update_bank(ctx.author)

        if amount == "max":
            amount = bal[1]

        amount = int(amount)
        if amount > bal[1]:
            return await ctx.reply(
                "lol dont try and cheat me you dont have that much money in your bank"
            )

        if amount < 0:
            return await ctx.reply(
                "ay stupid how can u withdraw **negative** money??????")

        await update_bank(ctx.author, amount)
        await update_bank(ctx.author, -1 * amount, "bank")

        with_emd = discord.Embed(
            title="Successful Withdrawal",
            description=f"You successfully withdrew {amount} coins!",
            color=discord.Color.green())
        with_emd.set_footer(text="what a nerd", icon_url=ctx.author.avatar_url)

        await ctx.reply(embed=with_emd)

    @commands.command(aliases=['dep'])
    async def deposit(self, ctx, amount=None):
        await open_account(ctx.author)

        if not amount:
            return await ctx.reply("enter the amount u dumb")

        bal = await update_bank(ctx.author)

        if amount == "max" or amount == "all":
            amount = bal[0]

        if int(amount) == 0:
            return await ctx.reply("BRUH YOU CANT DEPOSIT 0 COINS SMH")

        amount = int(amount)
        if amount > bal[0]:
            return await ctx.reply(
                "lol dont try and cheat me you dont have that much money in your wallet"
            )

        if amount < 0:
            return await ctx.reply(
                "ay stupid how can u deposit **negative** money??????")

        await update_bank(ctx.author, -1 * amount)
        await update_bank(ctx.author, amount, "bank")

        dep_emd = discord.Embed(
            title="Successful Deposit",
            description=f"You successfully deposited {amount} coins!",
            color=discord.Color.green())
        dep_emd.set_footer(text="what a nerd", icon_url=ctx.author.avatar_url)

        await ctx.reply(embed=dep_emd)

    @commands.command(aliases=['send','give'])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def share(self, ctx, member: discord.Member = None, amount=None):
        await open_account(ctx.author)
        await open_account(member)

        if not member:
            return await ctx.reply("whom are you sharing your coins with smh")
            self.share.reset_cooldown(ctx)

        if member == ctx.author:
            return await ctx.reply(
                "bro don't be such a piss-off you can't share coins with yourself dumbass"
            )

        bal = await update_bank(ctx.author)

        if not amount:
            return await ctx.reply("enter the amount u dumb")

        if amount == "max" or amount == "all":
            amount = bal[0]

        if int(amount) == 0:
            return await ctx.reply("Bro you can't share 0 coins. :/")

        amount = int(amount)
        if amount > bal[0]:
            return await ctx.reply(
                "lol dont try and cheat me you dont have that much money in your wallet"
            )

        if amount < 0:
            return await ctx.reply(
                "ay stupid how can u share **negative** money??????")

        await update_bank(ctx.author, -1 * amount)
        await update_bank(member, amount)

        dep_emd = discord.Embed(
            title="Successful Transfer",
            description=
            f"You successfully shared {amount} coins with {member.mention}",
            color=discord.Color.green())
        dep_emd.set_footer(text="sharing is caring",
                           icon_url=ctx.author.avatar_url)

        await ctx.reply(embed=dep_emd)

    @share.error
    async def shareerror(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            cool_emd = discord.Embed(
                title="no such member found",
                description=f"Don't be stupid and mention a valid user smh",
                color=discord.Color.dark_magenta())
            cool_emd.set_footer(text="imagine being so dumb lol")
            await ctx.send(embed=cool_emd)

        if isinstance(error, commands.CommandOnCooldown):
            cool_emd = discord.Embed(
                title="omg calm down bro",
                description=
                f"if you'll share so much you'll be broke in no time. Try again in {error.retry_after:.0f}s.",
                color=discord.Color.dark_magenta())
            cool_emd.set_footer(text="imagine spamming lol")
            await ctx.send(embed=cool_emd)

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def slots(self, ctx, amount=None):
        await open_account(ctx.author)

        bal = await update_bank(ctx.author)
        if not amount:
            return await ctx.reply("smh provide a valid amount to bet")
            self.slots.reset_cooldown(ctx)

        if amount == "max" or amount == "all":
            amount = bal[0]

        if amount < 1000:
            return await ctx.reply("you need to bet aleast 1000 coins")

        amount = int(amount)

        if amount > bal[0]:
            return await ctx.reply(
                "oof you don't have that much in your wallet to bet")

        if amount < 0:
            return await ctx.reply("you cant bet negative coins lol")

        final = []
        for i in range(3):
            a = random.choice(
                [":money_mouth:", ":money_with_wings:", ":moneybag:"])
            final.append(a)

        slot_emd = discord.Embed(title=f"{ctx.author.name}'s Slot Machine",
                                 description="")
        for slot in final:
            slot_emd.description += slot
        slot_emd.set_thumbnail(
            url=
            "https://c.tenor.com/7A4zjdP3ffMAAAAi/slot-machine-joypixels.gif")
        slot_emd.set_footer(text=":O", icon_url=ctx.author.avatar_url)

        await ctx.reply(embed=slot_emd)

        if final[0] == final[1] == final[2]:
            await update_bank(ctx.author, 2 * amount)
            win_emd = discord.Embed(
                title="You Won!",
                color=discord.Color.green(),
                description=
                f"Poggerz {ctx.author.mention} you actually won and earned **{10*amount}** coins! GG"
            )
            win_emd.set_footer(text="lucky bugger",
                               icon_url=ctx.author.avatar_url)

            await ctx.send(embed=win_emd)
        else:
            await update_bank(ctx.author, -1 * amount)
            lose_emd = discord.Embed(
                title="You Lost!",
                color=discord.Color.red(),
                description=
                f"LOL you lost the slots! You have lost **{amount}** coins!")
            lose_emd.set_footer(text="lol serves you right for gambling",
                                icon_url=ctx.author.avatar_url)

            await ctx.send(embed=lose_emd)

    @slots.error
    async def slotserror(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cool_emd = discord.Embed(
                title="omg calm down bro",
                description=
                f"dude if you gamble so much you'll be on the streets soon. Try again in {error.retry_after:.0f}s.",
                color=discord.Color.dark_magenta())
            cool_emd.set_footer(text="imagine spamming lol")
            await ctx.send(embed=cool_emd)

    @commands.command(aliases=['steal'])
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def rob(self, ctx, member: discord.Member = None):
        await open_account(ctx.author)
        await open_account(member)

        if not member:
            return await ctx.reply("whom are you robbing??!")
            self.rob.reset_cooldown(ctx)

        if member == ctx.author:
            return await ctx.reply("yo you can't rob yourself noob")
            self.rob.reset_cooldown(ctx)

        bal = await update_bank(member)
        author_bal = await update_bank(ctx.author)

        if bal[0] < 1000:
            return await ctx.reply(
                "this user has less than thousand coins. don't rob the poor idiot"
            )

        if author_bal[0] < 500:
            return await ctx.reply(
                "you need to have atleast 500 coins to rob someone else")

        win_lose_chance = random.randrange(1, 100)

        if win_lose_chance > 50:
            earnings = random.randrange(1, bal[0])
            await update_bank(ctx.author, earnings)
            await update_bank(member, -1 * earnings)

            win_emd = discord.Embed(
                title="Successful Robbery!",
                color=discord.Color.green(),
                description=
                f"You successfully stole {earnings} coins from {member.mention}! Are you happy now?"
            )
            win_emd.set_footer(text="mOnEy HeIsT",
                               icon_url=ctx.author.avatar_url)

            await ctx.reply(embed=win_emd)

        elif win_lose_chance <= 50:
            lost_money = random.randrange(1, author_bal[0])
            await update_bank(ctx.author, -1 * lost_money)

            lose_emd = discord.Embed(
                title="Failed Robbery!",
                color=discord.Color.red(),
                description=
                f"You messed up while robbing {member.mention} oof. You had to pay {lost_money} coins to bribe the police and get out of jail!"
            )
            lose_emd.set_footer(text="LMAO SERVES YOU RIGHT",
                                icon_url=ctx.author.avatar_url)

            await ctx.reply(embed=lose_emd)

    @rob.error
    async def roberror(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cool_emd = discord.Embed(
                title="omg calm down bro",
                description=
                f"lol if you steal so much you'll get caught by the cops! Try again in {error.retry_after:.0f}s.",
                color=discord.Color.dark_magenta())
            cool_emd.set_footer(text="imagine spamming lol")
            await ctx.send(embed=cool_emd)

    @commands.command()
    async def shop(self, ctx):
        shop_emd = discord.Embed(title="Shop", color=discord.Color.random())

        for item in shop:
            name = item["name"] + item["emote"]
            price = f"**{item['price']}** coins"

            if item['price'] == None:
                price = "**Not Buyable**"

            description = item["description"]
            sell_price = item["sell_price"]
            shop_emd.add_field(
                name=name,
                value=
                f"{price}\n**Description: **{description}\n**Sell Price: **`{sell_price}` coins"
            )

        await ctx.reply(embed=shop_emd)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def buy(self, ctx, item=None, amount=1):
        await open_account(ctx.author)

        if not item:
            await ctx.reply("what the hell do you want to buy")
            self.buy.reset_cooldown(ctx)

        res = await buy_this(ctx.author, item, amount)

        if not res[0]:
            if res[1] == 1:
                return await ctx.reply("no such thingy in the shop lol")
            if res[1] == 2:
                return await ctx.reply(
                    "oof you don't have enough coins in your wallet to buy this item!"
                )

        item_emote = get_emote(item)
        buy_emd = discord.Embed(
            title="Successful Purchase",
            color=discord.Color.green(),
            description=
            f"You bought **{amount} {item.capitalize()}** {item_emote}")
        buy_emd.set_footer(text="You are now 1 step closer to being broke!",
                           icon_url=ctx.author.avatar_url)

        await ctx.reply(embed=buy_emd)

    @buy.error
    async def buyerror(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cool_emd = discord.Embed(
                title="omg calm down bro",
                description=
                f"bro if you buy so much stuff you're gonna be broke in no time! Try again in {error.retry_after:.0f}s.",
                color=discord.Color.dark_magenta())
            cool_emd.set_footer(text="imagine spamming lol")
            await ctx.send(embed=cool_emd)

    @commands.command(aliases=["inv", "bag"])
    async def inventory(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author

        await open_account(member)

        users = await get_bank_data()
        try:
            inv = users[str(member.id)]["bag"]
        except:
            inv = []

        inv_emd = discord.Embed(title=f"{member}'s Inventory",
                                color=discord.Color.random(),
                                description="")
        inv_emd.set_footer(text="wow", icon_url=member.avatar_url)

        if inv == []:
            inv_emd.description += "IT'S EMPTY LOL"
        else:
            ind = 0
            for item in inv:
                name = item["item"].capitalize() + " " + get_emote(item["item"].capitalize())
                amount = item["amount"]

                if amount == 0:
                    ind += 1

                else:
                    inv_emd.add_field(name=name, value=amount)
                ind += 1

        await ctx.reply(embed=inv_emd)

    @commands.command()
    async def sell(self, ctx, item, amount=1):
        await open_account(ctx.author)
        users = await get_bank_data()
        

        # if amount == "max" or amount == "all":
        #     for item in users[str(ctx.author.id)]["bag"]:
        #         amount = int(item["amount"])
        
        # if amount == None:
        #     amount = 1

        res = await sell_this(ctx.author, item, amount)

        if not res[0]:
            if res[1] == 1:
                return await ctx.reply("no such thingy in your inventory lol")

            if res[1] == 2:
                return await ctx.send(
                    f"lol you don't have **{amount} {item.capitalize()}** in your inventory!"
                )

            if res[1] == 3:
                return await ctx.send(
                    f"You don't have any **{item} {get_emote(item.capitalize())}**s in your inventory."
                )

        sell_emd = discord.Embed(
            title="Successful Sale",
            description=
            f"You successfully sold **{amount} {item.capitalize()} {get_emote(item)}** for **{get_price(item.capitalize(), amount)}** coins!",
            color=discord.Color.green())
        sell_emd.set_footer(text="stonks", icon_url=ctx.author.avatar_url)

        await ctx.reply(embed=sell_emd)

    @commands.command(aliases=["lb", "top"])
    async def leaderboard(self, ctx, x: int = 5):
        users = await get_bank_data()
        leader_board = {}
        total = []
        max_inp: int = 20

        if x > max_inp:
            return await ctx.reply("10 is the maximum limit!")

        for user in users:
            name = int(user)
            total_amount = users[user]["wallet"] + users[user]["bank"]
            leader_board[total_amount] = name
            total.append(total_amount)

        total = sorted(total, reverse=True)

        em = discord.Embed(title=f"Top {x} Richest People",
                           color=discord.Color.gold())
        index = 1
        for amt in total:
            id_ = leader_board[amt]
            member = self.bot.get_user(id_)
            name = member.name
            if index == 1:
                em.add_field(name=f":first_place: {index}. {name}",
                             value=f"{amt}",
                             inline=False)

            elif index == 2:
                em.add_field(name=f":second_place: {index}. {name}",
                             value=f"{amt}",
                             inline=False)

            elif index == 3:
                em.add_field(name=f":third_place: {index}. {name}",
                             value=f"{amt}",
                             inline=False)

            else:
                em.add_field(name=f"{index}. {name}",
                             value=f"{amt}",
                             inline=False)

            if index == x:
                break
            else:
                index += 1

        await ctx.send(embed=em)

    @commands.command(aliases=["pm"])
    @commands.cooldown(1, 25, commands.BucketType.user)
    async def postmemes(self, ctx):
        await open_account(ctx.author)
        laptop = await check_for_item(ctx.author, "Laptop")

        if not laptop or laptop == False:
            self.postmemes.reset_cooldown(ctx)
            nolp_emd = discord.Embed(
                title="",
                description=
                "<:nex_cross:887950619950874634> You can't make memes without a **Laptop** <:laptop:887573704203198495> lol. Use `n!buy laptop` to buy one!",
                color=discord.Color.red())
            return await ctx.reply(embed=nolp_emd)

        async def pm_callback():
            users = await get_bank_data()
            scr = random.randrange(1, 100)
            print(scr)
            meme_emd = discord.Embed(title="", description="")

            earnings = None
            if scr < 5:
                earnings = 0
                await sell_this(ctx.author, "Laptop", 1)
                await update_bank(ctx.author, -1*get_price("laptop"), "wallet")
                meme_emd.title += "YOUR MEME WAS TRASH"
                meme_emd.description += f"THE PEOPLE DIED OF CRINGE WHEN THEY SAW YOUR MEME! SO YOU GOT **{earnings}** coins **AND** now your **Laptop** <:laptop:887573704203198495> is broken!"
                meme_emd.color = discord.Color.dark_magenta()
                meme_emd.set_footer(text="nIcE mEmE",
                                    icon_url=ctx.author.avatar_url)

            elif scr <= 10:
                earnings = random.randrange(0, 50)
                meme_emd.title += "OOF YOUR MEME SUCKED"
                meme_emd.description += f"your meme was not good at all so you only got **{earnings}** coins!"
                meme_emd.color = discord.Color.red()
                meme_emd.set_footer(text="lol you suck",
                                    icon_url=ctx.author.avatar_url)

            elif scr <= 50:
                earnings = random.randrange(51, 1000)
                meme_emd.title += "Your meme was okay-ish"
                meme_emd.description += f"your meme was kinda okay so you got **{earnings}** coins!"
                meme_emd.color = discord.Color.orange()
                meme_emd.set_footer(
                    text="Use n!leaderboard to view the richest people!",
                    icon_url=ctx.author.avatar_url)

            elif scr <= 75:
                earnings = random.randrange(1001, 2000)
                meme_emd.title += "Your meme was pretty good!"
                meme_emd.description += f"your meme was actually pretty good so you got **{earnings}** coins!"
                meme_emd.color = discord.Color.dark_green()
                meme_emd.set_footer(text="not bad",
                                    icon_url=ctx.author.avatar_url)

            elif scr <= 100:
                earnings = random.randrange(2001, 7500)
                meme_emd.title += "YOUR MEME BLEW UP!"
                meme_emd.description += f"POGGG YOUR MEME BROKE THE INTERNET LOL! YOU GOT **{earnings}** COINS!!"
                meme_emd.color = discord.Color.green()
                meme_emd.set_footer(text="WOW LEGENDARY MEME",
                                    icon_url=ctx.author.avatar_url)

            await update_bank(ctx.author, earnings, "wallet")

            await ctx.reply(embed=meme_emd)

        pm_emd = discord.Embed(
            title="Post a Meme!",
            description="Make and post a meme to Reddit. If it's not a stupid meme you might get coins!"
        )

        await ctx.reply(embed=pm_emd,
                        # components=[[
                        #     self.bot.components_manager.add_callback(
                        #         Button(label="Fresh Meme"), pm_callback),
                        #     self.bot.components_manager.add_callback(
                        #         Button(label="Copypasta Meme"), pm_callback),
                        #     self.bot.components_manager.add_callback(
                        #         Button(label="Intellectual Meme"),
                        #         pm_callback),
                        #     self.bot.components_manager.add_callback(
                        #         Button(label="Kind Meme"), pm_callback),
                        # ]]
        )

        # interaction = await self.bot.wait_for("button_click")
        # await interaction.edit_origin(components=[])
        await pm_callback()

    @postmemes.error
    async def postmemeserror(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cool_emd = discord.Embed(
                title="omg calm down bro",
                description=
                f"you'll look like a normie if you post too many memes! Try again in {error.retry_after:.0f}s.",
                color=discord.Color.dark_magenta())
            cool_emd.set_footer(text="imagine spamming lol")
            await ctx.send(embed=cool_emd)

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def dig(self, ctx):
        await ctx.reply("The command `n!dig` is temporarily disabled due to technical issues")
        await open_account(ctx.author)

        shovel = await check_for_item(ctx.author, "Shovel")
        ironShovel = await check_for_item(ctx.author, "iron shovel")
        goldShovel = await check_for_item(ctx.author, "gold shovel")
        diamondShovel = await check_for_item(ctx.author, "diamond shovel")

        if shovel[0] == False and ironShovel[0] == False and goldShovel[0] == False and diamondShovel[0] == False:
            self.dig.reset_cooldown(ctx)
            nolp_emd = discord.Embed(
                title="",
                description=
                "<:nex_cross:887950619950874634> You can't dig without a **Shovel** <:shovel:887574931729170433> lol. Use `n!buy shovel` to buy one!",
                color=discord.Color.red())
            return await ctx.reply(embed=nolp_emd)

        coins_chance = random.randrange(1, 100)
        earnings = 0
        dig_items = random.choice(["worm", "shovel", "stick"])
        premdigearning = random.choice(["iron", "copper"])
        ultrapremdigearning = random.choice(["diamond","drill","gold"])
        dig_emd = discord.Embed(title=f"{ctx.author.name}'s Digging Session", description="")
        if diamondShovel == True:
            ironShovel = False
            goldShovel = False
            shovel = False
            if coins_chance <= 10:
                earnings = dig_items
            if coins_chance <= 35:
                earnings =random.randrange(5000, 10000)
            # if coins_chance <=
                

        if coins_chance < 5:
            dig_emd.description += "Oof you found nothing while digging! Maybe try again later?"
            dig_emd.color = discord.Color.dark_magenta()
            dig_emd.set_footer(text="sad life", icon_url=ctx.author.avatar_url)

        elif coins_chance > 50:
            earnings = random.randrange(0, 7500)
            dig_emd.description += f"You dug out **{earnings}** coins!"
            dig_emd.color = discord.Color.green()
            dig_emd.set_footer(text="nice", icon_url=ctx.author.avatar_url)

        else:
            earnings = random.choice(dig_items)
            amount = random.randrange(1, 5)

        if earnings in dig_items:
            await add_item_to_inv(ctx.author, earnings, amount)
            dig_emd.description += f"You dug out **{amount} {earnings.capitalize()}** {get_emote(earnings)}!"
            dig_emd.color = discord.Color.green()
            dig_emd.set_footer(text="nice", icon_url=ctx.author.avatar_url)

        else:
            await update_bank(ctx.author, earnings, "wallet")

        await ctx.reply(embed=dig_emd)

    @dig.error
    async def digerror(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cool_emd = discord.Embed(
                title="omg calm down bro",
                description=
                f"Bruh if you dig so much the Earth will go brr. Try again after {error.retry_after:.0f}s.",
                color=discord.Color.dark_magenta())
            cool_emd.set_footer(text="imagine spamming lol")
            await ctx.send(embed=cool_emd)

    @commands.command()
    @commands.cooldown(1, 40, commands.BucketType.user)
    async def mine(self, ctx):
        drill = await check_for_item(ctx.author, "Drill")
        print(drill)

        pickaxe = await check_for_item(ctx.author, "Pickaxe")
        print("Drill", drill, "Pickaxe", pickaxe)
        earnings = None

        if drill == False and pickaxe == False:
            self.mine.reset_cooldown(ctx)
            nolp_emd = discord.Embed(
                title="",
                description=
                f"<:nex_cross:887950619950874634> You can't mine without a **Drill <:drill:887578635681271878> or a Pickaxe** {get_emote('pickaxe')} lol. Use `n!buy drill` to buy a drill and `n!buy pickaxe` to buy a pickaxe!",
                color=discord.Color.red())
            return await ctx.reply(embed=nolp_emd)

        normal_earnings = random.choice(["iron", "copper", "stick"])
        prem_earnings = random.choice(["gold", "silver"])
        ultraprem_earnings = random.choice(["platinum", "diamond"])

        scr = random.randrange(1, 101)
        
        if drill:
            pickaxe = False
            if scr <= 25:
                earnings = None

            if scr <= 65:
                earnings = normal_earnings

            if scr >= 85:
                earnings = prem_earnings

            if scr >= 95:
                earnings = ultraprem_earnings
            
        if pickaxe:
            if scr <= 45:
                earnings = None
            if scr <= 70:
                earnings = normal_earnings
            if scr >= 90:
                earnings = prem_earnings
            if scr >= 99:
                earnings = ultraprem_earnings
        
        print(earnings)
        mine_emd = discord.Embed(title=f"{ctx.author.name}'s Mining Session",
                                 description="")

        if not earnings:
            mine_emd.description += "oofff you mined **nothing** lol"
            mine_emd.color = discord.Color.red()
            mine_emd.set_footer(text="NiCe", icon_url=ctx.author.avatar_url)

        else:
            await add_item_to_inv(ctx.author, earnings, 1)
            mine_emd.description += f"You mined **{earnings.capitalize()}** {get_emote(earnings)}!"
            mine_emd.color = discord.Color.green()
            mine_emd.set_footer(text="good job",
                                icon_url=ctx.author.avatar_url)

        await ctx.reply(embed=mine_emd)

    @mine.error
    async def mineerror(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cool_emd = discord.Embed(
                title="omg calm down bro",
                description=
                f"Bruh if you mine so much the US will catch you. Try again after {error.retry_after:.0f}s.",
                color=discord.Color.dark_magenta())
            cool_emd.set_footer(text="imagine spamming lol")
            await ctx.send(embed=cool_emd)

    @commands.command()
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def cut(self, ctx):
        await open_account(ctx.author)
        axe = await check_for_item(ctx.author, "Axe")

        if not axe:
            self.mine.reset_cooldown(ctx)
            nolp_emd = discord.Embed(
                title="",
                description=
                f"<:nex_cross:887950619950874634> You can't cut trees without an **Axe** {get_emote('axe')} lol. Use `n!buy axe` to buy one!",
                color=discord.Color.red())
            return await ctx.reply(embed=nolp_emd)

        earnings = None
        amount = None
        cut_emd = discord.Embed(title=f"{ctx.author.name}'s Cutting Session",
                                description="")

        scr = random.randrange(1, 100)

        if scr <= 50:
            earnings = "stick"
            amount = random.randrange(1, 6)

        elif scr < 100:
            earnings = random.randrange(300, 501)

        elif scr == 100:
            earnings = None

        if not earnings:
            cut_emd.description += "oofff you got **nothing** lol"
            cut_emd.color = discord.Color.red()
            cut_emd.set_footer(text="NiCe", icon_url=ctx.author.avatar_url)

        elif type(earnings) == int:
            await update_bank(ctx.author, earnings, "wallet")
            cut_emd.description += f"You cut out **{earnings}** coins!"
            cut_emd.color = discord.Color.green()
            cut_emd.set_footer(text="good job", icon_url=ctx.author.avatar_url)

        else:
            await add_item_to_inv(ctx.author, earnings, amount)
            cut_emd.description += f"You cut out **{amount} {earnings.capitalize()}** {get_emote(earnings)}!"
            cut_emd.color = discord.Color.green()
            cut_emd.set_footer(text="good job", icon_url=ctx.author.avatar_url)

        await ctx.reply(embed=cut_emd)
    
    @cut.error
    async def cuterror(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cool_emd = discord.Embed(
                title="omg calm down bro",
                description=
                f"Cutting of trees leads to deforestation dude you learnt this in third grade. Try again after {error.retry_after:.0f}s.",
                color=discord.Color.dark_magenta())
            cool_emd.set_footer(text="imagine spamming lol")
            await ctx.send(embed=cool_emd)    
    
    # @commands.command(aliases=["fishing"])
    # @commands.cooldown(1, 25, commands.BucketType.user)
    # async def fish(self, ctx):
    #     await open_account(ctx.author)
    #     rod = await check_for_item(ctx.author, "Rod")

    #     if not rod or rod == False:
    #         self.postmemes.reset_cooldown(ctx)
    #         nolp_emd = discord.Embed(
    #             title="",
    #             description=
    #             "<:nex_cross:887950619950874634> You can't fish without a **Rod** <:fishingrod:889531742518669312> coz you're not a bear (right?). Use `n!buy rod` to buy one!",
    #             color=discord.Color.red())
    #         return await ctx.reply(embed=nolp_emd)

    #     async def fish_callback(interaction):
    #         users = await get_bank_data()
    #         scr = random.randrange(1, 100)
    #         meme_emd = discord.Embed(title="", description="")

    #         earnings = None
    #         if scr < 5:
    #             earnings = 0
    #             await sell_this(ctx.author, "Laptop", 1)
    #             await update_bank(ctx.author, -1*get_price("laptop"), "wallet")
    #             meme_emd.title += "YOUR MEME WAS TRASH"
    #             meme_emd.description += f"THE PEOPLE DIED OF CRINGE WHEN THEY SAW YOUR MEME! SO YOU GOT **{earnings}** coins **AND** now your **Laptop** <:laptop:887573704203198495> is broken!"
    #             meme_emd.color = discord.Color.dark_magenta()
    #             meme_emd.set_footer(text="nIcE mEmE",
    #                                 icon_url=ctx.author.avatar_url)

    #         elif scr <= 10:
    #             earnings = random.randrange(0, 50)
    #             meme_emd.title += "OOF YOUR MEME SUCKED"
    #             meme_emd.description += f"your meme was not good at all so you only got **{earnings}** coins!"
    #             meme_emd.color = discord.Color.red()
    #             meme_emd.set_footer(text="lol you suck",
    #                                 icon_url=ctx.author.avatar_url)

    #         elif scr <= 50:
    #             earnings = random.randrange(51, 1000)
    #             meme_emd.title += "Your meme was okay-ish"
    #             meme_emd.description += f"your meme was kinda okay so you got **{earnings}** coins!"
    #             meme_emd.color = discord.Color.orange()
    #             meme_emd.set_footer(
    #                 text="Use n!leaderboard to view the richest people!",
    #                 icon_url=ctx.author.avatar_url)

    #         elif scr <= 75:
    #             earnings = random.randrange(1001, 2000)
    #             meme_emd.title += "Your meme was pretty good!"
    #             meme_emd.description += f"your meme was actually pretty good so you got **{earnings}** coins!"
    #             meme_emd.color = discord.Color.dark_green()
    #             meme_emd.set_footer(text="not bad",
    #                                 icon_url=ctx.author.avatar_url)

    #         elif scr <= 100:
    #             earnings = random.randrange(2001, 7500)
    #             meme_emd.title += "YOUR MEME BLEW UP!"
    #             meme_emd.description += f"POGGG YOUR MEME BROKE THE INTERNET LOL! YOU GOT **{earnings}** COINS!!"
    #             meme_emd.color = discord.Color.green()
    #             meme_emd.set_footer(text="WOW LEGENDARY MEME",
    #                                 icon_url=ctx.author.avatar_url)

    #         await update_bank(ctx.author, earnings, "wallet")

    #         await ctx.reply(embed=meme_emd)

    # @fish.error
    # async def fisherror(self, ctx, error):
    #     if isinstance(error, commands.CommandOnCooldown):
    #         cool_emd = discord.Embed(
    #             title="omg calm down bro",
    #             description=
    #             f"you'll look like a normie if you post too many memes! Try again in {error.retry_after:.0f}s.",
    #             color=discord.Color.dark_magenta())
    #         cool_emd.set_footer(text="imagine spamming lol")
    #         await ctx.send(embed=cool_emd)


async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 100
        users[str(user.id)]["bank"] = 0

    with open("mainbank.json", "w") as f:
        json.dump(users, f)

    return True


async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)
    return users


async def update_bank(user, change=0, mode="wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("mainbank.json", "w") as f:
        json.dump(users, f)

    bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
    return bal


async def buy_this(user, item_name, amount):
    item_name = item_name.lower()
    name_ = None
    for item in shop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False, 1]

    cost = price * amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0] < cost:
        return [False, 2]

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index += 1
        if t == None:
            obj = {"item": item_name, "amount": amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item": item_name, "amount": amount}
        users[str(user.id)]["bag"] = [obj]

    with open("mainbank.json", "w") as f:
        json.dump(users, f)

    await update_bank(user, cost * -1, "wallet")

    return [True, "Worked"]


async def sell_this(user, item_name, amount):
    item_name = item_name.lower()
    name_ = None
    for item in shop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            break

    if name_ == None:
        return [False, 1]

    cost = 0
    for item in shop:
        name = item["name"].lower()
        if name == item_name:
            cost = item["sell_price"]

    users = await get_bank_data()

    bal = await update_bank(user)

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False, 2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index += 1
        if t == None:
            return [False, 3]
    except:
        return [False, 3]

    with open("mainbank.json", "w") as f:
        json.dump(users, f)

    await update_bank(user, cost, "wallet")

    return [True, "Worked"]


async def check_for_item(user, item_name):
    item_name = item_name.lower()
    name_ = None

    for item in shop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            break

    if name_ == None:
        return False
    users = await get_bank_data()
    try:
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            n_amt = None
            if n == item_name:
                n_amt = thing["amount"]
                if n_amt == 0 or not n_amt:
                    return False
                else:
                    return [True, n_amt]

        print(t)

        if t == None:
            return False
    except:
        return False


async def add_item_to_inv(user, item_name, amount):
    item_name = item_name.lower()
    name_ = None
    for item in shop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False, 1]

    users = await get_bank_data()

    bal = await update_bank(user)

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index += 1
        if t == None:
            obj = {"item": item_name, "amount": amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item": item_name, "amount": amount}
        users[str(user.id)]["bag"] = [obj]

    with open("mainbank.json", "w") as f:
        json.dump(users, f)

    return [True, "Worked"]

async def remove_item_from_inv(user, item_name, amount):
    item_name = item_name.lower()
    name_ = None
    for item in shop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
        
    if name_ == None:
        return [False, 1]

    users = await get_bank_data()

    bal = await update_bank(user)

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index += 1
        if t == None:
            obj = {"item": item_name, "amount": amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item": item_name, "amount": amount}
        users[str(user.id)]["bag"] = [obj]

    with open("mainbank.json", "w") as f:
        json.dump(users, f)

    return [True, "Worked"]

def setup(bot):
    bot.add_cog(EconCog(bot))
