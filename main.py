import os
import re
import urllib.parse
import threading
from flask import Flask
from telethon import TelegramClient, events

# --- SERVIDOR FLASK PARA MANTENER RENDER GRATIS 24/7 ---
app = Flask(name)

@app.route('/')
def home():
    return "Bot activo 24/7"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_flask, daemon=True).start()

# --- CONFIGURACIÓN DEL BOT TELETHON ---
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Fuentes configuradas
ANIMEFLV_BASE = "https://m.animeflv.net"
CUEVANA_SOURCES = [
    "https://wwcuevana.biz",
    "https://cuevana3s.pro",
    "https://cuevana3i.you"
]

# ----------------------------------------------------
# COMANDO /start
# ----------------------------------------------------
@bot.on(events.NewMessage(pattern=r'^/start$'))
async def start_handler(event):
    menu = (
        "👋 ¡Bienvenido al Bot de Streaming!\n\n"
        "🎬 **Películas (/pl):**\n"
        "• /pl cine <nombre>\n\n"
        "📺 **Series (/ss):**\n"
        "• /ss T01E01 <nombre>\n\n"
    Anime (/am):(/am):**\n"
        "• /am E01 <nombre> (Episodio)\n"
        "• /am cine <nombre> (Película)"
    )
    await event.respond(menu)

# ----------------------------------------------------
# COMANDO /am (AnimeFLV)
# ----------------------------------------------------
@bot.on(events.NewMessage(pattern=r'^/am(?:\s+(.*))?'))
async def anime_handler(event):
    raw_text = event.pattern_match.group(1)
    if not raw_text:
        await event.respond("⚠️ Uso correcto:\n/am E01 <nombre>\n/am cine <nombre>")
        return

    # Extraer formato y nombre
    match_ep = re.match(r'^(E\d+)\s+(.+)$', raw_text, re.IGNORECASE)
    match_cine = re.match(r'^(cine)\s+(.+)$', raw_text, re.IGNORECASE)

    if match_ep:
        ep_code = match_ep.group(1).upper()
        anime_name = match_ep.group(2)
        tipo = f"Episodio {ep_code}"
    elif match_cine:
        anime_name = match_cine.group(2)
        tipo = "Película"
    else:
        anime_name = raw_text
        tipo = "Búsqueda general"

    query_encoded = urllib.parse.quote(anime_name)
    search_url = f"{ANIMEFLV_BASE}/browse?q={query_encoded}"

    msg = (
     AnimeFLVimeFLV** — {tipo}\n"
     Búsqueda:queda:** {anime_name}\n\n"
        f"🔗 [Hacé clic acá para ver los resultados en AnimeFLV]({search_url})"
    )
    await event.respond(msg, link_preview=True)

# ----------------------------------------------------
# COMANDO /pl (Películas - Cuevana)
# ----------------------------------------------------
@bot.on(events.NewMessage(pattern=r'^/pl(?:\s+(.*))?'))
async def movie_handler(event):
    raw_text = event.pattern_match.group(1)
    if not raw_text:
        await event.respond("⚠️ Uso correcto: /pl cine <nombre de la película>")
        return

    # Limpiar prefijo cine si fue ingresado
    movie_name = re.sub(r'^cine\s+', '', raw_text, flags=re.IGNORECASE).strip()
    query_encoded = urllib.parse.quote(movie_name)

    links_cuevana = "\n".join([f"• [{src.split('//')[1]}]({src}/?s={query_encoded})" for src in CUEVANA_SOURCES])

    msg = (
     Película (Cine):Cine):** {movie_name}\n\n"
        f"Resultados disponibles en fuentes:\n{links_cuevana}"
    )
    await event.respond(msg, link_preview=True)

# ----------------------------------------------------
# COMANDO /ss (Series - Cuevana)
# ----------------------------------------------------
@bot.on(events.NewMessage(pattern=r'^/ss(?:\s+(.*))?'))
async def series_handler(event):
    raw_text = event.pattern_match.group(1)
    if not raw_text:
        await event.respond("⚠️ Uso correcto: /ss T01E01 <nombre de la serie>")
        return
AnimeFLV
Anime Online - AnimeFLV
Somos la Legendaria AnimeFLV, donde podrás encontrar todos tus animes favoritos para ver online y descargar en una calidad excelente, no olvides recom...
# Extraer temporada/episodio y título
    match_se = re.match(r'^(T\d+E\d+)\s+(.+)$', raw_text, re.IGNORECASE)
    if match_se:
        se_code = match_se.group(1).upper()
        series_name = match_se.group(2)
        info_ep = f" (Temporada/Episodio: {se_code})"
    else:
        series_name = raw_text
        info_ep = ""

    query_encoded = urllib.parse.quote(series_name)
    links_cuevana = "\n".join([f"• [{src.split('//')[1]}]({src}/?s={query_encoded})" for src in CUEVANA_SOURCES])

    msg = (
        f"📺 Serie: {series_name}{info_ep}\n\n"
        f"Buscar en fuentes de Cuevana:\n{links_cuevana}"
    )
    await event.respond(msg, link_preview=True)

# ----------------------------------------------------
# INICIO
# ----------------------------------------------------
print("🚀 Bot de Streaming iniciado con soporte para AnimeFLV y Cuevana.")
bot.run_until_disconnected()
