import discord
from discord.ext import commands
from discord import app_commands

class Payroll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="estimate_pay", description="Calculate pay for a specific number of hours")
    async def estimate_pay(self, interaction: discord.Interaction, hours: float, rate: float):
        total = hours * rate
        
        embed = discord.Embed(title="Payroll Estimate", color=discord.Color.green())
        embed.add_field(name="Hours Worked", value=f"{hours}", inline=True)
        embed.add_field(name="Hourly Rate", value=f"${rate:.2f}", inline=True)
        embed.add_field(name="Total Gross Pay", value=f"**${total:.2f}**", inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # Future Function Idea: /export_csv
    # This would query your Database and send a .csv file to the manager.

async def setup(bot):
    await bot.add_cog(Payroll(bot))
