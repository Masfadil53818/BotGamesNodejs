import discord
from discord import app_commands
from discord.ext import commands

# Dropdown menu role
class RoleSelect(discord.ui.Select):
    def __init__(self, roles: dict):
        options = [
            discord.SelectOption(label=name, description=f"Ambil atau hapus role {name}", emoji=emoji)
            for name, emoji in roles.items()
        ]
        super().__init__(placeholder="Pilih role kamu di Kampung Jongki 🏡", options=options, min_values=1, max_values=1)
        self.roles = roles

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        role_name = self.values[0]
        role = discord.utils.get(guild.roles, name=role_name)

        # Pastikan role-nya ada
        if not role:
            await interaction.response.send_message(f"⚙️ Membuat role **{role_name}** ...", ephemeral=True)
            role = await guild.create_role(name=role_name, reason="Auto-create oleh /pembagianrole")
            await interaction.followup.send(f"✅ Role **{role_name}** berhasil dibuat!", ephemeral=True)

        # Toggle role on/off
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.followup.send(f"🗑️ Role **{role_name}** dihapus dari kamu.", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.followup.send(f"✅ Kamu telah mendapatkan role **{role_name}**!", ephemeral=True)


# View untuk dropdown
class RoleView(discord.ui.View):
    def __init__(self, roles: dict):
        super().__init__(timeout=None)
        self.add_item(RoleSelect(roles))


class PembagianRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="pembagianrole", description="Tampilkan menu pembagian role warga Kampung Jongki 🎭")
    @app_commands.checks.has_permissions(administrator=True)
    async def pembagianrole(self, interaction: discord.Interaction):
        roles = {
            "Warga Tetap": "🧑‍🌾",
            "Warga Baru": "🧒",
            "Tukang Gosip": "🐓",
            "Gamer": "🎮",
            "Kreator": "🎨",
            "Fotografer": "📸",
        }

        embed = discord.Embed(
            title="🎭 Pembagian Role Kampung Jongki",
            description=(
                "Silakan pilih role yang cocok dengan dirimu!\n\n"
                "🧑‍🌾 **Warga Tetap** — Member aktif dan berpengalaman.\n"
                "🧒 **Warga Baru** — Pendatang baru di kampung.\n"
                "🐓 **Tukang Gosip** — Aktif di chat & suka ngobrol.\n"
                "🎮 **Gamer** — Pecinta game & player aktif.\n"
                "🎨 **Kreator** — Pembuat konten, desain, atau karya seni.\n"
                "📸 **Fotografer** — Suka share gambar & screenshot keren."
            ),
            color=0x00ff99
        )
        embed.set_footer(text="Kampung Jongki • Hidup Rukun & Ramai 🌾")

        # Buat role yang belum ada
        guild = interaction.guild
        created_roles = []
        for name in roles.keys():
            role = discord.utils.get(guild.roles, name=name)
            if not role:
                new_role = await guild.create_role(name=name, reason="Auto-create oleh /pembagianrole")
                created_roles.append(new_role.name)

        if created_roles:
            msg = "🛠️ Role baru dibuat otomatis: " + ", ".join(created_roles)
        else:
            msg = "✅ Semua role sudah tersedia."

        view = RoleView(roles)
        await interaction.response.send_message(embed=embed, view=view)
        await interaction.followup.send(msg, ephemeral=True)


async def setup(bot):
    await bot.add_cog(PembagianRole(bot))
