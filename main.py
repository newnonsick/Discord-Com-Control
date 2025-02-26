import asyncio
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.messages = True
intents.voice_states = True
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix="n!", intents=intents)


async def load_all_cogs(client: commands.Bot):
    for folder in ["client_event", "slash_commands", "prefix_commands"]:
        folder_path = f"cogs/{folder}"
        for filename in os.listdir(folder_path):
            if filename.endswith(".py") and filename != "__init__.py":
                cog_path = f"cogs.{folder}.{filename[:-3]}"
                try:
                    await client.load_extension(cog_path)
                    print(f"✅ Loaded cog: {cog_path}")
                except Exception as e:
                    print(f"❌ Failed to load cog {cog_path}: {e}")


async def main():
    async with client:
        load_dotenv()
        await load_all_cogs(client)
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
