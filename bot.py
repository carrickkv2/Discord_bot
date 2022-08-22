import os
from os import getenv

import discord
from cogs.help_commands import EmbedHelpCommand
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()  # For the env file

os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"

intents = discord.Intents.default()  # All but the two privileged ones

intents.members = True  # Subscribe to the Members intent

bot = commands.Bot(
    command_prefix="?",
    allowed_mentions=discord.AllowedMentions(
        users=False,  # Whether to ping individual user @mentions
        everyone=False,  # Whether to ping @everyone or @here mentions
        roles=False,  # Whether to ping role @mentions
        replied_user=False,  # Whether to ping on replies to messages
    ),
    intents=intents,
    help_command=EmbedHelpCommand(),
)

bot.load_extension("cogs.owner_commands")

bot.load_extension("jishaku")

bot.load_extension("cogs.admin")

bot.load_extension("cogs.error_handler")

bot.load_extension("cogs.message_attachments")

bot.load_extension("cogs.embed")

bot.load_extension("cogs.embed_no_timezone")

bot.load_extension("cogs.embed_day_timezone")

bot.load_extension("cogs.embed_days_timezone")

token = getenv("TOKEN")
bot.run(token)
