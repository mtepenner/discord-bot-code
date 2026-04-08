import discord
from discord.ext import commands
from discord import app_commands
import datetime
import asyncio

# Importing your custom utilities
from utils.database import get_connection
from utils.formatters import format_timedelta, calculate_hours, get_current_iso
from utils.jira_client import add_worklog_to_issue

class Timekeeping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clock_in", description="Start your work shift")
    @app_commands.describe(issue_key="Optional: The Jira issue key you are working on (e.g., PROJ-123)")
    async def clock_in(self, interaction: discord.Interaction, issue_key: str = None):
        user_id = interaction.user.id
        now_iso = get_current_iso()
        
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT user_id FROM active_shifts WHERE user_id = ?", (user_id,))
        if cursor.fetchone():
            await interaction.response.send_message("❌ You are already clocked in!", ephemeral=True)
        else:
            # Save the shift and the optional Jira issue key to the database
            cursor.execute(
                "INSERT INTO active_shifts (user_id, start_time, status, issue_key) VALUES (?, ?, ?, ?)", 
                (user_id, now_iso, 'working', issue_key)
            )
            conn.commit()
            
            readable_time = datetime.datetime.fromisoformat(now_iso).strftime('%H:%M')
            msg = f"✅ Clocked in at {readable_time}"
            if issue_key:
                msg += f"\nTracking time against Jira Issue: **{issue_key.upper()}**"
                
            await interaction.response.send_message(msg, ephemeral=True)
        
        conn.close()

    @app_commands.command(name="clock_out", description="End your shift and save to history")
    async def clock_out(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True) # Defer response in case Jira API is slow
        
        user_id = interaction.user.id
        now_iso = get_current_iso()
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Look for the user's active shift
        cursor.execute("SELECT start_time, total_break_seconds, issue_key FROM active_shifts WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        
        if not row:
            await interaction.followup.send("❌ You aren't currently clocked in.", ephemeral=True)
            conn.close()
            return

        start_iso = row[0]
        break_seconds = row[1]
        issue_key = row[2]
        
        hours_worked = calculate_hours(start_iso, now_iso)
        actual_hours = max(0, hours_worked - (break_seconds / 3600))
        actual_seconds = actual_hours * 3600
        readable_duration = format_timedelta(actual_seconds)

        # 1. Save to permanent history table
        cursor.execute(
            "INSERT INTO shift_history (user_id, start_time, end_time, total_hours, issue_key) VALUES (?, ?, ?, ?, ?)",
            (user_id, start_iso, now_iso, round(actual_hours, 2), issue_key)
        )
        
        # 2. Remove from active tracking
        cursor.execute("DELETE FROM active_shifts WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        
        # 3. Log to Jira if an issue key was provided
        jira_message = ""
        if issue_key:
            comment = f"Time logged automatically via Discord by {interaction.user.display_name}"
            # Run the synchronous Jira network call in a separate thread so it doesn't block the Discord bot
            success = await asyncio.to_thread(add_worklog_to_issue, issue_key, actual_seconds, comment)
            
            if success:
                jira_message = f"\n✅ Successfully logged {readable_duration} to Jira issue **{issue_key.upper()}**."
            else:
                jira_message = f"\n⚠️ Failed to push time to Jira issue **{issue_key.upper()}**. Double check the issue key or bot permissions."

        await interaction.followup.send(
            f"🏁 **Shift Ended**\n"
            f"Total Duration: **{readable_duration}**\n"
            f"Decimal Hours: `{round(actual_hours, 2)}`"
            f"{jira_message}", 
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Timekeeping(bot))
