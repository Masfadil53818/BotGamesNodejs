import discord
from discord import app_commands
from discord.ext import commands
import asyncio

class SetupKampung(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ---------- DATA ROLE ----------
    roles_data = [
        {"name": "👑 Kepala Desa", "color": discord.Color.gold(), "permissions": discord.Permissions(administrator=True)},
        {"name": "🧍‍♂️ Pak RT", "color": discord.Color.orange(), "permissions": discord.Permissions(manage_messages=True, kick_members=True, mute_members=True)},
        {"name": "🧑‍🌾 Warga Tetap", "color": discord.Color.green()},
        {"name": "🧒 Warga Baru", "color": discord.Color.light_grey()},
        {"name": "🐓 Tukang Gosip", "color": discord.Color.purple()},
        {"name": "🧙 Dukun Kampung", "color": discord.Color.blue()},
    ]

    # ---------- STRUKTUR CHANNEL ----------
    channel_structure = {
        "🏡 Gerbang Kampung": [
            "📜│peraturan", "📢│pengumuman", "👋│salam-datang",
            "🧾│panduan-warga", "💼│pembagian-role", "🗺️│peta-kampung"
        ],
        "💬 Balai Desa": [
            "💭│ngobrol-bebas", "🎭│meme-desa", "🖼️│galeri-warga",
            "📰│info-harian", "🎶│musik-warga", "🎮│gaming-bersama", "📚│cerita-desa"
        ],
        "🧑‍🌾 Aktivitas & Ekonomi Kampung": [
            "🪵│pasar-desa", "💰│dompet-warga", "🧑‍🔧│kerja-sambilan",
            "🎣│tempat-pancing", "🧵│crafting", "🏆│event-lomba"
        ],
        "🧠 Pusat Ide & Pendidikan": [
            "💡│ide-warga", "📖│belajar-bersama", "🧩│workshop"
        ],
        "🚨 Keamanan & Pemerintahan": [
            "🚓│lapor-satpam", "🧱│tahanan-desa", "📋│log-server",
            "🔧│perintah-bot", "📡│pengumuman-admin"
        ],
        "🗣️ Warung Nongkrong (Voice)": [
            "☕│warung-kopi", "🔊│obrolan-malam", "🎮│main-bareng", "🎤│karaoke-desa", "💤│afk-tempat-tidur"
        ],
        "💼 Kantor Kepala Desa (Staff Only)": [
            "🧠│diskusi-staff", "🗃️│arsip-laporan", "🛠│command-log",
            "🧾│jadwal-event", "🧩│testing-bot", "📢│staff-info"
        ]
    }

    # ---------- SLASH COMMAND /setup ----------
    @app_commands.command(name="setup", description="Bangun struktur server Kampung/Desa lengkap dengan role dan channel.")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup(self, interaction: discord.Interaction):
        guild = interaction.guild

        embed = discord.Embed(
            title="🏗️ Setup Kampung Dimulai",
            description="Bot sedang membangun kampung digital kamu... 🏡",
            color=discord.Color.green()
        )
        embed.add_field(name="Status", value="Membuat role...", inline=False)
        embed.set_footer(text="Proses setup oleh " + interaction.user.name)
        msg = await interaction.response.send_message(embed=embed, ephemeral=True)
        msg = await interaction.original_response()

        # === Buat ROLE ===
        created_roles = {}
        for role_data in self.roles_data:
            existing = discord.utils.get(guild.roles, name=role_data["name"])
            if not existing:
                role = await guild.create_role(**role_data)
            else:
                role = existing
            created_roles[role_data["name"]] = role
            embed.set_field_at(0, name="Status", value=f"✅ Role dibuat: {role.name}", inline=False)
            await msg.edit(embed=embed)
            await asyncio.sleep(0.5)

        # === Buat KATEGORI & CHANNEL ===
        embed.set_field_at(0, name="Status", value="🏗️ Membuat kategori & channel...", inline=False)
        await msg.edit(embed=embed)
        await asyncio.sleep(0.5)

        for category_name, channels in self.channel_structure.items():
            category = discord.utils.get(guild.categories, name=category_name)
            if not category:
                category = await guild.create_category(category_name)

            for ch_name in channels:
                if "│" in ch_name:
                    if not discord.utils.get(guild.text_channels, name=ch_name):
                        await guild.create_text_channel(ch_name, category=category)
                else:
                    if not discord.utils.get(guild.voice_channels, name=ch_name):
                        await guild.create_voice_channel(ch_name, category=category)

            embed.set_field_at(0, name="Status", value=f"✅ Kategori selesai: {category_name}", inline=False)
            await msg.edit(embed=embed)
            await asyncio.sleep(0.5)

        # === Atur PERMISSION ===
        embed.set_field_at(0, name="Status", value="🔒 Mengatur izin channel...", inline=False)
        await msg.edit(embed=embed)
        await asyncio.sleep(0.5)

        staff_role = created_roles.get("🧍‍♂️ Pak RT")
        warga_role = created_roles.get("🧑‍🌾 Warga Tetap")

        staff_category = discord.utils.get(guild.categories, name="💼 Kantor Kepala Desa (Staff Only)")
        if staff_category:
            await staff_category.set_permissions(guild.default_role, view_channel=False)
            if staff_role:
                await staff_category.set_permissions(staff_role, view_channel=True)

        balai = discord.utils.get(guild.categories, name="💬 Balai Desa")
        if balai and warga_role:
            await balai.set_permissions(warga_role, view_channel=True, send_messages=True)

        embed.set_field_at(0, name="Status", value="✅ Semua izin & struktur selesai!", inline=False)
        embed.title = "🏡 Setup Kampung Selesai!"
        embed.color = discord.Color.gold()
        embed.description = "Semua kategori, channel, dan role telah berhasil dibuat!\n\nSelamat datang di **Kampung Digital** 🎉"
        await msg.edit(embed=embed)

    # Error handler untuk izin admin
    @setup.error
    async def setup_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ Kamu butuh izin **Administrator** untuk menjalankan `/setup`.", ephemeral=True)
        else:
            await interaction.response.send_message(f"⚠️ Terjadi error: `{error}`", ephemeral=True)

# ---------- Fungsi untuk load Cog ----------
async def setup(bot: commands.Bot):
    await bot.add_cog(SetupKampung(bot))
