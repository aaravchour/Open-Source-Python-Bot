import nextcord
from nextcord.ext import commands
from nextcord import Interaction


class moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command()
    async def kick(self, interaction, member: nextcord.Member, *, reason=None):
        if reason == None:
            reason = "No Reason Provided"
        if interaction.user.guild_permissions.ban_members == True:
            await interaction.guild.kick(member, reason=reason)
            em = nextcord.Embed(
                title="**:white_check_mark: Kicked**",
                description=f"{member.name} has been kicked",
                color=nextcord.Color.green(),
            )
            em.add_field(name="**Reason:**", value=reason, inline=False)
            await interaction.send(embed=em)
            em2 = nextcord.Embed(
                title=":x: **Kicked**",
                description=f"You have been kicked from {interaction.guild.name}",
                colour=nextcord.Color.red(),
            )
            em.add_field(name="**Reason:**", value=reason, inline=False)
            await member.send(embed=em2)

    @nextcord.slash_command()
    async def unban(self, interaction, member: nextcord.User, *, reason=None):
        if reason == None:
            reason = "No Reason Provided"
        if interaction.user.guild_permissions.ban_members == True:
            await interaction.guild.unban(member, reason=reason)
            em = nextcord.Embed(
                title=":white_check_mark: **Unbanned**",
                description=f"{member.name} has been unbanned",
                colour=nextcord.Color.green(),
            )
            em.add_field(name="**Reason:**", value=reason, inline=False)
            await interaction.send(embed=em)
            em2 = nextcord.Embed(
                title=":white_check_mark: **Unbanned**",
                description=f"You have been unbanned from {interaction.guild.name}",
                colour=nextcord.Color.red(),
            )
            em.add_field(name="**Reason:**", value=reason, inline=False)
            await member.send(embed=em2)

    @nextcord.slash_command()
    async def ban(self, interaction, member: nextcord.User, *, reason=None):
        if reason == None:
            reason = "No Reason Provided"
        if interaction.user.guild_permissions.ban_members == True:
            await interaction.guild.ban(member, reason=reason)
            em = nextcord.Embed(
                title=":white_check_mark: **Banned**",
                description=f"{member.name} has been banned",
                colour=nextcord.Color.green(),
            )
            em.add_field(name="**Reason:**", value=reason, inline=False)
            await interaction.send(embed=em)
            em2 = nextcord.Embed(
                title=":x: **Banned**",
                description=f"You have been banned from {interaction.guild.name}",
                colour=nextcord.Color.red(),
            )
            em.add_field(name="**Reason:**", value=reason, inline=False)
            await member.send(embed=em2)

    @nextcord.slash_command(description="Mutes the specified user.")
    async def mute(self, interaction, member: nextcord.Member, *, reason=None):
        guild = interaction.guild
        mutedRole = nextcord.utils.get(guild.roles, name="Muted")

        if not mutedRole:

            for channel in guild.channels:
                await channel.set_permissions(
                    mutedRole,
                    speak=False,
                    send_messages=False,
                    read_message_history=True,
                    read_messages=False,
                )
        if interaction.user.guild_permissions.ban_members == True:
            embed = nextcord.Embed(
                title=":white_check_mark: **Muted**",
                description=f"{member.mention} was muted ",
                colour=nextcord.Color.green(),
            )
            embed.add_field(name="**Reason:**", value=reason, inline=False)
            await interaction.send(embed=embed)
            await member.add_roles(mutedRole, reason=reason)
            em = nextcord.Embed(
                title=":x:**Muted**",
                description=f"""You have been muted from {interaction.guild.name}""",
                colour=nextcord.Color.red(),
            )
            em.add_field(name="**Reason:**", value=reason, inline=False)
            await member.send(embed=em)

    @nextcord.slash_command(description="Unmutes a specified user.")
    async def unmute(self, interaction, member: nextcord.Member):
        if interaction.user.guild_permissions.ban_members == True:
            guild = interaction.guild
            role = nextcord.utils.get(guild.roles, name="Muted")
            await member.remove_roles(role)
            em = nextcord.Embed(
                title=":white_check_mark: **Unmuted**",
                description=f"{member.name} has been unmuted",
                colour=nextcord.Color.green(),
            )
            await interaction.send(embed=em)
            em2 = nextcord.Embed(
                title=":x: **Unmuted**",
                description=f"You have been unmuted from {interaction.guild.name}",
                colour=nextcord.Color.red(),
            )
            await member.send(embed=em2)


def setup(bot):
    bot.add_cog(moderation(bot))
