import discord
from discord.ext import commands
from discord import app_commands

class Pemerintahan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 🏗️ Command untuk inisialisasi role pemerintahan
    @app_commands.command(name="inisialisasi_pemerintahan", description="Buat sistem pemerintahan & keamanan kampung")
    @app_commands.checks.has_permissions(administrator=True)
    async def inisialisasi_pemerintahan(self, interaction: discord.Interaction):
        guild = interaction.guild
        roles = [
            ("Kepala Desa", discord.Color.gold()),
            ("Sekdes", discord.Color.blue()),
            ("Satpam", discord.Color.dark_teal()),
            ("Warga Tetap", discord.Color.green()),
            ("Warga Baru", discord.Color.light_gray()),
        ]

        created = []
        for name, color in roles:
            role = discord.utils.get(guild.roles, name=name)
            if not role:
                await guild.create_role(name=name, color=color, reason="Sistem Pemerintahan Kampung Jongki")
                created.append(name)

        # Buat kategori dan channel sistem
        kategori = discord.utils.get(guild.categories, name="🏛️ Pemerintahan Kampung")
        if not kategori:
            kategori = await guild.create_category("🏛️ Pemerintahan Kampung")

        channels = {
            "🧾│pengumuman-desa": "Kanal resmi pengumuman dari Kepala Desa",
            "💬│rapat-desa": "Tempat diskusi antar pejabat kampung",
            "📢│laporan-warga": "Tempat warga melapor kejadian di kampung",
            "🚨│pos-satpam": "Pusat keamanan kampung (khusus Satpam)",
        }

        for name, topic in channels.items():
            if not discord.utils.get(guild.text_channels, name=name):
                await guild.create_text_channel(name, category=kategori, topic=topic)

        created_text = ", ".join(created) if created else "Tidak ada role baru"
        await interaction.response.send_message(
            f"✅ Sistem pemerintahan & keamanan telah diinisialisasi!\n**Role dibuat:** {created_text}",
            ephemeral=True
        )

    # 📣 Command: Laporan warga
    @app_commands.command(name="lapor", description="Laporkan masalah ke pos Satpam atau Kepala Desa")
    async def lapor(self, interaction: discord.Interaction, laporan: str):
        log_channel = discord.utils.get(interaction.guild.text_channels, name="📢│laporan-warga")
        if not log_channel:
            await interaction.response.send_message("⚠️ Channel laporan belum ada!", ephemeral=True)
            return

        embed = discord.Embed(
            title="🚨 Laporan Warga Masuk!",
            description=f"**Pelapor:** {interaction.user.mention}\n**Isi Laporan:** {laporan}",
            color=discord.Color.red()
        )
        await log_channel.send(embed=embed)
        await interaction.response.send_message("✅ Laporan kamu sudah dikirim ke pemerintah kampung.", ephemeral=True)

    # 🪪 Command: Izin / Cuti
    @app_commands.command(name="izin", description="Minta izin tidak aktif sementara")
    async def izin(self, interaction: discord.Interaction, alasan: str):
        log_channel = discord.utils.get(interaction.guild.text_channels, name="💬│rapat-desa")
        if not log_channel:
            await interaction.response.send_message("⚠️ Channel rapat belum ada!", ephemeral=True)
            return

        embed = discord.Embed(
            title="🪪 Permintaan Izin Warga",
            description=f"**Dari:** {interaction.user.mention}\n**Alasan:** {alasan}",
            color=discord.Color.orange()
        )
        await log_channel.send(embed=embed)
        await interaction.response.send_message("📝 Permintaan izin kamu telah dikirim!", ephemeral=True)

    # ⚖️ Command: Sidang (hanya Kepala Desa)
    @app_commands.command(name="sidang", description="Sidang pelanggaran warga (hanya untuk Kepala Desa)")
    async def sidang(self, interaction: discord.Interaction, warga: discord.Member, keputusan: str):
        if not any(role.name == "Kepala Desa" for role in interaction.user.roles):
            await interaction.response.send_message("❌ Hanya Kepala Desa yang bisa mengadakan sidang!", ephemeral=True)
            return

        embed = discord.Embed(
            title="⚖️ Hasil Sidang Kampung",
            description=f"**Tersangka:** {warga.mention}\n**Keputusan:** {keputusan}",
            color=discord.Color.purple()
        )

        log_channel = discord.utils.get(interaction.guild.text_channels, name="💬│rapat-desa")
        if log_channel:
            await log_channel.send(embed=embed)

        await interaction.response.send_message("✅ Sidang telah diumumkan ke rapat desa.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Pemerintahan(bot))
