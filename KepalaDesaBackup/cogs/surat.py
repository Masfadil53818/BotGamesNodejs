import discord
from discord.ext import commands
from discord import app_commands

class Surat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="surat", 
        description="Buat surat perintah untuk warga ke channel tertentu"
    )
    @app_commands.describe(
        channel="Pilih channel untuk surat",
        user="User yang ditugaskan",
        tugas="Tugas yang diberikan"
    )
    async def surat(self, interaction: discord.Interaction, channel: discord.TextChannel, user: discord.Member, tugas: str):
        embed = discord.Embed(
            title="📜 Surat Perintah",
            description=f"{user.mention} ditugaskan: {tugas}",
            color=0xffa500
        )
        embed.set_footer(text="Dari Kepala Desa Pak Joko")
        await channel.send(embed=embed)
        await interaction.response.send_message(f"Surat perintah berhasil dikirim ke {channel.mention}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Surat(bot))
