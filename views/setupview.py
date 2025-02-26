import datetime
import os

import discord
from pyautogui import screenshot

from views.confirmationview import ConfirmationView


class SetupView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Shutdown", style=discord.ButtonStyle.danger, emoji="🛑")
    async def shutdown_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_message(
            "⚠️ Are you sure you want to shut down?",
            view=ConfirmationView("shutdown"),
            ephemeral=True,
        )

    @discord.ui.button(label="Restart", style=discord.ButtonStyle.primary, emoji="🔄")
    async def restart_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_message(
            "🔄 Are you sure you want to restart?",
            view=ConfirmationView("restart"),
            ephemeral=True,
        )

    @discord.ui.button(label="Lock PC", style=discord.ButtonStyle.secondary, emoji="🔒")
    async def lock_pc_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_message("🔒 Locking PC...", ephemeral=True)

        bot_owner = await interaction.client.application_info()
        if interaction.user.id != bot_owner.owner.id:
            await bot_owner.owner.send(
                f"🔒 {interaction.user.mention} has locked the computer"
            )

        os.system("rundll32.exe user32.dll,LockWorkStation")

    @discord.ui.button(
        label="Screenshot", style=discord.ButtonStyle.blurple, emoji="📸"
    )
    async def screenshot_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        try:
            await interaction.response.defer()

            screenshot_path = f"screenshot_{datetime.datetime.now().timestamp()}.png"
            img = screenshot()
            img.save(screenshot_path)

            await interaction.followup.send(
                file=discord.File(screenshot_path), ephemeral=True
            )

            bot_owner = await interaction.client.application_info()
            if interaction.user.id != bot_owner.owner.id:
                await bot_owner.owner.send(
                    f"📸 Screenshot taken by {interaction.user.mention} in {interaction.guild.name if interaction.guild else 'DM'}.",
                    file=discord.File(screenshot_path),
                )

        except Exception as e:
            await interaction.followup.send(
                f"❌ Error taking screenshot: {e}", ephemeral=True
            )

        finally:
            if os.path.exists(screenshot_path):
                os.remove(screenshot_path)
