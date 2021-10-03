import pymongo
import os
from discord.ext import commands
import discord
import random
from utils.beg import messages, people, slow
from data.shop import pg1, pg2, pg3
import discordSuperUtils

client = pymongo.MongoClient(f"mongodb+srv://staticvoid:{os.getenv('MONGO_PASSWD')}@cluster0.jj4xd.mongodb.net/nex?retryWrites=true&w=majority")

db = client["nex"]
econ = db["econ"]

COIN_EMOTE = "<:nexcoin:894136203836805131>"

class EconCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Cogs extension \"Economy\" ready.")
    
    @commands.command(aliases=["bal"])
    async def balance(self, ctx, user: discord.Member=None):
        acc = check_if_account_exists(ctx.author)
        
        if not user:
            user = ctx.author
        
        acc = check_if_account_exists(user)
        if not acc:
            if user == ctx.author:
                return await ctx.reply("You need to create an account first. Use `n!create_account` to do so!")
            else:
                return await ctx.reply("This user does not have an account!")

        bal = get_money(user)[0]
        bal_pretty = "{:,}".format(bal)
        bank = get_money(user)[1]
        bank_pretty = "{:,}".format(bank)
        bank_spc = get_money(user)[2]
        bank_spc_pretty = "{:,}".format(bank_spc)

        bal_emd = discord.Embed(title=f"{user.name}'s Balance", color=discord.Color.blurple(), description=f"{COIN_EMOTE} **Wallet**: {bal_pretty}\n{COIN_EMOTE} **Bank**: {bank_pretty}/{bank_spc_pretty}")
        bal_emd.set_footer(text="what a loser", icon_url=user.avatar_url)

        await ctx.reply(embed=bal_emd)
    
    @commands.command(aliases=["createaccount"])
    async def create_account(self, ctx): 
        if db.econ.find_one({"user": str(ctx.author.id)}):
            return await ctx.reply("You already have an account :/")
        else:
            db.econ.insert_one({"user": str(ctx.author.id), "balance": 100, "bank": 0, "bank_space": 500000, "inv": []})
            succ_emd = discord.Embed(title="<a:nex_tick:887946161275666474> You're all set!", description="Your account has successfully been created!", color=discord.Color.green())
            await ctx.reply(embed=succ_emd)
    
    @commands.command()
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def beg(self, ctx):
        acc = check_if_account_exists(ctx.author)
        
        if not acc:
            return await ctx.reply("You need to create an account first. Use `n!create_account` to do so!")

        bal = get_money(ctx.author)[0]
        earnings = random.randrange(0, 1001)
        desc = ""

        if earnings <= 45:
            desc = random.choice(messages)
            earnings = 0
        else:
            desc = f"wow nice lol you got {COIN_EMOTE} **{earnings}**"

        beg_emd = discord.Embed(title=random.choice(people),
                                description=desc,
                                color=discord.Color.random())
        beg_emd.set_footer(icon_url=ctx.author.avatar_url,
                           text="why are you begging lol")
        await ctx.reply(embed=beg_emd)

        new_obj = {"$set": {"balance": bal + earnings}}
        db.econ.update_one({"user": str(ctx.author.id)}, new_obj)

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
        acc = check_if_account_exists(ctx.author)
        
        if not acc:
            return await ctx.reply("You need to create an account first. Use `n!create_account` to do so!")

        if not amount:
            return await ctx.reply("enter the amount u dumb")

        bal = get_money(ctx.author)

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

        change_money(ctx.author, "balance", bal[0] + amount)
        change_money(ctx.author, "bank", bal[1] - amount)

        with_emd = discord.Embed(
            title="Successful Withdrawal",
            description=f"You successfully withdrew {COIN_EMOTE} **{'{:,}'.format(amount)}**!",
            color=discord.Color.green())
        with_emd.set_footer(text="what a nerd", icon_url=ctx.author.avatar_url)

        await ctx.reply(embed=with_emd)
    
    @commands.command(aliases=['dep'])
    async def deposit(self, ctx, amount=None):
        acc = check_if_account_exists(ctx.author)
        
        if not acc:
            return await ctx.reply("You need to create an account first. Use `n!create_account` to do so!")

        if not amount:
            return await ctx.reply("enter the amount u dumb")

        bal = get_money(ctx.author)

        if amount == "max":
            amount = bal[0]

        amount = int(amount)
        if amount > bal[0]:
            return await ctx.reply(
                "lol dont try and cheat me you dont have that much money in your wallet"
            )

        if amount < 0:
            return await ctx.reply(
                "ay stupid how can u deposit **negative** money??????")
        
        if amount > bal[2]:
            remaining_bal = bal[2] - bal[1]
            amount = remaining_bal
            if remaining_bal == 0:
                return await ctx.reply("Sorry your bank is full :rofl:")

        change_money(ctx.author, "bank", bal[1] + amount)
        change_money(ctx.author, "balance", bal[0] - amount)

        with_emd = discord.Embed(
            title="Successful Deposit",
            description=f"You successfully deposit {COIN_EMOTE} **{'{:,}'.format(amount)}** coins!",
            color=discord.Color.green())
        with_emd.set_footer(text="what a nerd", icon_url=ctx.author.avatar_url)

        await ctx.reply(embed=with_emd)
    
    @commands.command(aliases=['send','give'])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def share(self, ctx, member: discord.Member = None, amount=None):
        acc = check_if_account_exists(ctx.author)
        
        if not acc:
            return await ctx.reply("You need to create an account first. Use `n!create_account` to do so!")
        if not member:
            return await ctx.reply("whom are you sharing your coins with smh")
            self.share.reset_cooldown(ctx)

        if member == ctx.author:
            return await ctx.reply(
                "bro don't be such a piss-off you can't share coins with yourself dumbass"
            )
            self.share.reset_cooldown(ctx)

        bal = get_money(ctx.author)
        u_bal = get_money(member)

        if not amount:
            return await ctx.reply("enter the amount u dumb")
            self.share.reset_cooldown(ctx)

        if amount == "max" or amount == "all":
            amount = bal[0]

        if int(amount) == 0:
            return await ctx.reply(f"Bro you can't share 0 {COIN_EMOTE}. :rolling_eyes:")
            self.share.reset_cooldown(ctx)

        amount = int(amount)
        if amount > bal[0]:
            return await ctx.reply(
                "lol dont try and cheat me you dont have that much coins in your wallet"
            )
            self.share.reset_cooldown(ctx)

        if amount < 0:
            return await ctx.reply(
                "ay stupid how can u share **negative** coins??????")
            self.share.reset_cooldown(ctx)

        change_money(ctx.author, "balance", bal[0] - amount)
        change_money(member, "balance", u_bal[0] + amount)

        dep_emd = discord.Embed(
            title="Successful Transfer",
            description=
            f"You successfully shared {COIN_EMOTE} **{'{:,}'.format(amount)}** with {member.mention}",
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
            self.share.reset_cooldown(ctx)

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
        acc = check_if_account_exists(ctx.author)

        if not acc:
            return await ctx.reply("You need to create an account first. Use `n!create_account` to do so!")

        bal = get_money(ctx.author)
        if not amount:
            return await ctx.reply("smh provide a valid amount to bet")
            self.slots.reset_cooldown(ctx)

        if amount == "max" or amount == "all":
            amount = bal[0]

        if int(amount) < 1000:
            return await ctx.reply(f"you need to bet aleast **1000** {COIN_EMOTE}")

        amount = int(amount)

        if int(amount) > bal[0]:
            return await ctx.reply(
                "oof you don't have that much in your wallet")

        if int(amount) < 0:
            return await ctx.reply("you cant bet negative coins lol")

        final = []
        for i in range(3):
            a = random.choice(
                [":money_mouth:", ":money_with_wings:", ":moneybag:"])
            final.append(a)

        slot_emd = discord.Embed(title=f"{ctx.author.name}'s Slot Machine",
                                 description="", color=discord.Color.red())
        for slot in final:
            slot_emd.description += slot
        slot_emd.set_thumbnail(
            url=
            "https://c.tenor.com/7A4zjdP3ffMAAAAi/slot-machine-joypixels.gif")
        slot_emd.set_footer(text=":O", icon_url=ctx.author.avatar_url)

        await ctx.reply(embed=slot_emd)

        if final[0] == final[1] == final[2]:
            change_money(ctx.author, "balance", bal[0] + (2 * amount))
            win_emd = discord.Embed(
                title="You Won!",
                color=discord.Color.green(),
                description=
                f"Poggerz {ctx.author.mention} you actually won and earned **{10*amount}** {COIN_EMOTE}! GG"
            )
            win_emd.set_footer(text="lucky bugger",
                               icon_url=ctx.author.avatar_url)

            await ctx.send(embed=win_emd)
        else:
            change_money(ctx.author, "balance", bal[0] - amount)
            lose_emd = discord.Embed(
                title="You Lost!",
                color=discord.Color.red(),
                description=
                f"LOL you lost the slots! You have lost **{'{:,}'.format(amount)}** {COIN_EMOTE}!")
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
        acc = check_if_account_exists(ctx.author)
        user_acc = check_if_account_exists(member)

        if not acc:
            return await ctx.reply("You do not have an account! Use `n!create_account` to create one!")
            self.rob.reset_cooldown(ctx)
        
        if not user_acc:
            return await ctx.reply("LOL the person you are trying to rob doesn't have an account!")
            self.rob.reset_cooldown(ctx)

        if not member:
            return await ctx.reply("whom are you robbing??!")
            self.rob.reset_cooldown(ctx)

        if member == ctx.author:
            return await ctx.reply("yo you can't rob yourself noob")
            self.rob.reset_cooldown(ctx)

        bal = get_money(member)
        author_bal = get_money(ctx.author)

        if bal[0] < 1000:
            return await ctx.reply(
                f"this user has less than **1000** {COIN_EMOTE}. don't rob the poor idiot"
            )

        if author_bal[0] < 500:
            return await ctx.reply(
                f"you need to have atleast **500** {COIN_EMOTE} to rob someone else")

        win_lose_chance = random.randrange(1, 100)

        if win_lose_chance > 50:
            earnings = random.randrange(1, bal[0])
            change_money(ctx.author, "balance", bal[0] + earnings)
            change_money(member, "balance", bal[0] - earnings)

            win_emd = discord.Embed(
                title="Successful Robbery!",
                color=discord.Color.green(),
                description=
                f"You successfully stole **{'{:,}'.format(earnings)}** {COIN_EMOTE} from {member.mention}! Are you happy now?"
            )
            win_emd.set_footer(text="mOnEy HeIsT",
                               icon_url=ctx.author.avatar_url)

            await ctx.reply(embed=win_emd)

        elif win_lose_chance <= 50:
            lost_money = random.randrange(1, author_bal[0])
            change_money(ctx.author, "balance", author_bal[0] - lost_money)
            change_money(member, "balance", bal[0] + lost_money)

            lose_emd = discord.Embed(
                title="Failed Robbery!",
                color=discord.Color.red(),
                description=
                f"You messed up while robbing {member.mention} oof. You had to pay **{'{:,}'.format(lost_money)}** {COIN_EMOTE} to {member.mention} to stop him from reporting you to the police!"
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
        await discordSuperUtils.ButtonsPageManager(ctx, [pg1, pg2, pg3], button_color=2).run()

def get_money(user):
    user = db.econ.find_one({"user": str(user.id)})
    bal = user["balance"]
    bank = user["bank"]
    bank_spc = user["bank_space"]

    return [bal, bank, bank_spc]

def change_money(user, field, amt):
    new_obj = {"$set": {field: int(amt)}}
    db.econ.update_one({"user": str(user.id)}, new_obj)

def check_if_account_exists(user):
    user = db.econ.find_one({"user": str(user.id)})
    if not user:
        return None
    else:
        return "Worked"

def setup(bot):
    bot.add_cog(EconCog(bot))