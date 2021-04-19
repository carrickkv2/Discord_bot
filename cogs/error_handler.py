from discord.ext import commands


class CommandErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:

        """A global error handler cog."""

        if isinstance(error, commands.CommandNotFound):
            return  # Return because we don't want to show an error for every command not found

        elif isinstance(error, commands.CommandOnCooldown):
            message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."

        elif isinstance(error, commands.MissingPermissions):
            message = "You are missing the required permissions to run this command!"
            print(error)

        elif isinstance(error, commands.MissingRequiredArgument):
            message = "Please enter all the required arguments. Type ?help for more info on which arguments to add."
            print(error)

        elif isinstance(error, commands.CheckAnyFailure):
            message = "You do not have sufficient permissions to run this command!"
            print(error)

        elif isinstance(error, commands.UserInputError):
            message = "Something about your input was wrong, please check your input and try again!"
            print(error)

        elif isinstance(error, commands.CommandInvokeError):
            message = "Oh no! Your command failed to process \U0001f615."
            print(error)

        else:
            message = "Oh no! Something went wrong while running the command! \U0001f61f"
            print(error)

        await ctx.send(message, delete_after=8)

        await ctx.message.delete(delay=8)


def setup(bot: commands.Bot) -> None:
    """Load the Error_Handler cog."""
    print("I am being loaded!")
    bot.add_cog(CommandErrorHandler(bot))
