import discord
from discord.ext import commands
from discord import app_commands
import io
import csv
from utils.database import get_connection

class Payroll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="my_hours", description="Check your total hours worked in the system")
    async def my_hours(self, interaction: discord.Interaction):
        """Allows an employee to see their own total historical hours."""
        user_id = interaction.user.id
        
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT SUM(total_hours) FROM shift_history WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        conn.close()

        total = result[0] if result[0] else 0
        
        await interaction.response.send_message(
            f"📊 You have a total of **{total:.2f}** hours logged in the system.", 
            ephemeral=True
        )

    @app_commands.command(name="export_payroll", description="Download all shift history as a CSV file")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def export_payroll(self, interaction: discord.Interaction):
        """Generates a CSV file of all shifts and sends it to the admin."""
        await interaction.response.defer(ephemeral=True) # Give the bot time to think
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, start_time, end_time, total_hours FROM shift_history")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            await interaction.followup.send("No shift history found to export.", ephemeral=True)
            return

        # Create an in-memory text file
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['User ID', 'Start Time', 'End Time', 'Total Hours']) # Header
        writer.writerows(rows)
        output.seek(0)

        # Convert to a Discord File object
        discord_file = discord.File(fp=io.BytesIO(output.getvalue().encode()), filename="payroll_report.csv")
        
        await interaction.followup.send("Here is the latest payroll export:", file=discord_file, ephemeral=True)

    @app_commands.command(name="estimate_pay", description="Quickly calculate pay based on hours and rate")
    async def estimate_pay(self, interaction: discord.Interaction, hours: float, rate: float):
        total = hours * rate
        
        embed = discord.Embed(title="Payroll Estimate", color=discord.Color.green())
        embed.add_field(name="Hours Worked", value=f"{hours}", inline=True)
        embed.add_field(name="Hourly Rate", value=f"${rate:.2f}", inline=True)
        embed.add_field(name="Total Gross Pay", value=f"**${total:.2f}**", inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Payroll(bot))
