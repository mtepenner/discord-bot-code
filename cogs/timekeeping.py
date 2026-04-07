import discord
from discord.ext import commands
from discord import app_commands
import datetime

class Timekeeping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Temporary storage (Replace with Database calls later)
        self.active_shifts = {} 

    @app_commands.command(name="clock_in", description="Start your work shift")
    async def clock_in(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        if user_id in self.active_shifts:
            await interaction.response.send_message("You're already on the clock!", ephemeral=True)
            return

        self.active_shifts[user_id] = {
            'start': datetime.datetime.now(),
            'breaks': []
        }
        await interaction.response.send_message(f"✅ Clocked in at {datetime.datetime.now().strftime('%H:%M')}", ephemeral=True)

    @app_commands.command(name="clock_out", description="End your shift and see total time")
    async def clock_out(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        if user_id not in self.active_shifts:
            await interaction.response.send_message("You aren't clocked in.", ephemeral=True)
            return

        start_time = self.active_shifts[user_id]['start']
        end_time = datetime.datetime.now()
        duration = end_time - start_time
        
        # Remove them from active shifts
        del self.active_shifts[user_id]

        await interaction.response.send_message(
            f"🏁 **Shift Ended**\nStart: {start_time.strftime('%H:%M')}\nEnd: {end_time.strftime('%H:%M')}\nTotal: {str(duration).split('.')[0]}",
            ephemeral=True
        )

# This function is required for main.py to load the cog
async def setup(bot):
    await bot.add_cog(Timekeeping(bot))
