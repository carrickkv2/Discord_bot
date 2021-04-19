import os
from os import getenv
import discord
from discord.ext import commands
from dotenv import load_dotenv
from cogs import admin, embed, embed_no_timezone, embed_days_timezone, embed_day_timezone, error_handler, owner_commands,message_attachments
from cogs.help_commands import EmbedHelpCommand


load_dotenv()  # For the env file

os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"

intents = discord.Intents.default()  # All but the two privileged ones

intents.members = True  # Subscribe to the Members intent

bot = commands.Bot(command_prefix="?", allowed_mentions=discord.AllowedMentions(
    users=False,  # Whether to ping individual user @mentions
    everyone=False,  # Whether to ping @everyone or @here mentions
    roles=False,  # Whether to ping role @mentions
    replied_user=False,  # Whether to ping on replies to messages
), intents=intents, help_command=EmbedHelpCommand()
                   )

bot.load_extension("owner_commands")

bot.load_extension('jishaku')

bot.load_extension('admin')

bot.load_extension("error_handler")

bot.load_extension("message_attachments")

bot.load_extension("embed")

bot.load_extension("embed_no_timezone")

bot.load_extension("embed_day_timezone")

bot.load_extension("embed_days_timezone")

token = getenv("TOKEN")
bot.run(token)
