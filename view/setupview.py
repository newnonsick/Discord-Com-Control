import asyncio
import os

import discord


class SetupView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Shutdown", style=discord.ButtonStyle.danger, emoji="🛑")
    async def shutdown_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_message("⚠️ Shutting down...", ephemeral=True)
        os.system("shutdown /s /t 1")

    @discord.ui.button(label="Restart", style=discord.ButtonStyle.primary, emoji="🔄")
    async def restart_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_message("🔄 Restarting...", ephemeral=True)
        os.system("shutdown /r /t 1")

    @discord.ui.button(label="Lock PC", style=discord.ButtonStyle.secondary, emoji="🔒")
    async def lock_pc_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_message("🔒 Locking PC...", ephemeral=True)
        os.system("rundll32.exe user32.dll,LockWorkStation")
