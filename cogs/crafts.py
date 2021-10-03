import discord
from discord.ext import commands
from cogs.econ import sell_this, add_item_to_inv, update_bank, check_for_item, get_price, get_emote, remove_item_from_inv

# econ.sell_this()
# econ.update_bank(ctx.author, change=-1*econ.get_price(), "wallet")

class CraftsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cogs extension \"Crafts\" ready.")
    
    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def craft(self, ctx, category, item, amount=None):
        item =  item.lower()
        category = category.lower()
        stick = await check_for_item(ctx.author, "Stick")
        amtEnough = False
        if item == "shovel":
            if category == "iron" or category == "gold" or category == "diamond":
                str(category).capitalize()
                categoryBool = await check_for_item(ctx.author, str(category).capitalize())
                if stick[0] == True:
                    amt = stick[1]
                    if amt >= 2:
                        amtEnough = True
                else:
                    self.craft.reset_cooldown(ctx)
                    err_emd = discord.Embed(title="Crafting Failed", description="<:nex_cross:887950619950874634> You dont have **ANY** sticks ~~who doesnt have enough sticks~~ :rolling_eyes:", color=discord.Color.red())
                    await ctx.reply(embed=err_emd)
                print(categoryBool)
                if amtEnough == False:
                    self.craft.reset_cooldown(ctx)
                    err_emd = discord.Embed(title="Crafting Failed", description="<:nex_cross:887950619950874634> You dont have **ENOUGH** sticks ~~who doesnt have enough sticks~~ :rolling_eyes:", color=discord.Color.red())
                    await ctx.reply(embed=err_emd)
                if categoryBool == False:
                    self.craft.reset_cooldown(ctx)
                    err_emd = discord.Embed(title="", description=f"<:nex_cross:887950619950874634> LOL you don't have enough {category.capitalize()} {get_emote(category)} to craft this!", color=discord.Color.red())
                    await ctx.reply(embed=err_emd)

                elif amtEnough == True and categoryBool[0] == True:
                    await remove_item_from_inv(ctx.author, "Stick", 2)
                    await remove_item_from_inv(ctx.author, category, 1)
                    #give shovel here :)
                    await add_item_to_inv(ctx.author, category + " shovel", 1)
                    craft_emd = discord.Embed(title="Successful Crafting!", description=f"You successfuly crafted a **{category.capitalize()} Shovel** {get_emote(category + ' shovel')}!!", color=discord.Color.green())
                    craft_emd.set_footer(text="minecraft don't sue us please-", icon_url=ctx.author.avatar_url)
                    await ctx.reply(embed=craft_emd)
                    
            else:
                self.craft.reset_cooldown(ctx)
                err_emd = discord.Embed(title="", description="<:nex_cross:887950619950874634> Broooo, you can only craft an `Iron Shovel`, `Gold Shovel` and a `Diamond Shovel` for now", color=discord.Color.red())
                return await ctx.reply(embed=err_emd)
        else:
            self.craft.reset_cooldown(ctx)
            return await ctx.reply("You can't craft that yet :)")

    @craft.error
    async def crafterror(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cool_emd = discord.Embed(
                title="omg calm down bro",
                description=
                f"lol your hands are tired from the previous crafting! Try again in {error.retry_after:.0f}s.",
                color=discord.Color.dark_magenta())
            cool_emd.set_footer(text="imagine spamming lol")
            await ctx.send(embed=cool_emd)
        
        if isinstance(error, commands.errors.MissingRequiredArgument):
            self.craft.reset_cooldown(ctx)
            cool_emd = discord.Embed(
                title="",
                description="<:nex_cross:887950619950874634> dude- what do you want to craft-? (eg: `shovel`)",
                color=discord.Color.dark_magenta())
            cool_emd.set_footer(text="imagine being so dumb")
            await ctx.send(embed=cool_emd)
        
def setup(bot):
    bot.add_cog(CraftsCog(bot))