from maltego_trx.transform import DiscoverableTransform
from maltego_trx.entities import Alias, PhoneNumber
from telethon import TelegramClient
from telethon.tl.types import User
import asyncio

# TUS DATOS (Asegúrate de poner la 'r' en la ruta como aprendimos)
API_ID = TELEGRAM_API_ID
API_HASH = 'TELEGRAM_API_HASH'
SESSION_FILE = r'C:\Users\Pablo\Desktop\MaltegoTelegram\anon' 

class UsernameToInfo(DiscoverableTransform):
    """
    Toma un Alias (ej: @usuario), busca su ID y si es posible, su teléfono.
    """
    
    @classmethod
    def create_entities(cls, request, response):
        username_input = request.Value.strip()
        
        # Limpieza: Si el usuario pone "@pepe", quitamos el "@" para la API
        if username_input.startswith('@'):
            username_input = username_input[1:]

        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(cls.get_user_info(username_input))
            
            if result:
                # 1. Devolvemos siempre la entidad de ALIAS con el ID (Dato fijo)
                entity_user = response.addEntity(Alias, result['username'])
                entity_user.addProperty("uid", "User ID", "strict", str(result['id']))
                entity_user.setLinkLabel("ID Resolved")

                # 2. Si hubo suerte y el teléfono es público, devolvemos entidad TELEFONO
                if result['phone']:
                    entity_phone = response.addEntity(PhoneNumber, result['phone'])
                    entity_phone.setLinkLabel("Phone Exposed")
                    response.addUIMessage(f"¡ÉXITO! Teléfono encontrado: {result['phone']}")
                else:
                    response.addUIMessage(f"Usuario encontrado (ID: {result['id']}), pero el teléfono es privado.")
            else:
                response.addUIMessage(f"No se encontró el usuario @{username_input}")
                
        except Exception as e:
            response.addUIMessage(f"Error: {str(e)}")

    @staticmethod
    async def get_user_info(username):
        client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
        await client.connect()
        
        if not await client.is_user_authorized():
            return None 

        try:
            # Buscamos por nombre de usuario
            user = await client.get_entity(username)
            
            if isinstance(user, User):
                # Preparamos los datos
                return {
                    'id': user.id,
                    'username': user.username,
                    'phone': f"+{user.phone}" if user.phone else None # Telethon devuelve el phone sin el '+'
                }
        except Exception:
            return None
        finally:
            await client.disconnect()