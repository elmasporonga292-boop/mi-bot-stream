import os
import threading
from flask import Flask
from telethon import TelegramClient, events

# --- SERVIDOR FLASK PARA ENGAÑAR A RENDER Y QUE SIGA GRATIS ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot activo 24/7"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_flask, daemon=True).start()

# --- BOT DE TELEGRAM ---
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# COMANDO /start
@bot.on(events.NewMessage(pattern=r'^/start$'))
async def start_handler(event):
    menu = (
        "👋 ¡Bienvenido al Bot de Streaming!\n\n"
        "Comandos disponibles:\n"
        "• /am E01 <nombre> o /am cine <nombre> — Anime (AnimeFLV)\n"
        "• /pl cine <nombre> — Películas\n"
        "• /ss T01E01 <nombre> — Series\n"
    )
    await event.respond(menu)

# COMANDO /am (Anime)
@bot.on(events.NewMessage(pattern=r'^/am(?:\s+(.*))?'))
async def anime_handler(event):
    query = event.pattern_match.group(1)
    if not query:
        await event.respond("⚠️ Uso correcto: /am E01 <anime> o /am cine <pelicula>")
        return
    await event.respond(f"🔍 Buscando anime: {query}...")

# COMANDO /pl (Películas)
@bot.on(events.NewMessage(pattern=r'^/pl(?:\s+(.*))?'))
async def movie_handler(event):
    query = event.pattern_match.group(1)
    if not query:
        await event.respond("⚠️ Uso correcto: /pl cine <nombre de película>")
        return
    await event.respond(f"🎬 Buscando película: {query}...")

# COMANDO /ss (Series)
@bot.on(events.NewMessage(pattern=r'^/ss(?:\s+(.*))?'))
async def series_handler(event):
    query = event.pattern_match.group(1)
    if not query:
        await event.respond("⚠️ Uso correcto: /ss T01E01 <nombre de serie>")
        return
    await event.respond(f"📺 Buscando serie: {query}...")

print("🚀 Bot de Streaming iniciado en Web Service.")
bot.run_until_disconnected()
