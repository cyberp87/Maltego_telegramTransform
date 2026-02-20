from maltego_trx.transform import DiscoverableTransform
from maltego_trx.entities import Person
from telethon import TelegramClient
import asyncio
import re

# TUS DATOS (Ya sabes, usa variables de entorno en el futuro)
API_ID = TELEGRAM_API_ID
API_HASH = 'TELEGRAM_API_HASH'
SESSION_FILE = r'C:\Users\Pablo\Desktop\MaltegoTelegram\anon' 

HISTORY_BOT = 'SangMataInfo_bot'

class OldUserToID(DiscoverableTransform):
    """
    Toma un Username antiguo (texto) y pregunta al bot cuál era su ID numérico.
    Input: Alias (string)
    """
    
    @classmethod
    def create_entities(cls, request, response):
        # Input: El nombre de usuario antiguo (con o sin @)
        old_username = request.Value.strip()
        if not old_username.startswith('@'):
            old_username = f"@{old_username}"
            
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result_id = loop.run_until_complete(cls.reverse_lookup(old_username))
            
            if result_id:
                # Si encontramos el ID, creamos una entidad PERSONA con ese ID
                # Esto es clave: Convertimos un dato muerto (Old Name) en un dato vivo (ID)
                entity = response.addEntity(Person, f"Target ID: {result_id}")
                entity.addProperty("uid", "User ID", "strict", result_id)
                entity.setLinkLabel("ID Recovered from History")
                response.addUIMessage(f"¡Éxito! El nombre {old_username} pertenecía al ID {result_id}")
            else:
                response.addUIMessage(f"SangMata no tiene registros de {old_username}")
                
        except Exception as e:
            response.addUIMessage(f"Error: {str(e)}")

    @staticmethod
    async def reverse_lookup(username):
        client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
        await client.connect()
        
        if not await client.is_user_authorized():
            return None

        found_id = None
        try:
            async with client.conversation(HISTORY_BOT, timeout=12) as conv:
                # El comando mágico: /search_username
                await conv.send_message(f'/search_username {username}')
                
                response = await conv.get_response()
                text = response.text
                
                # Análisis Forense de la respuesta del Bot:
                # El bot suele responder algo como: "History of username @old:\nUser ID: 123456789"
                # Usamos Regex para cazar solo los números que vengan después de "ID"
                match = re.search(r'ID\D+(\d+)', text)
                if match:
                    found_id = match.group(1)
                
                # A veces el bot devuelve una lista si el nombre lo han tenido varias personas
                # Para este script simple, nos quedamos con el primero que pille.

        except Exception:
            return None
        finally:
            await client.disconnect()
            
        return found_id