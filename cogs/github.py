import discord
from discord.ext import commands
from github import Github

g = Github()


class Github(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cogs extension \"Github\" ready.")

    @commands.command()
    async def ghuser(self, ctx, *, username=None):
        try:
            if username == None:
                await ctx.reply("**ERROR**: `MissingParameters` Please provide a username.")
            else:
                user = g.search_users(username)[0]
        except:
            await ctx.reply("**ERROR**: `CommandInvokeError` Invalid username!")

        user_emb = discord.Embed(title=f"Search results for user `{username}`",
                                 color=discord.Color.random())
        user_emb.set_thumbnail(url=user.avatar_url)
        user_emb.add_field(name="Name", value=user.name, inline=False)
        user_emb.add_field(name="Bio", value=user.bio, inline=False)
        user_emb.add_field(name="Followers",
                           value=user.followers,
                           inline=False)
        user_emb.add_field(name="Following",
                           value=user.following,
                           inline=False)
        user_emb.add_field(name="Profile URL",
                           value=user.html_url,
                           inline=False)
        user_emb.add_field(name="Location", value=user.location, inline=False)
        user_emb.add_field(name="Public Repos",
                           value=user.public_repos,
                           inline=False)

        await ctx.send(embed=user_emb)

    @commands.command()
    async def ghrepo(self, ctx, *, reponame=None):
        try:
            if reponame == None:
                await ctx.reply("**ERROR**: `MissingParameters` Please enter a repository name.")
            else:
                repo = g.search_repositories(reponame)[0]
        except:
            await ctx.reply("**ERROR**: `CommandInvokeError` Invalid repository name!")

        repo_emd = discord.Embed(title=f"Search results for repo `{reponame}`",
                                 color=discord.Color.random())
        repo_emd.add_field(name="Name", value=repo.name, inline=False)
        repo_emd.add_field(name="Default Branch",
                           value=repo.default_branch,
                           inline=False)
        repo_emd.add_field(name="Most Used Language",
                           value=repo.language,
                           inline=False)
        repo_emd.add_field(name="Description",
                           value=repo.description,
                           inline=False)
        repo_emd.add_field(name="Stars",
                           value=repo.stargazers_count,
                           inline=False)
        repo_emd.add_field(name="Forks", value=repo.forks_count, inline=False)
        repo_emd.add_field(name="Open Issues",
                           value=repo.open_issues_count,
                           inline=False)
        repo_emd.add_field(name="Size",
                           value=f"{repo.size/1000} MB",
                           inline=False)
        repo_emd.add_field(name="Created At",
                           value=repo.created_at,
                           inline=False)
        repo_emd.add_field(name="Network Count", value=repo.network_count)
        repo_emd.add_field(name="Repo URL", value=repo.url, inline=False)
        repo_emd.add_field(name="Contributors URL",
                           value=repo.contributors_url,
                           inline=False)

        await ctx.send(embed=repo_emd)


def setup(client):
    client.add_cog(Github(client))
