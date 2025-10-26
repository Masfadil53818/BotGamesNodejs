import discord
from discord import app_commands
from discord.ext import commands

class PetaKampung(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="petakampung", description="Lihat peta lengkap Kampung Jongki 🗺️")
    async def petakampung(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🗺️ Peta Kampung Jongki",
            description="Berikut denah dan struktur lengkap kampung kita! 🌾",
            color=0x2ecc71
        )

        embed.add_field(
            name="🏡 Gerbang Kampung",
            value=(
                "📜│peraturan — Aturan dan tata tertib.\n"
                "📢│pengumuman — Info resmi dari kepala desa.\n"
                "👋│salam-datang — Sambutan warga baru.\n"
                "🧾│panduan-warga — Panduan umum server.\n"
                "💼│pembagian-role — Pilih role kamu.\n"
                "🗺️│peta-kampung — Lihat struktur server (command ini)."
            ),
            inline=False
        )

        embed.add_field(
            name="💬 Balai Desa",
            value=(
                "💭│ngobrol-bebas — Obrolan umum warga.\n"
                "🎭│meme-desa — Tempat share meme lucu.\n"
                "🖼️│galeri-warga — Karya dan screenshot warga.\n"
                "🎮│gaming-bersama — Koordinasi main bareng.\n"
                "🎶│musik-warga — Share musik / playlist.\n"
                "📚│cerita-desa — Cerita, lore, dan roleplay."
            ),
            inline=False
        )

        embed.add_field(
            name="🧑‍🌾 Aktivitas & Ekonomi",
            value=(
                "🪵│pasar-desa — Jual beli item atau jasa.\n"
                "💰│dompet-warga — Saldo dan ekonomi bot.\n"
                "🧑‍🔧│kerja-sambilan — Misi dan tugas warga.\n"
                "🎣│tempat-pancing — Santai dan minigame.\n"
                "🏆│event-lomba — Event dan kompetisi kampung."
            ),
            inline=False
        )

        embed.add_field(
            name="🧠 Pusat Ide & Pendidikan",
            value=(
                "💡│ide-warga — Tempat bagi ide baru.\n"
                "📖│belajar-bersama — Diskusi & sharing ilmu.\n"
                "🧩│workshop — Event edukasi / latihan skill."
            ),
            inline=False
        )

        embed.add_field(
            name="🚨 Keamanan & Pemerintahan",
            value=(
                "🚓│lapor-satpam — Lapor pelanggaran.\n"
                "🧱│tahanan-desa — Tempat warga yang dimute.\n"
                "📋│log-server — Catatan aktivitas bot/staff.\n"
                "📡│pengumuman-admin — Info dari staff & admin."
            ),
            inline=False
        )

        embed.add_field(
            name="🗣️ Warung Nongkrong (Voice)",
            value=(
                "☕│warung-kopi — VC ngobrol santai.\n"
                "🔊│obrolan-malam — VC malam hari.\n"
                "🎮│main-bareng — VC gaming.\n"
                "🎤│karaoke-desa — VC karaoke.\n"
                "💤│afk-tempat-tidur — VC AFK."
            ),
            inline=False
        )

        embed.add_field(
            name="💼 Kantor Kepala Desa (Staff Only)",
            value=(
                "🧠│diskusi-staff — Rapat staff.\n"
                "🗃️│arsip-laporan — Arsip laporan pelanggaran.\n"
                "🛠│command-log — Log bot admin.\n"
                "🧾│jadwal-event — Jadwal kegiatan kampung.\n"
                "🧩│testing-bot — Uji fitur bot baru.\n"
                "📢│staff-info — Informasi antar staff."
            ),
            inline=False
        )

        embed.set_footer(text="Kampung Jongki • Dibangun dengan gotong royong ❤️")

        await interaction.response.send_message(embed=embed, ephemeral=False)

async def setup(bot):
    await bot.add_cog(PetaKampung(bot))
