import discord
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class MyBot(commands.Bot):
    def __init__(self):
        # We define the bot with a prefix (for back-end) and intents
        intents = discord.Intents.default()
        intents.members = True  # Allows bot to see who is in the server
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # This loop looks into the /cogs folder and loads every .py file
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
                print(f'Loaded Cog: {filename}')
        
        # Syncs slash commands with Discord
        await self.tree.sync()

bot = MyBot()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

async def main():
    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
