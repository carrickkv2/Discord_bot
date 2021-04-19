import aiohttp
from discord.ext import commands, tasks
import discord
import time
from utils.extract_table import usage_extract
import random
import validators


class OwnerCommands(commands.Cog, name="General Commands", description="These commands don't really do anything"):
    """These commands are mainly for the owner of the bot."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @tasks.loop(minutes=10, count=None)
    async def my_background_task(self):
        """Will loop every 86400 seconds and change the bots presence."""
        while not self.bot.is_closed():
            statuses = [
                "CSGO",
                "Fall Guys",
                f"on {len(self.bot.guilds)} servers | ?help",
                "FIFA 21",
                "NARUTO SHIPPUDEN Ultimate Ninja STORM 4",
                "Valheim",
                "God Loves You",
                "Pace loves you",
                "Assassins Creed Odyssey",
                "Take care of yourself",
                "Jesus is there for you",
                "Jesus is Faithful",
                "Love of the Lord",
                "What's up dawg",
                "Python",
                "A Boy and His Blob"]
            status = random.choice(statuses)
            await self.bot.change_presence(activity=discord.Game(name=status))

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """Print a message whenever the bot logs on or reconnects."""
        print(f"Logged on as {self.bot.user}!")
        # Setting `Playing ` status
        await self.bot.wait_until_ready()
        self.my_background_task.start()

    @commands.command()
    async def hello(self, ctx: commands.Context) -> None:
        """Sends a message to the user saying hello with the prefix for help included."""
        user = await self.bot.fetch_user(230942498086846464)
        await ctx.send(f"Hello! I'm a robot created by {user.display_name} \nWant to know what I can do? Type `?help`")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def usage(self, ctx: commands.Context) -> None:
        """Allows the user to check how much credit they have for the extract API."""
        user = await self.bot.fetch_user(230942498086846464)
        await user.send(usage_extract())
        await ctx.message.delete(delay=2)

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context) -> None:
        """Get the bot's current websocket and API latency."""
        start_time = time.time()
        message = await ctx.send("Testing Ping...")
        end_time = time.time()
        await message.edit(
            content=f"Pong! {round(self.bot.latency * 1000)}ms\nAPI: {round((end_time - start_time) * 1000)}ms")

    @commands.command(name="setstatus", hidden=True)
    @commands.is_owner()
    async def setstatus(self, ctx: commands.Context, *, text: str) -> None:
        """Set the bot's status."""
        await self.bot.change_presence(activity=discord.Game(name=text))
        # todo: Get the right status forever

    # @commands.command(aliases=["run"], hidden=True)
    # @commands.is_owner()
    # async def eval(self, ctx, *, code: codeblock_converter) -> None:
    #     """Allows one to run python code"""
    #     jsk = self.bot.get_command("jishaku py")
    #     await jsk(ctx, argument=code)

    @commands.command(aliases=["edit"], hidden=True)
    @commands.is_owner()
    async def edit_bot_pic(self, ctx, avatar_location: str) -> None:
        """Changes the bot's profile picture"""
        valid = validators.url(avatar_location)
        if valid:
            async with aiohttp.ClientSession() as session:
                async with session.get(avatar_location) as resp:
                    img = await resp.read()
                    await self.bot.user.edit(avatar=img)
        else:
            with open(avatar_location, "rb") as file:
                avatar = file.read()
                await self.bot.user.edit(avatar=avatar)


def setup(bot: commands.Bot):
    print("I am being loaded!")
    bot.add_cog(OwnerCommands(bot))
