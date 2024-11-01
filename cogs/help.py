import nextcord
from nextcord.ext import commands
from nextcord import Interaction


class Dropdown(nextcord.ui.Select):
    def __init__(self):
        selectOptions = [
            nextcord.SelectOption(
                label="Moderation", description="View help for moderation commands"
            ),
            nextcord.SelectOption(
                label="Ranking and Economy System",
                description="View help for ranking and economy system commands",
            ),
            nextcord.SelectOption(
                label="Fun", description="View help for fun commands"
            ),
        ]
        super().__init__(
            placeholder="What do you need help with?",
            min_values=1,
            max_values=1,
            options=selectOptions,
        )

    async def callback(self, interaction):
        if self.values[0] == "Moderation":
            em1 = nextcord.Embed(
                title=":question: **Moderation**",
                description="All of the commands are listed below - If it is bold, it is optional",
                color=nextcord.Color.red(),
            )
            em1.add_field(
                name="</kick:1049422952237649960>",
                value="Kicks the specified user - Usage: /kick <user> **<reason>**",
            )
            em1.add_field(
                name="</ban:1049422950052417696>",
                value="Bans the specified user - Usage: /ban <user> **<reason>**",
            )
            em1.add_field(
                name="</unban:1049422869089747005>",
                value="Unbans the specified user - Usage: /unban <user> **<reason>**",
            )
            em1.add_field(
                name="</mute:1049422949075136625>",
                value="Mutes the specified user - Usage: /mute <user> **<reason>**",
            )
            em1.add_field(
                name="</unmute:1049422870486450297>",
                value="Unmutes the specified user - Usage: /unmute <user>",
            )
            em1.add_field(
                name="</rules:1054514208273870880>",
                value="Writes out rules for your server so you don't have to! - Usage: /rules",
            )
            em1.add_field(
                name="</logcset:1065392784653156464>",
                value="Set your log channel - Usage: /logcset <channel>",
            )
            view = DropdownView()
            await interaction.message.edit(embed=em1, view=view)

        elif self.values[0] == "Ranking and Economy System":
            em2 = nextcord.Embed(
                title=":question: **Ranking and Economy System**",
                description="All of the commands are listed below - If it is bold, it is optional",
                color=nextcord.Color.red(),
            )
            em2.add_field(
                name="</rank:1054514210345848843>",
                value="View yours or another person's rank - Usage: /rank **<user>**",
            )
            em2.add_field(
                name="</balance:1054514211813851166>",
                value="View yours or another person's balnce - Usage: /balance **<user>**",
            )
            em2.add_field(
                name="</beg:1054514213042786394>", value="Beg for money - Usage: /beg"
            )
            em2.add_field(
                name="</deposit:1054514293850243182>",
                value="Deposit money into your bank - Usage: /deposit <amount>",
            )
            em2.add_field(
                name="</withdraw:1054514214141706301>",
                value="Withdraw money from your bank - Usage: /withdraw <amount>",
            )
            em2.add_field(
                name="</send:1054514295423107132>",
                value="Send money to another person - Usage: /send <user> <amount>",
            )
            em2.add_field(
                name="</rob:1054514296756908082>",
                value="Rob money from another person - Usage: /Rob <user>",
            )
            em2.add_field(
                name="</shop:1054514297784520814>", value="View the shop - Usage: /shop"
            )
            em2.add_field(
                name="</buy:1054514298627559445>",
                value="Buy items from the shop - Usage: /buy <item>",
            )
            view = DropdownView()
            await interaction.message.edit(embed=em2, view=view)

        else:
            em3 = nextcord.Embed(
                title=":question: **Fun**",
                description="All of the commands are listed below - If it is bold, it is optional",
                color=nextcord.Color.red(),
            )
            em3.add_field(
                name="</shush:1049422868036984932>",
                value="Shush someone - Usage: /shush **<user>**",
            )
            em3.add_field(
                name="</speak:1050819650356777071>",
                value="Speak to Babe Tunde - Usage: /speak <message>",
            )
            view = DropdownView()
            await interaction.message.edit(embed=em3, view=view)


class DropdownView(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Dropdown())


class helpcommand(commands.Cog):
    @nextcord.slash_command(description="You need help from Babe Tunde")
    async def help(self, interaction: nextcord.Interaction):
        view = DropdownView()
        embed = nextcord.Embed(
            title=":question: **Help**",
            description="Got further questions? Join our support server :arrow_down:",
        )
        embed.add_field(name="Discord Server", value="https://discord.gg/UEQu6WCYV3")
        await interaction.send(embed=embed, view=view)


def setup(bot):
    bot.add_cog(helpcommand(bot))
