import random
import nextcord
from nextcord.ext import commands
import json


async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("mainbank.json", "w") as f:
        json.dump(users, f)

    return True


async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)

    return users


async def update_bank(user, change=0, mode="wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    bal = users[str(user.id)]["wallet"], users[str(user.id)]["bank"]
    return bal


async def buy_this(user, item_name, amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False, 1]

    cost = price * amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0] < cost:
        return [False, 2]

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index += 1
        if t == None:
            obj = {"item": item_name, "amount": amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item": item_name, "amount": amount}
        users[str(user.id)]["bag"] = [obj]

    with open("mainbank.json", "w") as f:
        json.dump(users, f)

    await update_bank(user, cost * -1, "wallet")

    return [True, "Worked"]


async def sell_this(user, item_name, amount, price=None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price == None:
                price = 0.7 * item["price"]
            break

    if name_ == None:
        return [False, 1]

    cost = price * amount

    users = await get_bank_data()

    bal = await update_bank(user)

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False, 2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index += 1
        if t == None:
            return [False, 3]
    except:
        return [False, 3]

    with open("mainbank.json", "w") as f:
        json.dump(users, f)

    await update_bank(user, cost, "wallet")

    return [True, "Worked"]


mainshop = [
    {"name": "Dal Makhani", "price": 2, "description": "Food"},
    {"name": "Pav Bhaji", "price": 1, "description": "Food"},
    {"name": "Butter Chicken", "price": 3, "description": "Food"},
    {"name": "Dosa and Idli", "price": 2, "description": "Food"},
    {"name": "Kukure", "price": 0.2, "description": "Food"},
    {"name": "Lays - India's Magic Masala", "price": 0.4, "description": "Food"},
    {"name": "Punjabi MC", "price": 50, "description": "Music"},
    {"name": "TATA Car", "price": 300000, "description": "Vehicles"},
]


class economy(commands.Cog):

    @nextcord.slash_command(description="View your balance")
    async def balance(self, interaction: nextcord.Interaction):
        emoji = "<:ravi_coin:1054142722405060640>"
        await open_account(interaction.user)
        user = interaction.user

        users = await get_bank_data()

        wallet_amt = users[str(user.id)]["wallet"]
        bank_amt = users[str(user.id)]["bank"]

        em = nextcord.Embed(
            title=f"{interaction.user} Balance", color=nextcord.Color.red()
        )
        em.add_field(
            name=f"Wallet Balance <:ravi_coin:1054142722405060640>", value=wallet_amt
        )
        em.add_field(
            name=f"Bank Balance <:ravi_coin:1054142722405060640>", value=bank_amt
        )
        await interaction.response.send_message(embed=em)

    @nextcord.slash_command(description="Beg for money")
    async def beg(self, interaction: nextcord.Interaction):
        emoji = "<:ravi_coin:1054142722405060640>"
        await open_account(interaction.user)
        user = interaction.user

        users = await get_bank_data()

        earnings = random.randrange(101)

        await interaction.response.send_message(
            f"{interaction.user.mention} Got {earnings} {emoji}"
        )

        users[str(user.id)]["wallet"] += earnings

        with open("mainbank.json", "w") as f:
            json.dump(users, f)

    @nextcord.slash_command(description="Take money from your bank to your wallet")
    async def withdraw(self, interaction: nextcord.Interaction, amount=None):
        emoji = "<:ravi_coin:1054142722405060640>"
        await open_account(interacion.user)
        if amount == None:
            await interaction.response.send_message("Please enter the amount")
            return

        bal = await update_bank(interaction.user)

        amount = int(amount)

        if amount > bal[1]:
            await interaction.response.send_message(
                "You do not have sufficient balance"
            )
            return
        if amount < 0:
            await interaction.response.send_message("Amount must be positive!")
            return

        await update_bank(interaction.user, amount)
        await update_bank(interaction.user, -1 * amount, "bank")
        await interaction.response.send_message(
            f"{interaction.user} You withdrew {amount} {emoji}"
        )

    @nextcord.slash_command(description="Put money in your bank")
    async def deposit(self, interaction: nextcord.Interaction, amount=None):
        emoji = "<:ravi_coin:1054142722405060640>"
        await open_account(interaction.user)
        if amount == None:
            await interaction.response.send_message("Please enter the amount")
            return

        bal = await update_bank(interaction.user)

        amount = int(amount)

        if amount > bal[0]:
            await interaction.response.send_message(
                "You do not have sufficient balance"
            )
            return
        if amount < 0:
            await interaction.response.send_message("Amount must be positive!")
            return

        await update_bank(interaction.user, -1 * amount)
        await update_bank(interaction.user, amount, "bank")
        await interaction.response.send_message(
            f"{interaction.user} You deposited {amount} {emoji}"
        )

    @nextcord.slash_command(description="Send money to someone")
    async def send(
        self, interaction: nextcord.Interaction, member: nextcord.Member, amount=None
    ):
        emoji = "<:ravi_coin:1054142722405060640>"
        await open_account(interaction.user)
        await open_account(member)
        if amount == None:
            await interaction.response.send_message("Please enter the amount")
            return

        bal = await update_bank(interaction.user)
        if amount == "all":
            amount = bal[0]

        amount = int(amount)

        if amount > bal[0]:
            await interaction.response.send_message(
                "You do not have sufficient balance"
            )
            return
        if amount < 0:
            await interaction.response.send_message("Amount must be positive!")
            return

        await update_bank(interaction.user, -1 * amount, "bank")
        await update_bank(member, amount, "bank")
        await interaction.response.send_message(
            f"{interaction.user} You gave {member} {amount} {emoji}"
        )

    @nextcord.slash_command(description="Rob someone")
    async def rob(self, interaction: nextcord.Interaction, member: nextcord.Member):
        emoji = "<:ravi_coin:1054142722405060640>"
        await open_account(interaction.user)
        await open_account(member)
        bal = await update_bank(member)

        if bal[0] < 100:
            await interaction.response.send_message("It is useless to rob him :(")
            return

        earning = random.randrange(0, bal[0])

        await update_bank(interaction.user, earning)
        await update_bank(member, -1 * earning)
        await interaction.response.send_message(
            f"{interaction.user.mention} You robbed {member} and got {earning} {emoji}"
        )

    @nextcord.slash_command(description="View the shop's items")
    async def shop(self, interaction: nextcord.Interaction):
        emoji = "<:ravi_coin:1054142722405060640>"
        em = nextcord.Embed(title="🛒**Shop**")

        for item in mainshop:

            name = item["name"]
            price = item["price"]
            desc = item["description"]
            em.add_field(name=name, value=f"{emoji} {price} | {desc}")

        await interaction.response.send_message(embed=em)

    @nextcord.slash_command(description="Buy something from the shop")
    async def buy(self, interaction: nextcord.Interaction, item, amount=1):
        emoji = "<:ravi_coin:1054142722405060640>"
        await open_account(interaction.user)

        res = await buy_this(interaction.user, item, amount)

        if not res[0]:
            if res[1] == 1:
                await interaction.response.send_message("That Object isn't there!")
                return
            if res[1] == 2:
                await interaction.response.send_message(
                    f"You don't have enough {emoji} in your wallet to buy {amount} {item}"
                )
                return

        await interaction.response.send_message(f"You just bought {amount} {item}")

    @nextcord.slash_command(description="View whats in your inventory")
    async def inventory(self, interaction: nextcord.Interaction):
        emoji = "<:inventory:1065703736846073947>"
        await open_account(interaction.user)
        user = interaction.user
        users = await get_bank_data()

        try:
            bag = users[str(user.id)]["bag"]
        except:
            bag = []

        em = nextcord.Embed(title=f"{emoji} Inventory")
        for item in bag:
            name = item["item"]
            amount = item["amount"]

            em.add_field(name=name, value=amount)

        await interaction.response.send_message(embed=em)

    @nextcord.slash_command(description="Sell something in your bag")
    async def sell(self, interaction: nextcord.Interaction, item, amount=1):
        emoji = "<:ravi_coin:1054142722405060640>"
        await open_account(interaction.user)

        res = await sell_this(interaction.user, item, amount)

        if not res[0]:
            if res[1] == 1:
                await interaction.response.send_message("That Object isn't there!")
                return
            if res[1] == 2:
                await interaction.response.send_message(
                    f"You don't have {amount} {item} in your bag."
                )
                return
            if res[1] == 3:
                await interaction.response.send_message(
                    f"You don't have {item} in your bag."
                )
                return

        await interaction.response.send_message(f"You just sold {amount} {item}.")

    @nextcord.slash_command(description="See who's the richest in your server")
    async def leaderboard(self, interaction: nextcord.Interaction, x=1):
        emoji = "<:ravi_coin:1054142722405060640>"
        users = await get_bank_data()
        leader_board = {}
        total = []
        for user in users:
            name = int(user)
            total_amount = users[user]["wallet"] + users[user]["bank"]
            leader_board[total_amount] = name
            total.append(total_amount)

        total = sorted(total, reverse=True)

        em = nextcord.Embed(
            title=f"Top {x} Richest People",
            description="This is decided on the basis of raw money in the bank and wallet",
            color=nextcord.Color(0xFA43EE),
        )
        index = 1
        for amt in total:
            id_ = leader_board[amt]
            member = interaction.user.id
            name = member.name
            em.add_field(name=f"{index}. {name}", value=f"{amt}", inline=False)
            if index == x:
                break
            else:
                index += 1

        await interaction.response.send_message(embed=em)

    @nextcord.slash_command()
    async def use(self, interaction: nextcord.Interaction, item: str):

        await interaction.send(f"{item}")
        if {item} == "tata car":
            await interaction.send("Where would you like to go?")


def setup(bot):
    bot.add_cog(economy(bot))
