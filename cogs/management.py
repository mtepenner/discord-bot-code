import discord
from discord.ext import commands
from discord import app_commands

class Management(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="who_is_working", description="See a list of all currently clocked-in employees")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def who_is_working(self, interaction: discord.Interaction):
        # We reach into the Timekeeping cog to see its 'active_shifts' dictionary
        time_cog = self.bot.get_cog('Timekeeping')
        
        if not time_cog or not time_cog.active_shifts:
            await interaction.response.send_message("No one is currently clocked in.", ephemeral=True)
            return

        embed = discord.Embed(title="Current Staff On-Shift", color=discord.Color.blue())
        
        for user_id, data in time_cog.active_shifts.items():
            member = interaction.guild.get_member(user_id)
            name = member.display_name if member else f"Unknown({user_id})"
            start_str = data['start'].strftime("%H:%M")
            status = "Working" if data.get('status') != 'on_break' else "On Break 🍱"
            
            embed.add_field(name=name, value=f"Started: {start_str}\nStatus: {status}", inline=False)

        await interaction.response.send_message(embed=embed)

    @who_is_working.error
    async def mgmt_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("❌ You don't have permission to view staff logs.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Management(bot))
