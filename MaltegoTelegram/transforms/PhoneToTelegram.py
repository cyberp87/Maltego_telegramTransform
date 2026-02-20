from maltego_trx.transform import DiscoverableTransform
from maltego_trx.entities import Alias
from telethon import TelegramClient
from telethon.tl.types import User
import asyncio

# TUS DATOS (Igual que antes)
API_ID = TELEGRAM_API_ID
API_HASH = 'TELEGRAM_API_HASH'
SESSION_FILE = r'C:\Users\Pablo\Desktop\MaltegoTelegram\anon' # Busca el archivo anon.session en la raíz

class PhoneToTelegram(DiscoverableTransform):
    """
    Transformada que toma un número de teléfono y busca su usuario en Telegram.
    """
    
    @classmethod
    def create_entities(cls, request, response):
        phone_number = request.Value
        
        # Maltego espera respuesta síncrona, pero Telegram es asíncrono.
        # Creamos un loop para ejecutar la tarea.
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(cls.check_telegram(phone_number))
            
            if result:
                # Si encontramos usuario, creamos la entidad en Maltego
                entity = response.addEntity(Alias, result['username'])
                entity.addProperty("uid", "User ID", "strict", str(result['id']))
                entity.addProperty("phone", "Phone", "strict", phone_number)
                entity.setLinkLabel("Telegram Account Found")
            else:
                response.addUIMessage(f"No se encontró cuenta pública para {phone_number}")
                
        except Exception as e:
            response.addUIMessage(f"Error técnico: {str(e)}")

    @staticmethod
    async def check_telegram(phone):
        # Conectamos usando la sesión ya guardada (sin pedir código)
        client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
        await client.connect()
        
        if not await client.is_user_authorized():
            return None # La sesión caducó o no existe

        try:
            # Esta es la llamada clave a la API
            # Intenta resolver la entidad (usuario) por el número
            contact = await client.get_entity(phone)
            
            if isinstance(contact, User):
                username = contact.username if contact.username else "No Alias"
                first_name = contact.first_name if contact.first_name else ""
                
                return {
                    'id': contact.id,
                    'username': f"{first_name} (@{username})"
                }
        except Exception:
            # Si el usuario tiene privacidad "Nadie" o no existe
            return None
        finally:
            await client.disconnect()