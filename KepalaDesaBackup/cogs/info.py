import discord
from discord.ext import commands
from discord import app_commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.kepala_desa = {
            "Nama": "Pak Joko",
            "Umur": "52",
            "Desa": "Desa Jongki",
            "Jabatan": "Kepala Desa"
        }

    @app_commands.command(name="info", description="Tampilkan info kepala desa")
    async def info(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Profil Kepala Desa", color=0x00ff00)
        for key, value in self.kepala_desa.items():
            embed.add_field(name=key, value=value, inline=False)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Info(bot))
