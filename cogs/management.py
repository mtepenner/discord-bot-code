import discord
from discord.ext import commands
from discord import app_commands
from utils.database import get_connection
from utils.formatters import format_timestamp

class Management(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="who_is_working", description="See a list of all currently clocked-in employees")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def who_is_working(self, interaction: discord.Interaction):
        """Queries the database for everyone currently marked as 'working' or 'on_break'."""
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get all active sessions from the database
        cursor.execute("SELECT user_id, start_time, status FROM active_shifts")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            await interaction.response.send_message("📡 No one is currently clocked in.", ephemeral=True)
            return

        embed = discord.Embed(
            title="🏢 Current Staff On-Shift", 
            color=discord.Color.blue(),
            description=f"Total Employees Active: **{len(rows)}**"
        )
        
        for user_id, start_time, status in rows:
            # Try to get the member object to show their server nickname
            member = interaction.guild.get_member(user_id)
            name = member.display_name if member else f"User ID: {user_id}"
            
            # Format the ISO timestamp into a readable 12-hour time
            friendly_start = format_timestamp(start_time)
            
            # Determine status emoji
            status_text = "Working ✅" if status == 'working' else "On Break 🍱"
            
            embed.add_field(
                name=name, 
                value=f"**Started:** {friendly_start}\n**Status:** {status_text}", 
                inline=False
            )

        await interaction.response.send_message(embed=embed)

    @who_is_working.error
    async def mgmt_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        """Error handler specifically for the who_is_working command."""
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("❌ **Access Denied:** You need 'Manage Server' permissions to use this.", ephemeral=True)
        else:
            # Logs other errors to the console so you can debug
            print(f"Management Error: {error}")

async def setup(bot):
    await bot.add_cog(Management(bot))
