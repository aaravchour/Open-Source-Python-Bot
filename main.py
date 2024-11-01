import os
import nextcord
from nextcord.ext import commands
from nextcord import TextChannel
from nextcord import Permissions
import asyncio
import sqlite3

connection = sqlite3.connect("logchannels.db")
print(connection.total_changes)
cursor = connection.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS logchannels(user_id INTEGER, log_id INTEGER)"
)
intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True
token = "INSERT TOKEN"
client_id = "INSERT CLIENT ID"
bot = commands.Bot(command_prefix="[", intents=intents, help_command=None)
intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True
len(bot.guilds)


@bot.event
async def on_ready():
    len(bot.guilds)
    await bot.change_presence(
        activity=nextcord.Activity(
            type=nextcord.ActivityType.watching, name=str(len(bot.guilds)) + " Servers!"
        )
    )

    print("Connected to bot: {}".format(bot.user.name))
    print("Bot ID: {}".format(bot.user.id))


# cogs
#
#
#
#
#
#
#


@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")
    em = nextcord.Embed(
        title=f":white_check_mark: ```{extension}``` has been loaded",
        color=nextcord.Color.green(),
    )
    await ctx.send(embed=em)


@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    em = nextcord.Embed(
        title=f":white_check_mark: ```{extension}``` has been unloaded",
        color=nextcord.Color.green(),
    )
    await ctx.send(embed=em)


@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    bot.load_extension(f"cogs.{extension}")
    em = nextcord.Embed(
        title=f":white_check_mark: ```{extension}``` has been reloaded",
        color=nextcord.Color.green(),
    )
    await ctx.send(embed=em)


#
#
#
#
#
# logging system


def myfunc(logchannel: int):
    print(logchannel)


@bot.slash_command(
    default_member_permissions=Permissions(administrator=True),
    description="Set your log channel",
)
async def logcset(interaction, logchannel: TextChannel):
    chnl = logchannel.id
    print(chnl)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO logchannels VALUES(?, ?)", (interaction.guild.id, chnl))
    connection.commit()
    print("done")
    await interaction.send("Done!")


@bot.event
async def on_message_delete(message):
    embed = nextcord.Embed(
        title="**Message Deleted**",
        description=f"{message.author.name} has deleted a message!",
        color=nextcord.Color.red(),
    )
    embed.add_field(name="Message Content", value=f"{message.content}")
    cur = connection.cursor()
    db_row = cur.execute(
        "SELECT log_id FROM logchannels WHERE user_id=?", (message.guild.id,)
    )
    db_row_result = db_row.fetchone()
    if db_row_result is None:
        print("no log channel for this user")
    else:
        log_id = db_row_result[0]
        print(log_id)
        channel = bot.get_channel(log_id)
        if channel is not None:
            await channel.send(embed=embed)


@bot.event
async def on_message_edit(message_before, message_after):
    embed = nextcord.Embed(
        title="**Message Edited**",
        description=f"{message_before.author.name} has edited a message!",
        color=nextcord.Color.blue(),
    )
    embed.add_field(name="Message Before", value=f"{message_before.content}")
    embed.add_field(name="Message After", value=f"{message_after.content}")
    cur = connection.cursor()
    db_row = cur.execute(
        "SELECT log_id FROM logchannels WHERE user_id=?", (message_before.guild.id,)
    )
    db_row_result = db_row.fetchone()
    if db_row_result is None:
        print("no log channel for this user")
    else:
        log_id = db_row_result[0]
        print(log_id)
        channel = bot.get_channel(log_id)
        if channel is not None:
            await channel.send(embed=embed)


#
#
#
#
#
# errors


@bot.event
async def on_application_command_error(interaction, error):
    if isinstance(error, commands.BadArgument):
        em = nextcord.Embed(
            title=":x: Wrong Arguement",
            description="Please try again with the correct arguements beta!",
        )
        await ctx.send(embed=em)


@bot.event
async def on_application_command_error(interaction, error):
    if isinstance(error, Forbidden.MissingPermissions):
        em = nextcord.Embed(
            title=":x: Missing Permissions",
            description="You are missing permissions to run this command beta!",
        )
        await ctx.send(embed=em)


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
        print(f"Loaded {filename[:-3]}")

bot.run(token)
