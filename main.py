import discord
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
from utils.database import init_db

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class MyBot(commands.Bot):
    def __init__(self):
        # Standard intents + members intent for management tracking
        intents = discord.Intents.default()
        intents.members = True  
        intents.message_content = True # Required if you use prefix commands
        
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        """Pre-launch setup: Database and Cogs"""
        
        # 1. Ensure the 'data' directory exists for SQLite
        if not os.path.exists('./data'):
            os.makedirs('./data')
            print("Created /data directory")

        # 2. Initialize the database tables
        init_db()
        print("Database initialized")

        # 3. Load all Cogs from the /cogs folder
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and not filename.startswith('__'):
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    print(f'✅ Loaded Cog: {filename}')
                except Exception as e:
                    print(f'❌ Failed to load Cog {filename}: {e}')
        
        # 4. Sync Slash Commands globally
        await self.tree.sync()
        print("Slash commands synced")

bot = MyBot()

@bot.event
async def on_ready():
    print(f'--- Bot Online ---')
    print(f'User: {bot.user}')
    print(f'ID: {bot.user.id}')
    print(f'Running in {len(bot.guilds)} servers')
    print('------------------')

async def main():
    async with bot:
        if not TOKEN:
            print("ERROR: DISCORD_TOKEN not found in environment variables.")
            return
        await bot.start(TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot shutting down...")
