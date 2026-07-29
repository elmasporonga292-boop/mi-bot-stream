import os
import requests
from bs4 import BeautifulSoup
from telethon import TelegramClient, events, Button

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

bot = TelegramClient('stream_bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

def buscar_animeflv(query):
    url_busqueda = f"https://animeflv.net/browse?q={query.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        resp = requests.get(url_busqueda, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        anime_card = soup.select_one('ul.ListAnimes li article.Anime')
        if not anime_card:
            return None
            
        titulo = anime_card.select_one('h3.Title').text.strip()
        link_rel = anime_card.select_one('a')['href']
        img_url = anime_card.select_one('div.Image figure img')['src']
        
        if img_url.startswith('/'):
            img_url = f"https://animeflv.net{img_url}"
            
        link_completo = f"https://animeflv.net{link_rel}"
        
        return {
            "titulo": titulo,
            "portada": img_url,
            "url_stream": link_completo
        }
    except Exception as e:
        print(f"Error en scraping: {e}")
        return None

@bot.on(events.NewMessage(pattern=r'^/anime(?:\s+(.+))?'))
async def handler_anime(event):
    query = event.pattern_match.group(1)
    
    if not query:
        await event.respond("📺 Buscador de Anime\n\nUso: /anime <nombre>\nEjemplo: /anime Chainsaw Man")
        return

    msg = await event.respond(f"🔍 Buscando {query} en la web...")
    
    resultado = buscar_animeflv(query)
    
    if not resultado:
        await msg.edit(f"❌ No encontré ningún resultado para {query}.")
        return
        
    await msg.delete()
    
    boton_webapp = Button.web(
        text="🍿 Ver en Telegram", 
        url=resultado["url_stream"]
    )
    
    await bot.send_file(
        event.chat_id,
        file=resultado["portada"],
        caption=f"🎬 {resultado['titulo']}\n\n¡Listo para transmitir!",
        buttons=[[boton_webapp]]
    )

print("🚀 Bot de Streaming iniciado correctamente.")
bot.run_until_disconnected()
