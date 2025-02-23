import discord
import os


class ConfirmationView(discord.ui.View):
    def __init__(self, action: str):
        super().__init__(timeout=30)
        self.action = action

    @discord.ui.button(label="✅ Confirm", style=discord.ButtonStyle.green)
    async def confirm(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if self.action == "shutdown":
            await interaction.response.send_message(
                "⚠️ Shutting down...", ephemeral=True
            )
            os.system("shutdown /s /t 1")
        elif self.action == "restart":
            await interaction.response.send_message("🔄 Restarting...", ephemeral=True)
            os.system("shutdown /r /t 1")
        self.stop()

    @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.gray)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("❌ Action canceled.", ephemeral=True)
        self.stop()
