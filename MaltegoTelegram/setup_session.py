from telethon import TelegramClient

# TUS DATOS AQUI (Los que sacaste en el Paso 1)
api_id = TELEGRAM_API_ID  # Tu ID (número)
api_hash = 'TELEGRAM_API_HASH'

client = TelegramClient('anon', api_id, api_hash)

async def main():
    print("¡Logueado con éxito! Se ha creado el archivo anon.session")
    me = await client.get_me()
    print(f"Sesión activa para: {me.username}")

with client:
    client.loop.run_until_complete(main())