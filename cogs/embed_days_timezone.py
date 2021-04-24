from discord.ext import commands
import discord
import pytz
import datetime
from cogs.utils.functions_used import get_days, modify_dict, csv_to_df_to_dict, get_deep_copy
from cogs.utils.timezone_finder import get_timezone_of_user
from cogs.utils.paths_for_functions import path_for_csv_to_dict


class EmbedDaysTimezone(commands.Cog, name="All Days In Your TimeZone"):
    """
    This cog sends back to the user all events and times of the events happening on all days.
    All times are in EST.
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(name="daystz",
                      aliases=["Daystz"],
                      brief="Shows the schedule of all days in the users TimeZone.",
                      help="Shows a detailed list of all events happening on all days and the time they happen "
                           "on in the users Timezone. Time is a required argument.\n"
                           "Example usage is `?daystz ghana`"
                      )
    async def emb_days_tz(self, ctx: commands.Context, timezone: str) -> None:

        async with ctx.message.channel.typing():

            user = await self.bot.fetch_user(230942498086846464)

            if timezone == 'EST':
                time_zone = pytz.timezone('EST')
            else:
                time_zone = pytz.timezone(get_timezone_of_user(timezone))

            embed = discord.Embed(
                title='Schedule For All Days' + " In The " + str(time_zone) + " timezone",
                colour=discord.Colour.random(),
                timestamp=datetime.datetime.utcnow(),
            )

            embed.set_footer(
                text=f"See any bugs? {user.display_name} \nType ?help for help commands",
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
                        date_aware_time = datetime.datetime.fromisoformat(key)
                        current_time = date_aware_time.astimezone(tz=time_zone)
                        final_time = current_time.strftime("%a %b %d %Y %I:%M %p")
                        embed.add_field(name=value, value=final_time, inline=False)

            embed.add_field(
                name="NB",
                value="Some of the days and times may have been changed to the next day because of your timezone\n",
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
    """Load the embed_days_timezone cog."""
    print("I am being loaded!")
    bot.add_cog(EmbedDaysTimezone(bot))
