# Telegram Maltego Transforms

🇬🇧 [English](#english) | 🇪🇸 [Español](#español)

---

<a name="english"></a>
## 🇬🇧 English

### Description
This project contains custom Maltego transforms developed in Python using the `maltego-trx` library and Telethon to interact with Telegram.

### Requirements
- Python 3.10+
- Maltego Desktop
- Docker & Docker Compose (optional, but recommended)
- A Telegram API ID and API Hash (get them from [my.telegram.org](https://my.telegram.org))

### Setup & Installation

**1. Set up your Telegram Session:**
First, you need to generate a valid Telegram session. Edit `setup_session.py` with your `api_id` and `api_hash`.
Run the script locally to authenticate and generate the `.session` file:
```bash
python setup_session.py
(Note: Never share your .session file or upload it to GitHub!)

2. Run the Maltego TRX Server (Docker):
You can easily spin up the local transform server using Docker:

Bash
docker-compose up --build
The server will run on port 8080.

3. Add to Maltego:
Import the transforms into your Maltego client by adding a new Local Transform Server pointing to http://localhost:8080.

Author
Developed by [Cyberp87].

<a name="español"></a>

🇪🇸 Español
Descripción
Este proyecto contiene transformadas personalizadas de Maltego desarrolladas en Python utilizando la librería maltego-trx y Telethon para interactuar con Telegram.

Requisitos
Python 3.10+

Cliente de escritorio de Maltego

Docker y Docker Compose (opcional, pero recomendado)

Un API ID y API Hash de Telegram (puedes obtenerlos en my.telegram.org)

Configuración e Instalación
1. Configurar la sesión de Telegram:
Primero necesitas generar una sesión de Telegram válida. Edita el archivo setup_session.py con tu propio api_id y api_hash.
Ejecuta el script localmente para iniciar sesión y generar tu archivo .session:

Bash
python setup_session.py

2. Ejecutar el servidor TRX de Maltego (Docker):
Puedes levantar el servidor local de transformadas fácilmente usando Docker:

Bash
docker-compose up --build
El servidor se ejecutará en el puerto 8080.

3. Añadir a Maltego:
Importa las transformadas a tu cliente de Maltego añadiendo un nuevo Servidor de Transformadas Local (Local Transform Server) apuntando a http://localhost:8080.

Autor
Desarrollado por [Cyberp87].