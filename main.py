import os
import re
import urllib.parse
import threading
from flask import Flask
from telethon import TelegramClient, events

# --- SERVIDOR FLASK ---
app = Flask(name)

@app.route('/')
def home():
    return "Bot activo 24/7"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_flask, daemon=True).start()

# --- TELETHON CLIENT ---
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# --- COMANDO /start ---
@bot.on(events.NewMessage(pattern=r'^/start$'))
async def start_handler(event):
    msg = (
        "👋 ¡Bienvenido al Bot de Streaming!\n\n"
        "Comandos disponibles:\n"
        "• /am E01 <nombre> o /am cine <nombre> — Anime\n"
        "• /pl cine <nombre> — Películas\n"
        "• /ss T01E01 <nombre> — Series"
    )
    await event.respond(msg)

# --- COMANDO /am (ANIMEFLV) ---
@bot.on(events.NewMessage(pattern=r'^/am(?:\s+(.*))?'))
async def anime_handler(event):
    raw_text = event.pattern_match.group(1)
    if not raw_text:
        await event.respond("⚠️ Uso: /am E01 <nombre> o /am cine <nombre>")
        return

    # Limpiar prefijos como E01, E01TP01, cine, etc.
    clean_title = re.sub(r'^(E\d+(?:TP\d+)?|cine)\s+', '', raw_text, flags=re.IGNORECASE).strip()
    
    # Extraer etiqueta si existía
    tag_match = re.match(r'^(E\d+(?:TP\d+)?|cine)', raw_text, re.IGNORECASE)
    tag_info = f" [{tag_match.group(1).upper()}]" if tag_match else ""

    q = urllib.parse.quote(clean_title)
    search_url = f"https://m.animeflv.net/browse?q={q}"

    response = (
        f"⛩️ AnimeFLV{tag_info}\n"
        f"📌 Título: {clean_title}\n\n"
        f"🔗 [Ver resultados directos en AnimeFLV]({search_url})"
    )
    await event.respond(response, link_preview=True)

# --- COMANDO /pl (PELÍCULAS) ---
@bot.on(events.NewMessage(pattern=r'^/pl(?:\s+(.*))?'))
async def movie_handler(event):
    raw_text = event.pattern_match.group(1)
    if not raw_text:
        await event.respond("⚠️ Uso: /pl cine <nombre>")
        return

    # Limpiar el prefijo 'cine' si lo pusieron
    clean_title = re.sub(r'^cine\s+', '', raw_text, flags=re.IGNORECASE).strip()
    q = urllib.parse.quote(clean_title)

    response = (
        f"🎬 Película: {clean_title}\n\n"
        f"Resultados de búsqueda:\n"
        f"• [Cuevana Biz](https://wwcuevana.biz/?s={q})\n"
        f"• [Cuevana 3S](https://cuevana3s.pro/?s={q})\n"
        f"• [Cuevana 3I](https://cuevana3i.you/?s={q})"
    )
    await event.respond(response, link_preview=True)

# --- COMANDO /ss (SERIES) ---
@bot.on(events.NewMessage(pattern=r'^/ss(?:\s+(.*))?'))
async def series_handler(event):
    raw_text = event.pattern_match.group(1)
    if not raw_text:
        await event.respond("⚠️ Uso: /ss T01E01 <nombre>")
        return

    # Limpiar prefijos de temporada/episodio (ej: T01E01, E01T01, etc.)
    clean_title = re.sub(r'^(T\d+E\d+|E\d+T\d+)\s+', '', raw_text, flags=re.IGNORECASE).strip()
    
    tag_match = re.match(r'^(T\d+E\d+|E\d+T\d+)', raw_text, re.IGNORECASE)
    tag_info = f" ({tag_match.group(1).upper()})" if tag_match else ""

    q = urllib.parse.quote(clean_title)

    response = (
        f"📺 Serie: {clean_title}{tag_info}\n\n"
        f"Resultados de búsqueda:\n"
        f"• [Cuevana Biz](https://wwcuevana.biz/?s={q})\n"
        f"• [Cuevana 3S](https://cuevana3s.pro/?s={q})\n"
        f"• [Cuevana 3I](https://cuevana3i.you/?s={q})"
    )
    await event.respond(response, link_preview=True)

print("🚀 Bot iniciado.")
bot.run_until_disconnected()
