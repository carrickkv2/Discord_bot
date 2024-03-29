import datetime

import discord
import pytz
from cogs.utils.functions_used import csv_to_df_to_dict
from cogs.utils.functions_used import get_deep_copy
from cogs.utils.functions_used import modify_dict
from cogs.utils.paths_for_functions import path_for_csv_to_dict
from cogs.utils.timezone_finder import get_timezone_of_user
from discord.ext import commands


class EmbedTimeZone(commands.Cog, name="Specific Day In Your Timezone"):
    """
    This cog sends back to the user all events and times associated with a day.
    Times for the events are returned in the users timezone.
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(
        name="daytz",
        aliases=["Daytz"],
        brief="Shows the schedule of a specific day in the users TimeZone.",
        help="Shows a detailed list of all events happening on a specific day and the time they happen "
        "on in the users Timezone. Both day and time are required arguments.\n"
        "Example usage is `?daytz tuesday ghana`",
    )
    async def emb_tz(self, ctx: commands.Context, day: str, timezone: str) -> None:
        """
        Gets the day from the user and returns an embed containing all events happening on that day.
        Both day and time are required arguments.
        """
        async with ctx.message.channel.typing():

            user = await self.bot.fetch_user(230942498086846464)

            if timezone == "EST":
                time_zone = pytz.timezone("EST")
            else:
                time_zone = pytz.timezone(get_timezone_of_user(timezone))

            day2 = "Schedule For " + str(day.title()) + " In The " + str(time_zone) + " timezone"

            embed = discord.Embed(
                title=day2,
                colour=discord.Colour.random(),
                timestamp=datetime.datetime.utcnow(),
            )

            embed.set_footer(
                text=f"See any bugs? {user.display_name} \nType ?help for help commands",
                icon_url="https://cdn.discordapp.com/emojis/754736642761424986.png",
            )

            copy_of_dictionary_from_numpy = modify_dict(get_deep_copy(csv_to_df_to_dict(path_for_csv_to_dict)))

            for key, value in copy_of_dictionary_from_numpy[day.title()].items():
                if "Eastern" in key:
                    embed.add_field(name=value, value="~\n", inline=False)
                else:
                    date_aware_time = datetime.datetime.fromisoformat(key)
                    current_time = date_aware_time.astimezone(tz=time_zone)
                    final_time = current_time.strftime("%a %b %d %Y %I:%M %p")
                    embed.add_field(name=value, value=final_time, inline=False)

            embed.add_field(
                name="NB",
                value="Some of the days and times may have been changed to the next day because of your timezone\n",
                inline=True,
            )

            emoji = "\N{Wastebasket}"

        message_reaction_embed = await ctx.send(embed=embed)
        await message_reaction_embed.add_reaction(emoji)

        await self.bot.wait_for(
            "reaction_add",
            check=lambda r, u: r.message == message_reaction_embed and u == ctx.author and str(r) == emoji,
        )
        await message_reaction_embed.delete()


def setup(bot: commands.Bot) -> None:
    """Load the embed_timezone cog."""
    print("I am being loaded!")
    bot.add_cog(EmbedTimeZone(bot))
