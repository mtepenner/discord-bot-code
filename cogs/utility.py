import discord
from discord.ext import commands
from discord import app_commands
import time

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Check the bot's connection speed")
    async def ping(self, interaction: discord.Interaction):
        """Returns the latency between the bot and Discord's servers."""
        # bot.latency is returned in seconds, so we multiply by 1000 for milliseconds
        latency = round(self.bot.latency * 1000)
        
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latency: **{latency}ms**",
            color=discord.Color.green()
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="server_info", description="Get quick stats about this Discord server")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def server_info(self, interaction: discord.Interaction):
        """A helpful tool for managers to see server stats."""
        guild = interaction.guild
        embed = discord.Embed(title=f"Stats for {guild.name}", color=discord.Color.gold())
        embed.add_field(name="Total Members", value=guild.member_count)
        embed.add_field(name="Created On", value=guild.created_at.strftime("%B %d, %Y"))
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))
