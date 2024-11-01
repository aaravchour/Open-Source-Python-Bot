import nextcord
from nextcord.ext import commands
from nextcord import Interaction


class fun(commands.Cog):

    @nextcord.slash_command()
    async def speak(self, interaction: nextcord.Interaction, message: str):
        await interaction.response.send_message("Babe Tunde will be with you shortly.")


def setup(bot):
    bot.add_cog(fun(bot))
