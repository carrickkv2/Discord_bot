from discord.ext import commands
import discord
import datetime
from cogs.utils.functions_used import get_days, modify_dict, get_deep_copy, csv_to_df_to_dict
from cogs.utils.paths_for_functions import path_for_csv_to_dict


class Embed(commands.Cog, name="AllDaysInEST"):
    """
    This cog sends back to the user all events and times of the events happening on all days.
    All times are in EST.
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.command(name="days",
                      aliases=["Days"],
                      brief="Shows the schedule of all days in EST",
                      help="Shows a detailed list of all events happening and the time they happen on in EST.\n"
                           "Example usage is `?days`"
                      )
    async def emb(self, ctx: commands.Context) -> None:
        """
        Gets the day from the user and returns an embed containing all events happening on that day.
        Both day and time are required arguments.
        """
        async with ctx.message.channel.typing():

            embed = discord.Embed(
                title='Schedule For All Days',
                colour=discord.Colour.random(),
                timestamp=datetime.datetime.utcnow(),
            )

            embed.set_footer(
                text="See any bugs? @Aslan(The Lion) \nType ?help for help commands",
                icon_url="https://cdn.discordapp.com/emojis/754736642761424986.png",
            )

            copy_of_dictionary_from_numpy = modify_dict(
                get_deep_copy(csv_to_df_to_dict(path_for_csv_to_dict)))

            for day in get_days():
                for key, value in copy_of_dictionary_from_numpy[day].items():
                    if "EST" in key:
                        val = str(day + " ") + "(" + str(value) + ")"
                        val = "`" + val + "`"
                        # val = '> ' + val
                        embed.add_field(name=val, value="~", inline=False)
                    else:
                        t = datetime.datetime.fromisoformat(key)
                        # t = t.strftime("%a %b %d %H:%M")
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
                                check=lambda r, u: r.message == message_reaction_embed and u == ctx.author and str(
                                    r) == emoji)
        await message_reaction_embed.delete()


def setup(bot: commands.Bot) -> None:
    """Load the embed cog."""
    print("I am being loaded!")
    bot.add_cog(Embed(bot))

# , description="Returns back to the User all events and times of the events \
#                                                         happening on all days. All times are in EST."
