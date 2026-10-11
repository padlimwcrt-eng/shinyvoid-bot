# -*- coding: utf-8 -*-
# ShinyVoid Bot v3.0 - Telegram Multifunction Bot
# Owner: Fadli | Key Access + Temp Mail + AI Fix + Jadwal Sholat + Music DL
# Key rahasia: shiny-void-fadli

import os
import re
import json
import socket
import random
import string
import hashlib
import base64
import qrcode
import requests
from datetime import datetime
from PIL import Image
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters,
)

# ============ CONFIG ============
BOT_NAME = "ShinyVoid"
OWNER = "Fadli"
VERSION = "3.0.0"
TOKEN = "8540676205:AAGokmKsg0go6S-GJUB8r_2sRbJ0rauJh7I"
LOGO_URL = "https://files.catbox.moe/4mcjxx.jpg"
PREFIX = "/"

# 🔐 KEY RAHASIA — jangan share ke siapapun!
SECRET_KEY = "shiny-void-fadli"
AUTHORIZED_USERS = set()

# 📁 Folder penyimpanan (di memori HP via Termux)
MUSIC_DIR = os.path.expanduser("~/storage/downloads/ShinyVoidMusic")
if not os.path.exists(MUSIC_DIR):
    try:
        os.makedirs(MUSIC_DIR, exist_ok=True)
    except:
        MUSIC_DIR = os.path.expanduser("~/ShinyVoidMusic")
        os.makedirs(MUSIC_DIR, exist_ok=True)

# ============ MENU TEXTS ============
def menu_main():
    return (
        "╔══════════════════════╗\n"
        "║   ✨ SHINYVOID BOT ✨   ║\n"
        "╚══════════════════════╝\n\n"
        "👤 Owner   : " + OWNER + "\n"
        "📦 Version : " + VERSION + "\n"
        "⚙️ Prefix  : " + PREFIX + "\n"
        "🟢 Status  : Online\n"
        "🔐 Access  : Authorized\n\n"
        "━━━ 「 MENU UTAMA 」 ━━━\n"
        "1️⃣ /menu1  → Info & Tools\n"
        "2️⃣ /menu2  → Text Tools\n"
        "3️⃣ /menu3  → Media & Download\n"
        "4️⃣ /menu4  → Fun & Game\n"
        "5️⃣ /menu5  → Utility\n"
        "6️⃣ /menu6  → Music & Islami\n"
        "7️⃣ /menu7  → Temp Mail\n\n"
        "💡 Total 80+ commands!"
    )

def menu_1():
    return (
        "📌 MENU 1 — INFO & TOOLS\n\n"
        "ℹ️ INFO:\n"
        "/start /menu /ping /info /owner\n"
        "/id /time /date /about\n\n"
        "🔧 TOOLS:\n"
        "/qrcode <teks>\n"
        "/shortlink <url>\n"
        "/hash <teks>\n"
        "/base64 enc/dec <teks>\n"
        "/calc <ekspresi>\n"
        "/pass [panjang]\n"
        "/uuid\n"
        "/ip"
    )

def menu_2():
    return (
        "✍️ MENU 2 — TEXT TOOLS\n\n"
        "/upper /lower /reverse /title\n"
        "/len /count /repeat\n"
        "/replace lama|baru|teks\n"
        "/spongebob /vaporwave\n\n"
        "🌐 TRANSLATE:\n"
        "/translate <kode> <teks>\n"
        "/toid /toen /tojp"
    )

def menu_3():
    return (
        "🎬 MENU 3 — MEDIA\n\n"
        "📥 UNIVERSAL DOWNLOAD:\n"
        "/ytmp3 <url>  → Audio (MP3)\n"
        "/ytmp4 <url>  → Video (MP4)\n"
        "/ytinfo <url> → Info media\n\n"
        "✅ Support: YouTube, TikTok,\n"
        "Instagram, Facebook, Twitter/X,\n"
        "Vimeo, Reddit, Pinterest, dll!\n\n"
        "🖼️ MEDIA:\n"
        "/sticker (reply foto)\n"
        "/logo /wallpaper /meme\n"
        "/cat /dog"
    )

def menu_4():
    return (
        "🎲 MENU 4 — FUN\n\n"
        "/dadu /koin /random\n"
        "/slot /quotes /motivasi\n"
        "/fakta /joke /truth /dare\n"
        "/tebak /guess <angka>"
    )

def menu_5():
    return (
        "🛠️ MENU 5 — UTILITY\n\n"
        "🔍 SEARCH:\n"
        "/wiki <kata>\n"
        "/cuaca <kota>\n"
        "/github <username>\n\n"
        "📊 LIFE:\n"
        "/bmi <bb> <tb>\n"
        "/umur DD-MM-YYYY\n"
        "/diskon <harga> <persen>\n"
        "/pajak <penghasilan>"
    )

def menu_6():
    return (
        "🎵 MENU 6 — MUSIC & ISLAMI\n\n"
        "🎵 MUSIC DOWNLOADER:\n"
        "/music <judul>  → Cari & download\n"
        "/musicdl <url>  → Download by URL\n"
        "/musiclist      → List lagu tersimpan\n"
        "/musicclear     → Hapus semua lagu\n\n"
        "🕌 JADWAL SHOLAT:\n"
        "/sholat <kota>  → Jadwal hari ini\n"
        "/sholat <kota> <tgl> (DD-MM-YYYY)\n"
        "/kiblat <kota>  → Arah kiblat\n"
        "/asmaulhusna    → 99 Asmaul Husna\n"
        "/doa            → Doa pilihan\n"
        "/ayat           → Ayat pilihan"
    )

def menu_7():
    return (
        "📧 MENU 7 — TEMP MAIL\n\n"
        "/tempmail  → Buat email sementara\n"
        "/inbox     → Cek kotak masuk\n"
        "/baca <n>  → Baca pesan ke-n\n"
        "/hapusmail → Ganti email baru"
    )

# ============ KEYBOARDS ============
def kb_main():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("ℹ️ Info", callback_data="info"),
         InlineKeyboardButton("📌 Tools", callback_data="m1")],
        [InlineKeyboardButton("✍️ Text", callback_data="m2"),
         InlineKeyboardButton("🎬 Media", callback_data="m3")],
        [InlineKeyboardButton("🎲 Fun", callback_data="m4"),
         InlineKeyboardButton("🛠️ Utility", callback_data="m5")],
        [InlineKeyboardButton("🎵 Music", callback_data="m6"),
         InlineKeyboardButton("📧 Mail", callback_data="m7")],
        [InlineKeyboardButton("🏓 Ping", callback_data="ping"),
         InlineKeyboardButton("❌ Tutup", callback_data="x")],
    ])

def kb_back():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Kembali ke Menu", callback_data="menu")]
    ])

# ============ AUTH CHECK ============
def is_authorized(user_id):
    return user_id in AUTHORIZED_USERS

async def require_key(update: Update):
    await update.message.reply_text(
        "🔐 *AKSES DIBATASI*\n\n"
        "Kamu belum memasukkan key akses.\n\n"
        "Ketik:\n"
        "`/key <key-akses>`\n\n"
        "💡 Key hanya diberikan oleh Owner.\n"
        "Hubungi owner untuk mendapatkan akses.",
        parse_mode="Markdown"
    )

