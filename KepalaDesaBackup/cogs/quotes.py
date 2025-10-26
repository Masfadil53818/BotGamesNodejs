import discord
from discord.ext import commands
from discord import app_commands
import random

class Quotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.quotes = [
            "Kerja keras adalah kunci kemajuan desa!",
            "Gotong royong membuat desa kuat!",
            "Hargai tetangga, jaga desa.",
            "Bersama kita bisa membangun Desa Jongki!"
        ]

    @app_commands.command(name="quotesdesa", description="Dapatkan quotes bijak dari kepala desa")
    async def quotesdesa(self, interaction: discord.Interaction):
        await interaction.response.send_message(random.choice(self.quotes))

async def setup(bot):
    await bot.add_cog(Quotes(bot))
