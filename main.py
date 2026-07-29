import os
import re
import urllib.parse
import threading
from flask import Flask
from telethon import TelegramClient, events

# Servidor web para Render
app = Flask(name)

@app.route('/')
def home():
    return "OK"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_flask, daemon=True).start()

# Cliente Telegram
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@bot.on(events.NewMessage(pattern=r'^/start$'))
async def start_handler(event):
    await event.respond("👋 Bot listo. Usá:\n/am E01 <nombre>\n/pl cine <nombre>\n/ss T01E01 <nombre>")

@bot.on(events.NewMessage(pattern=r'^/am(?:\s+(.*))?'))
async def anime_handler(event):
    query = event.pattern_match.group(1) or ""
    url = "https://m.animeflv.net/browse?q=" + urllib.parse.quote(query)
    await event.respond("⛩️ AnimeFLV: " + url)

@bot.on(events.NewMessage(pattern=r'^/pl(?:\s+(.*))?'))
async def movie_handler(event):
    query = event.pattern_match.group(1) or ""
    q = urllib.parse.quote(query)
    msg = f"🎬 Cuevana:\n• https://wwcuevana.biz/?s={q}\n• https://cuevana3s.pro/?s={q}\n• https://cuevana3i.you/?s={q}"
    await event.respond(msg)

@bot.on(events.NewMessage(pattern=r'^/ss(?:\s+(.*))?'))
async def series_handler(event):
    query = event.pattern_match.group(1) or ""
    q = urllib.parse.quote(query)
    msg = f"📺 Series:\n• https://wwcuevana.biz/?s={q}\n• https://cuevana3s.pro/?s={q}\n• https://cuevana3i.you/?s={q}"
    await event.respond(msg)

bot.run_until_disconnected()
