import discord
from discord import app_commands
from discord.ext import commands

class Panduan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="panduan", description="Tampilkan panduan dan peraturan warga Kampung Jongki 🏡")
    async def panduan(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📜 Panduan Warga Kampung Jongki",
            description="Selamat datang di **Kampung Jongki**! 🏡\nBerikut panduan agar kamu bisa hidup damai, asik, dan tertib di kampung ini:",
            color=0x00ff80
        )

        embed.add_field(
            name="👋 1. Warga Baru",
            value=(
                "• Setelah join, kamu akan otomatis mendapat role **Warga Baru**.\n"
                "• Perkenalkan dirimu di channel `💭│ngobrol-bebas`.\n"
                "• Baca semua aturan di `📜│peraturan` agar tidak salah langkah!"
            ),
            inline=False
        )

        embed.add_field(
            name="🧑‍🌾 2. Kehidupan di Kampung",
            value=(
                "• Nongkrong di `💬│Balai Desa` buat ngobrol santai.\n"
                "• Mau jual-beli atau cari kerja? Pergi ke `🧑‍🌾│pasar-desa` dan `💰│kerja-sambilan`.\n"
                "• Share karya, meme, atau musik di galeri dan ruang hiburan!"
            ),
            inline=False
        )

        embed.add_field(
            name="🚨 3. Peraturan Umum",
            value=(
                "✅ Hormati semua warga & staff.\n"
                "❌ Jangan spam, toxic, atau provoke.\n"
                "🚫 Dilarang share konten negatif (NSFW, SARA, dll).\n"
                "📩 Kalau ada masalah, lapor ke `🚓│lapor-satpam`."
            ),
            inline=False
        )

        embed.add_field(
            name="🎮 4. Event & Ekonomi",
            value=(
                "• Ikuti lomba di `🏆│event-lomba` biar dapat hadiah keren.\n"
                "• Cek saldo & kerjaan di `💰│dompet-warga` dan `🧑‍🔧│kerja-sambilan`.\n"
                "• Saling bantu biar kampung makin ramai!"
            ),
            inline=False
        )

        embed.add_field(
            name="🧠 5. Belajar & Ide",
            value=(
                "• Bagi ide keren di `💡│ide-warga`.\n"
                "• Mau belajar bareng? Cek `📖│belajar-bersama` dan `🧩│workshop`."
            ),
            inline=False
        )

        embed.add_field(
            name="💼 6. Role dan Status",
            value=(
                "👑 Kepala Desa — Pemilik / Admin utama.\n"
                "🧍‍♂️ Pak RT — Moderator.\n"
                "🧑‍🌾 Warga Tetap — Member aktif.\n"
                "🧒 Warga Baru — Pendatang baru.\n"
                "🐓 Tukang Gosip — Warga paling aktif di chat.\n"
                "🧙 Dukun Kampung — Bot & sistem AI server."
            ),
            inline=False
        )

        embed.add_field(
            name="⚙️ 7. Fitur Otomatis",
            value=(
                "• Auto welcome di channel `👋│salam-datang`.\n"
                "• Auto role **Warga Baru** saat join.\n"
                "• Laporan pelanggaran langsung ke staff."
            ),
            inline=False
        )

        embed.set_footer(text="💚 Kampung Jongki — Hidup rukun dan ramai selamanya!")

        await interaction.response.send_message(embed=embed, ephemeral=False)

async def setup(bot):
    await bot.add_cog(Panduan(bot))
