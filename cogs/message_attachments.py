from discord.ext import commands
import pathlib
from cogs.utils.extract_table import extract_to_csv, usage_extract
from cogs.utils.write_headers import write_csv
from cogs.utils.file_exists import rename_and_move, rename_csv
from cogs.utils.paths_for_functions import path_for_csv_output_for_both_rename_and_extract, path_for_write_csv


# from csv_to_df import csv_to_df_to_dict
# import logging


def my_custom_check():
    def predicate(ctx: commands.Context):
        if ctx.message.channel.id == 721443699288178778 or ctx.message.author.id == 230942498086846464:
            return True

    return commands.check(predicate)


class Attachments(commands.Cog):
    """
    This cog gets the image the user attaches to a message
    so that we can turn it into a csv.
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.check_any(my_custom_check())
    @commands.cooldown(1, 120, commands.BucketType.user)
    @commands.command(name="at",
                      aliases=["att"],
                      brief="Get's the image attachment from the message",
                      help="Get's the image posted in announcements and processes it so that it can be used by the bot.\n"
                           "This command can only be used in the announcements channel.\n"
                           "Example usage is `?at <message to post here>`"
                      )
    async def read_url(self, ctx: commands.Context) -> None:
        """
        Gets the image attachment from the message
        """
        # logger = logging.Logger('catch_all')

        attachment_string = ""
        output = pathlib.Path(path_for_csv_output_for_both_rename_and_extract)
        user = await self.bot.fetch_user(230942498086846464)
        if not ctx.message.attachments:
            await ctx.message.add_reaction('\U0000274c')
        else:
            async with ctx.message.channel.typing():
                try:
                    attachment = ctx.message.attachments[0]
                    attachment_string += str(attachment)
                    attachment_string = attachment_string.rstrip('\n')
                    rename_and_move(output)
                    await user.send(usage_extract())
                except Exception as e:
                    print(e)
                    await ctx.message.add_reaction('\U0000274c')
                    await user.send(str(e))
                    raise
                try:
                    if extract_to_csv(attachment_string, output):
                        try:
                            rename_csv(output)
                            write_csv(path_for_write_csv)
                            await ctx.message.add_reaction('\U00002611')
                        except Exception as e:
                            print(e)
                            await ctx.message.add_reaction('\U0000274c')
                            await user.send(str(e))
                            raise
                except Exception as e:
                    print(e)
                    # logger.exception('Failed: ' + str(e))
                    await ctx.message.add_reaction('\U0000274c')
                    await user.send(str(e))
                    raise

            # Put the extract API here and let the check mark come only after the extract API runs
            # Todo: Take all the rstrings and put them in one file, then import from that file to your functions


def setup(bot: commands.Bot) -> None:
    print("I am being loaded!")
    bot.add_cog(Attachments(bot))
