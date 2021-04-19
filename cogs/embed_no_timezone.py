import datetime
import discord
from discord.ext import commands
from utils.lists_dicts import order
from utils.functions_used import modify_dict, get_deep_copy, csv_to_df_to_dict
from utils.paths_for_functions import path_for_csv_to_dict


class EmbedNoTimeZone(commands.Cog, name="SpecificDayInEST"):
    """
    This cog sends back to the user all events and times associated with a day.
    All times are in EST.
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.command(name="day",
                      aliases=["Day"],
                      brief="Shows the schedule of a specific day in EST",
                      help="Shows a detailed list of all events happening on a specific day and the time they happen "
                           "on in EST. Day is a required argument.\n "
                           "Example usage is `?day tuesday`"
                      )
    async def emb_no_tz(self, ctx: commands.Context, *, day: str) -> None:

        # TODO: Raise an error if day is not given and print a string to the user. Also, log the error.
        """
        Gets the day from the user and returns an embed containing all events happening on that day.
        Day is a required argument.
        """
        async with ctx.message.channel.typing():

            for days in order:
                if days in day.title():
                    day = days

            day2 = "Schedule For " + str(day)

            embed = discord.Embed(
                title=day2,
                colour=discord.Colour.random(),
                timestamp=datetime.datetime.utcnow(),
            )

            embed.set_footer(
                text="See any bugs? @Aslan(The Lion) \nType ?help for help commands",
                icon_url="https://cdn.discordapp.com/emojis/754736642761424986.png",
            )

            copy_of_dictionary_from_numpy = modify_dict(
                get_deep_copy(csv_to_df_to_dict(path_for_csv_to_dict)))

            for key, value in copy_of_dictionary_from_numpy[day].items():
                if "EST" in key:
                    # val = str(day + " ") + "(" + str(value) + ")"
                    # val = "```py\n" + val + "\n```"
                    # val = '> ' + val
                    embed.add_field(name=value, value="~", inline=False)
                else:
                    t = datetime.datetime.fromisoformat(key)
                    t = t.strftime("%I:%M %p")
                    embed.add_field(name=value, value=t, inline=False)

            embed.add_field(
                name="NB",
                value="These times are in EST\n",
                inline=True
            )

            emoji = "\N{Wastebasket}"

        message_reaction_embed = await ctx.send(embed=embed)
        await message_reaction_embed.add_reaction(emoji)

        await self.bot.wait_for("reaction_add",
                                check=lambda r, u: r.message == message_reaction_embed and u == ctx.author and str(r) == emoji)
        await message_reaction_embed.delete()


def setup(bot: commands.Bot) -> None:
    """Load the embed_no_timezone cog."""
    print("I am being loaded!")
    bot.add_cog(EmbedNoTimeZone(bot))

# pick Tuesday from the EST, convert to utc
# If the UTC is the next day or the UTC is greater than 12 am
# then day should be the next Day and you should replace all the ESt times with UTC
# Else
# Just show the normal time
