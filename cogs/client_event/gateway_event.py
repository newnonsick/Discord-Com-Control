import asyncio
import os

import discord
from discord.ext import commands

from view.setupview import SetupView


class GatewayEvents(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client

    def getChannel(self) -> discord.TextChannel | None:
        if os.path.exists("channel_id.txt") and os.stat("channel_id.txt").st_size > 0:
            try:
                with open("channel_id.txt", "r") as file:
                    channel_id = int(file.read().strip())

                channel = self.client.get_channel(channel_id)

                if not isinstance(channel, discord.TextChannel) or not channel:
                    print("⚠️ Channel not found. Please use `/setup` again.")
                    return None

                return channel
            except ValueError:
                print("⚠️ Invalid channel ID stored. Please use `/setup` again.")
                return None
            except Exception as e:
                print(f"⚠️ Could not read channel ID: {e}")
                return None
        else:
            print("⚠️ No previous channel ID found. Use `/setup` to create one.")
            return None

    async def reloadView(self):
        channel = self.getChannel()
        if not channel:
            return

        if os.path.exists("message_id.txt") and os.stat("message_id.txt").st_size > 0:
            try:
                with open("message_id.txt", "r") as file:
                    message_id = int(file.read().strip())

                if isinstance(channel, discord.TextChannel):
                    try:
                        message = await channel.fetch_message(message_id)
                        await message.edit(view=SetupView())
                        print("🔄 Buttons reattached after restart!")
                    except discord.NotFound:
                        print(
                            "⚠️ Message not found. It may have been deleted. Please use `/setup` again."
                        )
                    except discord.Forbidden:
                        print(
                            "⚠️ Bot does not have permission to view/edit this message."
                        )
                    except Exception as e:
                        print(f"⚠️ Unexpected error while fetching message: {e}")
            except ValueError:
                print("⚠️ Invalid message ID stored. Please use `/setup` again.")
            except Exception as e:
                print(f"⚠️ Could not read message ID: {e}")
        else:
            print("⚠️ No previous setup message found. Use `/setup` to create one.")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.tree.sync()
        if not self.client.user:
            print("We are not logged in.")
            return

        await self.reloadView()
        await self.client.change_presence(
            activity=discord.Game(name="Online alongside New!"),
        )

        print(f"We have logged in as {self.client.user.name}")


async def setup(client: commands.Bot):
    await client.add_cog(GatewayEvents(client))
