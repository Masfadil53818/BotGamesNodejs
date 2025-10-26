import discord
from discord import app_commands
from discord.ext import commands

class Peraturan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="peraturan", description="Tampilkan peraturan resmi Kampung Jongki 📜")
    async def peraturan(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📜 Peraturan Warga Kampung Jongki",
            description=(
                "Selamat datang di **Kampung Jongki**! 🌾\n\n"
                "Agar kampung kita tetap damai, asik, dan rukun, mohon semua warga menaati peraturan berikut:"
            ),
            color=0xf1c40f
        )

        embed.add_field(
            name="1️⃣ Hormati Sesama Warga",
            value=(
                "• Bersikap sopan dan ramah kepada semua orang.\n"
                "• Tidak menghina, merendahkan, atau memprovokasi.\n"
                "• Perbedaan pendapat boleh, tapi tetap dengan etika."
            ),
            inline=False
        )

        embed.add_field(
            name="2️⃣ Jangan Spam atau Flood Chat",
            value=(
                "• Hindari kirim pesan berulang atau tidak penting secara cepat.\n"
                "• Jangan spam emoji, mention, atau huruf besar berlebihan."
            ),
            inline=False
        )

        embed.add_field(
            name="3️⃣ Dilarang Konten Negatif",
            value=(
                "🚫 Dilarang keras konten **SARA, NSFW, Politik, Kekerasan**, atau hal yang bisa menyinggung orang lain.\n"
                "📸 Semua konten harus aman dan pantas untuk umum."
            ),
            inline=False
        )

        embed.add_field(
            name="4️⃣ Gunakan Channel Sesuai Fungsinya",
            value=(
                "• Jangan ngobrol di channel yang khusus untuk informasi.\n"
                "• Lihat deskripsi channel untuk tahu fungsi masing-masing."
            ),
            inline=False
        )

        embed.add_field(
            name="5️⃣ Dilarang Iklan / Promosi Tanpa Izin",
            value=(
                "• Tidak boleh promosi server, sosial media, atau produk tanpa izin dari staff.\n"
                "• Promosi hanya boleh di channel khusus bila diizinkan."
            ),
            inline=False
        )

        embed.add_field(
            name="6️⃣ Gunakan Nama & Profil yang Layak",
            value=(
                "• Hindari nama yang mengandung kata kasar, provokatif, atau menyesatkan.\n"
                "• Gambar profil harus pantas untuk komunitas umum."
            ),
            inline=False
        )

        embed.add_field(
            name="7️⃣ Hormati Staff & Keputusan Mereka",
            value=(
                "• Keputusan Kepala Desa (Admin) dan Pak RT (Moderator) bersifat final.\n"
                "• Kalau merasa tidak adil, laporkan baik-baik di `🚓│lapor-satpam`."
            ),
            inline=False
        )

        embed.add_field(
            name="8️⃣ Keamanan Akun",
            value=(
                "• Jangan share akun, token, atau data pribadi ke siapapun.\n"
                "• Staff tidak akan pernah meminta password / login Discord kamu."
            ),
            inline=False
        )

        embed.add_field(
            name="9️⃣ Dilarang Menyalahgunakan Bot",
            value=(
                "• Jangan spam command bot atau ganggu bot bekerja.\n"
                "• Gunakan fitur bot sesuai panduan yang ada."
            ),
            inline=False
        )

        embed.add_field(
            name="🔟 Sanksi",
            value=(
                "• Pelanggaran ringan = **peringatan atau mute sementara**.\n"
                "• Pelanggaran berat = **kick atau ban permanen**.\n"
                "• Semua sanksi akan dicatat di channel `📋│log-server`."
            ),
            inline=False
        )

        embed.set_footer(text="Kampung Jongki • Tertib, Ramai, dan Damai 🏡")

        await interaction.response.send_message(embed=embed, ephemeral=False)

async def setup(bot):
    await bot.add_cog(Peraturan(bot))
