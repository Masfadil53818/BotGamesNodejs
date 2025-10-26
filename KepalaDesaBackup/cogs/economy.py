import discord
from discord.ext import commands
from discord import app_commands
import json
import os

DATA_FILE = "./data/economy.json"

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        os.makedirs("./data", exist_ok=True)
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w") as f:
                json.dump({}, f)

        # Shop default
        self.shop_items = {
            "VIP Role": {"type": "role", "price": 1000},
            "Golden Badge": {"type": "item", "price": 500},
            "Extra Misi": {"type": "item", "price": 300}
        }

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

    # ----- User Commands -----
    @app_commands.command(name="coin", description="Cek saldo koinmu")
    async def coin(self, interaction: discord.Interaction):
        data = self.ensure_user(interaction.user.id)
        coins = data[str(interaction.user.id)]["coins"]
        await interaction.response.send_message(f"{interaction.user.mention}, kamu punya **{coins} coins**.")

    @app_commands.command(name="inventory", description="Cek item yang kamu punya")
    async def inventory(self, interaction: discord.Interaction):
        data = self.ensure_user(interaction.user.id)
        inv = data[str(interaction.user.id)]["inventory"]
        await interaction.response.send_message(
            f"{interaction.user.mention}, inventory-mu: {', '.join(inv) if inv else 'kosong.'}"
        )

    @app_commands.command(name="shop", description="Lihat item yang bisa dibeli")
    async def shop(self, interaction: discord.Interaction):
        embed = discord.Embed(title="🛒 Shop Desa", color=0x00ff00)
        for idx, (item, info) in enumerate(self.shop_items.items(), start=1):
            qty_text = f" (Qty: {info['qty']})" if "qty" in info else ""
            embed.add_field(
                name=f"{idx}. {item}",
                value=f"Type: {info['type']}, Price: {info['price']} coins{qty_text}",
                inline=False
            )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="buy", description="Beli item di shop (bisa pakai angka atau nama)")
    @app_commands.describe(item="Nama item atau nomor item di shop")
    async def buy(self, interaction: discord.Interaction, item: str):
        # Bisa pakai angka
        try:
            index = int(item) - 1
            if index < 0 or index >= len(self.shop_items):
                await interaction.response.send_message(f"{interaction.user.mention}, item tidak valid!", ephemeral=True)
                return
            item = list(self.shop_items.keys())[index]
        except ValueError:
            item = item.strip()

        if item not in self.shop_items:
            await interaction.response.send_message(f"{interaction.user.mention}, item tidak ditemukan!", ephemeral=True)
            return

        data = self.ensure_user(interaction.user.id)
        user_data = data[str(interaction.user.id)]
        info = self.shop_items[item]
        price = info["price"]

        if "qty" in info and info["qty"] <= 0:
            await interaction.response.send_message(f"{interaction.user.mention}, item **{item}** sudah habis!", ephemeral=True)
            return

        if user_data["coins"] < price:
            await interaction.response.send_message(f"{interaction.user.mention}, koinmu tidak cukup!", ephemeral=True)
            return

        # Potong koin & tambah item ke inventory
        user_data["coins"] -= price
        user_data["inventory"].append(item)
        self.save_data(data)

        # Assign role jika type role
        if info["type"] == "role":
            role = discord.utils.get(interaction.guild.roles, name=item)
            if not role:
                # Buat role baru jika belum ada
                role = await interaction.guild.create_role(name=item)
            await interaction.user.add_roles(role)

        if "qty" in info:
            self.shop_items[item]["qty"] -= 1

        await interaction.response.send_message(f"{interaction.user.mention}, kamu berhasil membeli **{item}**!")

    @app_commands.command(name="use", description="Gunakan item dari inventory")
    @app_commands.describe(item="Nama item yang ingin digunakan")
    async def use(self, interaction: discord.Interaction, item: str):
        data = self.ensure_user(interaction.user.id)
        inv = data[str(interaction.user.id)]["inventory"]

        if item not in inv:
            await interaction.response.send_message(f"{interaction.user.mention}, kamu tidak punya item **{item}**!", ephemeral=True)
            return

        inv.remove(item)
        self.save_data(data)
        await interaction.response.send_message(f"{interaction.user.mention} menggunakan item **{item}**!")

    @app_commands.command(name="gift", description="Berikan item/koin ke user lain")
    @app_commands.describe(user="User penerima", item="Nama item atau coins", amount="Jumlah koin jika gift koin")
    async def gift(self, interaction: discord.Interaction, user: discord.Member, item: str, amount: int = None):
        data = self.ensure_user(interaction.user.id)
        inv = data[str(interaction.user.id)]["inventory"]

        # Gift koin
        if item.lower() == "coins":
            if amount is None or amount <= 0:
                await interaction.response.send_message(f"{interaction.user.mention}, masukkan jumlah coins yang valid!", ephemeral=True)
                return
            if data[str(interaction.user.id)]["coins"] < amount:
                await interaction.response.send_message(f"{interaction.user.mention}, koinmu tidak cukup!", ephemeral=True)
                return

            data[str(interaction.user.id)]["coins"] -= amount
            data = self.ensure_user(user.id)
            data[str(user.id)]["coins"] += amount
            self.save_data(data)
            await interaction.response.send_message(f"{interaction.user.mention} memberi **{amount} coins** ke {user.mention}!")
            return

        # Gift item
        if item not in inv:
            await interaction.response.send_message(f"{interaction.user.mention}, kamu tidak punya item **{item}**!", ephemeral=True)
            return

        inv.remove(item)
        data = self.ensure_user(user.id)
        data[str(user.id)]["inventory"].append(item)
        self.save_data(data)
        await interaction.response.send_message(f"{interaction.user.mention} memberi item **{item}** ke {user.mention}!")

    # ----- Admin Commands -----
    @app_commands.command(name="shopadd", description="Tambah item/role baru ke shop")
    @app_commands.describe(
        item="Nama item/role",
        type="role/item",
        price="Harga item",
        qty="Jumlah item (opsional)"
    )
    async def shopadd(self, interaction: discord.Interaction, item: str, type: str, price: int, qty: int = None):
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("Hanya admin yang bisa menambah shop!", ephemeral=True)

        type = type.lower()
        if type not in ["role", "item"]:
            return await interaction.response.send_message("Type harus 'role' atau 'item'!", ephemeral=True)

        # Jika role, pastikan role ada
        if type == "role":
            role = discord.utils.get(interaction.guild.roles, name=item)
            if not role:
                role = await interaction.guild.create_role(name=item)

        info = {"type": type, "price": price}
        if qty is not None:
            info["qty"] = qty
        self.shop_items[item] = info
        await interaction.response.send_message(f"Item **{item}** berhasil ditambahkan ke shop!")

    @app_commands.command(name="shopdelete", description="Hapus item/role dari shop")
    @app_commands.describe(item="Nama item yang akan dihapus")
    async def shopdelete(self, interaction: discord.Interaction, item: str):
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("Hanya admin yang bisa menghapus shop!", ephemeral=True)
        if item in self.shop_items:
            del self.shop_items[item]
            await interaction.response.send_message(f"Item **{item}** berhasil dihapus dari shop!")
        else:
            await interaction.response.send_message(f"Item **{item}** tidak ditemukan!", ephemeral=True)

    @app_commands.command(name="coinadd", description="Tambahkan koin ke user")
    @app_commands.describe(user="User yang diberikan koin", amount="Jumlah koin")
    async def coinadd(self, interaction: discord.Interaction, user: discord.Member, amount: int):
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("Hanya admin yang bisa menambah koin!", ephemeral=True)
        data = self.ensure_user(user.id)
        data[str(user.id)]["coins"] += amount
        self.save_data(data)
        await interaction.response.send_message(f"{amount} coins berhasil ditambahkan ke {user.mention}!")

    @app_commands.command(name="coinset", description="Set jumlah koin user")
    @app_commands.describe(user="User yang di-set", amount="Jumlah koin baru")
    async def coinset(self, interaction: discord.Interaction, user: discord.Member, amount: int):
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("Hanya admin yang bisa set koin!", ephemeral=True)
        data = self.ensure_user(user.id)
        data[str(user.id)]["coins"] = amount
        self.save_data(data)
        await interaction.response.send_message(f"Koin {user.mention} di-set menjadi {amount} coins!")

    @app_commands.command(name="coinremove", description="Kurangi koin user")
    @app_commands.describe(user="User yang dikurangi koin", amount="Jumlah koin")
    async def coinremove(self, interaction: discord.Interaction, user: discord.Member, amount: int):
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("Hanya admin yang bisa mengurangi koin!", ephemeral=True)
        data = self.ensure_user(user.id)
        data[str(user.id)]["coins"] = max(0, data[str(user.id)]["coins"] - amount)
        self.save_data(data)
        await interaction.response.send_message(f"{amount} coins berhasil dikurangi dari {user.mention}!")

async def setup(bot):
    await bot.add_cog(Economy(bot))
