import discord
from discord.ext import commands
from discord import app_commands
import random
import json
import os

DATA_FILE = "./data/economy.json"

class MiniGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        os.makedirs("./data", exist_ok=True)
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w") as f:
                json.dump({}, f)

    # ----- Helper -----
    def load_data(self):
        with open(DATA_FILE, "r") as f:
            return json.load(f)

    def save_data(self, data):
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def ensure_user(self, user_id):
        data = self.load_data()
        if str(user_id) not in data:
            data[str(user_id)] = {"coins": 500, "inventory": []}
            self.save_data(data)
        return data

    # ----- Tebak Angka -----
    @app_commands.command(name="tebakangka", description="Tebak angka antara 1-10 untuk dapat coin!")
    async def tebakangka(self, interaction: discord.Interaction):
        angka = random.randint(1, 10)
        await interaction.response.send_message(f"{interaction.user.mention}, tebak angka antara 1-10!", ephemeral=True)

        def check(m):
            return m.author == interaction.user and m.content.isdigit()

        try:
            guess = await self.bot.wait_for("message", check=check, timeout=15)
            guess_num = int(guess.content)
            data = self.ensure_user(interaction.user.id)
            if guess_num == angka:
                reward = random.randint(100, 300)
                data[str(interaction.user.id)]["coins"] += reward
                self.save_data(data)
                await interaction.followup.send(f"🎉 Benar! Kamu mendapatkan **{reward} coins**!")
            else:
                await interaction.followup.send(f"❌ Salah! Angkanya adalah {angka}.")
        except:
            await interaction.followup.send("⏰ Waktu habis!")

    # ----- Fishing -----
    @app_commands.command(name="fishing", description="Fishing untuk dapat coin atau item")
    async def fishing(self, interaction: discord.Interaction):
        data = self.ensure_user(interaction.user.id)
        outcomes = ["coin", "coin", "item"]  # lebih besar peluang coin
        result = random.choice(outcomes)
        if result == "coin":
            reward = random.randint(50, 200)
            data[str(interaction.user.id)]["coins"] += reward
            self.save_data(data)
            await interaction.response.send_message(f"🎣 Kamu berhasil fishing dan mendapatkan **{reward} coins**!")
        else:
            item_list = ["Golden Fish", "Magic Shell", "Silver Badge"]
            item = random.choice(item_list)
            data[str(interaction.user.id)]["inventory"].append(item)
            self.save_data(data)
            await interaction.response.send_message(f"🎣 Kamu mendapatkan item **{item}** dari fishing!")

    # ----- Lomba Panen -----
    @app_commands.command(name="panen", description="Ikut lomba panen untuk coin atau item")
    async def panen(self, interaction: discord.Interaction):
        data = self.ensure_user(interaction.user.id)
        chance = random.randint(1, 100)
        if chance <= 60:  # 60% dapat coin
            reward = random.randint(50, 250)
            data[str(interaction.user.id)]["coins"] += reward
            self.save_data(data)
            await interaction.response.send_message(f"🌾 Kamu berhasil panen dan mendapat **{reward} coins**!")
        else:
            items = ["Golden Wheat", "Rare Corn", "Silver Bag"]
            item = random.choice(items)
            data[str(interaction.user.id)]["inventory"].append(item)
            self.save_data(data)
            await interaction.response.send_message(f"🌾 Kamu mendapatkan item **{item}** dari panen!")

    # ----- Perang Desa (PvP) -----
    @app_commands.command(name="perangdesa", description="Bertarung dengan warga lain untuk hadiah coin")
    @app_commands.describe(target="User yang akan kamu tantang")
    async def perangdesa(self, interaction: discord.Interaction, target: discord.Member):
        if target.bot or target == interaction.user:
            await interaction.response.send_message("Tidak bisa menantang bot atau diri sendiri!", ephemeral=True)
            return

        user1_data = self.ensure_user(interaction.user.id)
        user2_data = self.ensure_user(target.id)

        outcome = random.choice([interaction.user, target])
        reward = random.randint(100, 300)
        data = self.load_data()

        if outcome == interaction.user:
            data[str(interaction.user.id)]["coins"] += reward
            await interaction.response.send_message(f"⚔️ {interaction.user.mention} menang melawan {target.mention} dan mendapatkan **{reward} coins**!")
        else:
            data[str(target.id)]["coins"] += reward
            await interaction.response.send_message(f"⚔️ {target.mention} menang melawan {interaction.user.mention} dan mendapatkan **{reward} coins**!")

        self.save_data(data)

async def setup(bot):
    await bot.add_cog(MiniGame(bot))
