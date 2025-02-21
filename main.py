import asyncio
import os

import discord
from discord.ext import commands

from client_event.gateway_event import GatewayEvents
from slash_commands.setup import Setup

intents = discord.Intents.default()
intents.messages = True
intents.voice_states = True
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix="n!", intents=intents)

async def main():
    async with client:
        await asyncio.gather(
            client.add_cog(GatewayEvents(client=client)),
            client.add_cog(Setup(client=client)),
        )
        await client.start(str(os.getenv("BOT_TOKEN")))


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except discord.HTTPException as e:
        if e.status == 429:
            print(
                "The Discord servers denied the connection for making too many requests."
            )
            print(
                "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
            )
            os.system("python restart.py")
            os.system("kill 1")
        else:
            raise e
