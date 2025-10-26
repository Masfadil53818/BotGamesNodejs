import discord
from discord.ext import commands
import os, json, asyncio
from flask import Flask, send_from_directory, jsonify, request
from threading import Thread
import datetime

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

TOKEN = "YOUR_BOT_TOKEN"

# === Flask Web Server ===
app = Flask(__name__, static_folder="web", static_url_path="/web")

@app.route("/")
def home():
    return send_from_directory("web", "dashboard.html")

@app.route("/<path:filename>")
def serve_html(filename):
    return send_from_directory("web", filename)

# Contoh API sederhana: ambil data bot
@app.route("/api/botinfo")
def bot_info():
    data = {
        "bot_name": str(bot.user.name) if bot.user else "Bot belum aktif",
        "guild_count": len(bot.guilds),
        "user_count": len(bot.users),
        "status": "Online" if bot.is_ready() else "Offline"
    }
    return jsonify(data)

# Contoh endpoint: kirim pesan ke channel lewat dashboard
@app.route("/api/send", methods=["POST"])
def send_message():
    content = request.json.get("message")
    channel_id = request.json.get("channel_id")
    if not content or not channel_id:
        return jsonify({"error": "message dan channel_id harus diisi"}), 400

    channel = bot.get_channel(int(channel_id))
    if channel:
        asyncio.run_coroutine_threadsafe(channel.send(content), bot.loop)
        return jsonify({"success": True, "sent_to": channel_id})
    else:
        return jsonify({"error": "Channel tidak ditemukan"}), 404

@app.route("/api/dashboard")
def dashboard_data():
    data = {
        "total_users": len(bot.users) if bot.user else 0,
        "active_sessions": len(bot.guilds) if bot.user else 0,
        "revenue": 12340,  # contoh angka dummy
        "server_status": "Online" if bot.is_ready() else "Offline",
        "usage_percentage": 76,
        "notifications": [
            "Bot berhasil diupdate ke versi 7.0",
            "3 pengguna baru bergabung hari ini",
            "Server Kampung Jongki aktif 99%"
        ]
    }
    return jsonify(data)

@app.route("/api/settings", methods=["POST"])
def save_settings():
    data = request.json
    prefix = data.get("prefix")
    max_users = data.get("max_users")
    theme = data.get("theme")

    # Simpan pengaturan ke config.json
    with open("config.json", "r") as f:
        config = json.load(f)

    config.update({
        "prefix": prefix,
        "max_users": max_users,
        "theme": theme
    })

    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

    # (Opsional) update prefix bot langsung
    if prefix:
        bot.command_prefix = prefix

    return jsonify({
        "message": "Pengaturan berhasil disimpan!",
        "data": config
    })

@app.route("/api/profile")
def get_profile():
    """Mengirimkan data profil bot ke halaman profile.html"""
    if not bot.user:
        return jsonify({"error": "Bot belum aktif"}), 503

    data = {
        "name": str(bot.user.name),
        "id": str(bot.user.id),
        "avatar_url": bot.user.display_avatar.url if bot.user.display_avatar else "",
        "description": "Bot Discord Kampung v7.0 — powered by CornelloTeam",
        "servers": len(bot.guilds),
        "members": sum(g.member_count for g in bot.guilds),
        "commands": len(bot.tree.get_commands())
    }
    return jsonify(data)

start_time = datetime.datetime.utcnow()

@app.route("/api/info")
def get_info():
    """Mengirimkan info umum tentang bot"""
    if not bot.user:
        return jsonify({"error": "Bot belum aktif"}), 503

    # Hitung uptime bot
    uptime_seconds = (datetime.datetime.utcnow() - start_time).total_seconds()
    hours, remainder = divmod(int(uptime_seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime = f"{hours:02}:{minutes:02}:{seconds:02}"

    data = {
        "name": str(bot.user.name),
        "version": "10.0.0",
        "library": "discord.py",
        "servers": len(bot.guilds),
        "members": sum(g.member_count for g in bot.guilds),
        "uptime": uptime
    }
    return jsonify(data)

# Jalankan Flask di thread terpisah
def run_web():
    app.run(host="0.0.0.0", port=5000, debug=False)

# === Event Bot ===
@bot.event
async def on_ready():
    print(f"🌾 Kepala desa {bot.user} siap bekerja ")
    try:
        synced = await bot.tree.sync()
        print(f"✅ {len(synced)} slash command desa tersinkronisasi secara GLOBAL 🌍")
    except Exception as e:
        print(f"⚠️ Gagal sync command: {e}")

    # Ubah status menjadi Watching
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="member Discord"
        )
    )
# === Load semua Cogs ===
async def load_cogs():
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            await bot.load_extension(f"cogs.{file[:-3]}")

# === Main Runner ===
async def main():
    Thread(target=run_web, daemon=True).start()  # Jalankan web server di thread lain
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

asyncio.run(main())
