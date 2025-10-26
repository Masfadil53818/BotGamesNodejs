import discord
from discord.ext import commands, tasks
from discord import app_commands
import asyncio
import random
import json
import os

ECON_FILE = "./data/economy.json"
EVENT_CHANNEL_FILE = "./data/event_channel.json"

class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        os.makedirs("./data", exist_ok=True)

        # File economy
        if not os.path.exists(ECON_FILE):
            with open(ECON_FILE, "w") as f:
                json.dump({}, f)
        
        # File event channel
        if not os.path.exists(EVENT_CHANNEL_FILE):
            with open(EVENT_CHANNEL_FILE, "w") as f:
                json.dump({}, f)

        self.event_loop.start()  # Mulai loop event otomatis

    # ----- Helper -----
    def load_data(self):
        with open(ECON_FILE, "r") as f:
            return json.load(f)

    def save_data(self, data):
        with open(ECON_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def ensure_user(self, user_id):
        data = self.load_data()
        if str(user_id) not in data:
            data[str(user_id)] = {"coins": 500, "inventory": []}
            self.save_data(data)
        return data

    def load_event_channel(self, guild_id):
        with open(EVENT_CHANNEL_FILE, "r") as f:
            channels = json.load(f)
        return channels.get(str(guild_id))

    def save_event_channel(self, guild_id, channel_id):
        with open(EVENT_CHANNEL_FILE, "r") as f:
            channels = json.load(f)
        channels[str(guild_id)] = channel_id
        with open(EVENT_CHANNEL_FILE, "w") as f:
            json.dump(channels, f, indent=4)

    # ----- Event Loop -----
    @tasks.loop(hours=1)
    async def event_loop(self):
        for guild in self.bot.guilds:
            channel_id = self.load_event_channel(guild.id)
            if channel_id:
                channel = guild.get_channel(channel_id)
                if not channel or not channel.permissions_for(guild.me).send_messages:
                    continue
            else:
                # Default random channel jika belum diset
                channel = random.choice([c for c in guild.text_channels if c.permissions_for(guild.me).send_messages])
            
            event_type = random.choice(["coin", "item", "role"])
            data = self.load_data()

            if event_type == "coin":
                if guild.members:
                    user = random.choice([m for m in guild.members if not m.bot])
                    amount = random.randint(50, 300)
                    self.ensure_user(user.id)
                    data[str(user.id)]["coins"] += amount
                    self.save_data(data)
                    await channel.send(f"🎉 Event! {user.mention} mendapatkan **{amount} coins** dari Kepala Desa!")

            elif event_type == "item":
                item_list = ["Golden Badge", "Magic Sword", "Extra Misi"]
                if guild.members:
                    user = random.choice([m for m in guild.members if not m.bot])
                    item = random.choice(item_list)
                    self.ensure_user(user.id)
                    data[str(user.id)]["inventory"].append(item)
                    self.save_data(data)
                    await channel.send(f"🎁 Event! {user.mention} mendapatkan **{item}** dari Kepala Desa!")

            elif event_type == "role":
                role_name = "Pahlawan Desa"
                role = discord.utils.get(guild.roles, name=role_name)
                if not role:
                    role = await guild.create_role(name=role_name, color=discord.Color.gold())
                if guild.members:
                    user = random.choice([m for m in guild.members if not m.bot])
                    await user.add_roles(role)
                    await channel.send(f"🏅 Event! {user.mention} mendapatkan role **{role_name}** dari Kepala Desa!")

    @event_loop.before_loop
    async def before_event(self):
        await self.bot.wait_until_ready()

    # ----- Manual Trigger -----
    @commands.command(name="runevent")
    @commands.has_permissions(administrator=True)
    async def run_event(self, ctx):
        """Admin bisa trigger event manual"""
        await ctx.send("Memicu event manual...")
        await self.event_loop()

    # ----- /channelevent -----
    @app_commands.command(name="channelevent", description="Set channel untuk event otomatis")
    @app_commands.describe(channel="Pilih channel untuk event")
    async def channelevent(self, interaction: discord.Interaction, channel: discord.TextChannel):
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("❌ Hanya admin yang bisa menggunakan command ini.", ephemeral=True)
        
        self.save_event_channel(interaction.guild.id, channel.id)
        await interaction.response.send_message(f"✅ Channel event telah diset ke {channel.mention}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Event(bot))