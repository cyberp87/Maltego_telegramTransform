from maltego_trx.transform import DiscoverableTransform
from maltego_trx.entities import Alias
from telethon import TelegramClient
import asyncio
import re
import os

# TUS CREDENCIALES (Acuérdate de poner la 'r' en la ruta de sesión)
API_ID = TELEGRAM_API_ID 
API_HASH = 'TELEGRAM_API_HASH'
SESSION_FILE = r'C:\Users\Pablo\Desktop\MaltegoTelegram\anon' 

# El bot que vamos a interrogar
HISTORY_BOT = 'SangMataInfo_bot'

class IDToHistory(DiscoverableTransform):
    """
    Input: Una entidad 'Phrase' o 'Person' con el ID numérico (ej: 123456789)
    Output: Entidades 'Alias' con los nombres antiguos.
    """
    
    @classmethod
    def create_entities(cls, request, response):
        target_id = request.Value.strip()
        
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            history = loop.run_until_complete(cls.get_history(target_id))
            
            if history:
                for name in history:
                    # Creamos una entidad por cada nombre encontrado
                    ent = response.addEntity(Alias, name)
                    ent.setLinkLabel("Historical Username")
            else:
                response.addUIMessage("SangMata no tiene registros de este ID.")
                
        except Exception as e:
            response.addUIMessage(f"Error: {str(e)}")

    @staticmethod
    async def get_history(target_id):
        client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
        await client.connect()
        
        if not await client.is_user_authorized():
            return []

        results = []
        try:
            # Iniciamos conversación con el bot
            async with client.conversation(HISTORY_BOT, timeout=15) as conv:
                # Enviamos el comando
                await conv.send_message(f'/search_id {target_id}')
                
                # Leemos la respuesta
                resp = await conv.get_response()
                text = resp.text
                
                # BUSCAMOS LOS ALIAS (@usuario)
                # Regex que busca palabras que empiecen por @
                aliases = re.findall(r'(@\w+)', text)
                
                # Filtramos para quitar el propio nombre del bot si sale
                results = [a for a in aliases if 'SangMata' not in a]
                
        except Exception as e:
            # Si el bot pide unirse a canales o falla
            print(f"Error con el bot: {e}")
            
        finally:
            await client.disconnect()
            
        return list(set(results)) # Quitamos duplicados