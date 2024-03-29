import datetime

import discord
from cogs.utils.functions_used import csv_to_df_to_dict
from cogs.utils.functions_used import get_deep_copy
from cogs.utils.functions_used import modify_dict
from cogs.utils.lists_dicts import order
from cogs.utils.paths_for_functions import path_for_csv_to_dict
from discord.ext import commands


class EmbedNoTimeZone(commands.Cog, name="Specific Day In EST"):
    """
    This cog sends back to the user all events and times associated with a day.
    All times are in EST.
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.command(
        name="day",
        aliases=["Day"],
        brief="Shows the schedule of a specific day in EST",
        help="Shows a detailed list of all events happening on a specific day and the time they happen "
        "on in EST. Day is a required argument.\n "
        "Example usage is `?day tuesday`",
    )
    async def emb_no_tz(self, ctx: commands.Context, *, day: str) -> None:
        """
        Gets the day from the user and returns an embed containing all events happening on that day.
        Day is a required argument.
        """
        async with ctx.message.channel.typing():

            user = await self.bot.fetch_user(230942498086846464)

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
                text=f"See any bugs? {user.display_name} \nType ?help for help commands",
                icon_url="https://cdn.discordapp.com/emojis/754736642761424986.png",
            )

            copy_of_dictionary_from_numpy = modify_dict(get_deep_copy(csv_to_df_to_dict(path_for_csv_to_dict)))

            for key, value in copy_of_dictionary_from_numpy[day].items():
                if "Eastern" in key:
                    embed.add_field(name=value, value="~", inline=False)
                else:
                    t = datetime.datetime.fromisoformat(key)
                    t = t.strftime("%I:%M %p")
                    embed.add_field(name=value, value=t, inline=False)

            embed.add_field(name="NB", value="These times are in EST\n", inline=True)

            emoji = "\N{Wastebasket}"

        message_reaction_embed = await ctx.send(embed=embed)
        await message_reaction_embed.add_reaction(emoji)

        await self.bot.wait_for(
            "reaction_add",
            check=lambda r, u: r.message == message_reaction_embed and u == ctx.author and str(r) == emoji,
        )
        await message_reaction_embed.delete()


def setup(bot: commands.Bot) -> None:
    """Load the embed_no_timezone cog."""
    print("I am being loaded!")
    bot.add_cog(EmbedNoTimeZone(bot))
