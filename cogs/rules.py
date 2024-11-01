import nextcord
from nextcord.ext import commands
from nextcord import Interaction


class rules(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(
        description="Writes out rules for your server so you don't have to!"
    )
    async def rules(self, interaction: nextcord.Interaction):
        embed = nextcord.Embed(
            title="**Rules**",
            description="""
**1. Be Respectful**

Show respect to all members of the Discord server. Harassment and bullying are not allowed in any form and may result in being muted or kicked.

**2. Follow Discord’s Rules**

Don’t do anything that would get yourself or this server banned from Discord. You can find the full list of Discord’s community guidelines here: https://discord.com/guidelines

**3. Follow Real-World Laws**

We do not allow discussion of anything that relates to breaking real-world laws. This includes topics like hacking or doxing.

**4. No Adult Content**

This is a community server. We do not allow discussion of adult or NSFW content, and images / video containing NSFW material are prohibited.

**5. No Offensive Profiles**

Profile names or pictures containing adult or offensive material will asked to be changed.

**6. No Spamming**

Please do not send a large volume of small messages in the server repeatedly. This makes it difficult for other people to follow and engage in discussions.

**7. Do Not Raid Other Servers**

Discussing raids or participating in the raids of other servers will not be tolerated here. Raiding another server may result in a permanent ban from this one.

**8. Abide By The Decisions Of Moderators**

Moderators reserve the right to kick, ban or mute server members at their discretion, even if a rule on this list was not violated. If you believe that you have been treated unfairly by a moderator, please contact the administrator. 
""",
            colour=0xF1C40F,
        )
        await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(rules(bot))
