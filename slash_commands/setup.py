import os

import discord
from discord import app_commands
from discord.ext import commands

from view.setupview import SetupView


class Setup(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(
        name="setup", description="Setup the bot for first time usage."
    )

    async def setup_command(self, interaction: discord.Interaction):
        if interaction.guild is None:
            return

        await interaction.response.send_message(
            "🎛️ Setting up the **Control Panel**... 🚀", ephemeral=True
        )

        embed = discord.Embed(
            title="💻 New's Control Panel",
            description=(
                "⚡ **Manage New's Computer with ease!**\n\n"
                "🛑 **Shutdown** – Power off safely\n"
                "🔄 **Restart** – Quick reboot\n"
                "🔒 **Lock PC** – Secure PC\n\n"
                "✨ *Tap a button below to begin!*"
            ),
            color=discord.Color.magenta(),
        )

        embed.set_image(url="https://i.gifer.com/WBON.gif")
        embed.set_footer(text="Made with ❤️ by New")

        if isinstance(interaction.channel, discord.TextChannel):
            message = await interaction.channel.send(embed=embed, view=SetupView())

            with open("message_id.txt", "w") as file:
                file.write(str(message.id))

            with open("channel_id.txt", "w") as file:
                file.write(str(interaction.channel.id))
        else:
            await interaction.followup.send("🚫 Use this in a text channel!", ephemeral=True)
