import discord
from discord.ext import commands
from discord import app_commands
import datetime

# Importing your custom utilities
from utils.database import get_connection
from utils.formatters import format_timedelta, calculate_hours, get_current_iso

class Timekeeping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clock_in", description="Start your work shift")
    async def clock_in(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        now_iso = get_current_iso()
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if the user is already in the active_shifts table
        cursor.execute("SELECT user_id FROM active_shifts WHERE user_id = ?", (user_id,))
        if cursor.fetchone():
            await interaction.response.send_message("❌ You are already clocked in!", ephemeral=True)
        else:
            # Save the shift to the database
            cursor.execute(
                "INSERT INTO active_shifts (user_id, start_time, status) VALUES (?, ?, ?)", 
                (user_id, now_iso, 'working')
            )
            conn.commit()
            
            # Use formatter for a clean response
            readable_time = datetime.datetime.fromisoformat(now_iso).strftime('%H:%M')
            await interaction.response.send_message(f"✅ Clocked in at {readable_time}", ephemeral=True)
        
        conn.close()

    @app_commands.command(name="clock_out", description="End your shift and save to history")
    async def clock_out(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        now_iso = get_current_iso()
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Look for the user's active shift
        cursor.execute("SELECT start_time, total_break_seconds FROM active_shifts WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        
        if not row:
            await interaction.response.send_message("❌ You aren't currently clocked in.", ephemeral=True)
        else:
            start_iso = row[0]
            break_seconds = row[1]
            
            # Calculate total decimal hours for payroll
            hours_worked = calculate_hours(start_iso, now_iso)
            
            # Adjust hours for any breaks taken (if you've implemented the meal logic)
            actual_hours = max(0, hours_worked - (break_seconds / 3600))
            
            # Create a pretty string for the user (e.g., "7h 30m")
            readable_duration = format_timedelta(actual_hours * 3600)

            # 1. Save to permanent history table
            cursor.execute(
                "INSERT INTO shift_history (user_id, start_time, end_time, total_hours) VALUES (?, ?, ?, ?)",
                (user_id, start_iso, now_iso, round(actual_hours, 2))
            )
            
            # 2. Remove from active tracking
            cursor.execute("DELETE FROM active_shifts WHERE user_id = ?", (user_id,))
            
            conn.commit()
            
            await interaction.response.send_message(
                f"🏁 **Shift Ended**\n"
                f"Total Duration: **{readable_duration}**\n"
                f"Decimal Hours: `{round(actual_hours, 2)}`", 
                ephemeral=True
            )
            
        conn.close()

async def setup(bot):
    await bot.add_cog(Timekeeping(bot))
