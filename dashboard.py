import os
from quart import Quart, render_template, redirect, url_for
from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from nextcord.ext import ipc
import nextcord

app = Quart(__name__)

app.secret_key = b"topgravi"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"

app.config["DISCORD_CLIENT_ID"] = 858637375218122772
app.config["DISCORD_CLIENT_SECRET"] = "hIAujr__pOOwNcQXxEB0hNQZ_E6I8lAr"
app.config["DISCORD_REDIRECT_URL"] = "http://127.0.0.1:5000/callback"
app.config["DISCORD_CLIENT_ID"] = (
    "ODU4NjM3Mzc1MjE4MTIyNzcy.GOREsE.eYY5T3FA2S1sV6AdWU5LrR9P_BHhJxdelb6Ptc"
)

discord = DiscordOAuth2Session(app)


@app.route("/login/")
async def login():
    return await discord.create_session()


@app.route("/callback/")
async def callback():
    try:
        await discord.callback()
    except:
        return redirec(url_for("login"))
    return redirect(url_for("dashboard"))


@app.route("/")
async def index():
    return await render_template("index.html")


@app.route("/dashboard/")
async def dashboard():
    user = await discord.fetch_user()
    return await render_template("dashboard.html", user=user)


if __name__ == "__main__":
    app.run(debug=True)
