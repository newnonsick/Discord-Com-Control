from discord.ext import commands


class ClearDM(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(name="cleardm")
    async def cleardm_command(self, ctx: commands.Context):
        bot_owner = await self.client.application_info()
        if ctx.author.id != bot_owner.owner.id or ctx.guild is not None:
            return

        await ctx.send("🧹 Clearing DMs...")

        async for message in ctx.channel.history(limit=None):
            if message.author == self.client.user:
                await message.delete()


async def setup(client: commands.Bot):
    await client.add_cog(ClearDM(client))
