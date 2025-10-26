import discord
from discord.ext import commands
from discord import app_commands
import random
import json
import os

DATA_FILE = "./data/warga.json"

class Warga(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w") as f:
                json.dump({}, f)

    @app_commands.command(name="vote", description="Vote warga")
    @app_commands.describe(pilihan="Masukkan pilihanmu")
    async def vote(self, interaction: discord.Interaction, pilihan: str):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        data[str(interaction.user.id)] = pilihan
        with open(DATA_FILE, "w") as f:
            json.dump(data, f)
        await interaction.response.send_message(f"{interaction.user.mention} memilih: {pilihan}")

    @app_commands.command(name="misiharian", description="Dapatkan misi harian dari kepala desa")
    async def misiharian(self, interaction: discord.Interaction):
        misi = [
            "Bersihkan lingkungan desa",
            "Bantu tetangga membawa air",
            "Tanam 5 pohon di desa",
            "Cek keamanan desa malam ini"
        ]
        await interaction.response.send_message(f"{interaction.user.mention}, misi hari ini: {random.choice(misi)}")

async def setup(bot):
    await bot.add_cog(Warga(bot))