# ============ COMMAND HANDLERS ============
async def cmd_key(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if is_authorized(user_id):
        return await update.message.reply_text("✅ Kamu sudah punya akses!")
    if not ctx.args:
        return await update.message.reply_text(
            "🔐 *VERIFIKASI KEY*\n\n"
            "Format: `/key <key-akses>`\n\n"
            "Contoh: `/key xxxx-xxxx-xxxx`",
            parse_mode="Markdown"
        )
    key = ctx.args[0].strip().lower()
    if key == SECRET_KEY.lower():
        AUTHORIZED_USERS.add(user_id)
        try:
            await update.message.reply_photo(
                photo=LOGO_URL,
                caption=(
                    "✅ *AKSES DIBERIKAN!*\n\n"
                    "Selamat datang di *" + BOT_NAME + "*!\n\n"
                    "👤 Nama : " + update.effective_user.first_name + "\n"
                    "🆔 ID : `" + str(user_id) + "`\n"
                    "🔐 Status : Authorized\n\n"
                    "Ketik /menu untuk mulai ✨"
                ),
                parse_mode="Markdown"
            )
        except:
            await update.message.reply_text(
                "✅ AKSES DIBERIKAN!\n\nKetik /menu untuk mulai."
            )
    else:
        await update.message.reply_text(
            "❌ *KEY SALAH!*\n\n"
            "Akses ditolak. Hubungi owner untuk key yang benar.",
            parse_mode="Markdown"
        )

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_authorized(user_id):
        return await require_key(update)
    try:
        await update.message.reply_photo(
            photo=LOGO_URL,
            caption=(
                "╔══════════════════════╗\n"
                "║   ✨ SHINYVOID BOT ✨   ║\n"
                "╚══════════════════════╝\n\n"
                "👋 Halo " + update.effective_user.first_name + "!\n\n"
                "Selamat datang di ShinyVoid v" + VERSION + "\n"
                "Bot multifungsi dengan 80+ fitur!\n\n"
                "Ketik /menu untuk mulai ✨"
            ),
        )
    except:
        await update.message.reply_text("Halo! Ketik /menu untuk mulai.")

async def cmd_menu(update, ctx):
    if not is_authorized(update.effective_user.id):
        return await require_key(update)
    await update.message.reply_text(menu_main(), reply_markup=kb_main())

async def cmd_m1(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    await update.message.reply_text(menu_1(), reply_markup=kb_back())

async def cmd_m2(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    await update.message.reply_text(menu_2(), reply_markup=kb_back())

async def cmd_m3(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    await update.message.reply_text(menu_3(), reply_markup=kb_back())

async def cmd_m4(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    await update.message.reply_text(menu_4(), reply_markup=kb_back())

async def cmd_m5(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    await update.message.reply_text(menu_5(), reply_markup=kb_back())

async def cmd_m6(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    await update.message.reply_text(menu_6(), reply_markup=kb_back())

async def cmd_m7(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    await update.message.reply_text(menu_7(), reply_markup=kb_back())

async def cmd_ping(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    host = socket.gethostname()
    now = datetime.now().strftime("%H:%M:%S")
    await update.message.reply_text(
        "🏓 PONG!\n\n"
        "🖥️ Host : " + host + "\n"
        "⏰ Waktu : " + now + "\n"
        "🟢 Status : Online"
    )

async def cmd_info(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    await update.message.reply_text(
        "✨ " + BOT_NAME + " v" + VERSION + "\n"
        "👤 Owner : " + OWNER + "\n"
        "🎯 Fitur : 80+ commands\n"
        "📥 Downloader : Universal\n"
        "🎵 Music : Saved to " + MUSIC_DIR + "\n"
        "🔐 Access : Key Protected\n"
        "📦 Status : Online"
    )

async def cmd_about(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    await update.message.reply_text(
        "ℹ️ Tentang " + BOT_NAME + "\n\n"
        "Bot Telegram multifungsi v" + VERSION + ":\n"
        "tools, downloader, music, temp mail,\n"
        "jadwal sholat, fun, utility, AI.\n\n"
        "Dibuat oleh " + OWNER
    )

async def cmd_owner(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    await update.message.reply_text("👤 Owner: " + OWNER)

async def cmd_id(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    u = update.effective_user
    await update.message.reply_text(
        "🆔 Info Kamu\n\n"
        "👤 Nama : " + u.first_name + "\n"
        "🆔 ID : " + str(u.id) + "\n"
        "🌐 Bahasa : " + str(u.language_code) + "\n"
        "🔐 Status : Authorized ✅"
    )

async def cmd_time(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    await update.message.reply_text("⏰ " + datetime.now().strftime("%H:%M:%S"))

async def cmd_date(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    await update.message.reply_text("📅 " + datetime.now().strftime("%d-%m-%Y (%A)"))

# ============ TOOLS ============
async def cmd_qrcode(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    if not ctx.args:
        return await update.message.reply_text("⚠️ Format: /qrcode <teks>")
    try:
        text = " ".join(ctx.args)
        img = qrcode.make(text)
        img.save("qrcode_out.png")
        await update.message.reply_photo(
            photo=open("qrcode_out.png", "rb"),
            caption="✅ QR Code dibuat!"
        )
    except Exception as e:
        await update.message.reply_text("❌ Error: " + str(e))

async def cmd_shortlink(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    if not ctx.args:
        return await update.message.reply_text("⚠️ Format: /shortlink <url>")
    try:
        r = requests.get("https://tinyurl.com/api-create.php?url=" + ctx.args[0], timeout=10)
        await update.message.reply_text("🔗 Link pendek:\n" + r.text)
    except Exception as e:
        await update.message.reply_text("❌ Error: " + str(e))

async def cmd_hash(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    if not ctx.args: return await update.message.reply_text("⚠️ Format: /hash <teks>")
    text = " ".join(ctx.args)
    await update.message.reply_text(
        "🔐 Hash dari: " + text + "\n\n"
        "MD5:\n" + hashlib.md5(text.encode()).hexdigest() + "\n\n"
        "SHA1:\n" + hashlib.sha1(text.encode()).hexdigest() + "\n\n"
        "SHA256:\n" + hashlib.sha256(text.encode()).hexdigest()
    )

async def cmd_base64(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    if len(ctx.args) < 2:
        return await update.message.reply_text("⚠️ Format:\n/base64 enc <teks>\n/base64 dec <teks>")
    mode = ctx.args[0]
    text = " ".join(ctx.args[1:])
    try:
        if mode == "enc":
            await update.message.reply_text("🔐 Encoded:\n" + base64.b64encode(text.encode()).decode())
        elif mode == "dec":
            await update.message.reply_text("🔓 Decoded:\n" + base64.b64decode(text.encode()).decode())
        else:
            await update.message.reply_text("⚠️ Mode harus enc atau dec")
    except Exception as e:
        await update.message.reply_text("❌ Error: " + str(e))

async def cmd_calc(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    if not ctx.args: return await update.message.reply_text("⚠️ Format: /calc 2+2*5")
    expr = " ".join(ctx.args)
    try:
        allowed = set("0123456789+-*/.() ")
        if not all(c in allowed for c in expr):
            return await update.message.reply_text("❌ Karakter tidak diizinkan")
        result = eval(expr, {"__builtins__": {}}, {})
        await update.message.reply_text("🧮 " + expr + " = " + str(result))
    except Exception as e:
        await update.message.reply_text("❌ Error: " + str(e))

async def cmd_pass(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    length = 16
    if ctx.args and ctx.args[0].isdigit():
        length = min(int(ctx.args[0]), 64)
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    pwd = "".join(random.choice(chars) for _ in range(length))
    await update.message.reply_text("🔐 Password baru:\n" + pwd + "\n\n⚠️ Simpan dengan aman!")

async def cmd_uuid(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    import uuid
    await update.message.reply_text("🆔 UUID:\n" + str(uuid.uuid4()))

async def cmd_ip(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    try:
        r = requests.get("https://ipinfo.io/json", timeout=10).json()
        await update.message.reply_text(
            "🌐 Info IP Publik\n\n"
            "IP : " + str(r.get("ip")) + "\n"
            "Kota : " + str(r.get("city")) + "\n"
            "Region : " + str(r.get("region")) + "\n"
            "Negara : " + str(r.get("country")) + "\n"
            "ISP : " + str(r.get("org"))
        )
    except Exception as e:
        await update.message.reply_text("❌ Error: " + str(e))

# ============ TEXT ============
async def cmd_upper(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    if not ctx.args: return await update.message.reply_text("⚠️ /upper <teks>")
    await update.message.reply_text(" ".join(ctx.args).upper())

async def cmd_lower(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    if not ctx.args: return await update.message.reply_text("⚠️ /lower <teks>")
    await update.message.reply_text(" ".join(ctx.args).lower())

async def cmd_reverse(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    if not ctx.args: return await update.message.reply_text("⚠️ /reverse <teks>")
    await update.message.reply_text(" ".join(ctx.args)[::-1])

async def cmd_title(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    if not ctx.args: return await update.message.reply_text("⚠️ /title <teks>")
    await update.message.reply_text(" ".join(ctx.args).title())

async def cmd_len(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    if not ctx.args: return await update.message.reply_text("⚠️ /len <teks>")
    await update.message.reply_text("📏 Panjang: " + str(len(" ".join(ctx.args))) + " karakter")

async def cmd_count(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    if not ctx.args: return await update.message.reply_text("⚠️ /count <teks>")
    await update.message.reply_text("📝 Jumlah kata: " + str(len(" ".join(ctx.args).split())))

async def cmd_repeat(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    if len(ctx.args) < 2: return await update.message.reply_text("⚠️ /repeat <n> <teks>")
    try:
        n = int(ctx.args[0])
        await update.message.reply_text((" ".join(ctx.args[1:]) + "\n") * n)
    except:
        await update.message.reply_text("❌ Format salah")

async def cmd_replace(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    if not ctx.args: return await update.message.reply_text("⚠️ /replace lama|baru|teks")
    parts = " ".join(ctx.args).split("|")
    if len(parts) < 3:
        return await update.message.reply_text("⚠️ Format: /replace lama|baru|teks")
    await update.message.reply_text(parts[2].strip().replace(parts[0].strip(), parts[1].strip()))

async def cmd_spongebob(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    if not ctx.args: return await update.message.reply_text("⚠️ /spongebob <teks>")
    text = " ".join(ctx.args)
    await update.message.reply_text("".join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(text)))

async def cmd_vaporwave(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    if not ctx.args: return await update.message.reply_text("⚠️ /vaporwave <teks>")
    text = " ".join(ctx.args)
    result = ""
    for c in text:
        if c.isalnum():
            result += chr(ord(c) + 0xFEE0)
        elif c == " ":
            result += "　"
        else:
            result += c
    await update.message.reply_text(result)

# ============ TRANSLATE ============
async def translate_text(text, target):
    try:
        from deep_translator import GoogleTranslator
        return GoogleTranslator(source="auto", target=target).translate(text)
    except Exception as e:
        return "❌ Error: " + str(e)

async def cmd_translate(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    if len(ctx.args) < 2:
        return await update.message.reply_text("⚠️ /translate <kode> <teks>")
    result = await translate_text(" ".join(ctx.args[1:]), ctx.args[0])
    await update.message.reply_text("🌐 " + result)

async def cmd_toid(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    if not ctx.args: return await update.message.reply_text("⚠️ /toid <teks>")
    await update.message.reply_text("🇮🇩 " + await translate_text(" ".join(ctx.args), "id"))

async def cmd_toen(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    if not ctx.args: return await update.message.reply_text("⚠️ /toen <teks>")
    await update.message.reply_text("🇬🇧 " + await translate_text(" ".join(ctx.args), "en"))

async def cmd_tojp(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    if not ctx.args: return await update.message.reply_text("⚠️ /tojp <teks>")
    await update.message.reply_text("🇯🇵 " + await translate_text(" ".join(ctx.args), "ja"))

# ============ UNIVERSAL DOWNLOADER ============
def is_valid_url(url):
    return url.startswith("http://") or url.startswith("https://")

async def cmd_ytmp3(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    if not ctx.args: return await update.message.reply_text("⚠️ /ytmp3 <url>")
    url = ctx.args[0]
    if not is_valid_url(url):
        return await update.message.reply_text("❌ URL tidak valid")
    msg = await update.message.reply_text("⬇️ Mengunduh audio... ⏳")
    try:
        import yt_dlp
        os.makedirs("downloads", exist_ok=True)
        opts = {
            "format": "bestaudio/best",
            "outtmpl": "downloads/%(title).80s.%(ext)s",
            "quiet": True, "no_warnings": True, "noplaylist": True,
            "nocheckcertificate": True,
            "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}],
            "http_headers": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            base, _ = os.path.splitext(filename)
            mp3_file = base + ".mp3"
            if not os.path.exists(mp3_file): mp3_file = filename
        await msg.edit_text("📤 Mengirim file...")
        await update.message.reply_audio(audio=open(mp3_file, "rb"), title=info.get("title", "")[:60])
        await msg.delete()
    except Exception as e:
        err = str(e).replace("ERROR:", "").strip()[:300]
        await msg.edit_text("❌ Gagal: " + err)

async def cmd_ytmp4(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    if not ctx.args: return await update.message.reply_text("⚠️ /ytmp4 <url>")
    url = ctx.args[0]
    if not is_valid_url(url): return await update.message.reply_text("❌ URL tidak valid")
    msg = await update.message.reply_text("⬇️ Mengunduh video... ⏳")
    try:
        import yt_dlp
        os.makedirs("downloads", exist_ok=True)
        opts = {
            "format": "best[ext=mp4]/best[height<=720]/best",
            "outtmpl": "downloads/%(title).80s.%(ext)s",
            "quiet": True, "no_warnings": True, "noplaylist": True,
            "nocheckcertificate": True, "merge_output_format": "mp4",
            "http_headers": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            base, _ = os.path.splitext(filename)
            mp4_file = base + ".mp4"
            if os.path.exists(mp4_file): filename = mp4_file
        await msg.edit_text("📤 Mengirim video...")
        await update.message.reply_video(video=open(filename, "rb"), caption=info.get("title", "")[:200], supports_streaming=True)
        await msg.delete()
    except Exception as e:
        err = str(e).replace("ERROR:", "").strip()[:300]
        await msg.edit_text("❌ Gagal: " + err)

async def cmd_ytinfo(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    if not ctx.args: return await update.message.reply_text("⚠️ /ytinfo <url>")
    url = ctx.args[0]
    if not is_valid_url(url): return await update.message.reply_text("❌ URL tidak valid")
    msg = await update.message.reply_text("🔍 Mengambil info...")
    try:
        import yt_dlp
        opts = {"quiet": True, "no_warnings": True, "noplaylist": True, "nocheckcertificate": True}
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
        duration = info.get("duration") or 0
        await msg.edit_text(
            "📹 Info Media\n\n"
            "🎬 Judul : " + str(info.get("title", "-"))[:100] + "\n"
            "👤 Uploader : " + str(info.get("uploader", "-"))[:50] + "\n"
            "⏱️ Durasi : " + str(duration // 60) + "m " + str(duration % 60) + "s\n"
            "👁️ Views : " + str(info.get("view_count", 0)) + "\n"
            "🌐 Platform : " + str(info.get("extractor", "-"))
        )
    except Exception as e:
        await msg.edit_text("❌ Gagal: " + str(e)[:300])

# ============ MUSIC DOWNLOADER (AUTO-SAVE) ============
async def cmd_music(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    if not ctx.args:
        return await update.message.reply_text("⚠️ /music <judul lagu>")
    query = " ".join(ctx.args)
    msg = await update.message.reply_text("🎵 Mencari: " + query + "\n⏳ Mohon tunggu...")
    try:
        import yt_dlp
        os.makedirs(MUSIC_DIR, exist_ok=True)
        opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(MUSIC_DIR, "%(title).80s.%(ext)s"),
            "quiet": True, "no_warnings": True, "noplaylist": True,
            "nocheckcertificate": True,
            "default_search": "ytsearch1",
            "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}],
            "http_headers": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info("ytsearch1:" + query, download=True)
            if "entries" in info:
                info = info["entries"][0]
            filename = ydl.prepare_filename(info)
            base, _ = os.path.splitext(filename)
            mp3_file = base + ".mp3"
            if not os.path.exists(mp3_file): mp3_file = filename
        await msg.edit_text(
            "✅ *Lagu berhasil diunduh!*\n\n"
            "🎵 Judul : " + info.get("title", "-")[:60] + "\n"
            "👤 Artis : " + str(info.get("uploader", "-"))[:40] + "\n"
            "📁 Tersimpan di : `" + mp3_file + "`\n\n"
            "💡 Cek di file manager HP kamu!",
            parse_mode="Markdown"
        )
        await update.message.reply_audio(audio=open(mp3_file, "rb"), title=info.get("title", "")[:60])
    except Exception as e:
        err = str(e).replace("ERROR:", "").strip()[:300]
        await msg.edit_text("❌ Gagal: " + err)

async def cmd_musicdl(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    if not ctx.args: return await update.message.reply_text("⚠️ /musicdl <url>")
    url = ctx.args[0]
    if not is_valid_url(url): return await update.message.reply_text("❌ URL tidak valid")
    msg = await update.message.reply_text("🎵 Mengunduh dari URL... ⏳")
    try:
        import yt_dlp
        os.makedirs(MUSIC_DIR, exist_ok=True)
        opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(MUSIC_DIR, "%(title).80s.%(ext)s"),
            "quiet": True, "no_warnings": True, "noplaylist": True,
            "nocheckcertificate": True,
            "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}],
            "http_headers": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            base, _ = os.path.splitext(filename)
            mp3_file = base + ".mp3"
            if not os.path.exists(mp3_file): mp3_file = filename
        await msg.edit_text(
            "✅ *Berhasil diunduh!*\n\n"
            "🎵 " + info.get("title", "-")[:60] + "\n"
            "📁 `" + mp3_file + "`",
            parse_mode="Markdown"
        )
        await update.message.reply_audio(audio=open(mp3_file, "rb"), title=info.get("title", "")[:60])
    except Exception as e:
        await msg.edit_text("❌ Gagal: " + str(e)[:300])

async def cmd_musiclist(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    try:
        if not os.path.exists(MUSIC_DIR):
            return await update.message.reply_text("📁 Folder music masih kosong.")
        files = [f for f in os.listdir(MUSIC_DIR) if f.endswith(".mp3")]
        if not files:
            return await update.message.reply_text("📁 Belum ada lagu tersimpan.")
        text = "🎵 *MUSIC LIST (" + str(len(files)) + " lagu)*\n\n"
        for i, f in enumerate(files[:30], 1):
            size = os.path.getsize(os.path.join(MUSIC_DIR, f)) / (1024 * 1024)
            text += str(i) + ". " + f[:50] + " (" + str(round(size, 1)) + " MB)\n"
        text += "\n📁 Lokasi: `" + MUSIC_DIR + "`"
        await update.message.reply_text(text, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text("❌ Error: " + str(e))

async def cmd_musicclear(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    try:
        if os.path.exists(MUSIC_DIR):
            for f in os.listdir(MUSIC_DIR):
                os.remove(os.path.join(MUSIC_DIR, f))
        await update.message.reply_text("🗑️ Semua lagu dihapus!")
    except Exception as e:
        await update.message.reply_text("❌ Error: " + str(e))

# ============ JADWAL SHOLAT ============
async def cmd_sholat(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    if not ctx.args:
        return await update.message.reply_text("⚠️ Format:\n/sholat <kota>\n/sholat <kota> <DD-MM-YYYY>")
    try:
        kota = ctx.args[0]
        if len(ctx.args) >= 2:
            tgl = ctx.args[1].split("-")
            if len(tgl) == 3:
                date_str = tgl[2] + "-" + tgl[1] + "-" + tgl[0]
            else:
                date_str = datetime.now().strftime("%d-%m-%Y")
        else:
            date_str = datetime.now().strftime("%d-%m-%Y")
        r = requests.get("https://api.aladhan.com/v1/timingsByCity?city=" + kota + "&country=Indonesia&method=11&date=" + date_str, timeout=15).json()
        if r.get("code") != 200:
            return await update.message.reply_text("❌ Kota tidak ditemukan atau API error")
        data = r["data"]
        timings = data["timings"]
        hijri = data["date"]["hijri"]
        await update.message.reply_text(
            "🕌 *JADWAL SHOLAT*\n"
            "📍 " + kota.title() + ", Indonesia\n"
            "📅 " + date_str + "\n"
            "🌙 " + hijri["day"] + " " + hijri["month"]["en"] + " " + hijri["year"] + " H\n\n"
            "┌─────────────────────\n"
            "│ 🌅 Imsak    : " + timings.get("Imsak", "-") + "\n"
            "│ 🌄 Subuh    : " + timings.get("Fajr", "-") + "\n"
            "│ ☀️ Syuruq   : " + timings.get("Sunrise", "-") + "\n"
            "│ 🌞 Dzuhur   : " + timings.get("Dhuhr", "-") + "\n"
            "│ 🌤️ Ashar    : " + timings.get("Asr", "-") + "\n"
            "│ 🌇 Maghrib  : " + timings.get("Maghrib", "-") + "\n"
            "│ 🌃 Isya     : " + timings.get("Isha", "-") + "\n"
            "└─────────────────────\n\n"
            "💡 Sumber: Aladhan API",
            parse_mode="Markdown"
        )
    except Exception as e:
        await update.message.reply_text("❌ Error: " + str(e)[:300])

async def cmd_kiblat(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    if not ctx.args: return await update.message.reply_text("⚠️ /kiblat <kota>")
    try:
        kota = " ".join(ctx.args)
        r = requests.get("https://api.aladhan.com/v1/qibla/" + kota, timeout=15).json()
        if r.get("code") != 200:
            return await update.message.reply_text("❌ Kota tidak ditemukan")
        data = r["data"]
        await update.message.reply_text(
            "🕋 *ARAH KIBLAT*\n\n"
            "📍 Kota : " + kota.title() + "\n"
            "🧭 Arah : " + str(round(data.get("direction", 0), 2)) + "° dari Utara\n\n"
            "💡 Kompas: Putar " + str(round(data.get("direction", 0), 2)) + "° dari arah Utara.",
            parse_mode="Markdown"
        )
    except Exception as e:
        await update.message.reply_text("❌ Error: " + str(e)[:300])

ASMAUL_HUSNA = [
    "Ar-Rahman (Yang Maha Pengasih)",
    "Ar-Rahim (Yang Maha Penyayang)",
    "Al-Malik (Yang Maha Merajai)",
    "Al-Quddus (Yang Maha Suci)",
    "As-Salam (Yang Maha Memberi Kesejahteraan)",
    "Al-Mu'min (Yang Maha Memberi Keamanan)",
    "Al-Muhaimin (Yang Maha Mengatur)",
    "Al-'Aziz (Yang Maha Perkasa)",
    "Al-Jabbar (Yang Memiliki Mutlak Kegagahan)",
    "Al-Mutakabbir (Yang Maha Megah)",
]

async def cmd_asmaulhusna(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    pilihan = random.sample(ASMAUL_HUSNA, 3)
    text = "📿 *ASMAUL HUSNA*\n\n"
    for i, a in enumerate(pilihan, 1):
        text += str(i) + ". " + a + "\n"
    text += "\n💡 Total 99 nama Allah SWT."
    await update.message.reply_text(text, parse_mode="Markdown")

DOA_LIST = [
    ("Doa Sebelum Makan", "Bismillahirahmanirrahim. Allahumma barik lana fima razaqtana wa qina azaban naar."),
    ("Doa Sesudah Makan", "Alhamdulillahilladzi ath'amana wa saqana wa ja'alana minal muslimin."),
    ("Doa Sebelum Tidur", "Bismikallahumma ahya wa bismika amut."),
    ("Doa Bangun Tidur", "Alhamdulillahilladzi ahyana ba'da ma amatana wa ilaihin nusyur."),
    ("Doa Keluar Rumah", "Bismillahi tawakkaltu 'alallah, wa laa haula wa laa quwwata illa billah."),
    ("Doa Masuk WC", "Allahumma inni a'udzubika minal khubutsi wal khabaits."),
    ("Doa Keluar WC", "Ghufranaka."),
    ("Doa Sebelum Belajar", "Rabbi zidni 'ilma warzuqni fahma."),
    ("Doa Untuk Orang Tua", "Rabbighfirli waliwalidayya warhamhuma kama rabbayani shaghira."),
    ("Doa Kebaikan Dunia Akhirat", "Rabbana atina fiddunya hasanah wa fil akhirati hasanah wa qina 'adzabannar."),
]

async def cmd_doa(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    judul, isi = random.choice(DOA_LIST)
    await update.message.reply_text(
        "🤲 *" + judul + "*\n\n_" + isi + "_",
        parse_mode="Markdown"
    )

AYAT_LIST = [
    ("QS. Al-Baqarah: 286", "Allah tidak membebani seseorang melainkan sesuai dengan kesanggupannya."),
    ("QS. Al-Insyirah: 6", "Sesungguhnya bersama kesulitan ada kemudahan."),
    ("QS. At-Talaq: 3", "Dan barangsiapa bertawakal kepada Allah, niscaya Allah akan mencukupkan (keperluan)nya."),
    ("QS. Ar-Ra'd: 28", "Ingatlah, hanya dengan mengingat Allah hati menjadi tenang."),
    ("QS. Al-Ankabut: 69", "Dan orang-orang yang berjihad untuk (mencari keridhaan) Kami, benar-benar akan Kami tunjukkan kepada mereka jalan-jalan Kami."),
    ("QS. Ali Imran: 139", "Dan janganlah kamu merasa lemah, dan janganlah kamu bersedih hati, sebab kamu paling tinggi (derajatnya), jika kamu orang beriman."),
    ("QS. Yusuf: 87", "Dan janganlah kamu berputus asa dari rahmat Allah."),
]

async def cmd_ayat(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    sumber, isi = random.choice(AYAT_LIST)
    await update.message.reply_text(
        "📖 *" + sumber + "*\n\n_" + isi + "_",
        parse_mode="Markdown"
    )

# ============ STICKER & MEDIA ============
async def cmd_sticker(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        return await update.message.reply_text("⚠️ Reply foto dengan /sticker")
    try:
        photo = update.message.reply_to_message.photo[-1]
        file = await ctx.bot.get_file(photo.file_id)
        await file.download_to_drive("input.jpg")
        img = Image.open("input.jpg").convert("RGBA")
        img.thumbnail((512, 512))
        img.save("sticker.webp", "WEBP")
        await update.message.reply_sticker(sticker=open("sticker.webp", "rb"))
    except Exception as e:
        await update.message.reply_text("❌ Error: " + str(e))

async def handle_photo(update, ctx):
    if not is_authorized(update.effective_user.id):
        return
    caption = (update.message.caption or "").lower()
    if caption.startswith("/sticker"):
        try:
            photo = update.message.photo[-1]
            file = await ctx.bot.get_file(photo.file_id)
            await file.download_to_drive("input.jpg")
            img = Image.open("input.jpg").convert("RGBA")
            img.thumbnail((512, 512))
            img.save("sticker.webp", "WEBP")
            await update.message.reply_sticker(sticker=open("sticker.webp", "rb"))
        except Exception as e:
            await update.message.reply_text("❌ Error: " + str(e))

async def cmd_logo(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    await update.message.reply_photo(photo=LOGO_URL, caption="✨ Logo resmi " + BOT_NAME)

async def cmd_wallpaper(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    url = "https://picsum.photos/1080/1920?random=" + str(random.randint(1, 9999))
    await update.message.reply_photo(photo=url, caption="🖼️ Wallpaper random")

async def cmd_meme(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    try:
        r = requests.get("https://meme-api.com/gimme", timeout=10).json()
        await update.message.reply_photo(photo=r.get("url"), caption="😂 Meme random")
    except Exception as e:
        await update.message.reply_text("❌ Gagal: " + str(e))

async def cmd_cat(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    await update.message.reply_photo(photo="https://cataas.com/cat", caption="🐱 Kucing random")

async def cmd_dog(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    try:
        r = requests.get("https://dog.ceo/api/breeds/image/random", timeout=10).json()
        await update.message.reply_photo(photo=r.get("message"), caption="🐶 Anjing random")
    except Exception as e:
        await update.message.reply_text("❌ Gagal: " + str(e))

# ============ FUN ============
QUOTES = [
    "Hidup itu seperti sepeda, agar tetap seimbang harus terus bergerak.",
    "Jangan tunggu kesempatan, ciptakanlah.",
    "Kesuksesan adalah hasil dari persiapan dan kerja keras.",
    "Mimpi tidak akan bekerja jika kamu tidak bekerja.",
]
MOTIVASI = [
    "💪 Kamu lebih kuat dari yang kamu pikirkan.",
    "🌟 Setiap hari adalah kesempatan baru.",
    "🔥 Jangan berhenti, kamu hampir sampai!",
    "🚀 Mimpi besar butuh langkah besar.",
]
FAKTA = [
    "🐙 Gurita memiliki 3 jantung.",
    "🍯 Madu tidak pernah basi.",
    "🌙 Bulan menjauh dari Bumi 3.8 cm/tahun.",
    "🐝 Lebah bisa mengenali wajah manusia.",
]
JOKE = [
    "Kenapa programmer suka kopi? Karena tanpa Java, mereka gak bisa ngoding!",
    "Kenapa komputer gak bisa sakit? Karena punya antivirus!",
    "Programmer: 'It works on my machine!'",
]
TRUTH = [
    "Siapa orang yang terakhir kamu chat?",
    "Apa hal paling memalukan yang pernah kamu lakukan?",
    "Siapa crush kamu saat SD?",
]
DARE = [
    "Kirim pesan 'Aku kangen kamu' ke kontak random!",
    "Update status 'Aku sedang mabuk cinta' selama 1 jam.",
    "Tirukan gaya artis favoritmu!",
]

async def cmd_dadu(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    await update.message.reply_text("🎲 Dadu: " + str(random.randint(1, 6)))

async def cmd_koin(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    await update.message.reply_text("🪙 Hasil: " + random.choice(["Kepala", "Ekor"]))

async def cmd_random(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    await update.message.reply_text("🎯 Angka random: " + str(random.randint(1, 100)))

async def cmd_slot(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    symbols = ["🍒", "🍋", "🍇", "⭐", "💎", "7️⃣"]
    r = [random.choice(symbols) for _ in range(3)]
    text = " | ".join(r)
    if r[0] == r[1] == r[2]:
        await update.message.reply_text("🎰 " + text + "\n\n🎉 JACKPOT! 🎉")
    else:
        await update.message.reply_text("🎰 " + text + "\n\n😅 Coba lagi!")

async def cmd_quotes(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    await update.message.reply_text("💭 " + random.choice(QUOTES))

async def cmd_motivasi(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    await update.message.reply_text(random.choice(MOTIVASI))

async def cmd_fakta(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    await update.message.reply_text("🧠 Fakta Unik:\n\n" + random.choice(FAKTA))

async def cmd_joke(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    await update.message.reply_text("😂 " + random.choice(JOKE))

async def cmd_truth(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    await update.message.reply_text("❓ TRUTH:\n" + random.choice(TRUTH))

async def cmd_dare(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    await update.message.reply_text("🔥 DARE:\n" + random.choice(DARE))

tebak_state = {}
async def cmd_tebak(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    tebak_state[update.effective_user.id] = random.randint(1, 100)
    await update.message.reply_text("🎮 Game Tebak Angka!\n\nAku pikirkan angka 1-100.\nCoba tebak dengan /guess <angka>")

async def cmd_guess(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    uid = update.effective_user.id
    if uid not in tebak_state:
        return await update.message.reply_text("⚠️ Mulai game dulu dengan /tebak")
    if not ctx.args or not ctx.args[0].isdigit():
        return await update.message.reply_text("⚠️ Format: /guess 50")
    tebakan = int(ctx.args[0])
    target = tebak_state[uid]
    if tebakan < target:
        await update.message.reply_text("⬆️ Terlalu kecil!")
    elif tebakan > target:
        await update.message.reply_text("⬇️ Terlalu besar!")
    else:
        await update.message.reply_text("🎉 BENAR! Angkanya " + str(target) + "!")
        del tebak_state[uid]

# ============ SEARCH + AI (MULTI FALLBACK) ============
async def cmd_wiki(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    if not ctx.args: return await update.message.reply_text("⚠️ /wiki <kata kunci>")
    try:
        import wikipedia
        wikipedia.set_lang("id")
        hasil = wikipedia.summary(" ".join(ctx.args), sentences=3)
        await update.message.reply_text("📚 Wikipedia\n\n" + hasil)
    except Exception as e:
        await update.message.reply_text("❌ Tidak ditemukan: " + str(e))

async def cmd_ai(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    if not ctx.args: return await update.message.reply_text("⚠️ /ai <pertanyaan>")
    prompt = " ".join(ctx.args)
    msg = await update.message.reply_text("🤖 AI sedang berpikir... ⏳")

    # Provider 1: SimSimi
    try:
        r = requests.get("https://api.simsimi.net/v2/?text=" + prompt + "&lc=id", timeout=10).json()
        if r.get("success"):
            return await msg.edit_text("🤖 " + str(r["success"]))
    except:
        pass

    # Provider 2: GPT4Free via pollinations
    try:
        url = "https://text.pollinations.ai/" + requests.utils.quote(prompt)
        r = requests.get(url, timeout=20)
        if r.status_code == 200 and r.text.strip():
            return await msg.edit_text("🤖 " + r.text.strip()[:1500])
    except:
        pass

    # Provider 3: ChatGPT free API
    try:
        r = requests.get(
            "https://api.davidcyriltech.my.id/ai/chatgpt",
            params={"text": prompt},
            timeout=20
        ).json()
        result = r.get("result") or r.get("response") or r.get("message")
        if result:
            return await msg.edit_text("🤖 " + str(result)[:1500])
    except:
        pass

    # Provider 4: Gemini free
    try:
        r = requests.get(
            "https://api.sandipbaruwal.com/ai/gemini",
            params={"q": prompt},
            timeout=20
        ).json()
        result = r.get("answer") or r.get("result") or r.get("response")
        if result:
            return await msg.edit_text("🤖 " + str(result)[:1500])
    except:
        pass

    await msg.edit_text(
        "❌ *Semua AI provider gagal!*\n\n"
        "Kemungkinan:\n"
        "• Koneksi internet bermasalah\n"
        "• API sedang down\n"
        "• Coba lagi nanti\n\n"
        "💡 Coba tulis pertanyaan lebih jelas.",
        parse_mode="Markdown"
    )

async def cmd_cuaca(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    if not ctx.args: return await update.message.reply_text("⚠️ /cuaca <kota>")
    try:
        kota = " ".join(ctx.args)
        r = requests.get("https://wttr.in/" + kota + "?format=j1", timeout=10).json()
        cur = r["current_condition"][0]
        await update.message.reply_text(
            "🌤️ Cuaca di " + kota.title() + "\n\n"
            "🌡️ Suhu : " + cur["temp_C"] + "°C\n"
            "💧 Lembab : " + cur["humidity"] + "%\n"
            "💨 Angin : " + cur["windspeedKmph"] + " km/h\n"
            "☁️ Kondisi : " + cur["weatherDesc"][0]["value"]
        )
    except Exception as e:
        await update.message.reply_text("❌ Gagal: " + str(e))

async def cmd_github(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    if not ctx.args: return await update.message.reply_text("⚠️ /github <username>")
    try:
        r = requests.get("https://api.github.com/users/" + ctx.args[0], timeout=10).json()
        if "login" not in r:
            return await update.message.reply_text("❌ User tidak ditemukan")
        await update.message.reply_text(
            "🐙 GitHub: " + r["login"] + "\n\n"
            "Nama : " + str(r.get("name", "-")) + "\n"
            "Bio : " + str(r.get("bio", "-")) + "\n"
            "Repo : " + str(r.get("public_repos")) + "\n"
            "Followers : " + str(r.get("followers")) + "\n"
            "Link : " + str(r.get("html_url"))
        )
    except Exception as e:
        await update.message.reply_text("❌ Error: " + str(e))

# ============ LIFE TOOLS ============
async def cmd_bmi(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    if len(ctx.args) < 2: return await update.message.reply_text("⚠️ /bmi <bb_kg> <tb_cm>")
    try:
        bb = float(ctx.args[0])
        tb = float(ctx.args[1]) / 100
        bmi = bb / (tb * tb)
        if bmi < 18.5: ket = "🔵 Kurus"
        elif bmi < 25: ket = "🟢 Normal"
        elif bmi < 30: ket = "🟡 Gemuk"
        else: ket = "🔴 Obesitas"
        await update.message.reply_text("⚖️ BMI: " + str(round(bmi, 2)) + "\n📌 Status: " + ket)
    except Exception as e:
        await update.message.reply_text("❌ Error: " + str(e))

async def cmd_umur(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    if not ctx.args: return await update.message.reply_text("⚠️ /umur DD-MM-YYYY")
    try:
        d = datetime.strptime(ctx.args[0], "%d-%m-%Y")
        now = datetime.now()
        years = now.year - d.year
        months = now.month - d.month
        days = now.day - d.day
        if days < 0:
            months -= 1
            days += 30
        if months < 0:
            years -= 1
            months += 12
        await update.message.reply_text("🎂 Umur: " + str(years) + " tahun, " + str(months) + " bulan, " + str(days) + " hari")
    except Exception as e:
        await update.message.reply_text("❌ Format: /umur 17-08-1945")

async def cmd_diskon(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    if len(ctx.args) < 2: return await update.message.reply_text("⚠️ /diskon <harga> <persen>")
    try:
        harga = float(ctx.args[0])
        diskon = float(ctx.args[1])
        potongan = harga * diskon / 100
        akhir = harga - potongan
        await update.message.reply_text(
            "💰 Kalkulator Diskon\n\n"
            "Harga awal : Rp " + str(int(harga)) + "\n"
            "Diskon : " + str(diskon) + "%\n"
            "Potongan : Rp " + str(int(potongan)) + "\n"
            "Bayar : Rp " + str(int(akhir))
        )
    except Exception as e:
        await update.message.reply_text("❌ Error: " + str(e))

async def cmd_pajak(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    if not ctx.args: return await update.message.reply_text("⚠️ /pajak <penghasilan>")
    try:
        p = float(ctx.args[0])
        pajak = p * 0.05
        await update.message.reply_text(
            "💸 Pajak 5%\n\n"
            "Penghasilan : Rp " + str(int(p)) + "\n"
            "Pajak : Rp " + str(int(pajak)) + "\n"
            "Netto : Rp " + str(int(p - pajak))
        )
    except Exception as e:
        await update.message.reply_text("❌ Error: " + str(e))

# ============ TEMP MAIL (mail.tm API) ============
MAIL_API = "https://api.mail.tm"
mail_sessions = {}

async def cmd_tempmail(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    uid = update.effective_user.id
    msg = await update.message.reply_text("📧 Membuat email sementara... ⏳")
    try:
        r = requests.get(MAIL_API + "/domains", timeout=15).json()
        if not r.get("hydra:member"):
            return await msg.edit_text("❌ Tidak ada domain tersedia")
        domain = r["hydra:member"][0]["domain"]
        username = "shiny" + "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
        password = "".join(random.choices(string.ascii_letters + string.digits, k=12))
        address = username + "@" + domain
        reg = requests.post(MAIL_API + "/accounts", json={"address": address, "password": password}, timeout=15)
        if reg.status_code not in [200, 201]:
            return await msg.edit_text("❌ Gagal buat email: " + reg.text[:200])
        login = requests.post(MAIL_API + "/token", json={"address": address, "password": password}, timeout=15).json()
        token = login.get("token")
        if not token:
            return await msg.edit_text("❌ Gagal login email")
        mail_sessions[uid] = {"address": address, "password": password, "token": token}
        await msg.edit_text(
            "📧 *EMAIL SEMENTARA AKTIF*\n\n"
            "┌─────────────────────────\n"
            "│ 📮 Alamat :\n"
            "│ `" + address + "`\n"
            "│\n"
            "│ 🔑 Password :\n"
            "│ `" + password + "`\n"
            "└─────────────────────────\n\n"
            "📥 Cek inbox: /inbox\n"
            "🔄 Ganti email: /hapusmail",
            parse_mode="Markdown"
        )
    except Exception as e:
        await msg.edit_text("❌ Error: " + str(e)[:300])

async def cmd_inbox(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    uid = update.effective_user.id
    if uid not in mail_sessions:
        return await update.message.reply_text("⚠️ Buat email dulu dengan /tempmail")
    session = mail_sessions[uid]
    msg = await update.message.reply_text("📥 Mengecek inbox... ⏳")
    try:
        headers = {"Authorization": "Bearer " + session["token"]}
        r = requests.get(MAIL_API + "/messages", headers=headers, timeout=15).json()
        messages = r.get("hydra:member", [])
        if not messages:
            return await msg.edit_text(
                "📭 *Inbox Kosong*\n\n"
                "📮 `" + session["address"] + "`\n\n"
                "💡 Tunggu, lalu cek lagi dengan /inbox",
                parse_mode="Markdown"
            )
        text = "📬 *INBOX (" + str(len(messages)) + " pesan)*\n\n📮 `" + session["address"] + "`\n\n"
        for i, m in enumerate(messages[:10], 1):
            sender = m.get("from", {}).get("address", "unknown")
            subject = m.get("subject", "(no subject)")
            text += str(i) + ". *" + subject[:40] + "*\n   📤 " + sender[:40] + "\n   📖 /baca " + str(i) + "\n\n"
        await msg.edit_text(text, parse_mode="Markdown")
    except Exception as e:
        await msg.edit_text("❌ Error: " + str(e)[:300])

async def cmd_baca(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    uid = update.effective_user.id
    if uid not in mail_sessions:
        return await update.message.reply_text("⚠️ Buat email dulu dengan /tempmail")
    if not ctx.args or not ctx.args[0].isdigit():
        return await update.message.reply_text("⚠️ Format: /baca <nomor>")
    idx = int(ctx.args[0]) - 1
    session = mail_sessions[uid]
    msg = await update.message.reply_text("📖 Membaca pesan... ⏳")
    try:
        headers = {"Authorization": "Bearer " + session["token"]}
        r = requests.get(MAIL_API + "/messages", headers=headers, timeout=15).json()
        messages = r.get("hydra:member", [])
        if idx < 0 or idx >= len(messages):
            return await msg.edit_text("❌ Nomor pesan tidak ditemukan")
        msg_id = messages[idx]["id"]
        detail = requests.get(MAIL_API + "/messages/" + msg_id, headers=headers, timeout=15).json()
        subject = detail.get("subject", "(no subject)")
        sender = detail.get("from", {}).get("address", "unknown")
        text_body = detail.get("text", "")
        html_body = detail.get("html", [])
        if isinstance(html_body, list):
            html_body = html_body[0] if html_body else ""
        if not text_body and html_body:
            text_body = re.sub(r"<[^>]+>", "", html_body)
        text_body = text_body.strip()[:1500] if text_body else "(kosong)"
        await msg.edit_text(
            "📧 *PESAN " + str(idx + 1) + "*\n\n"
            "📌 Subjek : " + subject[:60] + "\n"
            "📤 Dari : " + sender[:50] + "\n\n"
            "📄 *Isi:*\n\n" + text_body,
            parse_mode="Markdown"
        )
    except Exception as e:
        await msg.edit_text("❌ Error: " + str(e)[:300])

async def cmd_hapusmail(update, ctx):
    if not is_authorized(update.effective_user.id): return await require_key(update)
    uid = update.effective_user.id
    if uid in mail_sessions:
        del mail_sessions[uid]
    await update.message.reply_text("🗑️ Email dihapus!\n\nBuat baru: /tempmail")

# ============ CALLBACK ============
async def on_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if not is_authorized(q.from_user.id):
        return await q.edit_message_text("🔐 Kamu belum punya akses.\n\nKetik /key <key-akses>")
    d = q.data
    menus = {
        "menu": (menu_main(), kb_main()),
        "m1": (menu_1(), kb_back()),
        "m2": (menu_2(), kb_back()),
        "m3": (menu_3(), kb_back()),
        "m4": (menu_4(), kb_back()),
        "m5": (menu_5(), kb_back()),
        "m6": (menu_6(), kb_back()),
        "m7": (menu_7(), kb_back()),
    }
    if d == "x":
        await q.delete_message()
    elif d == "info":
        await q.edit_message_text(
            "✨ " + BOT_NAME + " v" + VERSION + "\n👤 " + OWNER + "\n🔐 Authorized ✅",
            reply_markup=kb_back()
        )
    elif d == "ping":
        await q.edit_message_text(
            "🏓 Pong!\n🖥️ " + socket.gethostname() + "\n⏰ " + datetime.now().strftime("%H:%M:%S"),
            reply_markup=kb_back()
        )
    elif d in menus:
        text, keyboard = menus[d]
        await q.edit_message_text(text, reply_markup=keyboard)

async def unknown(update, ctx):
    if not is_authorized(update.effective_user.id):
        return await require_key(update)
    await update.message.reply_text("❌ Perintah tidak dikenal.\nKetik /menu untuk melihat fitur.")

# ============ MAIN ============
def main():
    print("=" * 50)
    print("  ✨ SHINYVOID BOT v" + VERSION + " ✨")
    print("  Owner  : " + OWNER)
    print("  Type   : Universal Downloader + Key Access")
    print("  Music  : " + MUSIC_DIR)
    print("  Status : Online")
    print("=" * 50)
    print("[ShinyVoid] Menghubungkan ke Telegram...")

    app = ApplicationBuilder().token(TOKEN).build()

    commands = {
        "start": start,
        "key": cmd_key,
        "menu": cmd_menu,
        "menu1": cmd_m1, "menu2": cmd_m2, "menu3": cmd_m3,
        "menu4": cmd_m4, "menu5": cmd_m5, "menu6": cmd_m6, "menu7": cmd_m7,
        "ping": cmd_ping, "info": cmd_info, "about": cmd_about,
        "owner": cmd_owner, "id": cmd_id, "time": cmd_time, "date": cmd_date,
        "qrcode": cmd_qrcode, "shortlink": cmd_shortlink, "hash": cmd_hash,
        "base64": cmd_base64, "calc": cmd_calc, "pass": cmd_pass,
        "password": cmd_pass, "uuid": cmd_uuid, "ip": cmd_ip,
        "upper": cmd_upper, "lower": cmd_lower, "reverse": cmd_reverse,
        "title": cmd_title, "len": cmd_len, "count": cmd_count,
        "repeat": cmd_repeat, "replace": cmd_replace,
        "spongebob": cmd_spongebob, "vaporwave": cmd_vaporwave,
        "translate": cmd_translate, "toid": cmd_toid,
        "toen": cmd_toen, "tojp": cmd_tojp,
        "ytmp3": cmd_ytmp3, "ytmp4": cmd_ytmp4, "ytinfo": cmd_ytinfo,
        "sticker": cmd_sticker, "logo": cmd_logo,
        "wallpaper": cmd_wallpaper, "meme": cmd_meme,
        "cat": cmd_cat, "dog": cmd_dog,
        "dadu": cmd_dadu, "koin": cmd_koin, "random": cmd_random,
        "slot": cmd_slot, "quotes": cmd_quotes, "motivasi": cmd_motivasi,
        "fakta": cmd_fakta, "joke": cmd_joke,
        "truth": cmd_truth, "dare": cmd_dare,
        "tebak": cmd_tebak, "guess": cmd_guess,
        "wiki": cmd_wiki, "ai": cmd_ai, "cuaca": cmd_cuaca, "github": cmd_github,
        "bmi": cmd_bmi, "umur": cmd_umur, "diskon": cmd_diskon, "pajak": cmd_pajak,
        "music": cmd_music, "musicdl": cmd_musicdl,
        "musiclist": cmd_musiclist, "musicclear": cmd_musicclear,
        "sholat": cmd_sholat, "kiblat": cmd_kiblat,
        "asmaulhusna": cmd_asmaulhusna, "doa": cmd_doa, "ayat": cmd_ayat,
        "tempmail": cmd_tempmail, "inbox": cmd_inbox,
        "baca": cmd_baca, "hapusmail": cmd_hapusmail,
    }

    for name, func in commands.items():
        app.add_handler(CommandHandler(name, func))

    app.add_handler(CallbackQueryHandler(on_callback))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown))

    print("[ShinyVoid] Total commands: " + str(len(commands)))
    print("[ShinyVoid] Bot online! Tekan CTRL+C untuk stop.\n")

    app.run_polling()

if __name__ == "__main__":
    main()