import discord
from discord.ext import commands
from discord import app_commands

class Pengumuman(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="pengumuman",
        description="Buat pengumuman desa ke channel tertentu"
    )
    @app_commands.describe(
        channel="Pilih channel untuk pengumuman",
        pesan="Isi pengumuman"
    )
    async def pengumuman(self, interaction: discord.Interaction, channel: discord.TextChannel, pesan: str):
        embed = discord.Embed(
            title="📢 Pengumuman Desa",
            description=pesan,
            color=0xffd700
        )
        embed.set_footer(text="Dari Kepala Desa Pak Joko")
        
        # Kirim dengan mention @everyone
        await channel.send(content="@everyone", embed=embed)
        
        await interaction.response.send_message(
            f"Pengumuman berhasil dikirim ke {channel.mention} dan semua orang diberi notifikasi.",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Pengumuman(bot))